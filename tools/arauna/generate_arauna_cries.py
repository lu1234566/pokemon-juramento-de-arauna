#!/usr/bin/env python3
"""Synthesize a distinct cry for every Arauna Fakemon.

Each of the 386 Arauna species keeps the ``.cryId`` slot it already occupies in
``src/data/pokemon/species_info/arauna_dex.h``; this tool only regenerates the
underlying ``.wav`` sample for that slot, so the cry table, the cry enum and the
per-species ``.cryId`` never change. The build converts the ``.wav`` to a GBA
sample with ``WAV2AGB`` exactly as before.

The output is deterministic: the waveform is seeded from the Dex number, so a
regenerate always produces byte-identical files. Character comes from the
species' primary type (pitch band, timbre, vibrato, noise) and its size
(heavier / taller species sound lower).

Usage:
    python3 tools/arauna/generate_arauna_cries.py            # write all cries
    python3 tools/arauna/generate_arauna_cries.py --check    # verify only
"""

from __future__ import annotations

import argparse
import math
import re
import struct
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEX = ROOT / "src/data/pokemon/species_info/arauna_dex.h"
CRY_DIR = ROOT / "sound/direct_sound_samples/cries"

SAMPLE_RATE = 10512  # matches the vanilla Emerald cry samples
DEX_SIZE = 386

# Per-type sonic profile.
#   center      : base pitch centre in Hz before size/seed variation
#   spread      : +/- fractional pitch jitter drawn per species
#   partials    : (harmonic multiple, amplitude) pairs summed into the tone
#   noise       : fraction of breathy noise mixed in (0..1)
#   vib_hz      : vibrato rate in Hz
#   vib_depth   : vibrato depth as a fraction of the pitch
#   dur         : (min, max) duration in seconds
TYPE_PROFILE = {
    "TYPE_NORMAL":   dict(center=430, spread=0.28, partials=[(1,1.0),(2,0.45),(3,0.20)], noise=0.06, vib_hz=6,  vib_depth=0.010, dur=(0.34,0.50)),
    "TYPE_FIRE":     dict(center=470, spread=0.30, partials=[(1,1.0),(2,0.55),(3,0.30),(5,0.15)], noise=0.16, vib_hz=7, vib_depth=0.012, dur=(0.36,0.52)),
    "TYPE_WATER":    dict(center=400, spread=0.26, partials=[(1,1.0),(2,0.40),(4,0.18)], noise=0.05, vib_hz=11, vib_depth=0.030, dur=(0.40,0.58)),
    "TYPE_GRASS":    dict(center=380, spread=0.24, partials=[(1,1.0),(2,0.35),(3,0.15)], noise=0.05, vib_hz=5,  vib_depth=0.014, dur=(0.38,0.54)),
    "TYPE_ELECTRIC": dict(center=560, spread=0.30, partials=[(1,1.0),(2,0.60),(3,0.40),(4,0.25)], noise=0.10, vib_hz=16, vib_depth=0.022, dur=(0.30,0.44)),
    "TYPE_ICE":      dict(center=620, spread=0.28, partials=[(1,1.0),(3,0.45),(5,0.22)], noise=0.04, vib_hz=8,  vib_depth=0.016, dur=(0.34,0.50)),
    "TYPE_FIGHTING": dict(center=360, spread=0.24, partials=[(1,1.0),(2,0.55),(3,0.28)], noise=0.10, vib_hz=5,  vib_depth=0.008, dur=(0.28,0.42)),
    "TYPE_POISON":   dict(center=410, spread=0.30, partials=[(1,1.0),(2,0.42),(3,0.24)], noise=0.12, vib_hz=9,  vib_depth=0.026, dur=(0.36,0.52)),
    "TYPE_GROUND":   dict(center=300, spread=0.24, partials=[(1,1.0),(2,0.40),(3,0.18)], noise=0.14, vib_hz=4,  vib_depth=0.010, dur=(0.36,0.52)),
    "TYPE_FLYING":   dict(center=640, spread=0.30, partials=[(1,1.0),(2,0.50),(3,0.28)], noise=0.06, vib_hz=13, vib_depth=0.020, dur=(0.28,0.42)),
    "TYPE_PSYCHIC":  dict(center=520, spread=0.26, partials=[(1,1.0),(2,0.30),(4,0.30),(6,0.16)], noise=0.03, vib_hz=6, vib_depth=0.018, dur=(0.38,0.56)),
    "TYPE_BUG":      dict(center=600, spread=0.30, partials=[(1,1.0),(3,0.55),(5,0.35),(7,0.20)], noise=0.14, vib_hz=22, vib_depth=0.018, dur=(0.26,0.40)),
    "TYPE_ROCK":     dict(center=290, spread=0.22, partials=[(1,1.0),(2,0.38),(3,0.20)], noise=0.18, vib_hz=4,  vib_depth=0.008, dur=(0.30,0.46)),
    "TYPE_GHOST":    dict(center=350, spread=0.30, partials=[(1,1.0),(2,0.25),(3,0.30)], noise=0.10, vib_hz=7,  vib_depth=0.045, dur=(0.42,0.60)),
    "TYPE_DRAGON":   dict(center=270, spread=0.26, partials=[(1,1.0),(2,0.55),(3,0.32),(4,0.18)], noise=0.16, vib_hz=6, vib_depth=0.014, dur=(0.40,0.58)),
    "TYPE_DARK":     dict(center=320, spread=0.28, partials=[(1,1.0),(2,0.45),(3,0.26)], noise=0.18, vib_hz=5,  vib_depth=0.012, dur=(0.36,0.54)),
    "TYPE_STEEL":    dict(center=500, spread=0.24, partials=[(1,1.0),(2,0.30),(3,0.45),(5,0.28)], noise=0.06, vib_hz=8, vib_depth=0.010, dur=(0.32,0.48)),
    "TYPE_FAIRY":    dict(center=660, spread=0.26, partials=[(1,1.0),(2,0.35),(4,0.24),(6,0.14)], noise=0.03, vib_hz=9, vib_depth=0.020, dur=(0.34,0.50)),
}
DEFAULT_PROFILE = TYPE_PROFILE["TYPE_NORMAL"]

CONTOURS = ("fall", "rise", "rise_fall", "fall_rise", "warble")


class Rng:
    """Tiny deterministic PRNG (SplitMix64) so output never depends on host."""

    def __init__(self, seed: int) -> None:
        self.state = (seed * 0x9E3779B97F4A7C15 + 0x1234567) & 0xFFFFFFFFFFFFFFFF

    def next_u64(self) -> int:
        self.state = (self.state + 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF
        z = self.state
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & 0xFFFFFFFFFFFFFFFF
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & 0xFFFFFFFFFFFFFFFF
        return z ^ (z >> 31)

    def rand(self) -> float:
        return (self.next_u64() >> 11) / float(1 << 53)

    def uniform(self, lo: float, hi: float) -> float:
        return lo + (hi - lo) * self.rand()

    def choice(self, seq):
        return seq[self.next_u64() % len(seq)]


def parse_species() -> list[dict]:
    text = DEX.read_text(encoding="utf-8")
    blocks = re.findall(
        r"\[SPECIES_[A-Z0-9_]+\]\s*=\s*\{(.*?)\n    \},",
        text,
        flags=re.DOTALL,
    )
    species = []
    for block in blocks:
        cry = re.search(r"\.cryId\s*=\s*(CRY_[A-Z0-9_]+)", block)
        types = re.search(r"\.types\s*=\s*MON_TYPES\(([^)]*)\)", block)
        if not cry or not types:
            continue
        type_list = [t.strip() for t in types.group(1).split(",") if t.strip()]
        stats = [
            int(re.search(rf"\.{field}\s*=\s*(\d+)", block).group(1))
            for field in ("baseHP", "baseAttack", "baseDefense",
                          "baseSpeed", "baseSpAttack", "baseSpDefense")
        ]
        weight = re.search(r"\.weight\s*=\s*(\d+)", block)
        height = re.search(r"\.height\s*=\s*(\d+)", block)
        species.append({
            "cryId": cry.group(1),
            "types": type_list,
            "bst": sum(stats),
            "weight": int(weight.group(1)) if weight else 100,
            "height": int(height.group(1)) if height else 10,
        })
    return species


def envelope(i: int, n: int, attack: int, release: int, sustain: float) -> float:
    if i < attack:
        return (i / attack)
    if i > n - release:
        return sustain * ((n - i) / release)
    # gentle exponential settle from 1.0 to the sustain level
    t = (i - attack) / max(1, n - attack - release)
    return sustain + (1.0 - sustain) * math.exp(-3.2 * t)


def pitch_factor(contour: str, t: float, rng_phase: float) -> float:
    if contour == "fall":
        return 1.18 - 0.34 * t
    if contour == "rise":
        return 0.82 + 0.34 * t
    if contour == "rise_fall":
        return 0.86 + 0.30 * math.sin(math.pi * t)
    if contour == "fall_rise":
        return 1.14 - 0.30 * math.sin(math.pi * t)
    # warble
    return 1.0 + 0.06 * math.sin(2 * math.pi * (2.5 * t + rng_phase))


def synth(index: int, sp: dict) -> bytes:
    rng = Rng(index * 2654435761)
    profile = TYPE_PROFILE.get(sp["types"][0], DEFAULT_PROFILE)

    # size lowers pitch: fold weight (hectograms) and height (decimetres)
    size = math.log10(sp["weight"] + 10) + math.log10(sp["height"] + 5)
    size_factor = 1.28 - 0.11 * size            # ~0.7 (huge) .. ~1.15 (tiny)
    size_factor = max(0.62, min(1.22, size_factor))
    bst_factor = 1.0 - (sp["bst"] - 300) / 4000.0  # stronger -> slightly lower

    base = profile["center"] * size_factor * bst_factor
    base *= 1.0 + rng.uniform(-profile["spread"], profile["spread"])
    base = max(150.0, min(1050.0, base))

    duration = rng.uniform(*profile["dur"])
    n = int(SAMPLE_RATE * duration)
    attack = max(8, int(0.012 * SAMPLE_RATE))
    release = max(12, int(0.06 * SAMPLE_RATE))
    sustain = rng.uniform(0.45, 0.68)

    contour = rng.choice(CONTOURS)
    phase0 = rng.rand()
    vib_hz = profile["vib_hz"] * rng.uniform(0.8, 1.25)
    vib_depth = profile["vib_depth"]
    noise_amt = profile["noise"] * rng.uniform(0.7, 1.2)
    detune = rng.uniform(-0.015, 0.015)

    partials = profile["partials"]
    norm = sum(a for _, a in partials)

    # a cheap deterministic noise source
    noise_state = (index * 40503 + 12345) & 0xFFFF

    phase = 0.0
    dt = 1.0 / SAMPLE_RATE
    frames = bytearray(n)
    two_pi = 2 * math.pi
    for i in range(n):
        t = i / n
        vib = 1.0 + vib_depth * math.sin(two_pi * vib_hz * i * dt + phase0 * two_pi)
        freq = base * (1.0 + detune) * pitch_factor(contour, t, phase0) * vib
        phase += two_pi * freq * dt
        sample = 0.0
        for mult, amp in partials:
            sample += amp * math.sin(phase * mult)
        sample /= norm
        if noise_amt:
            noise_state = (noise_state * 1103515245 + 12345) & 0xFFFF
            sample += noise_amt * ((noise_state / 32768.0) - 1.0)
        sample *= envelope(i, n, attack, release, sustain)
        sample = max(-1.0, min(1.0, sample * 0.92))
        frames[i] = int(round(sample * 127)) + 128
    return bytes(frames)


def write_wav(path: Path, data: bytes) -> None:
    with wave.open(str(path), "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(1)
        out.setframerate(SAMPLE_RATE)
        out.writeframes(data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="validate mapping/format without writing audio")
    args = parser.parse_args()

    species = parse_species()
    if len(species) != DEX_SIZE:
        raise SystemExit(f"expected {DEX_SIZE} Arauna species, parsed {len(species)}")

    targets: dict[str, Path] = {}
    for sp in species:
        wav = CRY_DIR / (sp["cryId"][4:].lower() + ".wav")
        if sp["cryId"] in targets:
            raise SystemExit(f"duplicate cryId {sp['cryId']} in Arauna dex")
        targets[sp["cryId"]] = wav
        if args.check and not wav.exists():
            raise SystemExit(f"cry slot missing on disk: {wav}")
    if len(set(targets.values())) != DEX_SIZE:
        raise SystemExit("Arauna cry slots are not unique")

    if args.check:
        print(f"OK: {DEX_SIZE} Arauna cry slots map to unique existing .wav files")
        return 0

    for index, sp in enumerate(species, start=1):
        write_wav(targets[sp["cryId"]], synth(index, sp))
    print(f"generated {DEX_SIZE} Arauna cries "
          f"({SAMPLE_RATE} Hz, 8-bit mono) into {CRY_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
