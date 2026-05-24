#!/usr/bin/env python3
"""
Clover Job Search & Interview Prep — Local Demo

Simulates the MCP tools provided by @fourleafai/clover-mcp:
  - job_search: Search live job listings by role, location, filters
  - interview_prep: Get role-specific interview questions & guides
  - resume_review: Analyze a resume against a target role

Uses mock data so you can evaluate the workflow without API keys.
"""

import sys
from datetime import datetime, timedelta

# ─── Mock Data ────────────────────────────────────────────────────────────────

MOCK_JOBS = [
    {
        "id": "clv-4821",
        "title": "Senior Software Engineer",
        "company": "Stripe",
        "location": "San Francisco, CA (Hybrid)",
        "salary_range": "$190,000 - $250,000",
        "posted": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
        "seniority": "Senior",
        "tags": ["Python", "Go", "Distributed Systems", "Payments"],
        "url": "https://example.com/jobs/stripe-sse",
    },
    {
        "id": "clv-4822",
        "title": "Staff ML Engineer",
        "company": "Anthropic",
        "location": "San Francisco, CA (On-site)",
        "salary_range": "$300,000 - $400,000",
        "posted": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        "seniority": "Staff",
        "tags": ["PyTorch", "RLHF", "LLMs", "Distributed Training"],
        "url": "https://example.com/jobs/anthropic-ml",
    },
    {
        "id": "clv-4823",
        "title": "Software Engineer II",
        "company": "Figma",
        "location": "Remote (US)",
        "salary_range": "$150,000 - $200,000",
        "posted": datetime.now().strftime("%Y-%m-%d"),
        "seniority": "Mid",
        "tags": ["TypeScript", "React", "WebGL", "Collaboration"],
        "url": "https://example.com/jobs/figma-se2",
    },
    {
        "id": "clv-4824",
        "title": "Backend Engineer",
        "company": "Notion",
        "location": "New York, NY (Hybrid)",
        "salary_range": "$160,000 - $210,000",
        "posted": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
        "seniority": "Mid",
        "tags": ["Kotlin", "PostgreSQL", "APIs", "Productivity"],
        "url": "https://example.com/jobs/notion-be",
    },
    {
        "id": "clv-4825",
        "title": "Principal Engineer, AI Platform",
        "company": "Databricks",
        "location": "Remote (US)",
        "salary_range": "$280,000 - $370,000",
        "posted": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        "seniority": "Principal",
        "tags": ["Spark", "Python", "MLOps", "Data Infrastructure"],
        "url": "https://example.com/jobs/databricks-pe",
    },
]

MOCK_INTERVIEW_PREP = {
    "company": "Stripe",
    "role": "Senior Software Engineer",
    "process": [
        "Recruiter screen (30 min)",
        "Technical phone screen — coding (60 min)",
        "On-site: System design (60 min)",
        "On-site: Coding pair (60 min)",
        "On-site: Behavioral / values (45 min)",
        "Hiring committee review",
    ],
    "behavioral_questions": [
        "Tell me about a time you simplified a complex system.",
        "Describe a situation where you disagreed with a technical decision. How did you handle it?",
        "How do you prioritize when you have multiple urgent tasks from different stakeholders?",
        "Give an example of a project where you had to learn a new technology quickly.",
    ],
    "technical_questions": [
        "Design a payment processing pipeline that handles idempotency and retries.",
        "How would you build a rate limiter for an API with distributed servers?",
        "Explain the trade-offs between strong and eventual consistency in a payments context.",
        "Walk through how you'd debug a latency spike in a microservices architecture.",
    ],
    "tips": [
        "Stripe values clarity of thought — explain trade-offs explicitly.",
        "Show awareness of financial system constraints (idempotency, auditability).",
        "Prepare concrete examples of improving system reliability.",
        "Demonstrate user empathy — Stripe cares about developer experience.",
    ],
}

MOCK_RESUME_FEEDBACK = {
    "overall_score": 72,
    "sections": {
        "contact_info": {"score": 90, "feedback": "Clean and complete. Consider adding a GitHub/portfolio link."},
        "summary": {"score": 65, "feedback": "Too generic. Tailor to the target role — mention payments or fintech if applying to Stripe."},
        "experience": {
            "score": 70,
            "feedback": "Good breadth, but bullet points lack quantified impact. Use 'Reduced latency by 40%' instead of 'Improved performance'.",
        },
        "skills": {"score": 80, "feedback": "Relevant stack listed. Move Python and Go higher — they match the target role."},
        "education": {"score": 75, "feedback": "Adequate. Consider adding relevant coursework or certifications."},
    },
    "keyword_alignment": {
        "matched": ["Python", "distributed systems", "APIs", "microservices"],
        "missing": ["payments", "idempotency", "observability", "Terraform"],
    },
    "action_items": [
        "Add 2-3 quantified metrics per role (latency, throughput, cost savings).",
        "Include a 'payments' or 'fintech' keyword in your summary if you have relevant experience.",
        "Reorder skills to lead with the target role's primary languages.",
        "Shorten resume to 1 page — remove the 2014-2016 internship.",
    ],
}


# ─── Tool Implementations ────────────────────────────────────────────────────


def tool_job_search(query: str, location: str = "", seniority: str = "") -> list[dict]:
    """Simulate the clover.job_search MCP tool."""
    results = MOCK_JOBS
    q = query.lower()
    results = [j for j in results if q in j["title"].lower() or any(q in t.lower() for t in j["tags"])]
    if location:
        loc = location.lower()
        results = [j for j in results if loc in j["location"].lower()]
    if seniority:
        results = [j for j in results if seniority.lower() == j["seniority"].lower()]
    return results


def tool_interview_prep(company: str, role: str) -> dict:
    """Simulate the clover.interview_prep MCP tool."""
    return MOCK_INTERVIEW_PREP


def tool_resume_review(target_role: str) -> dict:
    """Simulate the clover.resume_review MCP tool."""
    return MOCK_RESUME_FEEDBACK


# ─── Pretty Printers ─────────────────────────────────────────────────────────

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def hr(char="─", width=72):
    print(f"{CYAN}{char * width}{RESET}")


def heading(text):
    print(f"\n{BOLD}{CYAN}{text}{RESET}")
    hr()


def print_jobs(jobs):
    if not jobs:
        print(f"  {YELLOW}No matching jobs found.{RESET}")
        return
    for i, j in enumerate(jobs, 1):
        print(f"  {BOLD}{i}. {j['title']}{RESET} @ {GREEN}{j['company']}{RESET}")
        print(f"     Location:  {j['location']}")
        print(f"     Salary:    {j['salary_range']}")
        print(f"     Posted:    {j['posted']}  |  Level: {j['seniority']}")
        print(f"     Tags:      {', '.join(j['tags'])}")
        print()


def print_interview_prep(prep):
    print(f"  {BOLD}Company:{RESET} {prep['company']}  |  {BOLD}Role:{RESET} {prep['role']}")
    print()
    print(f"  {BOLD}Interview Process:{RESET}")
    for step in prep["process"]:
        print(f"    {GREEN}>{RESET} {step}")
    print()
    print(f"  {BOLD}Behavioral Questions:{RESET}")
    for q in prep["behavioral_questions"]:
        print(f"    {YELLOW}Q:{RESET} {q}")
    print()
    print(f"  {BOLD}Technical Questions:{RESET}")
    for q in prep["technical_questions"]:
        print(f"    {YELLOW}Q:{RESET} {q}")
    print()
    print(f"  {BOLD}Preparation Tips:{RESET}")
    for t in prep["tips"]:
        print(f"    {GREEN}*{RESET} {t}")


def print_resume_review(review):
    score = review["overall_score"]
    color = GREEN if score >= 80 else YELLOW if score >= 60 else RED
    print(f"  {BOLD}Overall Score:{RESET} {color}{score}/100{RESET}")
    print()
    print(f"  {BOLD}Section Breakdown:{RESET}")
    for section, data in review["sections"].items():
        s = data["score"]
        c = GREEN if s >= 80 else YELLOW if s >= 60 else RED
        label = section.replace("_", " ").title()
        print(f"    {label:.<25} {c}{s}/100{RESET}  {data['feedback']}")
    print()
    print(f"  {BOLD}Keyword Alignment:{RESET}")
    matched = review["keyword_alignment"]["matched"]
    missing = review["keyword_alignment"]["missing"]
    print(f"    {GREEN}Matched:{RESET}  {', '.join(matched)}")
    print(f"    {RED}Missing:{RESET}  {', '.join(missing)}")
    print()
    print(f"  {BOLD}Action Items:{RESET}")
    for item in review["action_items"]:
        print(f"    {YELLOW}>{RESET} {item}")


# ─── Main ─────────────────────────────────────────────────────────────────────


def main():
    print(f"\n{BOLD}{CYAN}{'=' * 72}{RESET}")
    print(f"{BOLD}{CYAN}  Clover Job Search & Interview Prep — Demo{RESET}")
    print(f"{BOLD}{CYAN}  Simulating @fourleafai/clover-mcp MCP tools{RESET}")
    print(f"{BOLD}{CYAN}{'=' * 72}{RESET}")

    # 1. Job Search
    heading("1) Job Search: query='software engineer', location='', seniority=''")
    jobs = tool_job_search("software engineer")
    print_jobs(jobs)

    # 2. Filtered Search
    heading("2) Filtered Search: query='engineer', seniority='senior'")
    filtered = tool_job_search("engineer", seniority="senior")
    print_jobs(filtered)

    # 3. Interview Prep
    heading("3) Interview Prep: company='Stripe', role='Senior Software Engineer'")
    prep = tool_interview_prep("Stripe", "Senior Software Engineer")
    print_interview_prep(prep)

    # 4. Resume Review
    heading("\n4) Resume Review: target_role='Senior Software Engineer @ Stripe'")
    review = tool_resume_review("Senior Software Engineer")
    print_resume_review(review)

    # Summary
    print()
    hr("=")
    print(f"  {GREEN}Demo complete.{RESET} In production, these tools call the Clover MCP server")
    print(f"  which fetches live data from four-leaf.ai's job & interview APIs.")
    hr("=")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
