#!/usr/bin/env python3
"""Builds the explainer: narration audio, then index.html from src/template.html.

    python3 build.py            # voices any changed sentence, writes assets/vo.wav and index.html
    npx hyperframes render -o explainer.mp4

Each scene is a list of sentences. Each sentence is one beat: in src/template.html an element
with data-beat="2" appears when the scene's third sentence starts. Change a sentence here,
run build.py, and the timing follows.
"""
import hashlib
import json
import os
import re
import subprocess
import wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
VOICE = "af_heart"
SPEED = 1.0
LEAD, GAP, TAIL = 0.5, 0.35, 0.8        # seconds: before a scene's first line, between lines, after the last
PY = os.path.expanduser("~/.cache/hyperframes/tts-venv/bin/python")

SCENES = [
    ("s1", [
        "Your agent made a mistake last week, so you edited its instructions.",
        "Then it made another one, and you edited them again.",
        "You are still the one fixing it.",
        "This project hands that job to a second agent, and checks its work with plain code.",
    ]),
    ("s2", [
        "The first agent does one job.",
        "It reads the links you saved this week,",
        "and writes a short brief in three parts: what changed, who disagrees, and what to do.",
    ]),
    ("s3", [
        "How do you know a brief is good? A month later, you do.",
        "So you label every saved link: acted on it, should have, or noise.",
        "A brief earns a point for each link that mattered, and loses half a point for each piece of noise it called important.",
        "Citing everything does not pay.",
    ]),
    ("s4", [
        "The project is three folders.",
        "Harness holds the agent's setup: its instructions, its notes on your sources, and its tools.",
        "Verifier holds your labels and the scoring code. No agent may read it.",
        "Optimizer holds the second agent. It reads the first one's mistakes, and edits the harness.",
    ]),
    ("s5", [
        "Each round is a short loop.",
        "Only two steps call a model: writing the briefs, and proposing one change with a reason.",
        "Everything else is plain code: scoring, checking the change stayed inside its walls, and keeping it only if the score went up.",
        "If it didn't, git reverts it.",
    ]),
    ("s6", [
        "One week of labels stays locked.",
        "No agent sees it until the very end.",
        "If that week improves too, the harness learned how you decide.",
        "If only the weeks it saw improve, it memorised your past.",
    ]),
    ("s7", [
        "To rehearse, the repo ships a made-up month: a hundred links, and eight decisions.",
        "The reader uses Kiln, Orchard and Postgres. Nothing tells the agent that.",
        "And every week hides the same five traps.",
        "Urgent news about a tool they don't use.",
        "A newsletter recap of a changelog.",
        "A dull title hiding a breaking change.",
        "A thread with real data in it.",
        "And a famous name with nothing to say to them.",
    ]),
    ("s8", [
        "One run is a coin flip.",
        "The same setup scored point four six on one run, and point eight nine on another, on the same week.",
        "So every week runs three times, and the score is the average.",
    ]),
    ("s9", [
        "Here is a real run on the sample.",
        "It started at point seven four.",
        "Round one told the agent to fetch every link. It then cited everything. The score fell to point five, and the change was reverted.",
        "Round two worked out which tools the reader uses. Point nine three. Kept.",
        "Rounds three and four: measured findings count as news, and cite the changelog, not the recap.",
        "Point nine nine, on the weeks it could see.",
    ]),
    ("s10", [
        "Then week four opened, once.",
        "The first setup scored point six seven on it. The final setup scored point nine five.",
        "It learned. Partly by design, though: week four repeats the same tools. Your own month is the real test.",
    ]),
    ("s11", [
        "To check all of this yourself, go in three passes.",
        "First, read the recorded run. It costs nothing.",
        "Second, run it live in a separate worktree. About four dollars, and twenty minutes.",
        "Third, try to break it. Open the hidden week twice, or ask the optimizer to loosen a permission.",
        "Start with pass one.",
    ]),
]


def voice(text, out):
    """One sentence to a wav, skipped when the text has not changed."""
    stamp = out.with_suffix(".txt")
    key = hashlib.sha1(f"{VOICE}|{SPEED}|{text}".encode()).hexdigest()
    if out.exists() and stamp.exists() and stamp.read_text() == key:
        return
    subprocess.run(["hyperframes", "tts", text, "-v", VOICE, "-s", str(SPEED), "-o", str(out)],
                   check=True, capture_output=True, env={**os.environ, "HYPERFRAMES_PYTHON": PY})
    stamp.write_text(key)


def main():
    vo = HERE / "assets" / "vo"
    vo.mkdir(parents=True, exist_ok=True)
    frames, rate, t = [], None, 0.0
    scenes, beats, captions = {}, {}, []

    def silence(seconds):
        frames.append(b"\x00\x00" * int(seconds * rate))

    for sid, lines in SCENES:
        start = t
        beats[sid] = []
        for k, text in enumerate(lines):
            path = vo / f"{sid}-{k}.wav"
            voice(text, path)
            with wave.open(str(path)) as w:
                rate = rate or w.getframerate()
                data = w.readframes(w.getnframes())
                length = w.getnframes() / w.getframerate()
            pad = LEAD if k == 0 else GAP
            if not frames:
                frames.append(b"")
            silence(pad)
            t += pad
            beats[sid].append(round(t, 3))
            captions.append((round(t, 3), round(length, 3), text))
            frames.append(data)
            t += length
        silence(TAIL)
        t += TAIL
        scenes[sid] = (round(start, 3), round(t - start, 3))
        print(f"{sid}: {t - start:5.1f}s")

    with wave.open(str(HERE / "assets" / "vo.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(b"".join(frames))
    total = round(t, 3)

    html = (HERE / "src" / "template.html").read_text()
    html = html.replace("__TOTAL__", str(total))
    for sid, (s, d) in scenes.items():
        html, n = re.subn(rf'id="{sid}"', f'id="{sid}" data-start="{s}" data-duration="{d}"', html, count=1)
        assert n, f"src/template.html has no scene {sid}"
    caps = "\n".join(
        f'      <div id="cap-{i + 1}" class="cap clip" data-start="{s}" data-duration="{d}"><span>{text}</span></div>'
        for i, (s, d, text) in enumerate(captions))
    html = html.replace("<!--CAPTIONS-->", caps)
    html = html.replace("/*TIMING*/", "const SCENES = " + json.dumps(scenes) + ";\n"
                        "      const BEATS = " + json.dumps(beats) + ";")
    (HERE / "index.html").write_text(html)
    print(f"total {total:.1f}s ({total / 60:.1f} min) -> index.html, assets/vo.wav")


if __name__ == "__main__":
    main()
