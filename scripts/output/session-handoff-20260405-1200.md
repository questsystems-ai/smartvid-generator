# Session Handoff — 2026-04-05

## The Product
presentation.html — live collaborative animated slide builder. Author narrates intent, Claude builds animated slides with SVG figures, ElevenLabs TTS narration, and image injection. Single self-contained HTML file that plays like a film. The dad pitch ("The Workshop") is the ground-zero dev example.

## Stack
Single-file HTML/CSS/JS + ElevenLabs TTS + Python serve.py (port 8500) + asset pipeline scripts in scripts/

## Business Context
Aaron solo. First public demo = dad pitch (family funding ask). Release target: AI power user community via HN/GitHub. Phase 2: PowerPoint import. Phase 3: universal UI + publish-to-web + FlyIRL marketing dashboard integration.

## Current State — 2026-04-05, branch: main

**Done this session:**
- Migrated presentation.html + audio from parent repo (correct "The Workshop" dad pitch, not HAP demo)
- Asset pipeline: base64 portraits extracted → content/images/user-uploaded/ (newton.jpg, franklin.webp, cayley.jpg, babbage.webp); SVGs → content/svg/
- serve.py updated to port 8500
- notes/strategy.md written — PowerPoint killer thesis, 3-phase product arc, collaboration angle
- Slide 5 (the-portfolio): 3-column grouped layout, 11 projects, sequential category reveal (Tools → Businesses → Applied AI Research)
- Slide 6 (projects-progress): mirrors slide 5 layout, progress bars fill by category (blue/gold/purple)
- Slide 7 (forge-spotlight): cards float in open space above green electrical chain in PULSE PFD — no gradients
- Slide 8 (monetization): two-stream flow diagram (Direct Revenue vs Audience-First → Revenue node + cross-promo band)
- Rebuild scripts in scripts/ for each slide (reusable)

**Pending:**
- Slides 9–13 (the-flywheel, the-model, the-ask, timeline, close) — no visuals yet, still using old pillars templates
- Flywheel slide (slide 9) — verify it renders correctly landscape, may need position tweak
- Monetization slide font size at 1.5× — may need further tuning once seen on target screen
- PULSE forge-spotlight card positions (top: 8%, left: 54%) — may need nudging per screen size
- dad-pitch-2026.yaml narration says "Nine projects" — should be "Eleven" (already fixed in HTML but YAML is source of truth for re-renders)
- Export script (embed files back to base64 for single-file distribution) — not yet built

## Key Files
- `presentation.html` — the whole product, edit directly
- `notes/dad-pitch-2026.yaml` — master script (narration source of truth)
- `notes/strategy.md` — product vision and PowerPoint killer thesis
- `scripts/rebuild-*.py` — per-slide rebuild scripts (run from repo root)
- `scripts/extract-assets.py` — extract embedded base64 images from HTML
- `content/images/user-uploaded/` — portrait photos
- `content/svg/` — flywheel.svg, pulse-pfd.svg

## Quick Verify
```bash
python serve.py
# http://localhost:8500/presentation.html
# Navigate to slides 5-8 and verify animated reveals work
```
