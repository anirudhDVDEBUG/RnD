---
name: Clover Job Search & Interview Prep
description: |
  Claude skill + MCP integration for job search and interview preparation.
  Provides live job data, role-specific interview intelligence, and career tools.
  Triggers: job search, interview prep, career coaching, resume review, mock interview
---

# Clover Job Search & Interview Prep

Open-source Claude Skill and MCP integration for job search and interview preparation, powered by [four-leaf.ai](https://four-leaf.ai).

## When to use

- "Help me find jobs matching my skills and experience"
- "Prepare me for an interview at [company] for [role]"
- "What interview questions should I expect for a software engineer role?"
- "Review my resume and suggest improvements"
- "Give me role-specific interview intel for this position"

## How to use

### 1. Install the MCP Server

Add the Clover MCP server to your Claude configuration:

```json
{
  "mcpServers": {
    "clover": {
      "command": "npx",
      "args": ["-y", "@fourleafai/clover-mcp"]
    }
  }
}
```

### 2. Job Search

Use the skill to search for live job listings:

- Specify your target role, location, and preferences
- Get real-time job data with relevant matches
- Filter by company, seniority level, remote/hybrid/onsite

### 3. Interview Preparation

Leverage role-specific interview intelligence:

- Get common interview questions for the target role and company
- Receive structured preparation guides covering behavioral, technical, and situational questions
- Practice with role-specific scenarios

### 4. Resume & Career Tools

- Review and optimize your resume for target roles
- Get actionable feedback on content, formatting, and keyword alignment
- Align your experience with job requirements

### 5. Voice Mock Interviews

For interactive voice mock interviews, visit [four-leaf.ai](https://four-leaf.ai) to access the full platform experience.

## References

- **Source Repository**: [fourleafai/clover-public](https://github.com/fourleafai/clover-public)
- **Platform**: [four-leaf.ai](https://four-leaf.ai)
- **Topics**: claude-skill, mcp-server, job-search, interview-prep, career-tools, resume
