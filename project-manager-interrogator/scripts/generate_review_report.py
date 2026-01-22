#!/usr/bin/env python3
"""
需求评审报告生成器
根据用户输入的需求信息，生成结构化的评审报告
"""

import json
import argparse
from datetime import datetime
from pathlib import Path


def generate_review_report(requirements: dict) -> str:
    """生成需求评审报告"""

    sections = []

    # 1. 需求概述
    sections.append("# 需求评审报告\n")
    sections.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    sections.append(f"**需求名称**: {requirements.get('name', '未命名需求')}\n")
    sections.append(f"**需求来源**: {requirements.get('source', '未指定')}\n\n")

    # 2. 核心问题清单（根据五维度框架）
    sections.append("## 核心问题清单\n")
    sections.append("### 技术维度\n")
    for q in requirements.get("technical_questions", []):
        sections.append(f"- [ ] {q}\n")
    sections.append("\n### 商业维度\n")
    for q in requirements.get("business_questions", []):
        sections.append(f"- [ ] {q}\n")
    sections.append("\n### 用户维度\n")
    for q in requirements.get("user_questions", []):
        sections.append(f"- [ ] {q}\n")
    sections.append("\n### 团队维度\n")
    for q in requirements.get("team_questions", []):
        sections.append(f"- [ ] {q}\n")
    sections.append("\n### 时间线维度\n")
    for q in requirements.get("timeline_questions", []):
        sections.append(f"- [ ] {q}\n")

    # 3. 风险评估
    sections.append("\n## 风险评估\n")
    sections.append("### 高风险（需立即处理）\n")
    for risk in requirements.get("high_risks", []):
        sections.append(f"- [ ] {risk}\n")
    sections.append("\n### 中风险（需规划应对）\n")
    for risk in requirements.get("medium_risks", []):
        sections.append(f"- [ ] {risk}\n")
    sections.append("\n### 低风险（持续关注）\n")
    for risk in requirements.get("low_risks", []):
        sections.append(f"- [ ] {risk}\n")

    # 4. 建议行动项
    sections.append("\n## 建议行动项\n")
    sections.append("| 优先级 | 行动项 | 负责方 | 截止时间 |\n")
    sections.append("|--------|--------|--------|----------|\n")
    for action in requirements.get("action_items", []):
        sections.append(
            f"| {action.get('priority', '中')} | {action.get('item', '')} | {action.get('owner', '')} | {action.get('deadline', '')} |\n"
        )

    # 5. 结论
    sections.append("\n## 评审结论\n")
    conclusion = requirements.get("conclusion", "待定")
    sections.append(f"**总体评估**: {conclusion}\n\n")
    sections.append("**下一步建议**:\n")
    for next_step in requirements.get("next_steps", []):
        sections.append(f"- {next_step}\n")

    return "".join(sections)


def main():
    parser = argparse.ArgumentParser(description="生成需求评审报告")
    parser.add_argument("--input", "-i", required=True, help="输入JSON文件路径")
    parser.add_argument("--output", "-o", required=True, help="输出Markdown文件路径")

    args = parser.parse_args()

    # 读取输入
    with open(args.input, "r", encoding="utf-8") as f:
        requirements = json.load(f)

    # 生成报告
    report = generate_review_report(requirements)

    # 输出报告
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"报告已生成: {args.output}")


if __name__ == "__main__":
    main()
