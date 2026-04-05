#!/usr/bin/env python
"""Rewrite scene-4 (the-portfolio) — grouped sequential reveal, readable card size."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

NEW_SCENE = '''\
<div class="layer " id="scene-4">
<style>
  #portfolio-scene {
    display: grid;
    grid-template-columns: 1.55fr 1fr 1fr;
    gap: 0 44px;
    width: 100%;
    height: 100%;
    padding: 44px 68px 36px;
    align-content: start;
  }
  .pcol { display: flex; flex-direction: column; gap: 12px; }

  /* Category labels — animate in with first card of their group */
  .pcat {
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    padding-bottom: 11px;
    border-bottom: 1px solid rgba(255,255,255,0.09);
    margin-bottom: 2px;
    opacity: 0;
    transition: opacity 0.4s ease;
  }
  .cat-tools  .pcat { color: #0c8de9; }
  .cat-biz    .pcat { color: #c8a96e; }
  .cat-res    .pcat { color: #818cf8; }

  /* Cards */
  .pcard {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 14px 18px;
    display: flex;
    align-items: flex-start;
    gap: 13px;
    opacity: 0;
    transform: translateY(16px);
    transition: opacity 0.42s ease, transform 0.42s ease;
  }
  .cat-res .pcard {
    background: rgba(129,140,248,0.07);
    border-color: rgba(129,140,248,0.2);
  }
  .layer.active .pcard { opacity: 1; transform: none; }
  .layer.active .pcat  { opacity: 1; }

  .picon { font-size: 20px; line-height: 1; flex-shrink: 0; margin-top: 2px; }
  .pbody { display: flex; flex-direction: column; gap: 5px; }
  .pname { font-size: 14px; font-weight: 700; color: #e2e3e5; letter-spacing: 0.01em; }
  .pdesc { font-size: 12px; color: #737680; line-height: 1.45; }
</style>

<div id="portfolio-scene">

  <!-- TOOLS -->
  <div class="pcol cat-tools">
    <div class="pcat" style="transition-delay:0.15s">Tools</div>

    <div class="pcard" style="transition-delay:0.15s">
      <div class="picon">\u270d\ufe0f</div>
      <div class="pbody">
        <div class="pname">AuthorConsole / paperHTML</div>
        <div class="pdesc">Cryptographic proof of human authorship. paperHTML: research published as narrated interactive documents.</div>
      </div>
    </div>

    <div class="pcard" style="transition-delay:0.35s">
      <div class="picon">\U0001f4fd\ufe0f</div>
      <div class="pbody">
        <div class="pname">presentaHTML / smartvid</div>
        <div class="pdesc">YAML \u2192 narrated animated HTML presentation. Smartvid: topic \u2192 AI-generated educational explainer video.</div>
      </div>
    </div>

    <div class="pcard" style="transition-delay:0.55s">
      <div class="picon">\U0001f3ac</div>
      <div class="pbody">
        <div class="pname">presentation.html</div>
        <div class="pdesc">Live collaborative slide builder. Author narrates, Claude builds. You\u2019re watching it now.</div>
      </div>
    </div>

    <div class="pcard" style="transition-delay:0.75s">
      <div class="picon">\U0001f4ca</div>
      <div class="pbody">
        <div class="pname">api-dash</div>
        <div class="pdesc">Real-time AI spend dashboard across 8+ providers. Because someone has to watch the meter.</div>
      </div>
    </div>

    <div class="pcard" style="transition-delay:0.95s">
      <div class="picon">\U0001f4e3</div>
      <div class="pbody">
        <div class="pname">Marketing Dashboard</div>
        <div class="pdesc">Autonomous AI marketing agent. Manages ads, email, social, and experiments. No agency required.</div>
      </div>
    </div>

    <div class="pcard" style="transition-delay:1.15s">
      <div class="picon">\u26a1</div>
      <div class="pbody">
        <div class="pname">initiate / terminate</div>
        <div class="pdesc">Session continuity skills for AI-powered dev workflows. Zero ramp-up between sessions. Clean handoffs every time.</div>
      </div>
    </div>
  </div>

  <!-- BUSINESSES -->
  <div class="pcol cat-biz">
    <div class="pcat" style="transition-delay:2.0s">Businesses</div>

    <div class="pcard" style="transition-delay:2.0s">
      <div class="picon">\u2708\ufe0f</div>
      <div class="pbody">
        <div class="pname">FlyIRL / SkyPark</div>
        <div class="pdesc">Guided flight experiences in a defined SkyZone. For GA pilots and first-timers alike.</div>
      </div>
    </div>

    <div class="pcard" style="transition-delay:2.25s">
      <div class="picon">\U0001f3a8</div>
      <div class="pbody">
        <div class="pname">Illustrat-assist</div>
        <div class="pdesc">AI illustration studio for creative visual storytelling. Character portraits, world bibles, scene generation.</div>
      </div>
    </div>

    <div class="pcard" style="transition-delay:2.5s">
      <div class="picon">\U0001f529</div>
      <div class="pbody">
        <div class="pname">PULSE (Patent)</div>
        <div class="pdesc">Pulse combustion power module for drones and field equipment. H\u2082O\u2082 + propane \u2192 48V DC. Provisional filed March 2026.</div>
      </div>
    </div>
  </div>

  <!-- APPLIED AI RESEARCH -->
  <div class="pcol cat-res">
    <div class="pcat" style="transition-delay:3.4s">Applied AI Research</div>

    <div class="pcard" style="transition-delay:3.4s">
      <div class="picon">\U0001f9e0</div>
      <div class="pbody">
        <div class="pname">Problem Solver Engine</div>
        <div class="pdesc">Multi-agent AI research engine for hard policy problems. AETE: what happens to the economy when AI replaces knowledge work?</div>
      </div>
    </div>

    <div class="pcard" style="transition-delay:3.65s">
      <div class="picon">\U0001f9ec</div>
      <div class="pbody">
        <div class="pname">TRACER</div>
        <div class="pdesc">Bio-inspired AI memory. Use-reinforced, reconstructive, emotionally weighted \u2014 memory that grows like a relationship, not a database. arXiv target.</div>
      </div>
    </div>
  </div>

</div>
</div>'''

with open('presentation.html', 'r', encoding='utf-8') as f:
    html = f.read()

marker = '<div class="layer " id="scene-4">'
start = html.find(marker)
depth = 0; i = start
while i < len(html):
    if html[i:i+4] == '<div': depth += 1; i += 4
    elif html[i:i+6] == '</div>':
        depth -= 1
        if depth == 0: end = i + 6; break
        i += 6
    else: i += 1

html = html[:start] + NEW_SCENE + html[end:]

with open('presentation.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Replaced scene-4 ({end-start} -> {len(NEW_SCENE)} chars). Done.')
