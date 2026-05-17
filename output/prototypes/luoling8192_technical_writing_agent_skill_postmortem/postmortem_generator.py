#!/usr/bin/env python3
"""
Chinese Technical Writing — Postmortem Generator

Generates structured postmortem documents following Chinese internal
technical writing conventions: objective tone, short sentences,
quantified impact, and actionable improvement items.

This demonstrates the skill by:
1. Taking incident data (structured dict or JSON)
2. Producing a formatted postmortem in Markdown
3. Running a style linter to flag violations
"""

import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class TimelineEntry:
    time: str  # ISO 8601
    event: str


@dataclass
class ActionItem:
    priority: str  # P0, P1, P2
    description: str
    owner_role: str
    deadline: str
    acceptance_criteria: str


@dataclass
class IncidentData:
    title: str
    summary: str
    impact_duration: str
    affected_users: int
    peak_error_rate: str
    slo_budget_consumed: str
    timeline: list[TimelineEntry] = field(default_factory=list)
    root_cause_chain: list[str] = field(default_factory=list)
    fix_description: str = ""
    action_items: list[ActionItem] = field(default_factory=list)
    lessons_good: list[str] = field(default_factory=list)
    lessons_improve: list[str] = field(default_factory=list)
    lessons_luck: list[str] = field(default_factory=list)


def generate_postmortem(incident: IncidentData) -> str:
    """Generate a formatted postmortem markdown document."""
    lines = []

    # Title
    lines.append(f"# {incident.title} Postmortem\n")

    # Summary
    lines.append("## 摘要\n")
    lines.append(f"{incident.summary}\n")

    # Impact
    lines.append("## 影响范围\n")
    lines.append("| 指标 | 数值 |")
    lines.append("|------|------|")
    lines.append(f"| 影响时长 | {incident.impact_duration} |")
    lines.append(f"| 受影响用户数 | {incident.affected_users:,} |")
    lines.append(f"| 错误率峰值 | {incident.peak_error_rate} |")
    lines.append(f"| SLO 消耗 | {incident.slo_budget_consumed} |")
    lines.append("")

    # Timeline
    lines.append("## 时间线\n")
    lines.append("| 时间 (UTC+8) | 事件 |")
    lines.append("|---------------|------|")
    for entry in incident.timeline:
        lines.append(f"| {entry.time} | {entry.event} |")
    lines.append("")

    # Root Cause
    lines.append("## 根因分析\n")
    lines.append("使用 5 Whys 因果链：\n")
    for i, cause in enumerate(incident.root_cause_chain, 1):
        lines.append(f"{i}. **Why?** {cause}")
    lines.append("")

    # Fix
    lines.append("## 修复措施\n")
    lines.append(f"{incident.fix_description}\n")

    # Action Items
    lines.append("## 改进项\n")
    lines.append("| 优先级 | 改进项 | 负责角色 | 截止时间 | 验收标准 |")
    lines.append("|---------|--------|----------|----------|----------|")
    for item in incident.action_items:
        lines.append(
            f"| {item.priority} | {item.description} | "
            f"{item.owner_role} | {item.deadline} | {item.acceptance_criteria} |"
        )
    lines.append("")

    # Lessons
    lines.append("## 经验教训\n")
    lines.append("**做得好的：**")
    for lesson in incident.lessons_good:
        lines.append(f"- {lesson}")
    lines.append("")
    lines.append("**需要改进的：**")
    for lesson in incident.lessons_improve:
        lines.append(f"- {lesson}")
    lines.append("")
    lines.append("**运气成分：**")
    for lesson in incident.lessons_luck:
        lines.append(f"- {lesson}")
    lines.append("")

    return "\n".join(lines)


# --- Style Linter ---

@dataclass
class LintIssue:
    line_num: int
    severity: str  # "error" | "warning"
    rule: str
    message: str


def lint_postmortem(text: str) -> list[LintIssue]:
    """Check postmortem text against Chinese technical writing style rules."""
    issues = []
    lines = text.split("\n")

    required_sections = ["摘要", "影响范围", "时间线", "根因分析", "修复措施", "改进项", "经验教训"]
    found_sections = set()

    blame_patterns = [
        (r"[某他她].*[的]?错", "避免指责个人，应归因于系统或流程"),
        (r"不应该", "使用客观陈述替代主观判断"),
        (r"太[慢懒粗]", "避免带有情绪色彩的形容词"),
    ]

    for i, line in enumerate(lines, 1):
        # Check for required sections
        for section in required_sections:
            if f"## {section}" in line:
                found_sections.add(section)

        # Check sentence length (for non-header, non-table lines)
        if line and not line.startswith("#") and not line.startswith("|") and not line.startswith("-"):
            # Count Chinese characters
            chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', line))
            if chinese_chars > 60:
                issues.append(LintIssue(
                    line_num=i,
                    severity="warning",
                    rule="sentence-length",
                    message=f"句子过长（{chinese_chars} 字），建议拆分为短句（≤30 字/句）"
                ))

        # Check blame patterns
        for pattern, msg in blame_patterns:
            if re.search(pattern, line):
                issues.append(LintIssue(
                    line_num=i,
                    severity="error",
                    rule="no-blame",
                    message=msg
                ))

        # Check time format (should be ISO 8601-ish)
        time_matches = re.findall(r'\d{1,2}[::]\d{2}', line)
        if time_matches and "时间" not in line and "|--" not in line:
            if not re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}', line):
                # Only flag if it looks like a timeline entry
                if "|" in line and "时间" not in line:
                    pass  # Allow short time in tables for readability

    # Check missing sections
    missing = set(required_sections) - found_sections
    if missing:
        issues.append(LintIssue(
            line_num=0,
            severity="error",
            rule="required-sections",
            message=f"缺少必要章节：{', '.join(missing)}"
        ))

    return issues


def format_lint_report(issues: list[LintIssue]) -> str:
    """Format lint issues into a readable report."""
    if not issues:
        return "✅ 风格检查通过，无违规项。\n"

    lines = [f"⚠️  发现 {len(issues)} 个风格问题：\n"]
    for issue in sorted(issues, key=lambda x: (x.severity != "error", x.line_num)):
        icon = "❌" if issue.severity == "error" else "⚡"
        loc = f"L{issue.line_num}" if issue.line_num > 0 else "全局"
        lines.append(f"  {icon} [{issue.rule}] {loc}: {issue.message}")

    return "\n".join(lines) + "\n"


# --- Demo ---

def create_demo_incident() -> IncidentData:
    """Create a realistic demo incident for demonstration."""
    return IncidentData(
        title="支付服务 P99 延迟飙升",
        summary=(
            "2024-01-15T14:30 至 15:45（UTC+8），支付网关服务 P99 延迟从 200ms 飙升至 5200ms，"
            "导致约 12,000 名用户支付请求超时失败。根因为数据库连接池配置变更未经灰度验证直接上线。"
            "当前服务已恢复正常，改进项跟踪中。"
        ),
        impact_duration="1 小时 15 分钟",
        affected_users=12000,
        peak_error_rate="34.7%",
        slo_budget_consumed="本月 SLO 预算消耗 68%",
        timeline=[
            TimelineEntry("14:25", "变更工单 #CR-4521 合并，数据库连接池上限从 100 调整为 20"),
            TimelineEntry("14:30", "监控告警触发：支付服务 P99 > 2000ms"),
            TimelineEntry("14:35", "值班 SRE 确认告警，开始排查"),
            TimelineEntry("14:50", "定位到数据库连接池耗尽，活跃连接数持续为 20/20"),
            TimelineEntry("15:00", "尝试扩容连接池，但配置中心缓存未刷新"),
            TimelineEntry("15:20", "手动重启服务实例，强制拉取最新配置"),
            TimelineEntry("15:35", "连接池恢复至 100，延迟开始下降"),
            TimelineEntry("15:45", "P99 恢复至正常水平（< 300ms），告警解除"),
        ],
        root_cause_chain=[
            "支付服务 P99 延迟飙升 → 数据库连接池耗尽",
            "连接池耗尽 → 连接池上限被从 100 改为 20",
            "配置变更未被拦截 → 变更审批流程未包含性能影响评估",
            "无灰度验证 → 配置变更发布流程缺少灰度阶段",
            "缺少连接池水位告警 → 监控覆盖不完整",
        ],
        fix_description=(
            "1. 手动重启服务实例，强制刷新配置中心缓存，连接池恢复至 100。\n"
            "2. 回滚变更工单 #CR-4521，恢复原始配置。\n"
            "3. 临时添加连接池水位监控告警（阈值 80%）。"
        ),
        action_items=[
            ActionItem("P0", "配置变更发布流程增加灰度阶段", "平台工程负责人", "2024-02-01", "所有配置变更必须经过 5% → 50% → 100% 灰度"),
            ActionItem("P0", "添加数据库连接池水位告警", "SRE 团队", "2024-01-22", "连接池使用率 > 80% 时触发告警"),
            ActionItem("P1", "变更审批模板增加性能影响评估字段", "工程效能团队", "2024-02-15", "所有变更工单必须填写性能影响预估"),
            ActionItem("P2", "配置中心缓存刷新机制优化", "基础架构团队", "2024-03-01", "配置变更后 30s 内全量节点生效"),
        ],
        lessons_good=[
            "监控告警在 5 分钟内触发，值班响应及时",
            "时间线记录完整，排查方向正确",
        ],
        lessons_improve=[
            "配置变更缺少灰度验证机制",
            "变更审批未评估性能影响",
            "配置中心缓存刷新延迟过高",
        ],
        lessons_luck=[
            "事故发生在工作时间，值班人员快速响应；若发生在凌晨，影响时长可能翻倍",
        ],
    )


def main():
    print("=" * 60)
    print("  中文技术写作 Agent Skill — Postmortem 生成器 Demo")
    print("=" * 60)
    print()

    # Generate postmortem from demo data
    incident = create_demo_incident()
    postmortem_text = generate_postmortem(incident)

    print("📄 生成的 Postmortem 文档：")
    print("-" * 60)
    print(postmortem_text)
    print("-" * 60)

    # Run style linter
    print("\n🔍 风格检查结果：")
    issues = lint_postmortem(postmortem_text)
    print(format_lint_report(issues))

    # Demo: lint a bad example
    print("\n" + "=" * 60)
    print("  对比：违规写法检测 Demo")
    print("=" * 60)
    print()

    bad_example = """# 某次事故 Postmortem

## 摘要
小王不应该在没有经过审核的情况下直接修改了数据库的配置文件导致整个支付系统全部崩溃这件事情造成了非常严重的影响公司损失了很多钱客户也很不满意我们必须严肃处理这个问题。

## 时间线
| 时间 | 事件 |
|------|------|
| 下午两点半 | 小王改了配置 |
| 三点 | 系统挂了 |

## 修复措施
让小王把配置改回去了。他太粗心了。
"""

    print("📄 违规示例文本：")
    print("-" * 60)
    print(bad_example)
    print("-" * 60)

    print("\n🔍 风格检查结果：")
    bad_issues = lint_postmortem(bad_example)
    print(format_lint_report(bad_issues))

    # Write output file
    output_path = "output_postmortem.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(postmortem_text)
    print(f"\n✅ 完整 postmortem 已写入: {output_path}")


if __name__ == "__main__":
    main()
