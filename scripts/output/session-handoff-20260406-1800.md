# Session Handoff — 2026-04-06

## The Product
`presentation.html` — a single self-contained HTML file that plays like a film. Animated SVGs, ElevenLabs TTS narration with word-level timing, staggered CSS transitions, collapsible slide gallery sidebar (localhost only). Built collaboratively: author describes intent, Claude writes it. Anti-PowerPoint for solo founders, researchers, educators. First example: dad pitch ("The Workshop").

## Stack
Single-file HTML/CSS/JS · ElevenLabs TTS (George voice, eleven_multilingual_v2) · Python serve.py (POST /save) · `scripts/gen_audio.py` for TTS regeneration · audio/ + content/svg/ + content/video/ as siblings

## Business Context
Aaron, solo founder. Dad pitch deck for $12k/6-month funding ask. Presentation is also a live demo of the product being pitched.

## Current State — 2026-04-06, branch: main (93c9c40)

### Done this session
- **PULSE acronym** fixed everywhere: `Portable Unified Lightweight Scalable Engine`
- **Scene 7 (Illustrate-Assist)**: IA_SUBS remapped to 57.6s audio; ia-sub-9 (dashboard) removed; promo videos (ia-card1/2/3) now play sequentially via `ended` event chaining; slide waits for last video + 2s via `audioFinishedResolve`; `minDuration` set to 200 as sentinel
- **Scene 9 (Flywheel)**: all animation delays remapped to word-level timestamps from `the-flywheel_timing.json`
- **Scene 5 (Projects Progress)**: narration corrected to "eleven" projects, "sixty-one percent" (was "seven"/"forty-one") — audio regenerated
- **Audio regenerated**: forge-spotlight (PULSE rename), the-portfolio (PULSE rename), projects-progress (stats fix), illustrate-assist (first-ever generation)
- **Video card triggers**: updated from 64/70/76s → 46/47/48s to match new ia-sub-8 window
- **paper-draft-workshop-loop.md**: full paperHTML draft on the workshop loop method

### Key decisions
- `[PULSE acronym]`: Portable Unified Lightweight Scalable Engine
- `[Scene 7 minDuration]`: 200 (sentinel — actual advance triggered by card3 `ended` + 2s)
- `[IA_SUBS]`: `[[0,2],[2,13],[13,22],[22,25],[25,29],[29,34],[34,46],[46,60]]` (8 entries, ia-sub-9 removed)
- `[George voice]`: JBFqnCBsd6RMkjVDRZzb, eleven_multilingual_v2, stability 0.35, similarity 0.80, style 0.55

### Pending / next session
1. **Scene 9 text overlap**: one flywheel "door" circle has a text overlap — user noticed it but session ended before identifying which circle. Need visual inspection to fix
2. **Scene 8 (Monetization)**: no timing issues reported but not re-examined this session
3. **Slides 10–13**: scene-10 (The Model) is a plain title screen, scenes 11–13 have no custom visuals yet
4. **Export script**: single-file distribution (re-embed assets as base64) — not yet built
5. **paperHTML**: `notes/paper-draft-workshop-loop.md` is a complete draft — needs to go through paperHTML pipeline to publish

## Key files
- `presentation.html` — everything
- `scripts/gen_audio.py` — TTS regeneration: `python scripts/gen_audio.py <audio_id> <scene_index>`
- `audio/*_timing.json` — word-level timing per scene
- `notes/paper-draft-workshop-loop.md` — paperHTML draft

## Quick verify
```bash
python serve.py
# open http://localhost:8500/presentation.html
# navigate to slide 7 (illustrate-assist) — videos should play sequentially
# navigate to slide 9 (flywheel) — nodes should appear in sync with narration
```
