"""
知识库优化系统 - 使用示例
演示如何使用优化后的知识库系统
"""

from knowledge_base_optimized import (
    OptimizedKnowledgeBase,
    RetrievalStrategy,
    CacheLevel,
    create_optimized_index,
    benchmark_retrieval
)
import json
from pathlib import Path


# ============================================================================
# 示例1: 基本使用
# ============================================================================

def example_basic_usage():
    """示例1: 基本使用"""
    print("\n" + "=" * 70)
    print("示例1: 基本使用")
    print("=" * 70)

    # 初始化知识库
    kb = OptimizedKnowledgeBase(
        base_path="knowledge-base/cinematic-examples",
        hot_cache_size=50,
        warm_cache_size=200
    )

    print(f"\n✓ 知识库已初始化")
    print(f"  - 示例总数: {len(kb.access.examples)}")
    print(f"  - 分类: {list(set(ex.category for ex in kb.access.examples.values()))}")

    # 执行简单检索
    print("\n--- 执行检索 ---")
    query = "温馨"
    results = kb.retrieve(query, strategy=RetrievalStrategy.HYBRID)

    print(f"\n查询: '{query}'")
    print(f"找到 {len(results)} 个结果:\n")

    for i, result in enumerate(results, 1):
        print(f"{i}. {result.metadata.title}")
        print(f"   分类: {result.metadata.category}")
        print(f"   相关性: {result.relevance_score:.2f}")
        print(f"   匹配关键词: {', '.join(result.matched_keywords)}")
        print(f"   文件: {result.metadata.file_path}")
        print()


# ============================================================================
# 示例2: 不同检索策略对比
# ============================================================================

def example_retrieval_strategies():
    """示例2: 不同检索策略对比"""
    print("\n" + "=" * 70)
    print("示例2: 不同检索策略对比")
    print("=" * 70)

    kb = OptimizedKnowledgeBase("knowledge-base/cinematic-examples")

    query = "悬疑"
    strategies = [
        RetrievalStrategy.EXACT,
        RetrievalStrategy.FUZZY,
        RetrievalStrategy.SEMANTIC,
        RetrievalStrategy.HYBRID
    ]

    print(f"\n查询: '{query}'\n")

    for strategy in strategies:
        print(f"--- {strategy.value.upper()} 检索 ---")
        results = kb.retrieve(query, strategy=strategy)

        for i, result in enumerate(results, 1):
            print(f"  {i}. {result.metadata.title} (相关性: {result.relevance_score:.2f})")

        print()


# ============================================================================
# 示例3: 语义检索
# ============================================================================

def example_semantic_retrieval():
    """示例3: 语义检索"""
    print("\n" + "=" * 70)
    print("示例3: 语义检索")
    print("=" * 70)

    kb = OptimizedKnowledgeBase("knowledge-base/cinematic-examples")

    # 使用多个关键词进行语义检索
    query = "情感场景"
    query_keywords = ["情感", "温馨", "回忆", "特写"]

    print(f"\n查询: '{query}'")
    print(f"关键词: {', '.join(query_keywords)}\n")

    results = kb.retrieve(
        query,
        strategy=RetrievalStrategy.SEMANTIC,
        query_keywords=query_keywords
    )

    for i, result in enumerate(results, 1):
        print(f"{i}. {result.metadata.title}")
        print(f"   相关性: {result.relevance_score:.2f}")
        print(f"   所有关键词: {', '.join(result.metadata.keywords)}")
        print()


# ============================================================================
# 示例4: 获取推荐
# ============================================================================

def example_recommendations():
    """示例4: 获取推荐"""
    print("\n" + "=" * 70)
    print("示例4: 获取推荐")
    print("=" * 70)

    kb = OptimizedKnowledgeBase("knowledge-base/cinematic-examples")

    # 获取推荐
    query = "建立镜头"
    recommendations = kb.get_recommendations(query, limit=3)

    print(f"\n基于 '{query}' 的推荐:\n")

    for i, result in enumerate(recommendations, 1):
        print(f"{i}. {result.metadata.title}")
        print(f"   分类: {result.metadata.category}")
        print(f"   相关性: {result.relevance_score:.2f}")
        print(f"   适用模板: {', '.join(result.metadata.applicable_templates)}")
        print()


# ============================================================================
# 示例5: 按分类和优先级筛选
# ============================================================================

def example_filtering():
    """示例5: 按分类和优先级筛选"""
    print("\n" + "=" * 70)
    print("示例5: 按分类和优先级筛选")
    print("=" * 70)

    kb = OptimizedKnowledgeBase("knowledge-base/cinematic-examples")

    # 按分类筛选
    print("\n--- 按分类筛选 ---")
    categories = list(set(ex.category for ex in kb.access.examples.values()))

    for category in categories:
        examples = kb.access.get_examples_by_category(category)
        print(f"\n分类: {category}")
        for ex in examples:
            print(f"  - {ex.title} (优先级: {ex.retention_priority})")

    # 按优先级筛选
    print("\n--- 按优先级筛选 ---")
    priorities = ["high", "medium", "low"]

    for priority in priorities:
        examples = kb.access.get_examples_by_priority(priority)
        if examples:
            print(f"\n优先级: {priority}")
            for ex in examples:
                print(f"  - {ex.title}")


# ============================================================================
# 示例6: 通过ID获取示例
# ============================================================================

def example_get_by_id():
    """示例6: 通过ID获取示例"""
    print("\n" + "=" * 70)
    print("示例6: 通过ID获取示例")
    print("=" * 70)

    kb = OptimizedKnowledgeBase("knowledge-base/cinematic-examples")

    # 获取所有示例ID
    example_ids = list(kb.access.examples.keys())

    if example_ids:
        # 获取第一个示例
        example_id = example_ids[0]
        result = kb.get_example_by_id(example_id)

        if result:
            print(f"\n示例ID: {example_id}")
            print(f"标题: {result.metadata.title}")
            print(f"分类: {result.metadata.category}")
            print(f"访问次数: {result.metadata.access_count}")
            print(f"最后访问: {result.metadata.last_accessed}")
            print(f"\n内容预览:")
            print(result.content[:200] + "...")


# ============================================================================
# 示例7: 性能监控
# ============================================================================

def example_performance_monitoring():
    """示例7: 性能监控"""
    print("\n" + "=" * 70)
    print("示例7: 性能监控")
    print("=" * 70)

    kb = OptimizedKnowledgeBase("knowledge-base/cinematic-examples")

    # 执行多次查询
    queries = ["温馨", "悬疑", "远景", "情感表达", "建立镜头"]

    print("\n执行查询...")
    for query in queries:
        # 执行两次以测试缓存
        kb.retrieve(query)
        kb.retrieve(query)

    # 获取性能统计
    stats = kb.get_performance_stats()

    print("\n--- 性能指标 ---")
    print(f"总查询数: {stats['metrics']['total_queries']}")
    print(f"缓存命中: {stats['metrics']['cache_hits']}")
    print(f"缓存未命中: {stats['metrics']['cache_misses']}")
    print(f"缓存命中率: {stats['metrics']['cache_hit_rate']:.2%}")
    print(f"平均查询时间: {stats['metrics']['avg_query_time']*1000:.2f}ms")

    print("\n--- 策略分布 ---")
    for strategy, count in stats['metrics']['strategy_distribution'].items():
        print(f"{strategy}: {count} 次")

    print("\n--- 缓存统计 ---")
    print(f"热缓存: {stats['cache_stats']['hot_cache']['size']}/{stats['cache_stats']['hot_cache']['capacity']}")
    print(f"温缓存: {stats['cache_stats']['warm_cache']['size']}/{stats['cache_stats']['warm_cache']['capacity']}")

    print("\n--- 最近查询 ---")
    for query_record in stats['recent_queries']:
        print(f"查询: '{query_record['query']}'")
        print(f"  时间: {query_record['query_time']*1000:.2f}ms")
        print(f"  缓存命中: {'是' if query_record['cache_hit'] else '否'}")
        print(f"  策略: {query_record['strategy']}")
        print(f"  结果数: {query_record['result_count']}")


# ============================================================================
# 示例8: 缓存管理
# ============================================================================

def example_cache_management():
    """示例8: 缓存管理"""
    print("\n" + "=" * 70)
    print("示例8: 缓存管理")
    print("=" * 70)

    kb = OptimizedKnowledgeBase("knowledge-base/cinematic-examples")

    # 执行查询以填充缓存
    print("\n执行查询以填充缓存...")
    queries = ["温馨", "悬疑", "远景"]
    for query in queries:
        kb.retrieve(query)

    # 查看缓存状态
    stats = kb.get_performance_stats()
    print(f"\n缓存状态:")
    print(f"  热缓存: {stats['cache_stats']['hot_cache']['size']} 项")
    print(f"  温缓存: {stats['cache_stats']['warm_cache']['size']} 项")

    # 清空缓存
    print("\n清空缓存...")
    kb.clear_cache()

    # 再次查看缓存状态
    stats = kb.get_performance_stats()
    print(f"\n清空后缓存状态:")
    print(f"  热缓存: {stats['cache_stats']['hot_cache']['size']} 项")
    print(f"  温缓存: {stats['cache_stats']['warm_cache']['size']} 项")


# ============================================================================
# 示例9: 导出优化索引
# ============================================================================

def example_export_index():
    """示例9: 导出优化索引"""
    print("\n" + "=" * 70)
    print("示例9: 导出优化索引")
    print("=" * 70)

    kb = OptimizedKnowledgeBase("knowledge-base/cinematic-examples")

    # 导出索引
    output_path = "knowledge-base/cinematic-examples/index_optimized.json"
    index_data = kb.export_index(output_path)

    print(f"\n✓ 索引已导出到: {output_path}")
    print(f"\n索引信息:")
    print(f"  版本: {index_data['version']}")
    print(f"  创建时间: {index_data['created_at']}")
    print(f"  示例总数: {index_data['statistics']['total_examples']}")
    print(f"  分类: {', '.join(index_data['statistics']['categories'])}")
    print(f"  关键词总数: {index_data['statistics']['total_keywords']}")


# ============================================================================
# 示例10: 基准测试
# ============================================================================

def example_benchmark():
    """示例10: 基准测试"""
    print("\n" + "=" * 70)
    print("示例10: 基准测试")
    print("=" * 70)

    kb = OptimizedKnowledgeBase("knowledge-base/cinematic-examples")

    # 定义测试查询
    queries = ["温馨", "悬疑", "远景", "情感表达", "建立镜头"]

    # 执行基准测试
    print("\n执行基准测试...")
    benchmark_results = benchmark_retrieval(kb, queries, iterations=5)

    print(f"\n--- 基准测试结果 ---")
    print(f"查询数: {len(benchmark_results['queries'])}")
    print(f"迭代次数: {benchmark_results['iterations']}")
    print(f"总时间: {benchmark_results['total_time']:.4f}s")
    print(f"平均查询时间: {benchmark_results['avg_time_per_query']*1000:.2f}ms")
    print(f"最小查询时间: {benchmark_results['min_time']*1000:.2f}ms")
    print(f"最大查询时间: {benchmark_results['max_time']*1000:.2f}ms")

    print("\n--- 各查询详情 ---")
    for query_result in benchmark_results['results_per_query']:
        print(f"\n查询: '{query_result['query']}'")
        print(f"  平均时间: {query_result['avg_time']*1000:.2f}ms")
        print(f"  结果: {', '.join(query_result['results'])}")


# ============================================================================
# 示例11: 实际应用场景
# ============================================================================

def example_real_world_scenario():
    """示例11: 实际应用场景"""
    print("\n" + "=" * 70)
    print("示例11: 实际应用场景 - 分镜提示词生成")
    print("=" * 70)

    kb = OptimizedKnowledgeBase("knowledge-base/cinematic-examples")

    # 场景1: 用户想要创建一个温馨的回忆场景
    print("\n--- 场景1: 温馨回忆场景 ---")
    user_query = "温馨的回忆场景"
    results = kb.retrieve(user_query, strategy=RetrievalStrategy.HYBRID)

    print(f"\n用户需求: {user_query}")
    print(f"\n推荐的参考示例:")

    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result.metadata.title}")
        print(f"   相关性: {result.relevance_score:.2f}")
        print(f"   适用模板: {', '.join(result.metadata.applicable_templates)}")
        print(f"   关键词: {', '.join(result.metadata.keywords)}")

    # 场景2: 用户想要创建一个悬疑的揭示场景
    print("\n" + "-" * 70)
    print("\n--- 场景2: 悬疑揭示场景 ---")
    user_query = "悬疑的揭示"
    query_keywords = ["悬疑", "揭示", "紧张"]
    results = kb.retrieve(
        user_query,
        strategy=RetrievalStrategy.SEMANTIC,
        query_keywords=query_keywords
    )

    print(f"\n用户需求: {user_query}")
    print(f"关键词: {', '.join(query_keywords)}")
    print(f"\n推荐的参考示例:")

    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result.metadata.title}")
        print(f"   相关性: {result.relevance_score:.2f}")
        print(f"   适用模板: {', '.join(result.metadata.applicable_templates)}")

    # 场景3: 用户想要创建一个世界观建立镜头
    print("\n" + "-" * 70)
    print("\n--- 场景3: 世界观建立镜头 ---")
    user_query = "世界观建立"
    results = kb.retrieve(user_query, strategy=RetrievalStrategy.HYBRID)

    print(f"\n用户需求: {user_query}")
    print(f"\n推荐的参考示例:")

    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result.metadata.title}")
        print(f"   相关性: {result.relevance_score:.2f}")
        print(f"   适用模板: {', '.join(result.metadata.applicable_templates)}")
        print(f"   关键词: {', '.join(result.metadata.keywords)}")


# ============================================================================
# 示例12: 批量处理
# ============================================================================

def example_batch_processing():
    """示例12: 批量处理"""
    print("\n" + "=" * 70)
    print("示例12: 批量处理")
    print("=" * 70)

    kb = OptimizedKnowledgeBase("knowledge-base/cinematic-examples")

    # 批量查询
    queries = [
        ("温馨", RetrievalStrategy.HYBRID),
        ("悬疑", RetrievalStrategy.FUZZY),
        ("远景", RetrievalStrategy.EXACT),
        ("情感表达", RetrievalStrategy.SEMANTIC)
    ]

    print("\n批量查询结果:\n")

    for query, strategy in queries:
        results = kb.retrieve(query, strategy=strategy)

        print(f"查询: '{query}' (策略: {strategy.value})")
        print(f"结果数: {len(results)}")

        if results:
            print(f"最佳匹配: {results[0].metadata.title} (相关性: {results[0].relevance_score:.2f})")

        print()


# ============================================================================
# 主程序
# ============================================================================

def main():
    """主程序"""
    print("\n" + "=" * 70)
    print("知识库优化系统 - 使用示例")
    print("=" * 70)

    # 运行所有示例
    examples = [
        ("基本使用", example_basic_usage),
        ("不同检索策略对比", example_retrieval_strategies),
        ("语义检索", example_semantic_retrieval),
        ("获取推荐", example_recommendations),
        ("按分类和优先级筛选", example_filtering),
        ("通过ID获取示例", example_get_by_id),
        ("性能监控", example_performance_monitoring),
        ("缓存管理", example_cache_management),
        ("导出优化索引", example_export_index),
        ("基准测试", example_benchmark),
        ("实际应用场景", example_real_world_scenario),
        ("批量处理", example_batch_processing)
    ]

    print("\n可用示例:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")

    print("\n" + "=" * 70)
    print("运行所有示例...")
    print("=" * 70)

    for name, example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\n❌ 示例 '{name}' 执行失败: {e}")

    print("\n" + "=" * 70)
    print("所有示例执行完成!")
    print("=" * 70)


if __name__ == "__main__":
    main()
