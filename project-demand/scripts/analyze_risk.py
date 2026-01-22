#!/usr/bin/env python3
"""
风险分析工具
根据需求描述自动识别潜在风险
"""

import json
import argparse
from typing import List, Dict
from pathlib import Path


# 风险关键词库
RISK_KEYWORDS = {
    "high": [
        ("技术不可行", ["无法实现", "技术瓶颈", "突破极限"]),
        ("时间不现实", ["紧急", "尽快", "马上", " deadline", "来不及"]),
        ("资源严重不足", ["没有人", "缺人", "预算不够", "没钱"]),
        ("需求根本矛盾", ["既要又要", "冲突", "矛盾"]),
        ("商业价值存疑", ["不知道能不能赚钱", "不确定有没有用"]),
    ],
    "medium": [
        ("技术选型争议", ["新技术", "不熟悉", "没用过"]),
        ("扩展性不足", ["担心以后", "怕撑不住", " scalability"]),
        ("跨团队协作", ["需要其他部门", "依赖别的团队"]),
        ("需求变更风险", ["可能会改", "不确定", "待定"]),
        ("测试时间不足", ["测试不够", "来不及测"]),
    ],
    "low": [
        ("代码质量问题", ["先上线再说", "后面再优化"]),
        ("文档缺失", ["文档后面补", "没时间写文档"]),
        ("监控不完善", ["先上线", "监控后面再加"]),
    ],
}


def analyze_risk(requirements_text: str) -> Dict[str, List[str]]:
    """分析需求文本中的风险"""

    risks = {"high_risks": [], "medium_risks": [], "low_risks": []}

    text_lower = requirements_text.lower()

    # 检测高风险
    for risk_name, keywords in RISK_KEYWORDS["high"]:
        for keyword in keywords:
            if keyword.lower() in text_lower:
                risks["high_risks"].append(
                    f"检测到'{risk_name}'风险: 包含关键词'{keyword}'"
                )

    # 检测中风险
    for risk_name, keywords in RISK_KEYWORDS["medium"]:
        for keyword in keywords:
            if keyword.lower() in text_lower:
                risks["medium_risks"].append(
                    f"检测到'{risk_name}'风险: 包含关键词'{keyword}'"
                )

    # 检测低风险
    for risk_name, keywords in RISK_KEYWORDS["low"]:
        for keyword in keywords:
            if keyword.lower() in text_lower:
                risks["low_risks"].append(
                    f"检测到'{risk_name}'风险: 包含关键词'{keyword}'"
                )

    return risks


def generate_risk_report(risks: Dict, requirements: dict) -> str:
    """生成风险分析报告"""

    sections = []
    sections.append("# 风险分析报告\n\n")

    # 需求概要
    sections.append("## 需求概要\n")
    sections.append(f"**需求名称**: {requirements.get('name', '未命名')}\n")
    sections.append(
        f"**需求描述**: {requirements.get('description', '无描述')[:200]}...\n\n"
    )

    # 高风险
    sections.append("## 高风险（需立即处理）\n")
    if risks["high_risks"]:
        for risk in risks["high_risks"]:
            sections.append(f"- 🔴 {risk}\n")
    else:
        sections.append("- 未检测到明显高风险\n")
    sections.append("\n")

    # 中风险
    sections.append("## 中风险（需规划应对）\n")
    if risks["medium_risks"]:
        for risk in risks["medium_risks"]:
            sections.append(f"- 🟡 {risk}\n")
    else:
        sections.append("- 未检测到明显中风险\n")
    sections.append("\n")

    # 低风险
    sections.append("## 低风险（持续关注）\n")
    if risks["low_risks"]:
        for risk in risks["low_risks"]:
            sections.append(f"- 🔵 {risk}\n")
    else:
        sections.append("- 未检测到明显低风险\n")
    sections.append("\n")

    # 建议
    sections.append("## 应对建议\n")
    if risks["high_risks"]:
        sections.append(
            "⚠️ **建议**: 检测到高风险，建议暂停当前讨论，优先解决高风险问题。\n"
        )
    elif risks["medium_risks"]:
        sections.append("⚡ **建议**: 检测到中风险，建议在进入开发前制定应对计划。\n")
    else:
        sections.append("✅ **建议**: 风险较低，可以继续推进。\n")

    return "".join(sections)


def main():
    parser = argparse.ArgumentParser(description="分析需求风险")
    parser.add_argument("--input", "-i", required=True, help="输入JSON文件路径")
    parser.add_argument("--output", "-o", required=True, help="输出Markdown文件路径")

    args = parser.parse_args()

    # 读取输入
    with open(args.input, "r", encoding="utf-8") as f:
        requirements = json.load(f)

    # 分析风险
    requirements_text = requirements.get("description", "")
    risks = analyze_risk(requirements_text)

    # 生成报告
    report = generate_risk_report(risks, requirements)

    # 输出报告
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"风险分析报告已生成: {args.output}")


if __name__ == "__main__":
    main()
