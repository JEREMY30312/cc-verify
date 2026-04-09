"""
知识库优化系统 - 核心模块
提供多级索引、智能缓存、多模式检索等功能
"""

from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import json
import hashlib
import time
from collections import OrderedDict
from pathlib import Path
import re
from difflib import SequenceMatcher


# ============================================================================
# 数据结构定义
# ============================================================================

class RetrievalStrategy(Enum):
    """检索策略枚举"""
    EXACT = "exact"           # 精确匹配
    FUZZY = "fuzzy"           # 模糊匹配
    SEMANTIC = "semantic"     # 语义匹配
    HYBRID = "hybrid"         # 混合检索


class CacheLevel(Enum):
    """缓存级别枚举"""
    HOT = "hot"               # 热数据（高频访问）
    WARM = "warm"             # 温数据（中频访问）
    COLD = "cold"             # 冷数据（低频访问）


@dataclass
class ExampleMetadata:
    """示例元数据"""
    id: str
    title: str
    category: str
    file_path: str
    keywords: List[str]
    applicable_templates: List[str]
    retention_priority: str  # high, medium, low
    access_count: int = 0
    last_accessed: float = 0.0
    similarity_score: float = 0.0
    content_hash: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "file_path": self.file_path,
            "keywords": self.keywords,
            "applicable_templates": self.applicable_templates,
            "retention_priority": self.retention_priority,
            "access_count": self.access_count,
            "last_accessed": self.last_accessed,
            "similarity_score": self.similarity_score,
            "content_hash": self.content_hash
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ExampleMetadata':
        """从字典创建"""
        return cls(**data)


@dataclass
class RetrievalResult:
    """检索结果"""
    metadata: ExampleMetadata
    content: str
    relevance_score: float
    matched_keywords: List[str]
    strategy_used: RetrievalStrategy

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "metadata": self.metadata.to_dict(),
            "content": self.content,
            "relevance_score": self.relevance_score,
            "matched_keywords": self.matched_keywords,
            "strategy_used": self.strategy_used.value
        }


@dataclass
class PerformanceMetrics:
    """性能指标"""
    total_queries: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    avg_query_time: float = 0.0
    total_query_time: float = 0.0
    strategy_distribution: Dict[str, int] = field(default_factory=dict)

    def update(self, query_time: float, cache_hit: bool, strategy: RetrievalStrategy):
        """更新指标"""
        self.total_queries += 1
        self.total_query_time += query_time
        self.avg_query_time = self.total_query_time / self.total_queries

        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

        strategy_key = strategy.value
        self.strategy_distribution[strategy_key] = self.strategy_distribution.get(strategy_key, 0) + 1

    def get_cache_hit_rate(self) -> float:
        """获取缓存命中率"""
        if self.total_queries == 0:
            return 0.0
        return self.cache_hits / self.total_queries

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "total_queries": self.total_queries,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "cache_hit_rate": self.get_cache_hit_rate(),
            "avg_query_time": self.avg_query_time,
            "total_query_time": self.total_query_time,
            "strategy_distribution": self.strategy_distribution
        }


# ============================================================================
# 缓存系统
# ============================================================================

class LRUCache:
    """LRU缓存实现"""

    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.cache: OrderedDict[str, Any] = OrderedDict()
        self.access_count: Dict[str, int] = {}

    def get(self, key: str) -> Optional[Any]:
        """获取缓存项"""
        if key not in self.cache:
            return None

        # 移动到末尾（最近使用）
        self.cache.move_to_end(key)
        self.access_count[key] = self.access_count.get(key, 0) + 1
        return self.cache[key]

    def put(self, key: str, value: Any) -> None:
        """放入缓存项"""
        if key in self.cache:
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.capacity:
                # 移除最久未使用的项
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]
                del self.access_count[oldest_key]

        self.cache[key] = value
        self.access_count[key] = self.access_count.get(key, 0) + 1

    def remove(self, key: str) -> bool:
        """移除缓存项"""
        if key in self.cache:
            del self.cache[key]
            del self.access_count[key]
            return True
        return False

    def clear(self) -> None:
        """清空缓存"""
        self.cache.clear()
        self.access_count.clear()

    def size(self) -> int:
        """获取缓存大小"""
        return len(self.cache)

    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        return {
            "size": self.size(),
            "capacity": self.capacity,
            "utilization": self.size() / self.capacity if self.capacity > 0 else 0,
            "top_accessed": sorted(self.access_count.items(), key=lambda x: x[1], reverse=True)[:5]
        }


class MultiLevelCache:
    """多级缓存系统"""

    def __init__(self, hot_capacity: int = 50, warm_capacity: int = 200):
        self.hot_cache = LRUCache(hot_capacity)      # 热数据缓存
        self.warm_cache = LRUCache(warm_capacity)    # 温数据缓存
        self.promotion_threshold = 3                 # 提升阈值（访问次数）
        self.demotion_threshold = 1                  # 降级阈值

    def get(self, key: str) -> Optional[Any]:
        """获取缓存项（从热到冷）"""
        # 先查热缓存
        value = self.hot_cache.get(key)
        if value is not None:
            return value

        # 再查温缓存
        value = self.warm_cache.get(key)
        if value is not None:
            # 检查是否需要提升到热缓存
            access_count = self.warm_cache.access_count.get(key, 0)
            if access_count >= self.promotion_threshold:
                self.hot_cache.put(key, value)
                self.warm_cache.remove(key)
            return value

        return None

    def put(self, key: str, value: Any, level: CacheLevel = CacheLevel.WARM) -> None:
        """放入缓存项"""
        if level == CacheLevel.HOT:
            self.hot_cache.put(key, value)
        else:
            self.warm_cache.put(key, value)

    def remove(self, key: str) -> bool:
        """移除缓存项"""
        removed = False
        if self.hot_cache.remove(key):
            removed = True
        if self.warm_cache.remove(key):
            removed = True
        return removed

    def clear(self) -> None:
        """清空所有缓存"""
        self.hot_cache.clear()
        self.warm_cache.clear()

    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        return {
            "hot_cache": self.hot_cache.get_stats(),
            "warm_cache": self.warm_cache.get_stats(),
            "promotion_threshold": self.promotion_threshold,
            "demotion_threshold": self.demotion_threshold
        }


# ============================================================================
# 检索策略
# ============================================================================

class RetrievalEngine:
    """检索引擎"""

    def __init__(self, examples: List[ExampleMetadata]):
        self.examples = examples
        self._build_indexes()

    def _build_indexes(self):
        """构建索引"""
        self.keyword_index: Dict[str, List[str]] = {}
        self.template_index: Dict[str, List[str]] = {}
        self.category_index: Dict[str, List[str]] = {}

        for example in self.examples:
            # 关键词索引
            for keyword in example.keywords:
                if keyword not in self.keyword_index:
                    self.keyword_index[keyword] = []
                self.keyword_index[keyword].append(example.id)

            # 模板索引
            for template in example.applicable_templates:
                if template not in self.template_index:
                    self.template_index[template] = []
                self.template_index[template].append(example.id)

            # 分类索引
            if example.category not in self.category_index:
                self.category_index[example.category] = []
            self.category_index[example.category].append(example.id)

    def exact_retrieve(self, query: str, field: str = "keywords") -> List[Tuple[str, float]]:
        """精确检索"""
        query = query.lower().strip()
        results = []

        if field == "keywords":
            if query in self.keyword_index:
                results = [(example_id, 1.0) for example_id in self.keyword_index[query]]
        elif field == "templates":
            if query in self.template_index:
                results = [(example_id, 1.0) for example_id in self.template_index[query]]
        elif field == "category":
            if query in self.category_index:
                results = [(example_id, 1.0) for example_id in self.category_index[query]]

        return results

    def fuzzy_retrieve(self, query: str, threshold: float = 0.6) -> List[Tuple[str, float]]:
        """模糊检索"""
        query = query.lower().strip()
        results = []

        for example in self.examples:
            # 检查关键词匹配
            for keyword in example.keywords:
                similarity = SequenceMatcher(None, query, keyword.lower()).ratio()
                if similarity >= threshold:
                    results.append((example.id, similarity))
                    break

            # 检查标题匹配
            title_similarity = SequenceMatcher(None, query, example.title.lower()).ratio()
            if title_similarity >= threshold:
                results.append((example.id, title_similarity))

        # 去重并排序
        seen = set()
        unique_results = []
        for example_id, score in sorted(results, key=lambda x: x[1], reverse=True):
            if example_id not in seen:
                seen.add(example_id)
                unique_results.append((example_id, score))

        return unique_results

    def semantic_retrieve(self, query: str, query_keywords: List[str]) -> List[Tuple[str, float]]:
        """语义检索（基于关键词共现）"""
        query_keywords = [kw.lower().strip() for kw in query_keywords]
        results = []

        for example in self.examples:
            # 计算关键词重叠度
            example_keywords = [kw.lower() for kw in example.keywords]
            overlap = len(set(query_keywords) & set(example_keywords))

            if overlap > 0:
                # 计算相似度分数
                score = overlap / max(len(query_keywords), len(example_keywords))
                results.append((example.id, score))

        # 排序
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def hybrid_retrieve(self, query: str, query_keywords: List[str],
                       weights: Optional[Dict[str, float]] = None) -> List[Tuple[str, float]]:
        """混合检索"""
        if weights is None:
            weights = {
                "exact": 0.4,
                "fuzzy": 0.3,
                "semantic": 0.3
            }

        # 执行各种检索
        exact_results = self.exact_retrieve(query)
        fuzzy_results = self.fuzzy_retrieve(query)
        semantic_results = self.semantic_retrieve(query, query_keywords)

        # 合并结果
        combined_scores: Dict[str, float] = {}

        for example_id, score in exact_results:
            combined_scores[example_id] = combined_scores.get(example_id, 0) + score * weights["exact"]

        for example_id, score in fuzzy_results:
            combined_scores[example_id] = combined_scores.get(example_id, 0) + score * weights["fuzzy"]

        for example_id, score in semantic_results:
            combined_scores[example_id] = combined_scores.get(example_id, 0) + score * weights["semantic"]

        # 排序
        sorted_results = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_results


# ============================================================================
# 性能监控
# ============================================================================

class PerformanceMonitor:
    """性能监控器"""

    def __init__(self):
        self.metrics = PerformanceMetrics()
        self.query_history: List[Dict[str, Any]] = []
        self.max_history_size = 1000

    def record_query(self, query: str, query_time: float, cache_hit: bool,
                    strategy: RetrievalStrategy, result_count: int):
        """记录查询"""
        self.metrics.update(query_time, cache_hit, strategy)

        record = {
            "timestamp": time.time(),
            "query": query,
            "query_time": query_time,
            "cache_hit": cache_hit,
            "strategy": strategy.value,
            "result_count": result_count
        }

        self.query_history.append(record)

        # 限制历史记录大小
        if len(self.query_history) > self.max_history_size:
            self.query_history = self.query_history[-self.max_history_size:]

    def get_metrics(self) -> Dict[str, Any]:
        """获取性能指标"""
        return self.metrics.to_dict()

    def get_recent_queries(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取最近的查询记录"""
        return self.query_history[-limit:]

    def reset(self) -> None:
        """重置监控数据"""
        self.metrics = PerformanceMetrics()
        self.query_history.clear()


# ============================================================================
# 访问优化器
# ============================================================================

class KnowledgeBaseAccess:
    """知识库访问优化器"""

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.examples: Dict[str, ExampleMetadata] = {}
        self.content_cache: Dict[str, str] = {}
        self._load_index()

    def _load_index(self):
        """加载索引文件"""
        index_path = self.base_path / "index.json"
        if not index_path.exists():
            raise FileNotFoundError(f"索引文件不存在: {index_path}")

        with open(index_path, 'r', encoding='utf-8') as f:
            index_data = json.load(f)

        # 解析示例元数据
        for category, data in index_data.get("examples_index", {}).items():
            for example_path in data.get("full_examples", []):
                example_id = self._generate_id(example_path)
                title = self._extract_title_from_path(example_path)

                metadata = ExampleMetadata(
                    id=example_id,
                    title=title,
                    category=category,
                    file_path=example_path,
                    keywords=data.get("keywords", []),
                    applicable_templates=data.get("applicable_templates", []),
                    retention_priority=data.get("retention_priority", "medium")
                )

                self.examples[example_id] = metadata

    def _generate_id(self, path: str) -> str:
        """生成示例ID"""
        return hashlib.md5(path.encode()).hexdigest()[:12]

    def _extract_title_from_path(self, path: str) -> str:
        """从路径提取标题"""
        filename = Path(path).stem
        # 转换为更友好的标题格式
        title = filename.replace('-', ' ').replace('_', ' ').title()
        return title

    def get_metadata(self, example_id: str) -> Optional[ExampleMetadata]:
        """获取示例元数据"""
        return self.examples.get(example_id)

    def get_content(self, example_id: str) -> Optional[str]:
        """获取示例内容"""
        metadata = self.get_metadata(example_id)
        if not metadata:
            return None

        # 检查缓存
        if example_id in self.content_cache:
            return self.content_cache[example_id]

        # 读取文件
        file_path = self.base_path.parent / metadata.file_path
        if not file_path.exists():
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 缓存内容
        self.content_cache[example_id] = content

        return content

    def get_all_examples(self) -> List[ExampleMetadata]:
        """获取所有示例"""
        return list(self.examples.values())

    def get_examples_by_category(self, category: str) -> List[ExampleMetadata]:
        """按分类获取示例"""
        return [ex for ex in self.examples.values() if ex.category == category]

    def get_examples_by_priority(self, priority: str) -> List[ExampleMetadata]:
        """按优先级获取示例"""
        return [ex for ex in self.examples.values() if ex.retention_priority == priority]

    def update_access_stats(self, example_id: str):
        """更新访问统计"""
        if example_id in self.examples:
            self.examples[example_id].access_count += 1
            self.examples[example_id].last_accessed = time.time()


# ============================================================================
# 优化后的知识库系统
# ============================================================================

class OptimizedKnowledgeBase:
    """优化后的知识库系统"""

    def __init__(self, base_path: str, hot_cache_size: int = 50, warm_cache_size: int = 200):
        """
        初始化知识库

        Args:
            base_path: 知识库基础路径
            hot_cache_size: 热缓存大小
            warm_cache_size: 温缓存大小
        """
        self.base_path = Path(base_path)
        self.access = KnowledgeBaseAccess(base_path)
        self.cache = MultiLevelCache(hot_cache_size, warm_cache_size)
        self.monitor = PerformanceMonitor()

        # 初始化检索引擎
        examples = self.access.get_all_examples()
        self.retrieval_engine = RetrievalEngine(examples)

    def retrieve(self, query: str, strategy: RetrievalStrategy = RetrievalStrategy.HYBRID,
                query_keywords: Optional[List[str]] = None, max_results: int = 5) -> List[RetrievalResult]:
        """
        检索示例

        Args:
            query: 查询字符串
            strategy: 检索策略
            query_keywords: 查询关键词列表（用于语义检索）
            max_results: 最大结果数

        Returns:
            检索结果列表
        """
        start_time = time.time()

        # 检查缓存
        cache_key = self._generate_cache_key(query, strategy, query_keywords)
        cached_results = self.cache.get(cache_key)

        if cached_results is not None:
            query_time = time.time() - start_time
            self.monitor.record_query(query, query_time, True, strategy, len(cached_results))
            return cached_results

        # 执行检索
        if query_keywords is None:
            query_keywords = [query]

        if strategy == RetrievalStrategy.EXACT:
            scored_results = self.retrieval_engine.exact_retrieve(query)
        elif strategy == RetrievalStrategy.FUZZY:
            scored_results = self.retrieval_engine.fuzzy_retrieve(query)
        elif strategy == RetrievalStrategy.SEMANTIC:
            scored_results = self.retrieval_engine.semantic_retrieve(query, query_keywords)
        else:  # HYBRID
            scored_results = self.retrieval_engine.hybrid_retrieve(query, query_keywords)

        # 构建结果
        results = []
        for example_id, score in scored_results[:max_results]:
            metadata = self.access.get_metadata(example_id)
            content = self.access.get_content(example_id)

            if metadata and content:
                # 更新访问统计
                self.access.update_access_stats(example_id)

                # 确定匹配的关键词
                matched_keywords = self._find_matched_keywords(query, metadata)

                result = RetrievalResult(
                    metadata=metadata,
                    content=content,
                    relevance_score=score,
                    matched_keywords=matched_keywords,
                    strategy_used=strategy
                )
                results.append(result)

        # 缓存结果
        self.cache.put(cache_key, results, level=CacheLevel.WARM)

        query_time = time.time() - start_time
        self.monitor.record_query(query, query_time, False, strategy, len(results))

        return results

    def _generate_cache_key(self, query: str, strategy: RetrievalStrategy,
                           query_keywords: Optional[List[str]] = None) -> str:
        """生成缓存键"""
        key_parts = [query.lower(), strategy.value]
        if query_keywords:
            key_parts.extend(sorted(query_keywords))
        key_string = "|".join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()

    def _find_matched_keywords(self, query: str, metadata: ExampleMetadata) -> List[str]:
        """查找匹配的关键词"""
        query_lower = query.lower()
        matched = []

        for keyword in metadata.keywords:
            if query_lower in keyword.lower():
                matched.append(keyword)

        return matched

    def get_example_by_id(self, example_id: str) -> Optional[RetrievalResult]:
        """通过ID获取示例"""
        metadata = self.access.get_metadata(example_id)
        if not metadata:
            return None

        content = self.access.get_content(example_id)
        if not content:
            return None

        # 更新访问统计
        self.access.update_access_stats(example_id)

        return RetrievalResult(
            metadata=metadata,
            content=content,
            relevance_score=1.0,
            matched_keywords=[],
            strategy_used=RetrievalStrategy.EXACT
        )

    def get_performance_stats(self) -> Dict[str, Any]:
        """获取性能统计"""
        return {
            "metrics": self.monitor.get_metrics(),
            "cache_stats": self.cache.get_stats(),
            "recent_queries": self.monitor.get_recent_queries(5)
        }

    def clear_cache(self) -> None:
        """清空缓存"""
        self.cache.clear()

    def export_index(self, output_path: Optional[str] = None) -> Dict[str, Any]:
        """导出索引"""
        if output_path is None:
            output_path = str(self.base_path / "index_optimized.json")

        index_data = {
            "version": "2.0",
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "examples": [ex.to_dict() for ex in self.access.get_all_examples()],
            "statistics": {
                "total_examples": len(self.access.examples),
                "categories": list(set(ex.category for ex in self.access.examples.values())),
                "total_keywords": len(set(kw for ex in self.access.examples.values() for kw in ex.keywords))
            }
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)

        return index_data

    def get_recommendations(self, query: str, limit: int = 3) -> List[RetrievalResult]:
        """获取推荐示例（基于混合检索）"""
        return self.retrieve(query, strategy=RetrievalStrategy.HYBRID, max_results=limit)


# ============================================================================
# 工具函数
# ============================================================================

def create_optimized_index(base_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
    """
    创建优化的索引文件

    Args:
        base_path: 知识库基础路径
        output_path: 输出路径

    Returns:
        索引数据
    """
    kb = OptimizedKnowledgeBase(base_path)
    return kb.export_index(output_path)


def benchmark_retrieval(kb: OptimizedKnowledgeBase, queries: List[str],
                       iterations: int = 10) -> Dict[str, Any]:
    """
    基准测试检索性能

    Args:
        kb: 知识库实例
        queries: 查询列表
        iterations: 迭代次数

    Returns:
        基准测试结果
    """
    results = {
        "queries": queries,
        "iterations": iterations,
        "total_time": 0.0,
        "avg_time_per_query": 0.0,
        "min_time": float('inf'),
        "max_time": 0.0,
        "results_per_query": []
    }

    for query in queries:
        query_times = []
        query_results = []

        for _ in range(iterations):
            start_time = time.time()
            retrieved = kb.retrieve(query)
            query_time = time.time() - start_time

            query_times.append(query_time)
            if not query_results:
                query_results = [r.metadata.title for r in retrieved]

        avg_query_time = sum(query_times) / len(query_times)
        results["total_time"] += sum(query_times)
        results["min_time"] = min(results["min_time"], min(query_times))
        results["max_time"] = max(results["max_time"], max(query_times))

        results["results_per_query"].append({
            "query": query,
            "avg_time": avg_query_time,
            "results": query_results
        })

    results["avg_time_per_query"] = results["total_time"] / (len(queries) * iterations)

    return results


# ============================================================================
# 主程序入口
# ============================================================================

if __name__ == "__main__":
    # 示例用法
    print("知识库优化系统 - 核心模块")
    print("=" * 60)

    # 初始化知识库
    kb = OptimizedKnowledgeBase(
        base_path="knowledge-base/cinematic-examples",
        hot_cache_size=50,
        warm_cache_size=200
    )

    print(f"\n✓ 知识库已加载")
    print(f"  - 示例数量: {len(kb.access.examples)}")
    print(f"  - 分类: {list(set(ex.category for ex in kb.access.examples.values()))}")

    # 执行检索
    print("\n" + "=" * 60)
    print("检索测试")
    print("=" * 60)

    queries = ["温馨", "悬疑", "远景", "情感表达"]

    for query in queries:
        print(f"\n查询: '{query}'")
        results = kb.retrieve(query, strategy=RetrievalStrategy.HYBRID)

        for i, result in enumerate(results, 1):
            print(f"  {i}. {result.metadata.title}")
            print(f"     相关性: {result.relevance_score:.2f}")
            print(f"     匹配关键词: {', '.join(result.matched_keywords)}")

    # 性能统计
    print("\n" + "=" * 60)
    print("性能统计")
    print("=" * 60)

    stats = kb.get_performance_stats()
    print(f"\n总查询数: {stats['metrics']['total_queries']}")
    print(f"缓存命中率: {stats['metrics']['cache_hit_rate']:.2%}")
    print(f"平均查询时间: {stats['metrics']['avg_query_time']*1000:.2f}ms")
    print(f"\n缓存统计:")
    print(f"  热缓存: {stats['cache_stats']['hot_cache']['size']}/{stats['cache_stats']['hot_cache']['capacity']}")
    print(f"  温缓存: {stats['cache_stats']['warm_cache']['size']}/{stats['cache_stats']['warm_cache']['capacity']}")
