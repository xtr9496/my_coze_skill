#!/usr/bin/env python3
"""
中间件智能选型工具
根据场景需求自动推荐合适的中间件
"""

import json
import argparse
from typing import Dict, List
from pathlib import Path


# 中间件特性矩阵
MIDDLEWARE_MATRIX = {
    "database": {
        "mysql": {
            "name": "MySQL",
            "strengths": ["事务支持", "复杂查询", "成熟稳定", "生态丰富"],
            "weaknesses": ["水平扩展难", "大数据量有限"],
            "use_cases": ["OLTP", "电商订单", "用户系统", "金融交易"],
            "scale": "百万级用户",
            "performance": "高",
            "difficulty": "低",
        },
        "postgresql": {
            "name": "PostgreSQL",
            "strengths": ["高级特性", "JSON支持", "扩展性强", "标准兼容"],
            "weaknesses": ["写入性能", "生态"],
            "use_cases": ["GIS地理", "数据分析", "复杂查询", "企业应用"],
            "scale": "百万级用户",
            "performance": "高",
            "difficulty": "中",
        },
        "mongodb": {
            "name": "MongoDB",
            "strengths": ["文档模型", "水平扩展", "灵活 schema", "易上手"],
            "weaknesses": ["事务限制", "内存占用"],
            "use_cases": ["内容管理", "日志存储", "实时分析", "IoT数据"],
            "scale": "千万级用户",
            "performance": "高",
            "difficulty": "低",
        },
        "redis": {
            "name": "Redis",
            "strengths": ["极速性能", "丰富数据结构", "持久化", "集群成熟"],
            "weaknesses": ["单线程", "内存成本"],
            "use_cases": ["缓存", "会话", "排行榜", "实时计算"],
            "scale": "亿级用户",
            "performance": "极高",
            "difficulty": "低",
        },
    },
    "mq": {
        "kafka": {
            "name": "Kafka",
            "strengths": ["高吞吐", "持久化", "流处理", "生态完善"],
            "weaknesses": ["延迟", "复杂度"],
            "use_cases": ["日志收集", "事件流", "数据管道", "实时分析"],
            "scale": "亿级消息",
            "performance": "极高",
            "difficulty": "高",
        },
        "rabbitmq": {
            "name": "RabbitMQ",
            "strengths": ["灵活路由", "消息确认", "管理友好", "协议支持广"],
            "weaknesses": ["吞吐有限", "集群复杂"],
            "use_cases": ["任务队列", "复杂路由", "企业集成", "微服务通信"],
            "scale": "百万级消息",
            "performance": "高",
            "difficulty": "中",
        },
        "rocketmq": {
            "name": "RocketMQ",
            "strengths": ["事务消息", "顺序消息", "阿里背书", "中文友好"],
            "weaknesses": ["生态较小", "国际影响力有限"],
            "use_cases": ["订单系统", "金融交易", "电商场景", "分布式事务"],
            "scale": "千万级消息",
            "performance": "高",
            "difficulty": "中",
        },
    },
    "cache": {
        "redis": {
            "name": "Redis",
            "strengths": ["数据结构丰富", "持久化", "集群成熟"],
            "weaknesses": ["内存成本", "单线程"],
            "use_cases": ["页面缓存", "会话", "分布式锁"],
            "scale": "亿级",
            "performance": "极高",
            "difficulty": "低",
        },
        "memcached": {
            "name": "Memcached",
            "strengths": ["简单高效", "内存利用率高"],
            "weaknesses": ["无持久化", "功能单一"],
            "use_cases": ["简单缓存", "页面缓存"],
            "scale": "千万级",
            "performance": "高",
            "difficulty": "低",
        },
    },
    "search": {
        "elasticsearch": {
            "name": "Elasticsearch",
            "strengths": ["全文检索", "聚合分析", "实时搜索", "生态完善"],
            "weaknesses": ["资源消耗大", "复杂度"],
            "use_cases": ["全文搜索", "日志分析", "监控可视化"],
            "scale": "PB级数据",
            "performance": "高",
            "difficulty": "中",
        },
        "meilisearch": {
            "name": "Meilisearch",
            "strengths": ["简单易用", "搜索快", "开箱即用"],
            "weaknesses": ["功能有限", "新项目"],
            "use_cases": ["嵌入式搜索", "中小型应用"],
            "scale": "TB级数据",
            "performance": "高",
            "difficulty": "低",
        },
    },
    "gateway": {
        "kong": {
            "name": "Kong",
            "strengths": ["插件丰富", "性能好", "社区活跃"],
            "weaknesses": ["配置复杂", "学习曲线"],
            "use_cases": ["API网关", "认证鉴权", "流量控制"],
            "scale": "百万级QPS",
            "performance": "高",
            "difficulty": "中",
        },
        "apisix": {
            "name": "APISIX",
            "strengths": ["高性能", "国产开源", "动态配置"],
            "weaknesses": ["相对新", "生态建设中"],
            "use_cases": ["API网关", "服务网格"],
            "scale": "百万级QPS",
            "performance": "极高",
            "difficulty": "中",
        },
    },
}


def select_database(requirements: dict) -> Dict:
    """根据需求选择数据库"""
    use_cases = requirements.get("use_cases", [])
    scale = requirements.get("scale", "medium")
    need_transaction = requirements.get("need_transaction", False)
    need_complex_query = requirements.get("need_complex_query", False)
    need_geo = requirements.get("need_geo", False)

    # 交易系统优先选关系型
    if need_transaction:
        if need_geo:
            return {"type": "postgresql", "reason": "需要事务+地理信息功能"}
        return {"type": "mysql", "reason": "事务支持好，适合OLTP场景"}

    # 需要复杂查询
    if need_complex_query:
        return {"type": "postgresql", "reason": "复杂查询能力强，JSON支持好"}

    # 大数据量+灵活schema
    if "content" in use_cases or "log" in use_cases or "iot" in use_cases:
        return {"type": "mongodb", "reason": "文档模型灵活，适合非结构化数据"}

    # 默认选择
    return {"type": "mysql", "reason": "通用场景，稳定可靠"}


def select_mq(requirements: dict) -> Dict:
    """根据需求选择消息队列"""
    use_cases = requirements.get("use_cases", [])
    need_transaction = requirements.get("need_transaction", False)
    high_throughput = requirements.get("high_throughput", False)
    need_order = requirements.get("need_order", False)

    # 交易系统需要事务消息
    if need_transaction:
        return {"type": "rocketmq", "reason": "支持分布式事务消息，顺序消息"}

    # 高吞吐日志场景
    if "log" in use_cases or "stream" in use_cases or high_throughput:
        return {"type": "kafka", "reason": "高吞吐，适合日志和流处理"}

    # 通用场景
    return {"type": "rabbitmq", "reason": "灵活路由，消息确认机制完善"}


def select_cache(requirements: dict) -> Dict:
    """根据需求选择缓存"""
    need_complex_data = requirements.get("need_complex_data", False)
    need_persistence = requirements.get("need_persistence", False)

    # 需要复杂数据结构或持久化
    if need_complex_data or need_persistence:
        return {"type": "redis", "reason": "数据结构丰富，支持持久化"}

    # 简单缓存
    return {"type": "memcached", "reason": "简单高效，内存利用率高"}


def select_search(requirements: dict) -> Dict:
    """根据需求选择搜索引擎"""
    need_fulltext = requirements.get("need_fulltext", False)
    need_log_analysis = requirements.get("need_log_analysis", False)

    if need_log_analysis:
        return {"type": "elasticsearch", "reason": "ELK生态完善，适合日志分析"}

    if need_fulltext:
        return {"type": "elasticsearch", "reason": "全文检索能力强，生态完善"}

    return {"type": "elasticsearch", "reason": "通用搜索场景"}


def select_gateway(requirements: dict) -> Dict:
    """根据需求选择网关"""
    scale = requirements.get("scale", "medium")
    need_plugins = requirements.get("need_plugins", False)

    # 大规模或需要丰富插件
    if scale == "large" or need_plugins:
        return {"type": "kong", "reason": "插件丰富，社区活跃"}

    # 国产优先或追求高性能
    return {"type": "apisix", "reason": "高性能，动态配置能力强"}


def generate_recommendation(requirements: dict):
    """生成中间件选型推荐"""

    recommendations = {
        "database": select_database(requirements),
        "mq": select_mq(requirements),
        "cache": select_cache(requirements),
        "search": select_search(requirements),
        "gateway": select_gateway(requirements),
    }

    # 生成报告
    report = []
    report.append("# 中间件选型推荐报告\n\n")

    report.append("## 推荐方案\n\n")
    for category, rec in recommendations.items():
        mw_info = MIDDLEWARE_MATRIX.get(category, {}).get(rec["type"], {})
        report.append(f"### {category.upper()}\n")
        report.append(f"- **推荐选择**: {mw_info.get('name', rec['type'])}\n")
        report.append(f"- **推荐理由**: {rec['reason']}\n")
        if mw_info:
            report.append(f"- **适用规模**: {mw_info.get('scale', '待定')}\n")
            report.append(f"- **性能评级**: {mw_info.get('performance', '待定')}\n")
            report.append(f"- **上手难度**: {mw_info.get('difficulty', '待定')}\n")
        report.append("\n")

    report.append("## 备选方案\n\n")
    for category, rec in recommendations.items():
        mw_info = MIDDLEWARE_MATRIX.get(category, {}).get(rec["type"], {})
        alternatives = []
        for key, info in MIDDLEWARE_MATRIX.get(category, {}).items():
            if key != rec["type"]:
                alternatives.append(info.get("name", key))
        if alternatives:
            report.append(
                f"- **{category.upper()}备选**: {', '.join(alternatives[:2])}\n"
            )

    return recommendations, "".join(report)


def main():
    parser = argparse.ArgumentParser(description="中间件智能选型")
    parser.add_argument("--input", "-i", required=True, help="需求JSON文件路径")
    parser.add_argument("--output", "-o", required=True, help="输出Markdown文件路径")

    args = parser.parse_args()

    # 读取需求
    with open(args.input, "r", encoding="utf-8") as f:
        requirements = json.load(f)

    # 生成推荐
    recommendation_json, recommendation_report = generate_recommendation(requirements)

    # 输出JSON（用于后续处理）
    with open(args.output.replace(".md", ".json"), "w", encoding="utf-8") as f:
        json.dump(recommendation_json, f, ensure_ascii=False, indent=2)

    # 输出报告
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(recommendation_report)

    print(f"中间件选型报告已生成: {args.output}")


if __name__ == "__main__":
    main()
