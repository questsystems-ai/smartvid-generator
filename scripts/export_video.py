#!/usr/bin/env python3
"""
Export presentation.html as a YouTube-ready MP4 with SRT captions.

Usage:
    python scripts/export_video.py

Outputs (in export/):
    presentation.mp4  — upload to YouTube
    captions.srt      — upload as YouTube captions (Subtitles/CC)

serve.py must be running (port 8500), or this script will start it automatically.
"""

import json
import os
import subprocess
import sys
import time
import socket
import signal
from pathlib import Path

ROOT = Path(__file__).parent.parent
AUDIO_DIR = ROOT / 'audio'
VIDEO_DIR = ROOT / 'content' / 'video'
EXPORT_DIR = ROOT / 'export'

# Must match AUDIO_IDS and SKIPPED_SCENES in presentation.html
AUDIO_IDS = [
    "title", "the-moment", "the-insight", "citizen-scientist", "the-portfolio",
    "projects-progress", "forge-spotlight", "illustrate-assist", "monetization",
    "the-flywheel", "the-model", "the-ask", "timeline", "close"
]
SKIPPED_SCENES = {2}  # the-insight (deprecated)

# Scene 7 (illustrate-assist) has video cards that extend past audio end.
# card1+card2+card3 play sequentially starting at t=46s in the scene.
# Add this buffer on top of the audio duration for scene 7.
IA_VIDEO_EXTRA_SECONDS = 20  # cards=17s + 2s settle + 1s margin

WORDS_PER_CAPTION = 6
PRESENTATION_URL = 'http://localhost:8500/presentation.html'
END_BUFFER = 5  # seconds of extra wait after computed total


def ffprobe_duration(path):
    r = subprocess.run(
        ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
         '-of', 'csv=p=0', str(path)],
        capture_output=True, text=True, check=True
    )
    return float(r.stdout.strip())


def get_audio_durations():
    print("  Getting audio durations via ffprobe...")
    durations = {}
    for audio_id in AUDIO_IDS:
        path = AUDIO_DIR / f'{audio_id}.mp3'
        if path.exists():
            durations[audio_id] = ffprobe_duration(path)
        else:
            print(f"  Warning: {audio_id}.mp3 not found, using 30s estimate")
            durations[audio_id] = 30.0
    return durations


def build_narration_audio(durations):
    """Concatenate all active scene audio files into one MP3."""
    concat_txt = EXPORT_DIR / 'audio_concat.txt'
    active_ids = [aid for i, aid in enumerate(AUDIO_IDS) if i not in SKIPPED_SCENES]

    with open(concat_txt, 'w') as f:
        for audio_id in active_ids:
            path = (AUDIO_DIR / f'{audio_id}.mp3').resolve()
            # ffmpeg concat format requires forward slashes even on Windows
            f.write(f"file '{str(path).replace(chr(92), '/')}'\n")

    out = EXPORT_DIR / 'narration.mp3'
    subprocess.run([
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
        '-i', str(concat_txt), '-c', 'copy', str(out)
    ], check=True, capture_output=True)
    print(f"  Narration audio -> {out.name}")
    return out


def _fmt_srt_time(s):
    ms = int((s % 1) * 1000)
    return f"{int(s)//3600:02d}:{int(s)//60%60:02d}:{int(s)%60:02d},{ms:03d}"


def gen_srt(durations, time_offset=0.0):
    """Generate SRT from word-level timing JSONs.
    time_offset: seconds to add to all timestamps (accounts for video startup delay).
    """
    entries = []
    offset = 0.0

    for i, audio_id in enumerate(AUDIO_IDS):
        if i in SKIPPED_SCENES:
            continue
        timing_path = AUDIO_DIR / f'{audio_id}_timing.json'
        duration = durations.get(audio_id, 30.0)

        if timing_path.exists():
            words = json.loads(timing_path.read_text(encoding='utf-8'))
            for j in range(0, len(words), WORDS_PER_CAPTION):
                chunk = words[j:j + WORDS_PER_CAPTION]
                start = time_offset + offset + chunk[0][1]
                end = time_offset + offset + chunk[-1][2]
                text = ' '.join(w[0] for w in chunk)
                entries.append((start, end, text))
        else:
            print(f"  Warning: no timing JSON for {audio_id}, no captions for this scene")

        offset += duration
        # Scene 7 extra: IA video cards play past audio end
        if audio_id == 'illustrate-assist':
            offset += IA_VIDEO_EXTRA_SECONDS

    srt_path = EXPORT_DIR / 'captions.srt'
    with open(srt_path, 'w', encoding='utf-8') as f:
        for idx, (start, end, text) in enumerate(entries, 1):
            f.write(f"{idx}\n{_fmt_srt_time(start)} --> {_fmt_srt_time(end)}\n{text}\n\n")

    print(f"  Generated {len(entries)} captions -> {srt_path.name}")
    return srt_path


def is_serve_running(port=8500):
    try:
        with socket.create_connection(('localhost', port), timeout=1):
            return True
    except OSError:
        return False


def start_serve():
    """Start serve.py in background if not already running."""
    print("  serve.py not detected — starting it...")
    proc = subprocess.Popen(
        [sys.executable, str(ROOT / 'serve.py')],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        cwd=str(ROOT)
    )
    time.sleep(2)
    if not is_serve_running():
        raise RuntimeError("serve.py failed to start on port 8500")
    return proc


def record_video(durations, total_wait_seconds):
    """Launch Playwright headless, mock audio, record the presentation."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise RuntimeError("playwright not installed. Run: pip install playwright && playwright install chromium")

    video_tmp = EXPORT_DIR / '_playwright_video'
    video_tmp.mkdir(exist_ok=True)

    # JS that fires audio onended after real duration without actual playback.
    # VIDEO elements are NOT mocked — muted WebM cards must play normally.
    dur_map = json.dumps({aid: round(d, 3) for aid, d in durations.items()})
    audio_mock_js = f"""
(function() {{
  const DURATIONS = {dur_map};
  const _orig = HTMLMediaElement.prototype.play;
  HTMLMediaElement.prototype.play = function() {{
    if (this.tagName === 'VIDEO') return _orig.call(this);
    const m = (this.src || '').match(/audio\\/([^/?#]+)\\.mp3/);
    const aid = m ? m[1] : null;
    const dur = (aid && DURATIONS[aid]) ? DURATIONS[aid] : 15;
    const self = this;
    setTimeout(function() {{
      if (self.onended) self.onended(new Event('ended'));
    }}, dur * 1000);
    return Promise.resolve();
  }};
}})();
"""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--autoplay-policy=no-user-gesture-required'])
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            record_video_dir=str(video_tmp),
            record_video_size={'width': 1920, 'height': 1080}
        )
        t0 = time.time()
        page = context.new_page()
        page.add_init_script(audio_mock_js)

        print(f"  Navigating to {PRESENTATION_URL}...")
        page.goto(PRESENTATION_URL, wait_until='networkidle', timeout=30000)

        # Enter presentation mode: hides all chrome using the body class
        # (fullscreen is not requested — headless ignores it anyway)
        page.evaluate("document.body.classList.add('presentation-mode')")

        print("  Starting presentation (clicking overlay)...")
        page.click('#start-overlay')
        startup_delay = time.time() - t0
        print(f"  Startup delay (recording offset): {startup_delay:.2f}s")

        print(f"  Recording {total_wait_seconds:.0f}s ({total_wait_seconds/60:.1f} min)...")
        # Poll every 10s and print progress
        elapsed = 0
        interval = 10
        while elapsed < total_wait_seconds:
            time.sleep(min(interval, total_wait_seconds - elapsed))
            elapsed += interval
            pct = min(elapsed / total_wait_seconds * 100, 100)
            print(f"  ... {elapsed:.0f}s / {total_wait_seconds:.0f}s ({pct:.0f}%)")

        print("  Closing browser (flushing video)...")
        page.close()
        context.close()
        browser.close()

    # Find the recorded webm
    webms = sorted(video_tmp.glob('*.webm'), key=os.path.getmtime, reverse=True)
    if not webms:
        raise RuntimeError(f"No .webm found in {video_tmp}")
    return webms[0], startup_delay


def prepend_silence(audio_path, silence_seconds):
    """Prepend N seconds of silence to an audio file so it aligns with the video."""
    silence_path = EXPORT_DIR / 'silence.mp3'
    subprocess.run([
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100',
        '-t', f'{silence_seconds:.3f}',
        '-q:a', '2',
        str(silence_path)
    ], check=True, capture_output=True)

    concat_txt = EXPORT_DIR / 'narration_offset_concat.txt'
    with open(concat_txt, 'w') as f:
        f.write(f"file '{str(silence_path).replace(chr(92), '/')}'\n")
        f.write(f"file '{str(audio_path).replace(chr(92), '/')}'\n")

    out = EXPORT_DIR / 'narration_offset.mp3'
    subprocess.run([
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
        '-i', str(concat_txt), '-c', 'copy', str(out)
    ], check=True, capture_output=True)
    print(f"  Prepended {silence_seconds:.2f}s silence -> {out.name}")
    return out


def mux(video_path, audio_path):
    """Mux silent video + narration audio -> final MP4."""
    out = EXPORT_DIR / 'presentation.mp4'
    subprocess.run([
        'ffmpeg', '-y',
        '-i', str(video_path),
        '-i', str(audio_path),
        '-c:v', 'h264_mf', '-b:v', '10M',
        '-c:a', 'aac', '-b:a', '192k',
        '-map', '0:v:0', '-map', '1:a:0',
        '-shortest',
        str(out)
    ], check=True)
    size_mb = out.stat().st_size / 1024 / 1024
    print(f"  Muxed video -> {out.name} ({size_mb:.1f} MB)")
    return out


def burn_captions(video_path, srt_path):
    """Burn SRT subtitles into video frames -> YouTube-ready MP4.
    Uses imageio_ffmpeg's bundled binary which includes libass/libx264."""
    import imageio_ffmpeg
    out = EXPORT_DIR / 'presentation_final.mp4'
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    srt_escaped = str(srt_path).replace('\\', '/').replace(':', '\\:')
    style = 'FontName=Arial,FontSize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2,Shadow=1,Alignment=2'
    subprocess.run([
        ff, '-y',
        '-i', str(video_path),
        '-vf', f"subtitles='{srt_escaped}':force_style='{style}'",
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '20',
        '-c:a', 'copy',
        str(out)
    ], check=True)
    size_mb = out.stat().st_size / 1024 / 1024
    print(f"  Captioned video -> {out.name} ({size_mb:.1f} MB)")
    return out


def main():
    EXPORT_DIR.mkdir(exist_ok=True)

    print("\n=== presentation.html -> YouTube Export ===\n")

    print("Step 1: Audio durations")
    durations = get_audio_durations()

    print("\nStep 2: Concatenate narration audio")
    audio_path = build_narration_audio(durations)

    # Compute total recording duration
    total_audio = sum(
        durations.get(aid, 30.0)
        for i, aid in enumerate(AUDIO_IDS)
        if i not in SKIPPED_SCENES
    )
    total_wait = total_audio + IA_VIDEO_EXTRA_SECONDS + END_BUFFER
    print(f"\n  Total presentation duration: {total_audio:.0f}s audio + {IA_VIDEO_EXTRA_SECONDS}s IA cards + {END_BUFFER}s buffer = {total_wait:.0f}s")

    print("\nStep 3: Check serve.py")
    serve_proc = None
    if is_serve_running():
        print("  serve.py already running on :8500 OK")
    else:
        serve_proc = start_serve()
        print("  serve.py started OK")

    try:
        print("\nStep 4: Record video (Playwright headless, presentation mode)")
        video_path, startup_delay = record_video(durations, total_wait)
        print(f"  Raw recording -> {video_path.name}")

        print(f"\nStep 5: Offset audio by {startup_delay:.2f}s (prepend silence)")
        offset_audio_path = prepend_silence(audio_path, startup_delay)

        print(f"\nStep 6: Generate SRT captions (offset +{startup_delay:.2f}s)")
        srt_path = gen_srt(durations, time_offset=startup_delay)

        print("\nStep 7: Mux video + offset audio -> MP4")
        muxed_path = mux(video_path, offset_audio_path)

        print("\nStep 8: Burn captions into video")
        final_path = burn_captions(muxed_path, srt_path)
    finally:
        if serve_proc:
            serve_proc.terminate()

    print("\n=== Export complete ===")
    print(f"  export/presentation_final.mp4  <- upload to YouTube (captions baked in)")


if __name__ == '__main__':
    main()
