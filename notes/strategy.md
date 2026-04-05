# presentation.html — Strategic Vision

*Living doc. Append, don't edit history. Most recent thinking at top.*

---

## 2026-04-05 — The PowerPoint Killer Thesis

### What We're Actually Building

The product name is `presentation.html`. The tagline: *A guy and his Claude making a presentation.*

But the longer frame is this: **PowerPoint is a mockup tool.** People spend hours arranging rectangles to approximate something that should move, speak, and feel alive — and then they export a static file and email it. That's the problem we're solving. Not "better slides." The whole category of what a presentation can be.

PowerPoint's actual value is its ecosystem: ubiquitous on every machine, familiar to everyone, good enough. We don't fight that — we absorb it. You have an existing deck? Import it. We take what you've already built and bring it into the 21st century: animated, narrated, self-contained, publishable to the web.

The author still does the thinking. We just handle everything that comes after.

---

### The Product Arc (Three Phases)

#### Phase 1 — Claude Code Tool (Now)
For AI power users who have Claude Code and know their way around a repo.

- Author describes what they want. Claude builds it.
- In-browser Edit button for narration — changes save to disk, `authorLocked: true` so Claude never overwrites human edits.
- Single self-contained HTML file. No build step. Plays like a film.
- Served locally via `serve.py`. Deployed anywhere as a single file.
- **Target audience:** Aaron first. Then the AI power user / dev community.

This is also the dev example: the dad pitch (`notes/dad-pitch-2026.yaml`) is the proof of concept. It was built with the tools it describes. That's not a trick — that's the whole argument.

**Release play:** Launch to AI/dev community via HN/GitHub. README announces the in-progress universal tool. People who can't wait or can't build it themselves know it's coming.

#### Phase 2 — Import + Augment
PowerPoint isn't the enemy. It's the source material.

- **Import PowerPoint:** parse the deck, extract structure and content, ingest as slides.
- Author's existing work is honored — text, structure, intent preserved.
- We then augment: animate, narrate, add SVG figures, embed images as base64.
- Author stays in control; the tool handles the production work.

This is where we eat PowerPoint's lunch without fighting it. The pitch: *keep working the way you work. Just let us handle the last mile.*

#### Phase 3 — Universal UI (No VS Code Required)
For researchers, founders, educators, teachers — anyone who wants broadcast-quality presentations without video production overhead or a GitHub account.

- Browser-based UI handles everything: conversation to build, edit to refine, preview inline.
- User interacts to build what needs to be built, edits narration/content, optimizes.
- **"Publish to web"** — sends the single HTML to hosting. Hands off to the marketing dashboard for promotion control.
- **"Auto-promote"** — select a budget, agree on a strategy and target audiences, set target metrics, then execute. User watches the dashboard for results. (Marketing dashboard lives in FlyIRL repo in its current form; will be the distribution layer here.)
- The embedded agent (pre-trained, no Claude Code needed) lives in the UI. Anyone can open it and start building.

---

### The Collaboration Angle

Because it's all file-based + git version control, collaboration is a natural feature — not a bolt-on.

- Multiple contributors can work on the same presentation across branches.
- Author locking (`authorLocked: true`) is already the mechanism for protecting human-written content from AI rewrites — that same mechanism protects co-author work from each other.
- PR-based review model for shared decks: propose a slide change, collaborator approves or edits.
- Version history is baked in — every change is a commit, every deck is recoverable.

For Phase 3 UI users, this gets wrapped in something more approachable (like Google Slides sharing UX), but the underlying primitive is git.

---

### How We're Different

| Feature | PowerPoint | Google Slides | Canva | presentation.html |
|---|---|---|---|---|
| Animated figures | ❌ | ❌ | Limited | ✅ SVG, inline |
| Narrated audio | ❌ | ❌ | ❌ | ✅ ElevenLabs word-timed |
| Single-file deployable | ❌ | ❌ | ❌ | ✅ |
| Author-AI collaboration | ❌ | ❌ | ❌ | ✅ |
| Git version control | ❌ | ❌ | ❌ | ✅ |
| Import PowerPoint | ✅ native | ✅ | ✅ | 🔜 Phase 2 |
| One-click publish to web | ❌ | Partial | Partial | 🔜 Phase 3 |
| Auto-promote / marketing | ❌ | ❌ | ❌ | 🔜 Phase 3 + FlyIRL |
| No subscription for author | ❌ | ❌ | ❌ | ✅ (Phase 1–2) |

---

### Why It Works as a Product

**The self-referential proof:** The dad pitch was built using the tool it describes. That's the business card. Every time we demo it, the demo itself is the argument.

**The citizen scientist framing:** This is a publishing format, not just a presentation tool. Researchers, founders, independent thinkers — anyone who has something to say and needs more than a PDF but less than a video production studio.

**The compounding flywheel:** presentation.html → used by AI power users → they publish their presentations → audiences discover the tool → some want it for non-technical use → Phase 3 UI serves them → they publish → FlyIRL marketing dashboard gets more data → promotes better.

**The portfolio fit:** Every project in the portfolio (HAP paper, FORGE, romantasy, api-dash) eventually needs a presentation. They're all future customers of this tool. The portfolio IS the first customer base.

---

### Immediate Development Focus

Ground zero is the dad pitch. The goal: make it perfect as the public demo.

1. Verify flywheel slide (slide 9) renders correctly in landscape
2. Evaluate all slides against the YAML — does each slide look as good as the narration is?
3. Identify gaps: missing SVG figures, weak visual templates, animation opportunities
4. Ship as the launch demo alongside the AI power user release

After that: README, GitHub, HN post. Announce Phase 2 (PowerPoint import) and Phase 3 (universal UI) as in-progress roadmap.

---

### Open Questions

- **Pricing model for Phase 3:** Freemium? Pay-per-publish? Creator subscription? (Don't decide until there are users.)
- **ElevenLabs dependency:** For Phase 3, either the user brings their own key or we handle it (cost center). Decision deferred.
- **Video export:** Some users will want MP4 not HTML. Puppeteer/screen-record path exists. Scope for Phase 3.
- **PowerPoint import format:** PPTX is an open XML format — parseable with python-pptx. Scope for Phase 2 spike.
