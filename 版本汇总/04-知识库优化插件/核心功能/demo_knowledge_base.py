"""
知识库优化系统 - 简单演示
验证系统基本功能
"""

from knowledge_base_optimized import (
    OptimizedKnowledgeBase,
    RetrievalStrategy,
    create_optimized_index
)
import json
from pathlib import Path


def demo_basic_usage():
    """演示基本使用"""
    print("\n" + "=" * 70)
    print("知识库优化系统 - 基本使用演示")
    print("=" * 70)

    try:
        # 初始化知识库
        print("\n1. 初始化知识库...")
        kb = OptimizedKnowledgeBase(
            base_path="knowledge-base/cinematic-examples",
            hot_cache_size=50,
            warm_cache_size=200
        )

        print(f"✓ 知识库已加载")
        print(f"  - 示例总数: {len(kb.access.examples)}")

        # 显示所有示例
        print("\n2. 所有示例:")
        for i, (ex_id, metadata) in enumerate(kb.access.examples.items(), 1):
            print(f"  {i}. {metadata.title}")
            print(f"     ID: {ex_id}")
            print(f"     分类: {metadata.category}")
            print(f"     关键词: {', '.join(metadata.keywords)}")
            print(f"     文件: {metadata.file_path}")

        # 执行检索
        print("\n3. 执行检索测试:")

        test_queries = ["温馨", "悬疑", "远景", "情感表达"]

        for query in test_queries:
            print(f"\n   查询: '{query}'")
            results = kb.retrieve(query, strategy=RetrievalStrategy.HYBRID)

            if results:
                print(f"   找到 {len(results)} 个结果:")
                for i, result in enumerate(results, 1):
                    print(f"     {i}. {result.metadata.title}")
                    print(f"        相关性: {result.relevance_score:.2f}")
                    print(f"        匹配关键词: {', '.join(result.matched_keywords)}")
            else:
                print(f"   未找到结果")

        # 性能统计
        print("\n4. 性能统计:")
        stats = kb.get_performance_stats()

        print(f"  总查询数: {stats['metrics']['total_queries']}")
        print(f"  缓存命中: {stats['metrics']['cache_hits']}")
        print(f"  缓存未命中: {stats['metrics']['cache_misses']}")
        print(f"  缓存命中率: {stats['metrics']['cache_hit_rate']:.2%}")
        print(f"  平均查询时间: {stats['metrics']['avg_query_time']*1000:.2f}ms")

        # 缓存统计
        print(f"\n  缓存统计:")
        print(f"    热缓存: {stats['cache_stats']['hot_cache']['size']}/{stats['cache_stats']['hot_cache']['capacity']}")
        print(f"    温缓存: {stats['cache_stats']['warm_cache']['size']}/{stats['cache_stats']['warm_cache']['capacity']}")

        # 导出索引
        print("\n5. 导出优化索引...")
        output_path = "knowledge-base/cinematic-examples/index_optimized.json"
        index_data = kb.export_index(output_path)

        print(f"✓ 索引已导出到: {output_path}")
        print(f"  版本: {index_data['version']}")
        print(f"  示例总数: {index_data['statistics']['total_examples']}")
        print(f"  分类: {', '.join(index_data['statistics']['categories'])}")

        print("\n" + "=" * 70)
        print("演示完成!")
        print("=" * 70)

        return True

    except Exception as e:
        print(f"\n❌ 演示失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def demo_retrieval_strategies():
    """演示不同检索策略"""
    print("\n" + "=" * 70)
    print("知识库优化系统 - 检索策略演示")
    print("=" * 70)

    try:
        kb = OptimizedKnowledgeBase("knowledge-base/cinematic-examples")

        query = "温馨"
        strategies = [
            RetrievalStrategy.EXACT,
            RetrievalStrategy.FUZZY,
            RetrievalStrategy.SEMANTIC,
            RetrievalStrategy.HYBRID
        ]

        print(f"\n查询: '{query}'\n")

        for strategy in strategies:
            print(f"--- {strategy.value.upper()} 检索 ---")

            if strategy == RetrievalStrategy.SEMANTIC:
                results = kb.retrieve(
                    query,
                    strategy=strategy,
                    query_keywords=["温馨", "回忆", "特写"]
                )
            else:
                results = kb.retrieve(query, strategy=strategy)

            if results:
                print(f"找到 {len(results)} 个结果:")
                for i, result in enumerate(results, 1):
                    print(f"  {i}. {result.metadata.title} (相关性: {result.relevance_score:.2f})")
            else:
                print("未找到结果")

            print()

        print("=" * 70)
        return True

    except Exception as e:
        print(f"\n❌ 演示失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def demo_recommendations():
    """演示推荐功能"""
    print("\n" + "=" * 70)
    print("知识库优化系统 - 推荐功能演示")
    print("=" * 70)

    try:
        kb = OptimizedKnowledgeBase("knowledge-base/cinematic-examples")

        queries = ["温馨回忆", "悬疑揭示", "世界观建立"]

        for query in queries:
            print(f"\n查询: '{query}'")
            recommendations = kb.get_recommendations(query, limit=3)

            if recommendations:
                print(f"推荐 {len(recommendations)} 个示例:")
                for i, rec in enumerate(recommendations, 1):
                    print(f"  {i}. {rec.metadata.title}")
                    print(f"     相关性: {rec.relevance_score:.2f}")
                    print(f"     适用模板: {', '.join(rec.metadata.applicable_templates)}")
            else:
                print("未找到推荐")

        print("\n" + "=" * 70)
        return True

    except Exception as e:
        print(f"\n❌ 演示失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主程序"""
    print("\n" + "=" * 70)
    print("知识库优化系统 - 演示程序")
    print("=" * 70)

    demos = [
        ("基本使用", demo_basic_usage),
        ("检索策略", demo_retrieval_strategies),
        ("推荐功能", demo_recommendations)
    ]

    print("\n可用演示:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"{i}. {name}")

    print("\n" + "=" * 70)
    print("运行所有演示...")
    print("=" * 70)

    success_count = 0
    for name, demo_func in demos:
        try:
            if demo_func():
                success_count += 1
        except Exception as e:
            print(f"\n❌ 演示 '{name}' 执行失败: {e}")

    print("\n" + "=" * 70)
    print(f"演示完成! ({success_count}/{len(demos)} 成功)")
    print("=" * 70)


if __name__ == "__main__":
    main()
