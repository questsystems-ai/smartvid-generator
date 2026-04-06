#!/usr/bin/env python3
"""
Regenerate a single slide's audio (MP3 + word-level timing JSON).
Reads the narration text directly from presentation.html SCENES array.

Usage:
    python scripts/gen_audio.py <audio_id> <scene_index>

Example:
    python scripts/gen_audio.py citizen-scientist 3
    python scripts/gen_audio.py timeline 12
"""
import os, sys, json, base64, re
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
    print("ERROR: ELEVENLABS_API_KEY not found"); sys.exit(1)

if len(sys.argv) < 3:
    print("Usage: python scripts/gen_audio.py <audio_id> <scene_index>")
    sys.exit(1)

AUDIO_ID    = sys.argv[1]
SCENE_INDEX = int(sys.argv[2])

# ── Voice config (George — matches rest of deck) ──────────
VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"
MODEL_ID = "eleven_multilingual_v2"
SETTINGS = {"stability": 0.35, "similarity_boost": 0.80,
            "style": 0.55, "use_speaker_boost": True}

# ── Extract narration from presentation.html ──────────────
HTML_PATH = Path(__file__).parent.parent / "presentation.html"
html = HTML_PATH.read_text(encoding="utf-8")
scenes_match = re.search(r'const SCENES = (\[.*?\]);', html, re.DOTALL)
if not scenes_match:
    print("ERROR: Could not find SCENES array in presentation.html"); sys.exit(1)

scenes = json.loads(scenes_match.group(1))
scene = scenes[SCENE_INDEX]
# Strip HTML tags and trailing newline
text = re.sub(r'<[^>]+>', '', scene.get("narrationHtml", "")).strip()

if not text:
    print(f"ERROR: No narration text found for scene {SCENE_INDEX}"); sys.exit(1)

print(f"Scene {SCENE_INDEX} ({AUDIO_ID}): {len(text)} chars")
print(f"Text preview: {text[:80]}...")

# ── Call ElevenLabs with timestamps ──────────────────────
import urllib.request

url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps"
payload = json.dumps({
    "text": text,
    "model_id": MODEL_ID,
    "voice_settings": SETTINGS,
    "output_format": "mp3_44100_128",
}).encode()

req = urllib.request.Request(url, data=payload, headers={
    "xi-api-key": API_KEY,
    "Content-Type": "application/json",
}, method="POST")

print("Calling ElevenLabs...")
try:
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.loads(resp.read())
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()}"); sys.exit(1)

# ── Save MP3 ──────────────────────────────────────────────
OUT_DIR = Path(__file__).parent.parent / "audio"
mp3_path = OUT_DIR / f"{AUDIO_ID}.mp3"
timing_path = OUT_DIR / f"{AUDIO_ID}_timing.json"

audio_bytes = base64.b64decode(data["audio_base64"])
mp3_path.write_bytes(audio_bytes)
print(f"  Saved: {mp3_path.name} ({len(audio_bytes)/1024:.1f} KB)")

# ── Character alignment -> word-level timing ──────────────
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

timing_path.write_text(json.dumps(words), encoding="utf-8")
total_dur = words[-1][2] if words else 0
print(f"  Saved: {timing_path.name} ({len(words)} words, {total_dur:.1f}s)")
print(f"\n  Current minDuration: {scene.get('minDuration')}s")
print(f"  Suggested minDuration: {int(total_dur) + 3}s")
