#!/usr/bin/env python
"""
Extract embedded base64 images from presentation.html → content/images/user-uploaded/
Move SVGs → content/svg/
Update all references in presentation.html.

Usage:
    python scripts/extract-assets.py
"""
import re, base64, os, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_FILE = os.path.join(ROOT, 'presentation.html')
IMG_DIR = os.path.join(ROOT, 'content', 'images', 'user-uploaded')
AI_DIR = os.path.join(ROOT, 'content', 'images', 'ai-generated')
SVG_DIR = os.path.join(ROOT, 'content', 'svg')

os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(AI_DIR, exist_ok=True)
os.makedirs(SVG_DIR, exist_ok=True)

with open(HTML_FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# --- Extract embedded base64 images ---
# Name them by order in the gallery; user can rename after
pattern = re.compile(r'data:image/(\w+);base64,([A-Za-z0-9+/=\n]+?)(?=")')
matches = list(pattern.finditer(html))
print(f'Found {len(matches)} embedded image(s)')

# Map known scientists by position (order they appear in the gallery)
names = ['newton', 'franklin', 'cayley', 'babbage']

replacements = []
for i, m in enumerate(matches):
    ext = m.group(1)
    b64 = m.group(2).replace('\n', '')
    name = names[i] if i < len(names) else f'image-{i+1}'
    filename = f'{name}.{ext}'
    filepath = os.path.join(IMG_DIR, filename)
    with open(filepath, 'wb') as f:
        f.write(base64.b64decode(b64))
    rel_path = f'content/images/user-uploaded/{filename}'
    replacements.append((m.group(0), rel_path))
    print(f'  extracted -> {rel_path}')

for old, new in replacements:
    html = html.replace(old, new, 1)

# --- Move SVGs to content/svg/ ---
svg_files = ['flywheel.svg', 'pulse-pfd.svg']
for svg in svg_files:
    src = os.path.join(ROOT, svg)
    if os.path.exists(src):
        dst = os.path.join(SVG_DIR, svg)
        shutil.move(src, dst)
        html = html.replace(f'"{svg}"', f'"content/svg/{svg}"')
        print(f'  moved -> content/svg/{svg}')

with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print('\nDone. presentation.html updated.')
print('Folder layout:')
for dirpath, _, files in os.walk(os.path.join(ROOT, 'content')):
    rel = os.path.relpath(dirpath, ROOT)
    for fn in files:
        print(f'  {rel}/{fn}')
