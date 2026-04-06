#!/usr/bin/env python3
"""
Regenerate audio/timeline.mp3 and audio/timeline_timing.json
for the updated six-month roadmap narration.

Usage:
    python scripts/gen_timeline_audio.py
"""
import os, sys, json, base64
from pathlib import Path

# ── Load API key ──────────────────────────────────────────
ENV_PATH = Path(__file__).parent.parent.parent / ".env.local"
def load_env():
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                v = v.strip().strip("'\"")
                if k.strip() not in os.environ:
                    os.environ[k.strip()] = v
load_env()

API_KEY = os.environ.get("ELEVENLABS_API_KEY")
if not API_KEY:
    print("ERROR: ELEVENLABS_API_KEY not found in .env.local")
    sys.exit(1)

# ── Config ────────────────────────────────────────────────
VOICE_ID  = "JBFqnCBsd6RMkjVDRZzb"   # George — same voice as rest of deck
MODEL_ID  = "eleven_multilingual_v2"
SETTINGS  = {"stability": 0.35, "similarity_boost": 0.80,
             "style": 0.55, "use_speaker_boost": True}

TEXT = (
    "Here's the six-month roadmap. "
    "April and May: five things ship — AuthorConsole, the presentation engine, "
    "the A.I. Spend Tracker, Console Continuity Skills, and a-i-ron.com. "
    "Each one launches publicly, starts building an audience, and feeds the next. "
    "June through August: Illustrate-Assist and the Personal Marketing Agent go live, "
    "and Patreon revenue starts flowing. "
    "September and October: Patreon revenue funds the marketing spend, "
    "the first product revenue comes in, "
    "and we sit down and look at what's working. "
    "That's the re-evaluation point. By then, the picture is clear."
)

OUT_DIR     = Path(__file__).parent.parent / "audio"
MP3_PATH    = OUT_DIR / "timeline.mp3"
TIMING_PATH = OUT_DIR / "timeline_timing.json"

# ── Call ElevenLabs /with-timestamps ─────────────────────
import urllib.request

url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps"
payload = json.dumps({
    "text": TEXT,
    "model_id": MODEL_ID,
    "voice_settings": SETTINGS,
    "output_format": "mp3_44100_128",
}).encode()

req = urllib.request.Request(
    url,
    data=payload,
    headers={
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
    },
    method="POST",
)

print(f"Calling ElevenLabs ({len(TEXT)} chars, voice: George)...")
try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read())
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()}")
    sys.exit(1)

# ── Save MP3 ──────────────────────────────────────────────
audio_bytes = base64.b64decode(data["audio_base64"])
MP3_PATH.write_bytes(audio_bytes)
print(f"  Saved: {MP3_PATH.name} ({len(audio_bytes)/1024:.1f} KB)")

# ── Convert character alignment → word-level timing ───────
alignment = data.get("alignment") or data.get("normalized_alignment")
chars  = alignment["characters"]
starts = alignment["character_start_times_seconds"]
ends   = alignment["character_end_times_seconds"]

words = []
cur_word, cur_start, cur_end = "", None, None
for ch, s, e in zip(chars, starts, ends):
    if ch in (" ", "\n"):
        if cur_word:
            words.append([cur_word, round(cur_start, 3), round(cur_end, 3)])
            cur_word, cur_start, cur_end = "", None, None
    else:
        if cur_start is None:
            cur_start = s
        cur_word += ch
        cur_end = e
if cur_word:
    words.append([cur_word, round(cur_start, 3), round(cur_end, 3)])

TIMING_PATH.write_text(json.dumps(words), encoding="utf-8")
total_dur = words[-1][2] if words else 0
print(f"  Saved: {TIMING_PATH.name} ({len(words)} words, {total_dur:.1f}s)")
print(f"\n  ✓ Set minDuration in SCENES[12] to {int(total_dur) + 3}")
