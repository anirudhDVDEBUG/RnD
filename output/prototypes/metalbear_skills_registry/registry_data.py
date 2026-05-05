"""Mock registry data simulating the metalbear-co/skills repository structure."""

REGISTRY = [
    {
        "name": "k8s-debug",
        "description": "Debug Kubernetes pods, services, and deployments interactively",
        "triggers": ["debug kubernetes", "pod logs", "k8s troubleshoot"],
        "category": "infrastructure",
        "skill_md": """---
name: k8s-debug
description: |
  Debug Kubernetes pods, services, and deployments interactively with Claude.
  TRIGGER when: user asks to debug k8s resources, check pod logs, or troubleshoot deployments.
---

# K8s Debug

Interactively debug Kubernetes resources using kubectl and Claude's reasoning.

## When to use
- "Why is my pod crashing?"
- "Show me the logs for the api-gateway deployment"
- "Debug this CrashLoopBackOff"

## How to use
1. Ensure kubectl is configured with cluster access.
2. Describe the issue or resource to investigate.
3. Claude will run kubectl commands and analyze output.
""",
    },
    {
        "name": "docker-compose-gen",
        "description": "Generate docker-compose.yml from project structure",
        "triggers": ["docker compose", "generate docker", "containerize"],
        "category": "infrastructure",
        "skill_md": """---
name: docker-compose-gen
description: |
  Generate docker-compose.yml files by analyzing project structure and dependencies.
  TRIGGER when: user asks to create docker-compose, containerize a project, or set up local dev environment with Docker.
---

# Docker Compose Generator

Analyze your project and generate a production-ready docker-compose.yml.

## When to use
- "Create a docker-compose for this project"
- "Containerize my app with all its services"
- "Set up local dev with Docker"

## How to use
1. Point Claude at your project root.
2. It will analyze package files, Dockerfiles, and service dependencies.
3. Generates a docker-compose.yml with proper networking and volumes.
""",
    },
    {
        "name": "pytest-gen",
        "description": "Generate pytest test suites from source code",
        "triggers": ["generate tests", "pytest", "test coverage"],
        "category": "testing",
        "skill_md": """---
name: pytest-gen
description: |
  Generate comprehensive pytest test suites from Python source code.
  TRIGGER when: user asks to generate tests, improve test coverage, or create pytest fixtures.
---

# Pytest Generator

Generate pytest test suites with fixtures, mocks, and edge cases.

## When to use
- "Write tests for this module"
- "Generate pytest fixtures for my database models"
- "Improve test coverage for auth.py"

## How to use
1. Point to the source file(s) to test.
2. Claude analyzes function signatures, dependencies, and edge cases.
3. Generates test file with proper imports, fixtures, and assertions.
""",
    },
    {
        "name": "load-test-k6",
        "description": "Create k6 load test scripts with AI assistance",
        "triggers": ["load test", "k6", "performance test", "stress test"],
        "category": "testing",
        "skill_md": """---
name: load-test-k6
description: |
  Create k6 load test scripts by analyzing API endpoints and expected traffic patterns.
  TRIGGER when: user asks to create load tests, stress tests, or performance benchmarks.
---

# K6 Load Test Generator

Generate k6 load test scripts from API specs or route definitions.

## When to use
- "Create a load test for my API"
- "Generate k6 scripts for the checkout flow"
- "Stress test the /api/users endpoint"
""",
    },
    {
        "name": "helm-assist",
        "description": "Generate and validate Helm charts with Claude",
        "triggers": ["helm chart", "kubernetes helm", "helm template"],
        "category": "infrastructure",
        "skill_md": """---
name: helm-assist
description: |
  Generate and validate Helm charts for Kubernetes deployments.
  TRIGGER when: user asks to create helm charts, validate templates, or manage k8s packaging.
---

# Helm Assist

Generate, validate, and debug Helm charts.
""",
    },
    {
        "name": "api-doc-gen",
        "description": "Generate OpenAPI/Swagger docs from source code",
        "triggers": ["api documentation", "openapi", "swagger"],
        "category": "documentation",
        "skill_md": """---
name: api-doc-gen
description: |
  Generate OpenAPI 3.0 documentation by analyzing route handlers and models.
  TRIGGER when: user asks to generate API docs, create swagger specs, or document endpoints.
---

# API Documentation Generator

Analyze route handlers and generate OpenAPI 3.0 specs.
""",
    },
    {
        "name": "git-pr-review",
        "description": "Automated pull request review with security and style checks",
        "triggers": ["review pr", "pull request review", "code review"],
        "category": "workflow",
        "skill_md": """---
name: git-pr-review
description: |
  Review pull requests for security issues, style violations, and logic errors.
  TRIGGER when: user asks to review a PR, check code quality, or audit changes.
---

# PR Review

Automated pull request review covering security, style, and correctness.
""",
    },
    {
        "name": "sql-migrate",
        "description": "Generate safe SQL migrations from schema changes",
        "triggers": ["sql migration", "database migration", "schema change"],
        "category": "database",
        "skill_md": """---
name: sql-migrate
description: |
  Generate safe, reversible SQL migrations from schema diffs.
  TRIGGER when: user asks to create migrations, alter tables, or manage schema changes.
---

# SQL Migrate

Generate safe SQL migrations with up/down scripts.
""",
    },
    {
        "name": "ci-pipeline-gen",
        "description": "Generate CI/CD pipeline configs for GitHub Actions, GitLab CI",
        "triggers": ["ci pipeline", "github actions", "gitlab ci", "ci/cd"],
        "category": "workflow",
        "skill_md": """---
name: ci-pipeline-gen
description: |
  Generate CI/CD pipeline configurations for popular platforms.
  TRIGGER when: user asks to set up CI/CD, create GitHub Actions workflows, or configure GitLab CI.
---

# CI Pipeline Generator

Generate CI/CD configs for GitHub Actions, GitLab CI, and CircleCI.
""",
    },
    {
        "name": "k8s-migration",
        "description": "Migrate workloads between Kubernetes clusters with AI guidance",
        "triggers": ["migrate kubernetes", "cluster migration", "k8s move"],
        "category": "infrastructure",
        "skill_md": """---
name: k8s-migration
description: |
  Guide workload migration between Kubernetes clusters.
  TRIGGER when: user asks to migrate between clusters, move workloads, or plan k8s migrations.
---

# K8s Migration

Guided migration of workloads between Kubernetes clusters.
""",
    },
    {
        "name": "env-vault",
        "description": "Manage environment variables securely with encrypted .env files",
        "triggers": ["env variables", "secrets management", "encrypted env"],
        "category": "security",
        "skill_md": """---
name: env-vault
description: |
  Manage environment variables with encryption and secure sharing.
  TRIGGER when: user asks to manage secrets, encrypt env files, or share credentials securely.
---

# Env Vault

Secure environment variable management with encryption.
""",
    },
    {
        "name": "mcp-scaffold",
        "description": "Scaffold new MCP server projects with best practices",
        "triggers": ["create mcp server", "mcp scaffold", "new mcp"],
        "category": "claude-ecosystem",
        "skill_md": """---
name: mcp-scaffold
description: |
  Scaffold new MCP (Model Context Protocol) server projects following best practices.
  TRIGGER when: user asks to create an MCP server, scaffold MCP project, or start a new tool server.
---

# MCP Scaffold

Generate MCP server boilerplate with proper tool definitions and transport setup.
""",
    },
]
