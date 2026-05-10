"""Demo: capture and display SdkMessage events from the agent loop."""

from deepseek_loop import AgentLoop, PermissionMode

events = []

def capture(event):
    events.append(event)

agent = AgentLoop(permission_mode=PermissionMode.ALLOW_ALL, event_callback=capture)
agent.run("Demo prompt")

print(f"Captured {len(events)} SdkMessage events:")
for e in events:
    tool = e.tool_name or "-"
    preview = str(e.content)[:60]
    print(f"  [{e.type:12s}] tool={tool:15s} content_preview={preview}")
