#!/usr/bin/env python
"""Rewrite scene-5 (projects-progress) — mirrors slide 5 layout, bars animate by category."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

NEW_SCENE = '''\
<div class="layer " id="scene-5">
<style>
  #progress-scene {
    display: grid;
    grid-template-columns: 1.55fr 1fr 1fr;
    gap: 0 44px;
    width: 100%;
    height: 100%;
    padding: 44px 68px 36px;
    align-content: start;
  }
  /* Columns mirror slide 5 exactly */
  #progress-scene .pcol2 { display: flex; flex-direction: column; gap: 12px; }
  #progress-scene .pcat2 {
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    padding-bottom: 11px;
    border-bottom: 1px solid rgba(255,255,255,0.09);
    margin-bottom: 2px;
  }
  .cat-tools2 .pcat2  { color: #0c8de9; }
  .cat-biz2   .pcat2  { color: #c8a96e; }
  .cat-res2   .pcat2  { color: #818cf8; }

  /* Cards — appear instantly (carry over from slide 5) */
  #progress-scene .pcard2 {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 14px 18px;
    display: flex;
    align-items: flex-start;
    gap: 13px;
  }
  .cat-res2 .pcard2 {
    background: rgba(129,140,248,0.07);
    border-color: rgba(129,140,248,0.2);
  }
  #progress-scene .picon2 { font-size: 20px; line-height: 1; flex-shrink: 0; margin-top: 2px; }
  #progress-scene .pbody2 { display: flex; flex-direction: column; gap: 8px; flex: 1; }
  #progress-scene .pname2 { font-size: 14px; font-weight: 700; color: #e2e3e5; letter-spacing: 0.01em; }

  /* Progress bar */
  .prg-row { display: flex; align-items: center; gap: 10px; }
  .prg-track {
    flex: 1;
    height: 7px;
    background: rgba(255,255,255,0.1);
    border-radius: 4px;
    overflow: hidden;
  }
  .prg-fill {
    height: 100%;
    width: 0;
    border-radius: 4px;
    transition: width 1.0s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  }
  .cat-tools2 .prg-fill { background: linear-gradient(90deg, #0c8de9, #38bdf8); }
  .cat-biz2   .prg-fill { background: linear-gradient(90deg, #c8a96e, #f0d090); }
  .cat-res2   .prg-fill { background: linear-gradient(90deg, #818cf8, #b06be0); }

  .prg-pct {
    font-size: 13px;
    font-weight: 700;
    color: #fff;
    min-width: 36px;
    text-align: right;
    white-space: nowrap;
  }
  .prg-label {
    font-size: 10px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.38);
    white-space: nowrap;
  }

  /* Bars fill when active, grouped by category via transition-delay on .prg-fill */
  .layer.active .prg-fill { width: var(--pct); }
</style>

<div id="progress-scene">

  <!-- TOOLS -->
  <div class="pcol2 cat-tools2">
    <div class="pcat2">Tools</div>

    <div class="pcard2">
      <div class="picon2">\u270d\ufe0f</div>
      <div class="pbody2">
        <div class="pname2">AuthorConsole / paperHTML</div>
        <div class="prg-row">
          <div class="prg-track"><div class="prg-fill" style="--pct:100%; transition-delay:0.1s"></div></div>
          <div class="prg-pct">100%</div>
        </div>
        <div class="prg-label">shipped</div>
      </div>
    </div>

    <div class="pcard2">
      <div class="picon2">\U0001f4fd\ufe0f</div>
      <div class="pbody2">
        <div class="pname2">presentaHTML / smartvid</div>
        <div class="prg-row">
          <div class="prg-track"><div class="prg-fill" style="--pct:75%; transition-delay:0.25s"></div></div>
          <div class="prg-pct">75%</div>
        </div>
        <div class="prg-label">weeks to ship</div>
      </div>
    </div>

    <div class="pcard2">
      <div class="picon2">\U0001f3ac</div>
      <div class="pbody2">
        <div class="pname2">presentation.html</div>
        <div class="prg-row">
          <div class="prg-track"><div class="prg-fill" style="--pct:75%; transition-delay:0.4s"></div></div>
          <div class="prg-pct">75%</div>
        </div>
        <div class="prg-label">weeks to ship</div>
      </div>
    </div>

    <div class="pcard2">
      <div class="picon2">\U0001f4ca</div>
      <div class="pbody2">
        <div class="pname2">api-dash</div>
        <div class="prg-row">
          <div class="prg-track"><div class="prg-fill" style="--pct:100%; transition-delay:0.55s"></div></div>
          <div class="prg-pct">100%</div>
        </div>
        <div class="prg-label">shipped</div>
      </div>
    </div>

    <div class="pcard2">
      <div class="picon2">\U0001f4e3</div>
      <div class="pbody2">
        <div class="pname2">Marketing Dashboard</div>
        <div class="prg-row">
          <div class="prg-track"><div class="prg-fill" style="--pct:65%; transition-delay:0.7s"></div></div>
          <div class="prg-pct">65%</div>
        </div>
        <div class="prg-label">weeks to ship</div>
      </div>
    </div>

    <div class="pcard2">
      <div class="picon2">\u26a1</div>
      <div class="pbody2">
        <div class="pname2">initiate / terminate</div>
        <div class="prg-row">
          <div class="prg-track"><div class="prg-fill" style="--pct:100%; transition-delay:0.85s"></div></div>
          <div class="prg-pct">100%</div>
        </div>
        <div class="prg-label">shipped</div>
      </div>
    </div>
  </div>

  <!-- BUSINESSES -->
  <div class="pcol2 cat-biz2">
    <div class="pcat2">Businesses</div>

    <div class="pcard2">
      <div class="picon2">\u2708\ufe0f</div>
      <div class="pbody2">
        <div class="pname2">FlyIRL / SkyPark</div>
        <div class="prg-row">
          <div class="prg-track"><div class="prg-fill" style="--pct:30%; transition-delay:1.8s"></div></div>
          <div class="prg-pct" style="font-size:11px">Phase I</div>
        </div>
        <div class="prg-label">deployment phase I</div>
      </div>
    </div>

    <div class="pcard2">
      <div class="picon2">\U0001f3a8</div>
      <div class="pbody2">
        <div class="pname2">Illustrat-assist</div>
        <div class="prg-row">
          <div class="prg-track"><div class="prg-fill" style="--pct:80%; transition-delay:1.95s"></div></div>
          <div class="prg-pct">80%</div>
        </div>
        <div class="prg-label">weeks to ship</div>
      </div>
    </div>

    <div class="pcard2">
      <div class="picon2">\U0001f529</div>
      <div class="pbody2">
        <div class="pname2">PULSE (Patent)</div>
        <div class="prg-row">
          <div class="prg-track"><div class="prg-fill" style="--pct:15%; transition-delay:2.1s"></div></div>
          <div class="prg-pct">15%</div>
        </div>
        <div class="prg-label">18–24 months</div>
      </div>
    </div>
  </div>

  <!-- APPLIED AI RESEARCH -->
  <div class="pcol2 cat-res2">
    <div class="pcat2">Applied AI Research</div>

    <div class="pcard2">
      <div class="picon2">\U0001f9e0</div>
      <div class="pbody2">
        <div class="pname2">Problem Solver Engine</div>
        <div class="prg-row">
          <div class="prg-track"><div class="prg-fill" style="--pct:15%; transition-delay:3.0s"></div></div>
          <div class="prg-pct">15%</div>
        </div>
        <div class="prg-label">research phase</div>
      </div>
    </div>

    <div class="pcard2">
      <div class="picon2">\U0001f9ec</div>
      <div class="pbody2">
        <div class="pname2">TRACER</div>
        <div class="prg-row">
          <div class="prg-track"><div class="prg-fill" style="--pct:15%; transition-delay:3.15s"></div></div>
          <div class="prg-pct">15%</div>
        </div>
        <div class="prg-label">research phase</div>
      </div>
    </div>
  </div>

</div>
</div>'''

with open('presentation.html', 'r', encoding='utf-8') as f:
    html = f.read()

marker = '<div class="layer " id="scene-5">'
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

print(f'scene-5 replaced ({end-start} -> {len(NEW_SCENE)} chars). Done.')
