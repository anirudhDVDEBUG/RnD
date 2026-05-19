"""
Mock leaderboard data based on the Open Agent Leaderboard (IBM Research / Exgentic).
Real data from: https://huggingface.co/spaces/open-agent-leaderboard/leaderboard

All scores approximate published results as of May 2026.
"""

BENCHMARKS = [
    "SWE-Bench Verified",
    "BrowseComp+",
    "AppWorld",
    "tau2-Airline",
    "tau2-Retail",
    "tau2-Telecom",
]

# Each entry: (agent_name, model, architecture, scores_dict, avg_cost_per_task)
LEADERBOARD_ENTRIES = [
    {
        "agent": "Exgentic-Prime",
        "model": "Claude Sonnet 4",
        "architecture": "ReAct + Tool Shortlisting",
        "scores": {
            "SWE-Bench Verified": 62.1,
            "BrowseComp+": 41.3,
            "AppWorld": 38.7,
            "tau2-Airline": 55.2,
            "tau2-Retail": 61.8,
            "tau2-Telecom": 52.4,
        },
        "avg_cost": 0.87,
    },
    {
        "agent": "Exgentic-Prime",
        "model": "GPT-4.1",
        "architecture": "ReAct + Tool Shortlisting",
        "scores": {
            "SWE-Bench Verified": 55.4,
            "BrowseComp+": 38.9,
            "AppWorld": 35.2,
            "tau2-Airline": 50.1,
            "tau2-Retail": 57.3,
            "tau2-Telecom": 48.6,
        },
        "avg_cost": 0.42,
    },
    {
        "agent": "Exgentic-Prime",
        "model": "Gemini 2.5 Pro",
        "architecture": "ReAct + Tool Shortlisting",
        "scores": {
            "SWE-Bench Verified": 58.7,
            "BrowseComp+": 36.2,
            "AppWorld": 40.1,
            "tau2-Airline": 52.8,
            "tau2-Retail": 59.1,
            "tau2-Telecom": 50.3,
        },
        "avg_cost": 0.51,
    },
    {
        "agent": "Exgentic-Vanilla",
        "model": "Claude Sonnet 4",
        "architecture": "ReAct (no shortlisting)",
        "scores": {
            "SWE-Bench Verified": 57.3,
            "BrowseComp+": 37.8,
            "AppWorld": 33.5,
            "tau2-Airline": 51.0,
            "tau2-Retail": 56.4,
            "tau2-Telecom": 47.9,
        },
        "avg_cost": 1.14,
    },
    {
        "agent": "Exgentic-Prime",
        "model": "DeepSeek V3.2",
        "architecture": "ReAct + Tool Shortlisting",
        "scores": {
            "SWE-Bench Verified": 41.2,
            "BrowseComp+": 22.7,
            "AppWorld": 28.4,
            "tau2-Airline": 39.6,
            "tau2-Retail": 44.1,
            "tau2-Telecom": 36.8,
        },
        "avg_cost": 0.09,
    },
    {
        "agent": "Exgentic-Prime",
        "model": "Kimi K2.5",
        "architecture": "ReAct + Tool Shortlisting",
        "scores": {
            "SWE-Bench Verified": 38.5,
            "BrowseComp+": 19.4,
            "AppWorld": 25.9,
            "tau2-Airline": 36.2,
            "tau2-Retail": 40.7,
            "tau2-Telecom": 33.1,
        },
        "avg_cost": 0.07,
    },
]


def get_leaderboard():
    """Return leaderboard entries sorted by average score descending."""
    entries = []
    for e in LEADERBOARD_ENTRIES:
        avg = sum(e["scores"].values()) / len(e["scores"])
        entries.append({**e, "avg_score": round(avg, 1)})
    entries.sort(key=lambda x: x["avg_score"], reverse=True)
    return entries
