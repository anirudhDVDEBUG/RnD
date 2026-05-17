# How to Use

## Installation (Claude Code Skill)

This is a **Claude Code skill**. No pip/npm install needed.

### 1. Copy the skill folder

```bash
mkdir -p ~/.claude/skills/chinese_technical_writing_postmortem
cp SKILL.md ~/.claude/skills/chinese_technical_writing_postmortem/SKILL.md
```

### 2. Trigger phrases

Once installed, Claude Code activates this skill when you say any of:

- "写 postmortem"
- "事故复盘"
- "故障报告"
- "postmortem"
- "incident report"

### 3. What it does when activated

Claude will:
1. Ask for incident details (or accept structured input)
2. Generate a postmortem following the mandated structure
3. Self-check against style rules (no blame, short sentences, quantified impact)
4. Output the final document in Markdown

## Running the Demo (standalone)

No API keys required. Pure Python, stdlib only.

```bash
bash run.sh
```

This generates a sample postmortem from mock incident data and runs the style
linter against both a good and bad example.

## First 60 Seconds

**Input** (tell Claude):
```
写 postmortem：今天下午支付服务挂了一个多小时，大概影响了一万多用户，
原因是有人改了连接池配置没有灰度就上线了。
```

**Output** (Claude produces):
```markdown
# 支付服务 P99 延迟飙升 Postmortem

## 摘要
2024-01-15T14:30 至 15:45（UTC+8），支付网关服务 P99 延迟从 200ms
飙升至 5200ms，导致约 12,000 名用户支付请求超时失败。...

## 影响范围
| 指标 | 数值 |
|------|------|
| 影响时长 | 1 小时 15 分钟 |
| 受影响用户数 | 12,000 |
...

## 改进项
| 优先级 | 改进项 | 负责角色 | 截止时间 | 验收标准 |
|---------|--------|----------|----------|----------|
| P0 | 配置变更增加灰度阶段 | 平台工程负责人 | 2024-02-01 | ... |
```

Key conventions enforced:
- No personal blame (uses roles, not names)
- Quantified impact table
- ISO 8601 timestamps
- Every action item has owner role + deadline + acceptance criteria
