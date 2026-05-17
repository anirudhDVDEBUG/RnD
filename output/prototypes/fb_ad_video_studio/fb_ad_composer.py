"""
FB Ad Video Studio - HyperFrames Composition Generator

Generates HTML-based motion-graphics video ad compositions following
the battle-tested ad structure: Hook -> Problem -> Solution -> Proof -> CTA.
"""

import json
import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AdBrief:
    product_name: str
    tagline: str
    target_audience: str
    platform: str  # fb_feed, ig_reels, tiktok
    duration: int  # seconds
    hook_text: str
    problem_text: str
    solution_text: str
    proof_text: str
    cta_text: str
    brand_color: str = "#FF6B35"
    accent_color: str = "#004E89"
    font: str = "Inter, system-ui, sans-serif"


@dataclass
class Frame:
    section: str
    text: str
    duration_ms: int
    transition: str = "fade"
    animation: str = "slide-up"
    bg_color: str = "#000000"
    text_color: str = "#FFFFFF"
    font_size: str = "3rem"
    subtext: Optional[str] = None


PLATFORM_SPECS = {
    "fb_feed": {"aspect": "4:5", "width": 1080, "height": 1350, "max_duration": 30},
    "ig_reels": {"aspect": "9:16", "width": 1080, "height": 1920, "max_duration": 60},
    "tiktok": {"aspect": "9:16", "width": 1080, "height": 1920, "max_duration": 60},
}


def build_frames(brief: AdBrief) -> list[Frame]:
    """Build frame sequence from ad brief using the 5-part structure."""
    total_ms = brief.duration * 1000

    # Time allocation: Hook 10%, Problem 17%, Solution 33%, Proof 20%, CTA 20%
    allocations = [0.10, 0.17, 0.33, 0.20, 0.20]
    durations = [int(total_ms * a) for a in allocations]

    frames = [
        Frame(
            section="hook",
            text=brief.hook_text,
            duration_ms=durations[0],
            transition="zoom-in",
            animation="scale-bounce",
            bg_color=brief.brand_color,
            text_color="#FFFFFF",
            font_size="3.5rem",
        ),
        Frame(
            section="problem",
            text=brief.problem_text,
            duration_ms=durations[1],
            transition="slide-left",
            animation="shake",
            bg_color="#1a1a1a",
            text_color="#FF4444",
            font_size="2.8rem",
        ),
        Frame(
            section="solution",
            text=brief.solution_text,
            duration_ms=durations[2],
            transition="fade",
            animation="slide-up",
            bg_color=brief.accent_color,
            text_color="#FFFFFF",
            font_size="2.5rem",
            subtext=brief.product_name,
        ),
        Frame(
            section="proof",
            text=brief.proof_text,
            duration_ms=durations[3],
            transition="fade",
            animation="fade-in",
            bg_color="#0d1117",
            text_color="#00FF88",
            font_size="2.2rem",
        ),
        Frame(
            section="cta",
            text=brief.cta_text,
            duration_ms=durations[4],
            transition="zoom-in",
            animation="pulse",
            bg_color=brief.brand_color,
            text_color="#FFFFFF",
            font_size="3rem",
            subtext="Tap to learn more",
        ),
    ]
    return frames


def generate_html(brief: AdBrief, frames: list[Frame]) -> str:
    """Generate a self-contained HTML HyperFrames composition."""
    spec = PLATFORM_SPECS[brief.platform]
    w, h = spec["width"], spec["height"]

    # Build frame HTML sections
    frame_html_parts = []
    frame_js_data = []
    for i, f in enumerate(frames):
        subtext_html = f'<p class="subtext">{f.subtext}</p>' if f.subtext else ""
        frame_html_parts.append(f"""
    <div class="frame" id="frame-{i}" data-section="{f.section}"
         style="background:{f.bg_color}; color:{f.text_color}; display:none;">
      <div class="frame-content animate-{f.animation}">
        <h1 style="font-size:{f.font_size}">{f.text}</h1>
        {subtext_html}
      </div>
      <div class="section-label">{f.section.upper()}</div>
      <div class="timer-bar"></div>
    </div>""")
        frame_js_data.append(
            f'{{id:"frame-{i}",duration:{f.duration_ms},transition:"{f.transition}",section:"{f.section}"}}'
        )

    frames_joined = "\n".join(frame_html_parts)
    js_data = ",".join(frame_js_data)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{brief.product_name} - Video Ad ({brief.platform})</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
  font-family: {brief.font};
  background: #000;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}}
.viewport {{
  width: {w // 3}px;
  height: {h // 3}px;
  position: relative;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.8);
}}
.frame {{
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 2rem;
  text-align: center;
}}
.frame-content {{
  max-width: 90%;
}}
.frame-content h1 {{
  line-height: 1.2;
  font-weight: 800;
  text-shadow: 0 2px 10px rgba(0,0,0,0.3);
}}
.subtext {{
  margin-top: 1rem;
  font-size: 1.2rem;
  opacity: 0.85;
  font-weight: 500;
}}
.section-label {{
  position: absolute;
  top: 12px;
  left: 12px;
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 2px;
  opacity: 0.5;
  background: rgba(255,255,255,0.15);
  padding: 4px 8px;
  border-radius: 4px;
}}
.timer-bar {{
  position: absolute;
  bottom: 0;
  left: 0;
  height: 4px;
  background: rgba(255,255,255,0.7);
  width: 0%;
  transition: width linear;
}}
.info-panel {{
  position: fixed;
  top: 20px;
  right: 20px;
  background: #1a1a2e;
  color: #eee;
  padding: 1.5rem;
  border-radius: 10px;
  font-size: 0.8rem;
  line-height: 1.6;
  max-width: 250px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.5);
}}
.info-panel h3 {{ color: {brief.brand_color}; margin-bottom: 0.5rem; }}

/* Animations */
@keyframes slideUp {{ from {{ transform: translateY(40px); opacity:0; }} to {{ transform: translateY(0); opacity:1; }} }}
@keyframes scaleBounce {{ 0% {{ transform: scale(0.5); opacity:0; }} 60% {{ transform: scale(1.05); }} 100% {{ transform: scale(1); opacity:1; }} }}
@keyframes shake {{ 0%,100% {{ transform: translateX(0); }} 20% {{ transform: translateX(-8px); }} 40% {{ transform: translateX(8px); }} 60% {{ transform: translateX(-4px); }} 80% {{ transform: translateX(4px); }} }}
@keyframes fadeIn {{ from {{ opacity:0; }} to {{ opacity:1; }} }}
@keyframes pulse {{ 0%,100% {{ transform: scale(1); }} 50% {{ transform: scale(1.05); }} }}

.animate-slide-up {{ animation: slideUp 0.6s ease-out forwards; }}
.animate-scale-bounce {{ animation: scaleBounce 0.5s ease-out forwards; }}
.animate-shake {{ animation: shake 0.6s ease-out forwards; }}
.animate-fade-in {{ animation: fadeIn 0.8s ease-out forwards; }}
.animate-pulse {{ animation: pulse 1s ease-in-out infinite; }}

/* Transitions */
.trans-fade {{ animation: fadeIn 0.3s ease-out; }}
.trans-slide-left {{ animation: slideFromRight 0.4s ease-out; }}
.trans-zoom-in {{ animation: scaleBounce 0.4s ease-out; }}
@keyframes slideFromRight {{ from {{ transform: translateX(100%); }} to {{ transform: translateX(0); }} }}
</style>
</head>
<body>
<div class="viewport">
{frames_joined}
</div>
<div class="info-panel">
  <h3>{brief.product_name}</h3>
  <p><strong>Platform:</strong> {brief.platform.replace('_',' ').title()}</p>
  <p><strong>Duration:</strong> {brief.duration}s</p>
  <p><strong>Aspect:</strong> {spec['aspect']}</p>
  <p><strong>Resolution:</strong> {w}x{h}</p>
  <p><strong>Audience:</strong> {brief.target_audience}</p>
  <hr style="border-color:#333;margin:0.5rem 0">
  <p id="current-section" style="color:{brief.brand_color};font-weight:700;">READY</p>
  <p id="time-display">0.0s / {brief.duration}s</p>
  <button onclick="startPlayback()" style="margin-top:0.5rem;padding:6px 12px;background:{brief.brand_color};color:#fff;border:none;border-radius:6px;cursor:pointer;font-weight:600;">Play</button>
  <button onclick="location.reload()" style="margin-top:0.5rem;padding:6px 12px;background:#333;color:#fff;border:none;border-radius:6px;cursor:pointer;">Reset</button>
</div>
<script>
const frames = [{js_data}];
let currentFrame = 0;
let playing = false;
let startTime = 0;
const totalDuration = {brief.duration * 1000};

function showFrame(idx) {{
  frames.forEach((f, i) => {{
    const el = document.getElementById(f.id);
    el.style.display = i === idx ? 'flex' : 'none';
    if (i === idx) {{
      el.className = 'frame trans-' + f.transition;
      const bar = el.querySelector('.timer-bar');
      bar.style.width = '0%';
      bar.style.transitionDuration = f.duration + 'ms';
      setTimeout(() => bar.style.width = '100%', 50);
    }}
  }});
  document.getElementById('current-section').textContent = frames[idx].section.toUpperCase();
}}

function startPlayback() {{
  if (playing) return;
  playing = true;
  currentFrame = 0;
  startTime = Date.now();
  showFrame(0);
  scheduleNext();
  updateTimer();
}}

function scheduleNext() {{
  if (currentFrame >= frames.length) return;
  setTimeout(() => {{
    currentFrame++;
    if (currentFrame < frames.length) {{
      showFrame(currentFrame);
      scheduleNext();
    }} else {{
      document.getElementById('current-section').textContent = 'COMPLETE';
      playing = false;
    }}
  }}, frames[currentFrame].duration);
}}

function updateTimer() {{
  if (!playing) return;
  const elapsed = (Date.now() - startTime) / 1000;
  document.getElementById('time-display').textContent =
    elapsed.toFixed(1) + 's / ' + (totalDuration/1000) + 's';
  requestAnimationFrame(updateTimer);
}}

// Auto-play after 1s
setTimeout(startPlayback, 1000);
</script>
</body>
</html>"""
    return html


def generate_audio_cues(brief: AdBrief, frames: list[Frame]) -> dict:
    """Generate audio pipeline timing cues for the composition."""
    cues = {
        "background_track": {
            "style": "upbeat-electronic" if brief.platform == "tiktok" else "corporate-ambient",
            "bpm": 120,
            "fade_in_ms": 500,
            "fade_out_ms": 1000,
        },
        "voiceover": [],
        "sfx": [],
    }

    time_offset = 0
    for f in frames:
        cues["voiceover"].append({
            "text": f.text,
            "start_ms": time_offset,
            "end_ms": time_offset + f.duration_ms,
            "emphasis": f.section in ("hook", "cta"),
        })
        cues["sfx"].append({
            "trigger": "transition",
            "type": "whoosh" if f.transition == "slide-left" else "pop",
            "at_ms": time_offset,
        })
        time_offset += f.duration_ms

    return cues


def generate_template(brief: AdBrief, frames: list[Frame]) -> dict:
    """Export a reusable reverse-template from this composition."""
    return {
        "template_name": f"{brief.product_name.lower().replace(' ', '_')}_template",
        "platform": brief.platform,
        "total_duration_s": brief.duration,
        "structure": [
            {
                "section": f.section,
                "duration_pct": round(f.duration_ms / (brief.duration * 1000) * 100),
                "transition": f.transition,
                "animation": f.animation,
                "font_size": f.font_size,
                "bg_color": f.bg_color,
            }
            for f in frames
        ],
        "brand": {
            "primary_color": brief.brand_color,
            "accent_color": brief.accent_color,
            "font": brief.font,
        },
    }


def compose_ad(brief: AdBrief, output_dir: str = "output") -> dict:
    """Main entry point: compose a full video ad from a brief."""
    os.makedirs(output_dir, exist_ok=True)

    frames = build_frames(brief)
    html = generate_html(brief, frames)
    audio_cues = generate_audio_cues(brief, frames)
    template = generate_template(brief, frames)

    # Write outputs
    html_path = os.path.join(output_dir, "ad_composition.html")
    with open(html_path, "w") as f:
        f.write(html)

    audio_path = os.path.join(output_dir, "audio_cues.json")
    with open(audio_path, "w") as f:
        json.dump(audio_cues, f, indent=2)

    template_path = os.path.join(output_dir, "template.json")
    with open(template_path, "w") as f:
        json.dump(template, f, indent=2)

    spec = PLATFORM_SPECS[brief.platform]
    summary = {
        "product": brief.product_name,
        "platform": brief.platform,
        "resolution": f"{spec['width']}x{spec['height']}",
        "aspect_ratio": spec["aspect"],
        "duration_s": brief.duration,
        "frames": len(frames),
        "output_files": [html_path, audio_path, template_path],
    }

    summary_path = os.path.join(output_dir, "summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    return summary
