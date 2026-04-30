"""Stage 5: digest, GitHub issue, email."""
from .email_sender import send_daily_email
from .github_issue import open_issue
from .morning_brief import render_brief

__all__ = ["render_brief", "open_issue", "send_daily_email"]
