# The Workshop

A narrated, animated single-file presentation — built with [presentation.html](https://github.com/questsystems-ai/smartvid-generator).

**Live demo:** [questsystems-ai.github.io/smartvid-generator](https://questsystems-ai.github.io/smartvid-generator) *(or Vercel URL)*

## What it is

An anti-PowerPoint. Instead of slides, it plays like a film: animated SVG figures, ElevenLabs TTS narration with word-level caption sync, and a single self-contained HTML file that runs anywhere.

This repo contains Aaron's dad pitch — "The Workshop" — a 7-minute narrated presentation making the case for a $12k / 6-month funding runway to finish an AI product portfolio.

## Stack

- Single-file HTML/CSS/JS (zero build step, zero dependencies)
- ElevenLabs TTS (`george` voice, `eleven_multilingual_v2`)
- Animated SVGs built inline per slide
- Word-level caption timing via ElevenLabs alignment API
- Python `serve.py` dev server for local editing

## Usage

### View (production)
Open `index.html` in any browser — or visit the hosted URL above.

### Develop locally
```bash
python serve.py
# open http://localhost:8500/presentation.html
```

The dev version (`presentation.html`) includes an Edit button (localhost only) that lets you fix narration text in-browser and save back to disk with `authorLocked: true`.

### Export to video
```bash
pip install playwright imageio-ffmpeg
playwright install chromium
python scripts/export_video.py
# outputs export/presentation_final.mp4
```

## Files

| Path | What it is |
|------|-----------|
| `index.html` | Production presentation (no edit UI) |
| `presentation.html` | Dev version (includes Edit button + save-to-disk) |
| `audio/` | MP3 narration + word-timing JSONs |
| `content/svg/` | SVG assets |
| `content/video/` | WebM video cards (Illustrate-Assist slide) |
| `serve.py` | Dev server (POST /save for in-browser edits) |
| `scripts/gen_audio.py` | Regenerate TTS for a single scene |
| `scripts/export_video.py` | Export full video via Playwright + ffmpeg |

## License

MIT
