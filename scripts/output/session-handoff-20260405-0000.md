# Session Handoff — 2026-04-05

## The Product
slide-studio — Live collaborative presentation builder. Product name: **presentation.html**. Author narrates intent, Claude builds animated slides with SVG figures, ElevenLabs TTS narration, and image injection.

## Stack
Single-file HTML/CSS/JS + ElevenLabs TTS + Python serve.py dev server.

## Business Context
Part of the citizen scientist paper series / a-i-ron.com portfolio. Dad pitch is the first public example. Long-term: ships with embedded agent so anyone can use it without VS Code.

## Current State
Brand new project. `presentation.html` and its audio assets live in `human-author-provenance/paper/` and need to be migrated here. The in-browser Edit button (narration editing → authorLocked) was just built in the HAP session.

## Pending
1. **Migrate** `presentation.html` + `audio/` + `serve.py` from `human-author-provenance/paper/` into this repo
2. Update serve.py port to 8500 (currently 8421 in HAP)
3. Build out the dad pitch slides with graphics
4. Add `notes/dad-pitch-2026.yaml` (copy from HAP `notes/`)

## Quick Verify
```bash
python serve.py
# http://localhost:8500/presentation.html
```
