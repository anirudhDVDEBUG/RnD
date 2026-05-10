"""
OpenWally Mock Pipeline
Simulates the multi-agent AI pipeline that turns a plain-text idea
into a scaffolded full-stack project (FastAPI + React + tests).

In real OpenWally, each agent is a CrewAI agent backed by Claude.
This mock demonstrates the pipeline stages and output structure
without requiring API keys.
"""

import json
import os
import sys
import time
import textwrap
from pathlib import Path


# ── Agent definitions (mirrors real OpenWally crew) ──────────────────────

AGENTS = [
    {
        "name": "Architect Agent",
        "role": "System Architect",
        "description": "Designs project structure, API endpoints, and data models",
    },
    {
        "name": "Backend Agent",
        "role": "Backend Developer",
        "description": "Generates FastAPI backend code with routes, models, and logic",
    },
    {
        "name": "Frontend Agent",
        "role": "Frontend Developer",
        "description": "Scaffolds React UI with components, pages, and styling",
    },
    {
        "name": "Testing Agent",
        "role": "QA Engineer",
        "description": "Creates test suites for backend and frontend",
    },
    {
        "name": "Integration Agent",
        "role": "DevOps Engineer",
        "description": "Wires everything together into a git-ready repository",
    },
]


# ── Simulated outputs per agent ──────────────────────────────────────────

def architect_output(idea: str) -> dict:
    return {
        "project_name": "taskflow",
        "description": idea,
        "architecture": "monorepo (backend/ + frontend/)",
        "backend_framework": "FastAPI",
        "frontend_framework": "React + Vite",
        "database": "SQLite (dev) / PostgreSQL (prod)",
        "endpoints": [
            {"method": "POST", "path": "/api/auth/register", "desc": "User registration"},
            {"method": "POST", "path": "/api/auth/login", "desc": "User login (JWT)"},
            {"method": "GET", "path": "/api/projects", "desc": "List projects"},
            {"method": "POST", "path": "/api/projects", "desc": "Create project"},
            {"method": "GET", "path": "/api/projects/{id}/tasks", "desc": "List tasks"},
            {"method": "POST", "path": "/api/projects/{id}/tasks", "desc": "Create task"},
            {"method": "PATCH", "path": "/api/tasks/{id}", "desc": "Update task status"},
            {"method": "GET", "path": "/api/notifications", "desc": "SSE notification stream"},
        ],
        "models": ["User", "Project", "Task", "Notification"],
    }


def backend_output(arch: dict) -> dict:
    files = {
        "backend/main.py": textwrap.dedent('''\
            from fastapi import FastAPI
            from fastapi.middleware.cors import CORSMiddleware
            from .routers import auth, projects, tasks, notifications

            app = FastAPI(title="TaskFlow API")
            app.add_middleware(CORSMiddleware, allow_origins=["*"],
                               allow_methods=["*"], allow_headers=["*"])

            app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
            app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
            app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
            app.include_router(notifications.router, prefix="/api/notifications", tags=["notifications"])
        '''),
        "backend/models.py": textwrap.dedent('''\
            from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
            from sqlalchemy.orm import relationship, DeclarativeBase
            from datetime import datetime

            class Base(DeclarativeBase):
                pass

            class User(Base):
                __tablename__ = "users"
                id = Column(Integer, primary_key=True)
                email = Column(String, unique=True, nullable=False)
                hashed_password = Column(String, nullable=False)
                projects = relationship("Project", back_populates="owner")

            class Project(Base):
                __tablename__ = "projects"
                id = Column(Integer, primary_key=True)
                name = Column(String, nullable=False)
                owner_id = Column(Integer, ForeignKey("users.id"))
                owner = relationship("User", back_populates="projects")
                tasks = relationship("Task", back_populates="project")

            class Task(Base):
                __tablename__ = "tasks"
                id = Column(Integer, primary_key=True)
                title = Column(String, nullable=False)
                status = Column(String, default="todo")
                project_id = Column(Integer, ForeignKey("projects.id"))
                project = relationship("Project", back_populates="tasks")
                created_at = Column(DateTime, default=datetime.utcnow)
        '''),
        "backend/routers/auth.py": "# JWT auth routes: register, login, me",
        "backend/routers/projects.py": "# CRUD routes for projects",
        "backend/routers/tasks.py": "# CRUD routes for tasks with status transitions",
        "backend/routers/notifications.py": "# SSE endpoint for real-time notifications",
        "backend/requirements.txt": "fastapi\nuvicorn\nsqlalchemy\npyjwt\npasslib[bcrypt]",
    }
    return {"files": files, "file_count": len(files)}


def frontend_output(arch: dict) -> dict:
    files = {
        "frontend/src/App.jsx": "// Main app with React Router",
        "frontend/src/pages/Login.jsx": "// Login form with JWT handling",
        "frontend/src/pages/Register.jsx": "// Registration form",
        "frontend/src/pages/Dashboard.jsx": "// Project board overview",
        "frontend/src/pages/ProjectBoard.jsx": "// Kanban board with drag-and-drop",
        "frontend/src/components/TaskCard.jsx": "// Draggable task card",
        "frontend/src/components/Navbar.jsx": "// Navigation bar with user menu",
        "frontend/src/components/NotificationBell.jsx": "// Real-time notification indicator",
        "frontend/src/hooks/useAuth.js": "// Auth context and JWT management",
        "frontend/src/hooks/useNotifications.js": "// SSE hook for live notifications",
        "frontend/package.json": '{"name":"taskflow-ui","dependencies":{"react":"^18","react-router-dom":"^6","axios":"^1"}}',
        "frontend/vite.config.js": "// Vite config with API proxy",
    }
    return {"files": files, "file_count": len(files)}


def testing_output(arch: dict) -> dict:
    files = {
        "backend/tests/test_auth.py": "# Tests for register/login endpoints",
        "backend/tests/test_projects.py": "# Tests for project CRUD",
        "backend/tests/test_tasks.py": "# Tests for task CRUD and status transitions",
        "frontend/src/__tests__/Login.test.jsx": "// Login component tests",
        "frontend/src/__tests__/Dashboard.test.jsx": "// Dashboard render tests",
        "frontend/src/__tests__/TaskCard.test.jsx": "// TaskCard interaction tests",
    }
    return {"files": files, "file_count": len(files)}


def integration_output(arch: dict, all_files: dict) -> dict:
    extra = {
        "docker-compose.yml": "# Docker Compose for backend + frontend + db",
        ".gitignore": "node_modules/\n__pycache__/\n.env\n*.db",
        "README.md": f"# {arch['project_name'].title()}\n\n{arch['description']}",
        "Makefile": "# dev, build, test, lint targets",
    }
    total = sum(f.get("file_count", 0) for f in all_files) + len(extra)
    return {"files": extra, "total_files": total}


# ── Pipeline runner ──────────────────────────────────────────────────────

def print_header(text: str):
    width = 60
    print("\n" + "=" * width)
    print(f"  {text}")
    print("=" * width)


def print_agent(agent: dict, step: int, total: int):
    bar = f"[{step}/{total}]"
    print(f"\n{bar} {agent['name']} ({agent['role']})")
    print(f"    {agent['description']}")


def run_pipeline(idea: str, output_dir: str = "generated_project"):
    print_header("OpenWally Multi-Agent Pipeline (Mock Demo)")
    print(f"\nIdea: \"{idea}\"")
    print(f"Output: ./{output_dir}/")
    total = len(AGENTS)

    # Step 1: Architect
    print_agent(AGENTS[0], 1, total)
    time.sleep(0.3)
    arch = architect_output(idea)
    print(f"    -> Designed {len(arch['endpoints'])} endpoints, {len(arch['models'])} models")
    print(f"    -> Stack: {arch['backend_framework']} + {arch['frontend_framework']}")

    # Step 2: Backend
    print_agent(AGENTS[1], 2, total)
    time.sleep(0.3)
    be = backend_output(arch)
    print(f"    -> Generated {be['file_count']} backend files")

    # Step 3: Frontend
    print_agent(AGENTS[2], 3, total)
    time.sleep(0.3)
    fe = frontend_output(arch)
    print(f"    -> Generated {fe['file_count']} frontend files")

    # Step 4: Testing
    print_agent(AGENTS[3], 4, total)
    time.sleep(0.3)
    te = testing_output(arch)
    print(f"    -> Generated {te['file_count']} test files")

    # Step 5: Integration
    print_agent(AGENTS[4], 5, total)
    time.sleep(0.3)
    ig = integration_output(arch, [be, fe, te])
    print(f"    -> Total files in scaffold: {ig['total_files']}")

    # Write files to disk
    all_files = {}
    for stage in [be, fe, te, ig]:
        all_files.update(stage["files"])

    for rel_path, content in all_files.items():
        full_path = Path(output_dir) / rel_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content + "\n")

    # Print summary
    print_header("Scaffold Complete")
    print(f"\n  Project: {arch['project_name']}")
    print(f"  Files generated: {len(all_files)}")
    print(f"  Directory: ./{output_dir}/")
    print("\n  API Endpoints:")
    for ep in arch["endpoints"]:
        print(f"    {ep['method']:6s} {ep['path']:35s} {ep['desc']}")

    print("\n  File tree:")
    for p in sorted(all_files.keys()):
        print(f"    {p}")

    # Write manifest
    manifest = {
        "idea": idea,
        "architecture": arch,
        "files_generated": sorted(all_files.keys()),
        "agents_used": [a["name"] for a in AGENTS],
    }
    manifest_path = Path(output_dir) / "openwally_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"\n  Manifest: {output_dir}/openwally_manifest.json")
    print("\nDone. Review the generated project and iterate as needed.")

    return manifest


if __name__ == "__main__":
    idea = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else (
        "A task management app with user auth, project boards, "
        "and real-time notifications"
    )
    run_pipeline(idea)
