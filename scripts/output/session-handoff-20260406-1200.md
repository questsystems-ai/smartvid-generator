# Session Handoff — 2026-04-06

## The Product
slide-studio — Live collaborative presentation builder. Product name: presentation.html. Author narrates intent, Claude builds animated slides. First example: dad pitch.

## Stack
Single-file HTML/CSS/JS, ElevenLabs TTS, Python serve.py (port 8500)

## Business Context
Part of citizen scientist portfolio. Dad pitch is first public example. Long-term ships with embedded agent.

## Current State
- Project bootstrapped this session
- Dad pitch migrated from notes/dad-pitch-output/: presentation.html, audio/, flywheel.svg, pulse-pfd.svg
- notes/dad-pitch-2026.yaml copied in
- serve.py configured for port 8500 + presentation.html default
- In-browser Edit button for narration (authorLocked: true) built in HAP session, present in migrated presentation.html

## Pending
- Actually build out the dad pitch slides with graphics (slides still text-only, no visuals)
- Verify Edit button works on serve.py port 8500
- Commit presentation.html + assets

## Key Files
- `presentation.html` — the dad pitch (start here)
- `notes/dad-pitch-2026.yaml` — source script
- `serve.py` — dev server port 8500

## Quick Verify
```bash
python serve.py
# http://localhost:8500/presentation.html
```
