# smartvid-generator

## Startup Protocol
On every new conversation, run `/initiate` before anything else. Zero ramp-up time between sessions.

## Product Vision
**smartvid-generator** is an AI-powered narrated educational video generator. It takes a topic and audience description, uses Claude (Sonnet) to generate a full YAML presentation script with scene-level animated SVG diagrams, fetches real images from Wikimedia Commons for scenes that need photos, and pipes the assembled config to presentaHTML to produce a single self-contained HTML file — a professional-quality narrated audiovisual explainer.

**The thesis:** Any scientific or technical concept, for any audience, from script to published presentation in one command and under $3 in API spend.

**Proof of concept — dual-domain validation:**
1. Math/CS: SHA-256 explainer (already built manually with presentaHTML) — cryptography for non-technical readers
2. Wet bio/chemistry: PCR explainer for high schoolers — the first generated output from this tool

**PCR demo specifics:**
- Audience: high school students learning history, mechanics, and impact of the Polymerase Chain Reaction
- Visual needs: animated SVG showing DNA denaturation → primer annealing → extension cycle; real image of Thermus aquaticus source environment (Yellowstone hot springs — NOT hydrothermal vents); Kary Mullis / Nobel Prize context
- Note: Taq polymerase comes from Thermus aquaticus, discovered in Yellowstone's hot springs (Thomas Brock, 1966) — a better visual story than hydrothermal vents

**Future: The Studio UI**
Once the pipeline is proven (PCR demo), the next phase is a browser-based authoring environment:
- User describes topic + audience
- Claude generates full YAML draft
- Collaborative scene-by-scene optimization (rewrite narration, adjust jargon, generate/swap visuals)
- One-click final export → publishable HTML

**Positioning:** Part of the citizen scientist stack. Sibling to presentaHTML. The citizen scientist tool for producing mass-distributable audiovisual scientific communication at zero marginal cost per viewer.

**Consumer name:** TBD — candidates: SmartVid, ExplainerForge, ClearScience
**Monetization path:** Open-source core → hosted service for non-technical users → institutional licensing (university science communication offices, journal publishers)

## Stack
- **Language:** Python 3
- **LLM:** Anthropic Claude Sonnet (via API) — YAML generation + SVG generation
- **TTS:** ElevenLabs (primary), Edge TTS (free fallback)
- **Image fetching:** Wikimedia Commons API (free, open license)
- **Image generation:** DALL-E 3 / Replicate (optional, user API key)
- **Presentation engine:** presentaHTML (sibling project at `../presentaHTML/`)
- **Entry point:** `generate.py <topic> --audience <description>`

## Architecture (MVP)
```
generate.py
  ├── call Claude → full YAML script + per-scene SVG code
  ├── for each scene with image: fetch from Wikimedia Commons
  ├── assemble config.yaml (with embedded SVGs + image paths)
  └── call presentahtml.py → output HTML
```

## Complexity Check (Self-Audit Rule)
After 2 failed attempts at the same problem: STOP. Diagnose what's tangled, propose a focused fix, estimate the effort, let the user decide. Don't brute-force.

## When Searching
If Glob or Grep returns a directory or file path that's plausibly relevant to the question, read inside it before answering. Don't stop at the listing.

## Git Workflow
- Default branch: `main`. Use `dev/wip` for in-progress work, never push broken code to `main`.
- Never commit `.env.local`, `node_modules/`, `__pycache__/`, `*.pyc`
- Commit often — clean git state = fast next session recovery

## Session Continuity
- Handoff report: `scripts/output/session-handoff-YYYYMMDD-HHMM.md` (timestamped, written by `/terminate`, read by `/initiate`)
- Session log: `scripts/output/session-log.md` (auto-logged via hooks, crash insurance)
- End of session: run `/terminate` — commit check, handoff write, memory update
- New terminal: open a new terminal in this project directory and run `claude`

## Budget Discipline
- Run as Sonnet (cost-aware mode always active)
- Opus only as a contained subagent for frontier reasoning — announced before launch
- ~25 message soft cap per session — open a fresh terminal and run `claude` to swap context
