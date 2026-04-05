#!/usr/bin/env python
"""Rewrite scene-7 (monetization) — two-stream flow diagram."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

NEW_SCENE = """\
<div class="layer " id="scene-7">
<style>
  #mono-scene {
    position: absolute;
    inset: 0;
    display: grid;
    grid-template-columns: 1fr 60px 1fr;
    grid-template-rows: auto 1fr auto auto auto auto;
    padding: 36px 72px 36px;
    gap: 0;
    align-items: start;
  }
  .mono-head {
    text-align: center;
    padding-bottom: 14px;
    opacity: 0;
    transition: opacity 0.45s ease;
  }
  .layer.active .mono-head { opacity: 1; }
  .mono-head-left  { transition-delay: 0.1s; }
  .mono-head-right { transition-delay: 0.2s; }
  .mono-head-icon  { font-size: 26px; margin-bottom: 5px; }
  .mono-head-label { font-size: 11px; font-weight: 800; letter-spacing: 0.14em; text-transform: uppercase; }
  .col-direct   .mono-head-label { color: #c8a96e; }
  .col-audience .mono-head-label { color: #0c8de9; }

  .mono-chips { display: flex; flex-direction: column; gap: 8px; padding: 0 8px; }
  .mono-chip {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 9px 14px;
    font-size: 13px;
    font-weight: 600;
    color: #d0d1d4;
    text-align: center;
    opacity: 0;
    transform: scale(0.96);
    transition: opacity 0.38s ease, transform 0.38s ease;
  }
  .col-direct   .mono-chip { border-color: rgba(200,169,110,0.2); }
  .col-audience .mono-chip { border-color: rgba(12,141,233,0.2); }
  .layer.active .mono-chip { opacity: 1; transform: scale(1); }
  .col-direct   .mono-chip:nth-child(1) { transition-delay: 0.25s; }
  .col-direct   .mono-chip:nth-child(2) { transition-delay: 0.40s; }
  .col-direct   .mono-chip:nth-child(3) { transition-delay: 0.55s; }
  .col-audience .mono-chip:nth-child(1) { transition-delay: 0.30s; }
  .col-audience .mono-chip:nth-child(2) { transition-delay: 0.45s; }
  .col-audience .mono-chip:nth-child(3) { transition-delay: 0.60s; }
  .col-audience .mono-chip:nth-child(4) { transition-delay: 0.75s; }

  .mono-arrow {
    text-align: center;
    font-size: 24px;
    padding: 8px 0 4px;
    opacity: 0;
    transition: opacity 0.4s ease;
  }
  .layer.active .mono-arrow { opacity: 1; }
  .col-direct   .mono-arrow { color: rgba(200,169,110,0.5); transition-delay: 0.65s; }
  .col-audience .mono-arrow { color: rgba(12,141,233,0.4);  transition-delay: 0.85s; }

  .mono-mid {
    border-radius: 10px;
    padding: 11px 16px;
    text-align: center;
    margin: 0 8px;
    opacity: 0;
    transform: translateY(8px);
    transition: opacity 0.45s ease, transform 0.45s ease;
  }
  .layer.active .mono-mid { opacity: 1; transform: none; }
  .mid-direct   { background: rgba(200,169,110,0.08); border: 1px solid rgba(200,169,110,0.28); transition-delay: 0.80s; }
  .mid-audience { background: rgba(12,141,233,0.08);  border: 1px solid rgba(12,141,233,0.28);  transition-delay: 1.00s; }
  .mono-mid-icon  { font-size: 18px; margin-bottom: 3px; }
  .mono-mid-label { font-size: 13px; font-weight: 700; color: #e2e3e5; }
  .mono-mid-sub   { font-size: 10.5px; color: #737680; margin-top: 3px; line-height: 1.4; }

  .mono-converge {
    grid-column: 1 / 4;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 10px 0 2px;
    opacity: 0;
    transition: opacity 0.4s ease 1.2s;
  }
  .layer.active .mono-converge { opacity: 1; }
  .conv-line-l { height: 2px; width: 26%; background: linear-gradient(90deg, rgba(200,169,110,0), rgba(200,169,110,0.55)); }
  .conv-line-r { height: 2px; width: 26%; background: linear-gradient(90deg, rgba(12,141,233,0.55), rgba(12,141,233,0)); }
  .conv-arrow  { font-size: 16px; color: rgba(255,255,255,0.25); }

  .mono-revenue {
    grid-column: 1 / 4;
    text-align: center;
    padding: 4px 0 6px;
    opacity: 0;
    transform: translateY(10px);
    transition: opacity 0.5s ease 1.4s, transform 0.5s ease 1.4s;
  }
  .layer.active .mono-revenue { opacity: 1; transform: none; }
  .rev-box {
    display: inline-flex;
    align-items: center;
    gap: 12px;
    background: rgba(68,221,136,0.08);
    border: 1px solid rgba(68,221,136,0.3);
    border-radius: 12px;
    padding: 12px 40px;
  }
  .rev-icon  { font-size: 22px; }
  .rev-label { font-size: 17px; font-weight: 800; color: #44dd88; letter-spacing: 0.04em; }
  .rev-sub   { font-size: 10px; color: #737680; margin-top: 2px; }

  .mono-xpromo {
    grid-column: 1 / 4;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding-top: 6px;
    opacity: 0;
    transition: opacity 0.4s ease 1.85s;
  }
  .layer.active .mono-xpromo { opacity: 1; }
  .xp-label  { font-size: 10px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #818cf8; }
  .xp-dash   { height: 1px; width: 100px; background: linear-gradient(90deg, rgba(129,140,248,0), rgba(129,140,248,0.45)); }
  .xp-dash-r { height: 1px; width: 100px; background: linear-gradient(90deg, rgba(129,140,248,0.45), rgba(129,140,248,0)); }
  .xp-arrow  { font-size: 13px; color: #818cf8; opacity: 0.7; }
</style>

<div id="mono-scene">

  <div class="col-direct">
    <div class="mono-head mono-head-left">
      <div class="mono-head-icon">\U0001f4b0</div>
      <div class="mono-head-label">Direct Revenue</div>
    </div>
    <div class="mono-chips">
      <div class="mono-chip">Illustrat-assist</div>
      <div class="mono-chip">FlyIRL / SkyPark</div>
      <div class="mono-chip">PULSE \u2014 gov\u2019t grants</div>
    </div>
    <div class="mono-arrow">\u2193</div>
    <div class="mono-mid mid-direct">
      <div class="mono-mid-icon">\U0001f4b3</div>
      <div class="mono-mid-label">Subscriptions &amp; Licensing</div>
      <div class="mono-mid-sub">Monthly SaaS \u00b7 technology licensing \u00b7 SBIR grants</div>
    </div>
  </div>

  <div></div>

  <div class="col-audience">
    <div class="mono-head mono-head-right">
      <div class="mono-head-icon">\U0001f465</div>
      <div class="mono-head-label">Audience-First</div>
    </div>
    <div class="mono-chips">
      <div class="mono-chip">AuthorConsole</div>
      <div class="mono-chip">presentaHTML</div>
      <div class="mono-chip">presentation.html</div>
      <div class="mono-chip">api-dash</div>
    </div>
    <div class="mono-arrow">\u2193</div>
    <div class="mono-mid mid-audience">
      <div class="mono-mid-icon">\U0001f3a7</div>
      <div class="mono-mid-label">Patreon Audience</div>
      <div class="mono-mid-sub">Followers support independent research \u00b7 cross-discovers products</div>
    </div>
  </div>

  <div class="mono-converge">
    <div class="conv-line-l"></div>
    <div class="conv-arrow">\u2198</div>
    <div class="conv-arrow">\u2193</div>
    <div class="conv-arrow">\u2199</div>
    <div class="conv-line-r"></div>
  </div>

  <div class="mono-revenue">
    <div class="rev-box">
      <div class="rev-icon">\U0001f4c8</div>
      <div>
        <div class="rev-label">Revenue</div>
        <div class="rev-sub">audience is the asset \u2014 everything else follows</div>
      </div>
    </div>
  </div>

  <div class="mono-xpromo">
    <div class="xp-arrow">\u21c4</div>
    <div class="xp-dash"></div>
    <div class="xp-label">Each audience feeds every other project</div>
    <div class="xp-dash-r"></div>
    <div class="xp-arrow">\u21c4</div>
  </div>

</div>
</div>"""

with open('presentation.html', 'r', encoding='utf-8') as f:
    html = f.read()

marker = '<div class="layer " id="scene-7">'
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

print(f'scene-7 replaced ({end - start} -> {len(NEW_SCENE)} chars). Done.')
