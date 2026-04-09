"""
知识库优化系统 - 单元测试
测试所有核心功能
"""

import unittest
import tempfile
import shutil
import json
from pathlib import Path
from knowledge_base_optimized import (
    OptimizedKnowledgeBase,
    RetrievalStrategy,
    CacheLevel,
    LRUCache,
    MultiLevelCache,
    ExampleMetadata,
    RetrievalResult,
    PerformanceMetrics,
    RetrievalEngine
)


class TestLRUCache(unittest.TestCase):
    """测试LRU缓存"""

    def setUp(self):
        """设置测试环境"""
        self.cache = LRUCache(capacity=3)

    def test_basic_operations(self):
        """测试基本操作"""
        self.cache.put("key1", "value1")
        self.cache.put("key2", "value2")
        self.cache.put("key3", "value3")

        self.assertEqual(self.cache.get("key1"), "value1")
        self.assertEqual(self.cache.get("key2"), "value2")
        self.assertEqual(self.cache.get("key3"), "value3")

    def test_eviction(self):
        """测试淘汰机制"""
        self.cache.put("key1", "value1")
        self.cache.put("key2", "value2")
        self.cache.put("key3", "value3")
        self.cache.put("key4", "value4")  # 应该淘汰key1

        self.assertIsNone(self.cache.get("key1"))
        self.assertEqual(self.cache.get("key2"), "value2")
        self.assertEqual(self.cache.get("key4"), "value4")

    def test_lru_order(self):
        """测试LRU顺序"""
        self.cache.put("key1", "value1")
        self.cache.put("key2", "value2")
        self.cache.put("key3", "value3")

        # 访问key1，使其成为最近使用
        self.cache.get("key1")

        # 添加新项，应该淘汰key2
        self.cache.put("key4", "value4")

        self.assertEqual(self.cache.get("key1"), "value1")
        self.assertIsNone(self.cache.get("key2"))
        self.assertEqual(self.cache.get("key3"), "value3")
        self.assertEqual(self.cache.get("key4"), "value4")

    def test_remove(self):
        """测试移除操作"""
        self.cache.put("key1", "value1")
        self.assertTrue(self.cache.remove("key1"))
        self.assertFalse(self.cache.remove("key1"))
        self.assertIsNone(self.cache.get("key1"))

    def test_clear(self):
        """测试清空操作"""
        self.cache.put("key1", "value1")
        self.cache.put("key2", "value2")
        self.cache.clear()

        self.assertEqual(self.cache.size(), 0)
        self.assertIsNone(self.cache.get("key1"))


class TestMultiLevelCache(unittest.TestCase):
    """测试多级缓存"""

    def setUp(self):
        """设置测试环境"""
        self.cache = MultiLevelCache(hot_capacity=2, warm_capacity=4)

    def test_basic_operations(self):
        """测试基本操作"""
        self.cache.put("key1", "value1", level=CacheLevel.HOT)
        self.cache.put("key2", "value2", level=CacheLevel.WARM)

        self.assertEqual(self.cache.get("key1"), "value1")
        self.assertEqual(self.cache.get("key2"), "value2")

    def test_promotion(self):
        """测试提升机制"""
        # 放入温缓存
        self.cache.put("key1", "value1", level=CacheLevel.WARM)

        # 多次访问以触发提升
        for _ in range(3):
            self.cache.get("key1")

        # 应该被提升到热缓存
        self.assertEqual(self.cache.hot_cache.size(), 1)
        self.assertEqual(self.cache.warm_cache.size(), 0)

    def test_clear(self):
        """测试清空操作"""
        self.cache.put("key1", "value1", level=CacheLevel.HOT)
        self.cache.put("key2", "value2", level=CacheLevel.WARM)
        self.cache.clear()

        self.assertEqual(self.cache.hot_cache.size(), 0)
        self.assertEqual(self.cache.warm_cache.size(), 0)


class TestExampleMetadata(unittest.TestCase):
    """测试示例元数据"""

    def test_to_dict(self):
        """测试转换为字典"""
        metadata = ExampleMetadata(
            id="test_id",
            title="Test Example",
            category="test_category",
            file_path="test/path.md",
            keywords=["keyword1", "keyword2"],
            applicable_templates=["template1"],
            retention_priority="high"
        )

        data = metadata.to_dict()
        self.assertEqual(data["id"], "test_id")
        self.assertEqual(data["title"], "Test Example")
        self.assertEqual(data["category"], "test_category")

    def test_from_dict(self):
        """测试从字典创建"""
        data = {
            "id": "test_id",
            "title": "Test Example",
            "category": "test_category",
            "file_path": "test/path.md",
            "keywords": ["keyword1", "keyword2"],
            "applicable_templates": ["template1"],
            "retention_priority": "high",
            "access_count": 0,
            "last_accessed": 0.0,
            "similarity_score": 0.0,
            "content_hash": ""
        }

        metadata = ExampleMetadata.from_dict(data)
        self.assertEqual(metadata.id, "test_id")
        self.assertEqual(metadata.title, "Test Example")


class TestPerformanceMetrics(unittest.TestCase):
    """测试性能指标"""

    def test_update(self):
        """测试更新指标"""
        metrics = PerformanceMetrics()
        metrics.update(0.1, True, RetrievalStrategy.EXACT)
        metrics.update(0.2, False, RetrievalStrategy.HYBRID)

        self.assertEqual(metrics.total_queries, 2)
        self.assertEqual(metrics.cache_hits, 1)
        self.assertEqual(metrics.cache_misses, 1)
        self.assertAlmostEqual(metrics.avg_query_time, 0.15)

    def test_cache_hit_rate(self):
        """测试缓存命中率"""
        metrics = PerformanceMetrics()
        metrics.update(0.1, True, RetrievalStrategy.EXACT)
        metrics.update(0.2, True, RetrievalStrategy.HYBRID)
        metrics.update(0.3, False, RetrievalStrategy.FUZZY)

        self.assertAlmostEqual(metrics.get_cache_hit_rate(), 2/3)


class TestRetrievalEngine(unittest.TestCase):
    """测试检索引擎"""

    def setUp(self):
        """设置测试环境"""
        self.examples = [
            ExampleMetadata(
                id="ex1",
                title="温馨回忆",
                category="emotional_closeup",
                file_path="path1.md",
                keywords=["温馨", "回忆", "特写"],
                applicable_templates=["模板1"],
                retention_priority="high"
            ),
            ExampleMetadata(
                id="ex2",
                title="悬疑揭示",
                category="emotional_closeup",
                file_path="path2.md",
                keywords=["悬疑", "揭示", "紧张"],
                applicable_templates=["模板2"],
                retention_priority="high"
            ),
            ExampleMetadata(
                id="ex3",
                title="孤独远景",
                category="establishing_shot",
                file_path="path3.md",
                keywords=["孤独", "远景", "氛围"],
                applicable_templates=["模板3"],
                retention_priority="high"
            )
        ]
        self.engine = RetrievalEngine(self.examples)

    def test_exact_retrieve(self):
        """测试精确检索"""
        results = self.engine.exact_retrieve("温馨", field="keywords")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], "ex1")
        self.assertEqual(results[0][1], 1.0)

    def test_fuzzy_retrieve(self):
        """测试模糊检索"""
        results = self.engine.fuzzy_retrieve("温", threshold=0.5)
        self.assertGreater(len(results), 0)

    def test_semantic_retrieve(self):
        """测试语义检索"""
        results = self.engine.semantic_retrieve("温馨", ["温馨", "回忆"])
        self.assertGreater(len(results), 0)

    def test_hybrid_retrieve(self):
        """测试混合检索"""
        results = self.engine.hybrid_retrieve("温馨", ["温馨", "回忆"])
        self.assertGreater(len(results), 0)


class TestOptimizedKnowledgeBase(unittest.TestCase):
    """测试优化后的知识库"""

    @classmethod
    def setUpClass(cls):
        """设置测试类"""
        # 创建临时测试目录
        cls.test_dir = tempfile.mkdtemp()
        cls.kb_dir = Path(cls.test_dir) / "cinematic-examples"
        cls.kb_dir.mkdir()

        # 创建测试索引文件
        index_data = {
            "version": "1.0",
            "created_at": "2026-01-29T20:01:40+08:00",
            "examples_index": {
                "emotional_closeup": {
                    "full_examples": [
                        "cinematic-examples/full-examples/02-warm-memory.md",
                        "cinematic-examples/full-examples/05-suspense-reveal.md"
                    ],
                    "core_rules": "cinematic-examples/rules-extracted/emotional-closeup-rules.md",
                    "applicable_templates": ["情绪特写模板", "对话场景变体"],
                    "keywords": ["温馨", "悬疑", "特写", "情感表达", "回忆", "揭示"],
                    "retention_priority": "high"
                },
                "establishing_shot": {
                    "full_examples": [
                        "cinematic-examples/full-examples/03-lonely-vista.md",
                        "cinematic-examples/full-examples/06-world-building.md"
                    ],
                    "core_rules": "cinematic-examples/rules-extracted/establishing-shot-rules.md",
                    "applicable_templates": ["建立镜头模板"],
                    "keywords": ["孤独", "世界观", "远景", "氛围建立", "奇幻", "科幻"],
                    "retention_priority": "high"
                }
            },
            "statistics": {
                "total_full_examples": 4,
                "total_rules_files": 2,
                "coverage_rate": "100%"
            }
        }

        index_path = cls.kb_dir / "index.json"
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2)

        # 创建测试示例文件
        full_examples_dir = cls.kb_dir / "full-examples"
        full_examples_dir.mkdir()

        example_content = """# 温馨回忆

这是一个温馨的回忆场景示例。

## 场景描述
- 情感基调：温馨、怀旧
- 镜头类型：特写
- 关键元素：回忆、情感

## 提示词示例
温馨的回忆场景，特写镜头...
"""

        for i in range(1, 5):
            example_path = full_examples_dir / f"0{i}-example.md"
            with open(example_path, 'w', encoding='utf-8') as f:
                f.write(example_content)

    @classmethod
    def tearDownClass(cls):
        """清理测试类"""
        shutil.rmtree(cls.test_dir)

    def setUp(self):
        """设置测试环境"""
        self.kb = OptimizedKnowledgeBase(
            base_path=str(self.kb_dir),
            hot_cache_size=10,
            warm_cache_size=20
        )

    def test_initialization(self):
        """测试初始化"""
        self.assertEqual(len(self.kb.access.examples), 4)

    def test_retrieve_exact(self):
        """测试精确检索"""
        results = self.kb.retrieve("温馨", strategy=RetrievalStrategy.EXACT)
        self.assertGreater(len(results), 0)

    def test_retrieve_fuzzy(self):
        """测试模糊检索"""
        results = self.kb.retrieve("温", strategy=RetrievalStrategy.FUZZY)
        self.assertGreater(len(results), 0)

    def test_retrieve_semantic(self):
        """测试语义检索"""
        results = self.kb.retrieve(
            "温馨",
            strategy=RetrievalStrategy.SEMANTIC,
            query_keywords=["温馨", "回忆"]
        )
        self.assertGreater(len(results), 0)

    def test_retrieve_hybrid(self):
        """测试混合检索"""
        results = self.kb.retrieve("温馨", strategy=RetrievalStrategy.HYBRID)
        self.assertGreater(len(results), 0)

    def test_cache_hit(self):
        """测试缓存命中"""
        # 第一次查询
        results1 = self.kb.retrieve("温馨")
        # 第二次查询（应该命中缓存）
        results2 = self.kb.retrieve("温馨")

        self.assertEqual(len(results1), len(results2))

    def test_get_example_by_id(self):
        """测试通过ID获取示例"""
        example_ids = list(self.kb.access.examples.keys())
        if example_ids:
            result = self.kb.get_example_by_id(example_ids[0])
            self.assertIsNotNone(result)

    def test_get_recommendations(self):
        """测试获取推荐"""
        recommendations = self.kb.get_recommendations("温馨", limit=2)
        self.assertLessEqual(len(recommendations), 2)

    def test_clear_cache(self):
        """测试清空缓存"""
        self.kb.retrieve("温馨")
        self.kb.clear_cache()

        stats = self.kb.get_performance_stats()
        self.assertEqual(stats['cache_stats']['hot_cache']['size'], 0)
        self.assertEqual(stats['cache_stats']['warm_cache']['size'], 0)

    def test_export_index(self):
        """测试导出索引"""
        output_path = Path(self.test_dir) / "exported_index.json"
        index_data = self.kb.export_index(str(output_path))

        self.assertTrue(output_path.exists())
        self.assertEqual(index_data['version'], '2.0')
        self.assertEqual(index_data['statistics']['total_examples'], 4)

    def test_performance_stats(self):
        """测试性能统计"""
        # 执行一些查询
        for _ in range(5):
            self.kb.retrieve("温馨")

        stats = self.kb.get_performance_stats()
        self.assertGreater(stats['metrics']['total_queries'], 0)
        self.assertIn('cache_hit_rate', stats['metrics'])


class TestIntegration(unittest.TestCase):
    """集成测试"""

    @classmethod
    def setUpClass(cls):
        """设置测试类"""
        cls.test_dir = tempfile.mkdtemp()
        cls.kb_dir = Path(cls.test_dir) / "cinematic-examples"
        cls.kb_dir.mkdir()

        # 创建测试索引和文件（与TestOptimizedKnowledgeBase相同）
        index_data = {
            "version": "1.0",
            "created_at": "2026-01-29T20:01:40+08:00",
            "examples_index": {
                "emotional_closeup": {
                    "full_examples": [
                        "cinematic-examples/full-examples/02-warm-memory.md"
                    ],
                    "core_rules": "cinematic-examples/rules-extracted/emotional-closeup-rules.md",
                    "applicable_templates": ["情绪特写模板"],
                    "keywords": ["温馨", "回忆", "特写"],
                    "retention_priority": "high"
                }
            },
            "statistics": {
                "total_full_examples": 1,
                "total_rules_files": 1,
                "coverage_rate": "100%"
            }
        }

        index_path = cls.kb_dir / "index.json"
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2)

        full_examples_dir = cls.kb_dir / "full-examples"
        full_examples_dir.mkdir()

        example_content = """# 温馨回忆

这是一个温馨的回忆场景示例。
"""
        example_path = full_examples_dir / "02-warm-memory.md"
        with open(example_path, 'w', encoding='utf-8') as f:
            f.write(example_content)

    @classmethod
    def tearDownClass(cls):
        """清理测试类"""
        shutil.rmtree(cls.test_dir)

    def test_full_workflow(self):
        """测试完整工作流"""
        # 1. 初始化知识库
        kb = OptimizedKnowledgeBase(str(self.kb_dir))

        # 2. 执行检索
        results = kb.retrieve("温馨", strategy=RetrievalStrategy.HYBRID)
        self.assertGreater(len(results), 0)

        # 3. 检查缓存
        results2 = kb.retrieve("温馨")
        self.assertEqual(len(results), len(results2))

        # 4. 获取性能统计
        stats = kb.get_performance_stats()
        self.assertGreater(stats['metrics']['total_queries'], 0)

        # 5. 导出索引
        output_path = Path(self.test_dir) / "exported_index.json"
        kb.export_index(str(output_path))
        self.assertTrue(output_path.exists())


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestLRUCache))
    suite.addTests(loader.loadTestsFromTestCase(TestMultiLevelCache))
    suite.addTests(loader.loadTestsFromTestCase(TestExampleMetadata))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformanceMetrics))
    suite.addTests(loader.loadTestsFromTestCase(TestRetrievalEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestOptimizedKnowledgeBase))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # 返回测试结果
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
