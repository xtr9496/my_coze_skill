#!/usr/bin/env python3
"""
架构设计文档生成器
根据需求分析和架构决策，生成完整的架构设计文档
"""

import json
import argparse
from datetime import datetime
from pathlib import Path


def generate_architecture_doc(requirements: dict, architecture: dict) -> str:
    """生成完整的架构设计文档"""

    sections = []

    # 标题
    sections.append(f"# {requirements.get('name', '系统')} 架构设计文档\n")
    sections.append(f"**版本**: 1.0\n")
    sections.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    sections.append(f"**架构师**: AI Assistant\n\n")

    # 目录
    sections.append("## 目录\n")
    sections.append("- [1. 需求概述](#1-需求概述)\n")
    sections.append("- [2. 架构总览](#2-架构总览)\n")
    sections.append("- [3. 模块设计](#3-模块设计)\n")
    sections.append("- [4. 技术选型](#4-技术选型)\n")
    sections.append("- [5. 数据设计](#5-数据设计)\n")
    sections.append("- [6. 部署架构](#6-部署架构)\n")
    sections.append("- [7. 风险评估](#7-风险评估)\n")
    sections.append("- [8. 演进路线](#8-演进路线)\n\n")

    # 1. 需求概述
    sections.append("## 1. 需求概述\n\n")
    sections.append("### 1.1 功能性需求\n")
    for feature in requirements.get("features", []):
        sections.append(f"- {feature}\n")
    sections.append("\n")
    sections.append("### 1.2 非功能性需求\n")
    nfr = requirements.get("non_functional", {})
    sections.append(
        f"- **性能指标**: QPS目标 {nfr.get('qps', '待定')}, 响应时间 {nfr.get('response_time', '待定')}\n"
    )
    sections.append(
        f"- **可用性要求**: SLA {nfr.get('sla', '待定')}, 容灾目标 {nfr.get('disaster_recovery', '待定')}\n"
    )
    sections.append(
        f"- **扩展性需求**: 支持用户数 {nfr.get('users', '待定')}, 数据量 {nfr.get('data_volume', '待定')}\n"
    )
    sections.append(f"- **安全性要求**: {nfr.get('security', '待定')}\n")
    sections.append(f"- **成本预算**: {nfr.get('budget', '待定')}\n")
    sections.append(f"- **时间约束**: {nfr.get('timeline', '待定')}\n\n")

    # 2. 架构总览
    sections.append("## 2. 架构总览\n\n")
    sections.append(f"**架构模式**: {architecture.get('pattern', '待定')}\n\n")
    sections.append("### 2.1 架构图\n")
    sections.append("```mermaid\n")
    sections.append(
        architecture.get(
            "mermaid_diagram", "graph TD\n    A[用户] --> B[网关]\n    B --> C[服务]\n"
        )
    )
    sections.append("```\n\n")
    sections.append("### 2.2 设计原则\n")
    for principle in architecture.get("principles", []):
        sections.append(f"- {principle}\n")
    sections.append("\n")

    # 3. 模块设计
    sections.append("## 3. 模块设计\n\n")
    modules = architecture.get("modules", [])
    for idx, module in enumerate(modules, 1):
        sections.append(f"### 3.{idx} {module.get('name', '模块')}\n")
        sections.append(f"- **职责**: {module.get('responsibility', '待定')}\n")
        sections.append(f"- **接口**: {module.get('interfaces', '待定')}\n")
        sections.append(f"- **依赖**: {module.get('dependencies', '无')}\n\n")

    # 4. 技术选型
    sections.append("## 4. 技术选型\n\n")
    tech_stack = architecture.get("tech_stack", {})
    sections.append("### 4.1 前端技术\n")
    sections.append(
        f"- **框架**: {tech_stack.get('frontend', {}).get('framework', '待定')}\n"
    )
    sections.append(
        f"- **状态管理**: {tech_stack.get('frontend', {}).get('state_management', '待定')}\n"
    )
    sections.append(
        f"- **UI库**: {tech_stack.get('frontend', {}).get('ui_library', '待定')}\n\n"
    )
    sections.append("### 4.2 后端技术\n")
    sections.append(
        f"- **语言**: {tech_stack.get('backend', {}).get('language', '待定')}\n"
    )
    sections.append(
        f"- **框架**: {tech_stack.get('backend', {}).get('framework', '待定')}\n"
    )
    sections.append(
        f"- **运行时**: {tech_stack.get('backend', {}).get('runtime', '待定')}\n\n"
    )
    sections.append("### 4.3 中间件选型\n")
    middleware = tech_stack.get("middleware", {})
    sections.append(f"- **数据库**: {middleware.get('database', '待定')}\n")
    sections.append(f"- **缓存**: {middleware.get('cache', '待定')}\n")
    sections.append(f"- **消息队列**: {middleware.get('mq', '待定')}\n")
    sections.append(f"- **搜索引擎**: {middleware.get('search', '待定')}\n")
    sections.append(f"- **服务治理**: {middleware.get('governance', '待定')}\n\n")

    # 5. 数据设计
    sections.append("## 5. 数据设计\n\n")
    sections.append("### 5.1 数据存储方案\n")
    for ds in architecture.get("data_storage", []):
        sections.append(
            f"- **{ds.get('type', '类型')}**: {ds.get('description', '描述')}\n"
        )
    sections.append("\n")
    sections.append("### 5.2 数据流转\n")
    sections.append("```\n")
    sections.append(
        architecture.get("data_flow", "用户请求 -> 网关 -> 服务 -> 数据库\n")
    )
    sections.append("```\n\n")

    # 6. 部署架构
    sections.append("## 6. 部署架构\n\n")
    sections.append(
        f"**部署环境**: {architecture.get('deployment', {}).get('environment', '待定')}\n"
    )
    sections.append(
        f"**容器编排**: {architecture.get('deployment', {}).get('orchestration', '待定')}\n"
    )
    sections.append(
        f"**CI/CD**: {architecture.get('deployment', {}).get('cicd', '待定')}\n\n"
    )
    sections.append("### 6.1 部署拓扑\n")
    sections.append("```\n")
    sections.append(architecture.get("deployment_topology", "负载均衡 -> 多实例服务\n"))
    sections.append("```\n\n")

    # 7. 风险评估
    sections.append("## 7. 风险评估\n\n")
    risks = architecture.get("risks", [])
    for risk in risks:
        sections.append(f"### {risk.get('name', '风险')}\n")
        sections.append(f"- **等级**: {risk.get('level', '待定')}\n")
        sections.append(f"- **描述**: {risk.get('description', '待定')}\n")
        sections.append(f"- **应对措施**: {risk.get('mitigation', '待定')}\n\n")

    # 8. 演进路线
    sections.append("## 8. 演进路线\n\n")
    roadmap = architecture.get("roadmap", [])
    for idx, phase in enumerate(roadmap, 1):
        sections.append(f"### 阶段{idx}: {phase.get('name', '待定')}\n")
        sections.append(f"- **时间**: {phase.get('timeline', '待定')}\n")
        sections.append(f"- **目标**: {phase.get('goal', '待定')}\n")
        sections.append(f"- **交付物**: {phase.get('deliverables', '待定')}\n\n")

    return "".join(sections)


def main():
    parser = argparse.ArgumentParser(description="生成架构设计文档")
    parser.add_argument("--requirements", "-r", required=True, help="需求JSON文件路径")
    parser.add_argument(
        "--architecture", "-a", required=True, help="架构决策JSON文件路径"
    )
    parser.add_argument("--output", "-o", required=True, help="输出Markdown文件路径")

    args = parser.parse_args()

    # 读取输入
    with open(args.requirements, "r", encoding="utf-8") as f:
        requirements = json.load(f)
    with open(args.architecture, "r", encoding="utf-8") as f:
        architecture = json.load(f)

    # 生成文档
    doc = generate_architecture_doc(requirements, architecture)

    # 输出文档
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(doc)

    print(f"架构设计文档已生成: {args.output}")


if __name__ == "__main__":
    main()
