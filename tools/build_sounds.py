#!/usr/bin/env python3
"""Synthesise Manna's feedback sounds ("Leise": soft, short sine tones with a little room).

Usage: python3 tools/build_sounds.py   (needs numpy + scipy)
Output (44.1 kHz mono 16-bit WAV): app/src/main/res/raw/chime_{ok,soft,done}.wav
(the web app copies them from there at build time, see web/scripts/copy-assets.mjs)
  chime_ok   = correct      (A5)
  chime_soft = try again    (D5, a bit softer and shorter – never punishing)
  chime_done = section done (D5 → A5, rising fifth)
Playback volumes are set in code (Feedback.kt / feedback.ts).
"""
import pathlib
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt, fftconvolve

SR = 44100
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'app/src/main/res/raw'


def note(name):
    n = {'C': -9, 'D': -7, 'E': -5, 'F': -4, 'G': -2, 'A': 0, 'B': 2}[name[0]]
    return 440 * 2 ** ((n + (int(name[1:]) - 4) * 12) / 12)


def t_(dur):
    return np.arange(int(dur * SR)) / SR


def env(t, attack, tau):
    a = np.clip(t / attack, 0, 1)
    return (0.5 - 0.5 * np.cos(np.pi * a)) * np.exp(-t / tau)  # raised-cosine attack: no click


def soft_sine(f, dur, attack, tau):
    t = t_(dur)
    return (np.sin(2 * np.pi * f * t) + 0.08 * np.sin(4 * np.pi * f * t)) * env(t, attack, tau)


def place(parts, total):
    out = np.zeros(int(total * SR))
    for start, sig in parts:
        i = int(start * SR)
        j = min(len(out), i + len(sig))
        out[i:j] += sig[: j - i]
    return out


def reverb(x, size=0.9, mix=0.15, damp=4000, predelay=0.012, seed=7):
    n = int(size * SR)
    t = np.arange(n) / SR
    ir = np.random.default_rng(seed).standard_normal(n) * np.exp(-t / (size / 6.5))
    ir = sosfilt(butter(2, damp, 'low', fs=SR, output='sos'), ir)
    ir[: int(predelay * SR)] = 0
    ir /= np.sqrt((ir ** 2).sum())
    wet = np.concatenate([fftconvolve(x, ir), [0.0]])[: len(x) + n]
    dry = np.concatenate([x, np.zeros(n)])
    return dry * (1 - mix) + wet * mix * 2.2


def finish(x, peak=0.6, tail_fade=0.08):
    last = np.nonzero(np.abs(x) > np.abs(x).max() * 0.004)[0][-1] + 1  # trim silent tail
    x = x[: max(last, int(0.1 * SR))]
    f = int(tail_fade * SR)
    x[-f:] *= np.linspace(1, 0, f) ** 2
    x = sosfilt(butter(2, 60, 'high', fs=SR, output='sos'), x)
    return x / np.abs(x).max() * peak


SOUNDS = {
    'chime_ok': place([(0, soft_sine(note('A5'), 0.4, 0.01, 0.1))], 0.5),
    'chime_soft': place([(0, soft_sine(note('D5'), 0.35, 0.015, 0.08) * 0.8)], 0.45),
    'chime_done': place([(0, soft_sine(note('D5'), 0.5, 0.01, 0.15)),
                         (0.12, soft_sine(note('A5'), 0.6, 0.01, 0.2))], 0.8),
}

if __name__ == '__main__':
    for name, sig in SOUNDS.items():
        data = (np.clip(finish(reverb(sig)), -1, 1) * 32767).astype(np.int16)
        wavfile.write(OUT / f'{name}.wav', SR, data)
        print(f'{name}: {len(data) / SR:.2f} s')
