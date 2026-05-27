"""
Hardened agent handler — demonstrates mitigations against exfiltration.
Compare with vulnerable_handler.py to see the difference.
"""

import re


def process_email_inbox(inbox_client):
    """Read emails but sanitize before agent processing."""
    messages = inbox_client.fetch_unread()
    for msg in messages:
        sanitized = sanitize_input(msg.body)
        handle_user_message(sanitized, msg.sender)


def sanitize_input(content):
    """Strip potential injection payloads from untrusted input."""
    # Remove image tags, markdown images, script tags
    content = re.sub(r'<img[^>]*>', '', content)
    content = re.sub(r'!\[.*?\]\(.*?\)', '', content)
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    return content


def handle_user_message(content, sender):
    """Process with human-in-the-loop approval gate."""
    # Generate response WITHOUT file context in same call
    response = generate_agent_response(content)

    # Human approval required before sending
    approval = request_human_approval(
        action="send_email",
        recipient=sender,
        content=response
    )

    if approval.approved:
        send_email_with_csp(sender, response)


def generate_agent_response(user_input):
    """LLM generates response WITHOUT access to sensitive files."""
    # Sensitive data is NOT in the same context as untrusted input
    return call_llm(system_prompt="You are a helpful assistant.", user_prompt=user_input)


def send_email_with_csp(recipient, body):
    """Send email with output sanitization — allowlist approach."""
    # Strip all external resource references
    body = strip_external_resources(body)
    # Rate limit outbound emails
    rate_limit_check("email_send", max_per_hour=10)
    send_email(to=recipient, body=body, skip_approval=False)


def strip_external_resources(html):
    """Remove any external URLs from rendered output — defense in depth."""
    # Remove external image sources
    html = re.sub(r'<img\s+src="https?://[^"]*"', '<img src=""', html)
    # Remove CSS url() references
    html = re.sub(r'url\s*\([^)]*\)', 'url()', html)
    return html


# --- Stubs ---
def call_llm(system_prompt, user_prompt): pass
def request_human_approval(action, recipient, content): pass
def send_email(to, body, skip_approval): pass
def rate_limit_check(action, max_per_hour): pass
