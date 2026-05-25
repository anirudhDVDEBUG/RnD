#!/usr/bin/env python3
"""
Coding with Beat — Demo/Mock TUI
Demonstrates the terminal music player interface without requiring
actual audio playback or external music service credentials.
"""

import time
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.text import Text
from rich.layout import Layout
from rich.align import Align

console = Console()

# Mock playlist
PLAYLIST = [
    {"title": "Lofi Chill Vibes", "artist": "CodeBeats", "duration": "3:45", "bpm": 85},
    {"title": "Midnight Debug", "artist": "Terminal FM", "duration": "4:12", "bpm": 72},
    {"title": "Async Dreams", "artist": "Promise.all()", "duration": "3:28", "bpm": 90},
    {"title": "Stack Overflow Blues", "artist": "404 Band", "duration": "2:55", "bpm": 110},
    {"title": "Merge Conflict Anthem", "artist": "Git Rebels", "duration": "4:01", "bpm": 128},
]

# Mock synced lyrics
LYRICS = [
    (0.0, ""),
    (1.0, "Writing code at 3am..."),
    (3.0, "The cursor blinks in silence"),
    (5.0, "Another function, another dream"),
    (7.0, "The tests will pass, I believe"),
    (9.0, "Compiling hopes and memories"),
    (11.0, "One more commit before I sleep"),
    (13.0, "The terminal glows softly"),
    (15.0, "As bugs dissolve to nothing"),
]


def render_player(track_idx, progress, mode="normal", lyric_idx=0):
    """Render the TUI player frame."""
    track = PLAYLIST[track_idx]

    # Mode styling
    if mode == "panic":
        border_style = "bold red"
        mode_label = " PANIC MODE "
        status_icon = "!!"
    elif mode == "celebrate":
        border_style = "bold green"
        mode_label = " TESTS PASSED "
        status_icon = "**"
    else:
        border_style = "cyan"
        mode_label = ""
        status_icon = ">>"

    # Progress bar
    bar_width = 30
    filled = int(progress * bar_width)
    bar = "━" * filled + "╸" + "─" * (bar_width - filled - 1)

    # Current lyric
    lyric_line = LYRICS[lyric_idx % len(LYRICS)][1] if LYRICS[lyric_idx % len(LYRICS)][1] else "..."

    # Build display
    lines = []
    lines.append(f"  CODEBEAT DJ v1.0 {mode_label}")
    lines.append(f"  {'─' * 38}")
    lines.append(f"  Now Playing: {track['title']}")
    lines.append(f"  Artist:      {track['artist']}")
    lines.append(f"  BPM: {track['bpm']}    Duration: {track['duration']}")
    lines.append(f"")
    lines.append(f"  {status_icon} {bar} {int(progress*100)}%")
    lines.append(f"")
    lines.append(f'  ~ "{lyric_line}"')
    lines.append(f"")
    lines.append(f"  [n]ext  [p]ause  [s]kip  [q]uit")

    content = "\n".join(lines)
    return Panel(content, border_style=border_style, title="[bold]coding-with-beat[/bold]", width=50)


def render_playlist(current_idx):
    """Render the playlist sidebar."""
    table = Table(title="Playlist", show_header=True, header_style="bold magenta", width=40)
    table.add_column("#", width=3)
    table.add_column("Track", width=22)
    table.add_column("BPM", width=5)

    for i, track in enumerate(PLAYLIST):
        marker = ">>" if i == current_idx else "  "
        style = "bold cyan" if i == current_idx else ""
        table.add_row(f"{marker}{i+1}", track["title"], str(track["bpm"]), style=style)

    return table


def run_demo():
    """Run the full demo sequence."""
    console.print("\n[bold cyan]coding-with-beat[/bold cyan] Demo Mode\n", justify="center")
    console.print("[dim]Simulating terminal music player with reactive coding events...[/dim]\n")

    # Phase 1: Normal playback
    console.print("[bold]Phase 1:[/bold] Normal playback — lofi coding vibes\n")
    for i in range(8):
        progress = i / 7
        lyric_idx = i
        frame = render_player(0, progress, mode="normal", lyric_idx=lyric_idx)
        console.print(frame)
        if i < 7:
            time.sleep(0.4)
            # Clear previous frame (simple approach for demo)
            console.print("")

    console.print()

    # Phase 2: Test failure -> panic mode
    console.print("[bold red]Phase 2:[/bold red] Test failure detected! Entering PANIC MODE\n")
    console.print("[dim]Event received: pytest returned exit code 1[/dim]\n")
    time.sleep(0.5)

    for i in range(4):
        progress = i / 3
        frame = render_player(3, progress, mode="panic", lyric_idx=i + 4)
        console.print(frame)
        if i < 3:
            time.sleep(0.4)
            console.print("")

    console.print()

    # Phase 3: Tests pass -> celebrate
    console.print("[bold green]Phase 3:[/bold green] All tests passing! Celebration mode\n")
    console.print("[dim]Event received: pytest returned exit code 0[/dim]\n")
    time.sleep(0.5)

    frame = render_player(2, 0.5, mode="celebrate", lyric_idx=6)
    console.print(frame)

    console.print()

    # Show playlist
    console.print("[bold]Current Playlist:[/bold]\n")
    console.print(render_playlist(2))

    # MCP tool summary
    console.print("\n[bold]MCP Tools Available (when running with --mcp):[/bold]\n")
    tools_table = Table(show_header=True, header_style="bold")
    tools_table.add_column("Tool", width=20)
    tools_table.add_column("Description", width=45)
    tools_table.add_row("play_track", "Play a specific track by name or index")
    tools_table.add_row("pause", "Pause current playback")
    tools_table.add_row("skip", "Skip to next track in playlist")
    tools_table.add_row("search", "Search tracks across configured sources")
    tools_table.add_row("set_mood", "Change playlist mood (chill/focus/hype)")
    tools_table.add_row("get_lyrics", "Get synced lyrics for current track")
    tools_table.add_row("panic_mode", "Trigger panic mode (test failure reaction)")
    console.print(tools_table)

    console.print("\n[dim]Demo complete. Install coding-with-beat for full functionality.[/dim]\n")


if __name__ == "__main__":
    run_demo()
