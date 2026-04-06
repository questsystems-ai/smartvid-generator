#!/usr/bin/env python3
"""
insert-ia-slide.py
Inserts a new "illustrate-assist" scene-7 into presentation.html,
renumbering the existing scenes 7-12 to 8-13.
All modifications happen atomically (read, modify in memory, write once).
"""

import re
import json
import sys
from pathlib import Path

HTML_PATH = Path(__file__).parent.parent / "presentation.html"

# ---------------------------------------------------------------------------
# New scene-7 HTML to insert
# ---------------------------------------------------------------------------
NEW_SCENE_HTML = r'''</div>  <div class="layer " id="scene-7">
<style>
  #ia-scene { position: absolute; inset: 0; background: #0d1117; overflow: hidden; }
  .ia-sub {
    position: absolute; inset: 0; opacity: 0; pointer-events: none;
    transition: opacity 0.6s ease;
    display: flex; align-items: center; justify-content: center;
  }
  .ia-sub.ia-visible { opacity: 1; pointer-events: auto; }
  .ia-num { font-family: 'Courier New',monospace; font-size: 10px; color: #4da6ff; letter-spacing: 2px; margin-bottom: 10px; }
  .ia-title { font-family: 'Courier New',monospace; font-size: 11px; color: #fff; letter-spacing: 2px; font-weight: bold; margin-bottom: 10px; }
  .ia-body { font-size: 14px; color: #9a9b9e; line-height: 1.65; }
  .ia-tag { font-family: 'Courier New',monospace; font-size: 8px; color: #4c4f57; letter-spacing: 1px; margin-top: 20px; }
  /* Split layout */
  .ia-split { flex-direction: row; gap: 48px; padding: 40px 60px; align-items: center; }
  .ia-img-panel { flex: 0 0 54%; }
  .ia-img-panel img { width: 100%; max-height: 78vh; object-fit: contain; border-radius: 8px; }
  .ia-text-panel { flex: 1; display: flex; flex-direction: column; }
  /* Full-bleed */
  .ia-full { padding: 0; }
  .ia-full > img { width: 100%; height: 100%; object-fit: cover; }
  .ia-full-overlay {
    position: absolute; bottom: 0; left: 0; right: 0; padding: 28px 52px;
    background: linear-gradient(to top, rgba(13,17,23,0.97) 0%, rgba(13,17,23,0.55) 65%, transparent 100%);
  }
  /* iframe sub */
  .ia-iframe-sub { flex-direction: column; padding: 0; }
  .ia-iframe-sub iframe { flex: 1; width: 100%; border: none; background: #030712; min-height: 0; }
  .ia-iframe-bar {
    flex-shrink: 0; height: 38px; background: #0d1117; border-top: 1px solid #1a1d23;
    display: flex; align-items: center; padding: 0 28px; gap: 14px;
  }
  /* Video cards */
  .ia-cards-sub { flex-direction: column; gap: 18px; padding: 28px 48px; }
  .ia-cards-row { display: flex; gap: 20px; justify-content: center; align-items: center; flex: 1; min-height: 0; }
  .ia-cards-row video { flex: 1; min-width: 0; max-height: 58vh; border-radius: 8px; border: 1px solid #2a2d35; background: #000; }
  /* Marketing text */
  .ia-text-only { flex-direction: column; gap: 14px; text-align: center; max-width: 640px; }
  .ia-text-only .ia-title { font-size: 14px; }
  .ia-text-only .ia-body { font-size: 16px; }
</style>

<div id="ia-scene">
  <!-- 7.1 Intro (dungeonforge.jpg) -->
  <div class="ia-sub ia-full" id="ia-sub-1">
    <img src="content/images/illustratorslide/dungeonforge.jpg" alt="Illustrate Assist">
    <div class="ia-full-overlay">
      <div class="ia-num">7.1</div>
      <div class="ia-title">ILLUSTRATE ASSIST — ROMANTASY STUDIO</div>
      <div class="ia-body">From idea to illustrated book, screenplay, or pitch.</div>
    </div>
  </div>
  <!-- 7.2 Input (storynotes.jpg) -->
  <div class="ia-sub ia-split" id="ia-sub-2">
    <div class="ia-img-panel">
      <img src="content/images/illustratorslide/storynotes.jpg" alt="Story notes">
    </div>
    <div class="ia-text-panel">
      <div class="ia-num">7.2 &nbsp; INPUT</div>
      <div class="ia-title">UPLOAD TEXT OR JUST AN IDEA</div>
      <div class="ia-body">Finished manuscript? Import it. Just a concept? Claude collaborates on research and writing to develop your ideas into full books, screenplays, and pitches.</div>
    </div>
  </div>
  <!-- 7.3 Pipeline (iframe) -->
  <div class="ia-sub ia-iframe-sub" id="ia-sub-3">
    <iframe src="content/svg/scene-prompt-pathways.html" title="Scene Prompt Pathways"></iframe>
    <div class="ia-iframe-bar">
      <span class="ia-num" style="margin:0">7.3</span>
      <span class="ia-body" style="font-size:11px;color:#7b7f88;">Sophisticated multi-agent pipeline &nbsp;·&nbsp; world bible extraction &nbsp;·&nbsp; model-specific prompt generation</span>
    </div>
  </div>
  <!-- 7.4 Characters (characters.jpg) -->
  <div class="ia-sub ia-split" id="ia-sub-4">
    <div class="ia-img-panel">
      <img src="content/images/illustratorslide/characters.jpg" alt="Character refinement">
    </div>
    <div class="ia-text-panel">
      <div class="ia-num">7.4 &nbsp; CHARACTERS</div>
      <div class="ia-title">REFINE YOUR CHARACTERS</div>
      <div class="ia-body">Work with Claude to develop and lock character appearance — faces, clothing, distinctive traits. The agent remembers everything across your entire project.</div>
    </div>
  </div>
  <!-- 7.5 Scenes (sceness.jpg) -->
  <div class="ia-sub ia-split" id="ia-sub-5">
    <div class="ia-img-panel">
      <img src="content/images/illustratorslide/sceness.jpg" alt="Cinematic scenes">
    </div>
    <div class="ia-text-panel">
      <div class="ia-num">7.5 &nbsp; SCENES</div>
      <div class="ia-title">CINEMATIC SCENE COLLABORATION</div>
      <div class="ia-body">Compose scenes with cinematic precision. The agent holds your world bible in context throughout, ensuring visual consistency across every illustration.</div>
    </div>
  </div>
  <!-- 7.6 Agent (forge.jpg) -->
  <div class="ia-sub ia-split" id="ia-sub-6">
    <div class="ia-img-panel">
      <img src="content/images/illustratorslide/forge.jpg" alt="Sonnet agent">
    </div>
    <div class="ia-text-panel">
      <div class="ia-num">7.6 &nbsp; AGENT</div>
      <div class="ia-title">FULLY TOOLED SONNET WITH MEMORY</div>
      <div class="ia-body">A production Claude Sonnet agent with full tool access, persistent project memory, and deep context — collaborating until exactly the right image is produced.</div>
    </div>
  </div>
  <!-- 7.7 Output (elmore-test-1.png) -->
  <div class="ia-sub ia-full" id="ia-sub-7">
    <img src="content/images/illustratorslide/elmore-test-1.png" alt="Final illustration">
    <div class="ia-full-overlay">
      <div class="ia-num">7.7 &nbsp; OUTPUT</div>
      <div class="ia-title">UNTIL JUST THE RIGHT IMAGE IS PRODUCED</div>
      <div class="ia-body">Auto-incorporated into flipbooks, interactive lookbooks, and pitches for publishing houses or Hollywood executives.</div>
    </div>
  </div>
  <!-- 7.8 Promotional videos -->
  <div class="ia-sub ia-cards-sub" id="ia-sub-8">
    <div style="text-align:center;flex-shrink:0">
      <span class="ia-num" style="display:inline">7.8 &nbsp;</span><span class="ia-title" style="display:inline">PROMOTIONAL MATERIALS</span>
    </div>
    <div class="ia-cards-row">
      <video id="ia-card1" src="content/video/card1.webm" muted loop playsinline></video>
      <video id="ia-card2" src="content/video/card2.webm" muted loop playsinline style="opacity:0.15;transition:opacity 0.6s"></video>
      <video id="ia-card3" src="content/video/card3.webm" muted loop playsinline style="opacity:0.15;transition:opacity 0.6s"></video>
    </div>
    <div class="ia-body" style="text-align:center;font-size:12px;flex-shrink:0">Generated automatically from your project assets</div>
  </div>
  <!-- 7.9 Marketing agent -->
  <div class="ia-sub ia-text-only" id="ia-sub-9">
    <div class="ia-num">7.9</div>
    <div class="ia-title">FULL PROJECT MARKETING AGENT</div>
    <div class="ia-body">A project-specific Claude marketing agent and dashboard — audience building, PR outreach, and engagement management, all included.</div>
    <div class="ia-tag">ILLUSTRATE ASSIST &nbsp;·&nbsp; ROMANTASY STUDIO &nbsp;·&nbsp; A COMPOUNDING SYSTEM</div>
  </div>
</div>
  </div>  <div class="layer " id="scene-8">'''

# ---------------------------------------------------------------------------
# JS: sub-slide management block (goes before "// Animation loop")
# ---------------------------------------------------------------------------
IA_JS_BLOCK = r'''// Illustrate-Assist sub-slide management
const IA_SUBS = [[0,9],[9,22],[22,35],[35,43],[43,50],[50,57],[57,64],[64,82],[82,90]];
function updateIAScene(elapsed) {
  IA_SUBS.forEach(([s,e],i) => {
    const el = document.getElementById('ia-sub-'+(i+1));
    if (!el) return;
    el.classList.toggle('ia-visible', elapsed >= s && elapsed < e);
  });
  if (elapsed >= 64 && !window._iaV1) { document.getElementById('ia-card1')?.play().catch(()=>{}); window._iaV1=true; }
  if (elapsed >= 70 && !window._iaV2) { const v=document.getElementById('ia-card2'); if(v){v.style.opacity='1';v.play().catch(()=>{})} window._iaV2=true; }
  if (elapsed >= 76 && !window._iaV3) { const v=document.getElementById('ia-card3'); if(v){v.style.opacity='1';v.play().catch(()=>{})} window._iaV3=true; }
}

'''

# ---------------------------------------------------------------------------
# JS: showScene override (goes before "showScene(0);")
# ---------------------------------------------------------------------------
SHOW_SCENE_OVERRIDE = r'''// Reset IA video flags when scene changes
const _origShowScene = showScene;
showScene = function(index) {
  if (index !== 7) { window._iaV1=window._iaV2=window._iaV3=false; }
  _origShowScene(index);
};
'''

# ---------------------------------------------------------------------------
# New scene entry for SCENES array (index 7)
# ---------------------------------------------------------------------------
NEW_SCENE_ENTRY = {
    "minDuration": 90,
    "narrationHtml": (
        "Let's look at Illustrate Assist. The user uploads text \u2014 if it's finished, great. "
        "If just an idea, the app uses Claude to collaborate on research and writing to develop "
        "your ideas into books, screenplays, and pitches. The app uses a sophisticated multi-agent "
        "process to parse and extract a world bible and auto-generate model-specific prompts, at "
        "which point the user works with Claude to refine the characters, and then the cinematic "
        "scenes, collaborating with a fully tooled Sonnet agent with memory and project-context, "
        "until just the right image is produced. These are then automatically incorporated into "
        "publishable flipbooks, audiovisual interactive lookbooks, or project pitches designed for "
        "publishing houses or Hollywood executives. The app also generates promotional materials "
        "\u2014 and contains access to a project-specific full marketing agent and dashboard tool "
        "to manage audience and PR outreach and engagement.\n"
    )
}


def main():
    print(f"Reading {HTML_PATH} ...")
    content = HTML_PATH.read_text(encoding="utf-8")
    original_len = len(content)
    print(f"  File size: {original_len:,} bytes")

    # -----------------------------------------------------------------------
    # STEP 1: Renumber HTML id attributes (reverse order to avoid conflicts)
    # -----------------------------------------------------------------------
    print("\nStep 1: Renumbering scene id attributes (7-12 -> 8-13) ...")
    for old, new in [
        ('id="scene-12"', 'id="scene-13"'),
        ('id="scene-11"', 'id="scene-12"'),
        ('id="scene-10"', 'id="scene-11"'),
        ('id="scene-9"',  'id="scene-10"'),
        ('id="scene-8"',  'id="scene-9"'),
        ('id="scene-7"',  'id="scene-8"'),
    ]:
        count = content.count(old)
        content = content.replace(old, new)
        print(f"  {old} -> {new}  ({count} replacement(s))")

    # Renumber CSS selectors (reverse order; scene-7 had no custom selectors)
    print("\nStep 1b: Renumbering CSS selectors ...")
    for old, new in [
        ('#scene-12.active', '#scene-13.active'),
        ('#scene-11.active', '#scene-12.active'),
        ('#scene-10.active', '#scene-11.active'),
        ('#scene-8.active',  '#scene-9.active'),
    ]:
        count = content.count(old)
        content = content.replace(old, new)
        print(f"  {old} -> {new}  ({count} replacement(s))")

    # -----------------------------------------------------------------------
    # STEP 2: Update AUDIO_IDS
    # -----------------------------------------------------------------------
    print("\nStep 2: Updating AUDIO_IDS array ...")
    old_audio = (
        'const AUDIO_IDS = ["title", "the-moment", "the-insight", "citizen-scientist", '
        '"the-portfolio", "projects-progress", "forge-spotlight", "monetization"'
    )
    new_audio = (
        'const AUDIO_IDS = ["title", "the-moment", "the-insight", "citizen-scientist", '
        '"the-portfolio", "projects-progress", "forge-spotlight", "illustrate-assist", "monetization"'
    )
    if old_audio not in content:
        print("  ERROR: Could not find AUDIO_IDS target string!", file=sys.stderr)
        sys.exit(1)
    content = content.replace(old_audio, new_audio, 1)
    print("  Done.")

    # -----------------------------------------------------------------------
    # STEP 3: Update SCENES array
    # -----------------------------------------------------------------------
    print("\nStep 3: Updating SCENES array ...")
    scenes_match = re.search(r'const SCENES = (\[.*?\]);', content)
    if not scenes_match:
        print("  ERROR: Could not find SCENES array!", file=sys.stderr)
        sys.exit(1)

    scenes_json = scenes_match.group(1)
    scenes = json.loads(scenes_json)
    print(f"  Found {len(scenes)} existing scenes.")

    scenes.insert(7, NEW_SCENE_ENTRY)
    print(f"  Inserted new scene at index 7. Total: {len(scenes)} scenes.")

    new_scenes_json = json.dumps(scenes, ensure_ascii=False)
    content = content.replace(
        f"const SCENES = {scenes_json};",
        f"const SCENES = {new_scenes_json};",
        1
    )

    # -----------------------------------------------------------------------
    # STEP 4: Insert new scene-7 HTML
    # -----------------------------------------------------------------------
    print("\nStep 4: Inserting scene-7 HTML block ...")
    # After Step 1, old scene-7 is now scene-8. We insert BEFORE the pattern
    # that starts the (now-renumbered) scene-8.
    # The NEW_SCENE_HTML already ends with the scene-8 opening tag.
    target_pattern = '</div>  <div class="layer " id="scene-8">'
    if target_pattern not in content:
        print("  ERROR: Could not find insertion target for scene-8!", file=sys.stderr)
        # Try to diagnose
        for n in range(6, 15):
            pat = f'id="scene-{n}"'
            print(f"    {pat}: {content.count(pat)} occurrences")
        sys.exit(1)

    # Replace just the first occurrence of the scene-8 opening with [new HTML + scene-8 opening]
    content = content.replace(target_pattern, NEW_SCENE_HTML, 1)
    print("  Done.")

    # -----------------------------------------------------------------------
    # STEP 5: Add JavaScript sub-slide management
    # -----------------------------------------------------------------------
    print("\nStep 5: Inserting JavaScript blocks ...")

    # 5a: Insert IA_JS_BLOCK before "// Animation loop"
    anim_loop_marker = "// Animation loop"
    if anim_loop_marker not in content:
        print("  ERROR: Could not find '// Animation loop'!", file=sys.stderr)
        sys.exit(1)
    content = content.replace(anim_loop_marker, IA_JS_BLOCK + anim_loop_marker, 1)
    print("  Inserted IA sub-slide JS block before '// Animation loop'.")

    # 5b: Insert updateIAScene call before "  // Narration progress bar"
    narration_marker = "  // Narration progress bar"
    if narration_marker not in content:
        print("  ERROR: Could not find '  // Narration progress bar'!", file=sys.stderr)
        sys.exit(1)
    content = content.replace(
        narration_marker,
        "  if (currentScene === 7) updateIAScene(elapsed);\n" + narration_marker,
        1
    )
    print("  Inserted updateIAScene(elapsed) call before narration progress bar.")

    # 5c: Insert showScene override before "showScene(0);"
    # There are two occurrences — we want the one near preloadAudio() / overlay setup,
    # which is the second one (the first is in a comment/save function).
    # Let's be precise: find "preloadAudio();\nshowScene(0);"
    show_scene_target = "preloadAudio();\nshowScene(0);"
    if show_scene_target not in content:
        print("  ERROR: Could not find 'preloadAudio();\\nshowScene(0);'!", file=sys.stderr)
        # Fallback: try with \r\n
        show_scene_target = "preloadAudio();\r\nshowScene(0);"
        if show_scene_target not in content:
            print("  ERROR: Fallback also failed!", file=sys.stderr)
            sys.exit(1)
    content = content.replace(
        show_scene_target,
        SHOW_SCENE_OVERRIDE + show_scene_target,
        1
    )
    print("  Inserted showScene override before preloadAudio()/showScene(0).")

    # -----------------------------------------------------------------------
    # Write output
    # -----------------------------------------------------------------------
    print(f"\nWriting modified file ({len(content):,} bytes) ...")
    HTML_PATH.write_text(content, encoding="utf-8")
    print("  Done.")

    # -----------------------------------------------------------------------
    # VERIFICATION
    # -----------------------------------------------------------------------
    print("\n--- VERIFICATION ---")

    # Re-read fresh
    final = HTML_PATH.read_text(encoding="utf-8")

    # 1. SCENES array count
    sm = re.search(r'const SCENES = (\[.*?\]);', final)
    if sm:
        sc = json.loads(sm.group(1))
        print(f"1. SCENES array length: {len(sc)}  (expected 14) {'OK' if len(sc) == 14 else 'FAIL'}")
    else:
        print("1. SCENES array: NOT FOUND  FAIL")

    # 2. AUDIO_IDS length
    am = re.search(r'const AUDIO_IDS = (\[.*?\]);', final)
    if am:
        ai = json.loads(am.group(1))
        print(f"2. AUDIO_IDS length: {len(ai)}  (expected 14) {'OK' if len(ai) == 14 else 'FAIL'}")
    else:
        print("2. AUDIO_IDS: NOT FOUND  FAIL")

    # 3. scene-7 exists
    s7_count = final.count('id="scene-7"')
    print(f"3. id=\"scene-7\" occurrences: {s7_count}  (expected 1) {'OK' if s7_count == 1 else 'FAIL'}")

    # 4. scene-13 exists
    s13_count = final.count('id="scene-13"')
    print(f"4. id=\"scene-13\" occurrences: {s13_count}  (expected 1) {'OK' if s13_count == 1 else 'FAIL'}")

    # 5. No duplicate scene IDs
    print("5. Checking for duplicate scene IDs ...")
    all_ok = True
    for n in range(14):
        pat = f'id="scene-{n}"'
        cnt = final.count(pat)
        status = "OK" if cnt == 1 else f"FAIL (count={cnt})"
        print(f"   scene-{n}: {status}")
        if cnt != 1:
            all_ok = False

    # 6. Check ia-sub-* present
    ia_subs = sum(1 for i in range(1, 10) if f'id="ia-sub-{i}"' in final)
    print(f"6. ia-sub elements found: {ia_subs}  (expected 9) {'OK' if ia_subs == 9 else 'FAIL'}")

    # 7. updateIAScene function present
    has_fn = "function updateIAScene" in final
    print(f"7. updateIAScene function: {'OK' if has_fn else 'FAIL'}")

    # 8. showScene override present
    has_override = "_origShowScene" in final
    print(f"8. showScene override: {'OK' if has_override else 'FAIL'}")

    print("\nAll done." if all_ok else "\nSome checks FAILED — review output above.")


if __name__ == "__main__":
    main()
