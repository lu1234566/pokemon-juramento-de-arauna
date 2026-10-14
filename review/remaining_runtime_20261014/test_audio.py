"""Capture actual engine output; signal checks do not certify musical taste."""
import ctypes as C
import wave
import numpy as np
from runtime import *

LIB.captureaudio.argtypes = [C.c_char_p, C.c_int]
boot()
fixture()
results = []

def capture(name, frame_count):
    path = Q / (name + ".pcm")
    samples = LIB.captureaudio(str(path).encode(), frame_count)
    data = path.read_bytes()
    values = np.frombuffer(data, dtype="<i2").astype(np.float64)
    assert samples and values.size == samples * 2
    peak = int(np.max(np.abs(values)))
    rms = float(np.sqrt(np.mean(values ** 2)))
    assert rms > 1 and peak > 16, (name, "silent output", rms)
    assert not np.any(np.abs(values) >= 32767), (name, "clipped output")
    with wave.open(str(Q / (name + ".wav")), "wb") as out:
        out.setnchannels(2)
        out.setsampwidth(2)
        out.setframerate(24000)
        out.writeframes(data)
    path.unlink()
    return {"clip": name + ".wav", "frames": frame_count, "samples": samples, "sample_rate": 24000, "peak": peak, "rms": round(rms, 2), "clipped_samples": 0}

for map_name, x, y in (("LittlerootTown", 10, 8), ("Route101", 8, 13), ("GraniteCave_StevensRoom", 7, 9), ("MtPyre_Summit", 9, 15), ("EverGrandeCity_PhoebesRoom", 6, 10), ("EverGrandeCity_ChampionsRoom", 6, 10)):
    warp(map_name, x, y)
    actual_music = call("GetCurrentMapMusic")
    expected_music = constant(json.loads((R / "data/maps" / map_name / "map.json").read_text())["music"])
    assert actual_music == expected_music, (map_name, actual_music, expected_music)
    snapshot("audio_context_" + map_name)
    results.append(capture("music_" + map_name, 360) | {"map": map_name, "song_id": actual_music})

warp("LittlerootTown", 10, 8)
for species in ("SPECIES_TREECKO", "SPECIES_TORCHIC", "SPECIES_MUDKIP", "SPECIES_DEOXYS"):
    music = call("GetCurrentMapMusic")
    call("PlayCry_Script", constant(species), constant("CRY_MODE_ENCOUNTER"))
    results.append(capture("cry_" + species, 180) | {"species": species, "cry_playing_after_clip": bool(call("IsCryPlaying")), "music_after": call("GetCurrentMapMusic")})
    assert not call("IsCryPlaying"), species
    assert call("GetCurrentMapMusic") == music

call("PlayFanfare", constant("MUS_OBTAIN_ITEM"))
results.append(capture("fanfare_item", 240))
assert call("IsFanfareTaskInactive")
(Q / "audio_receipt.json").write_text(json.dumps(metadata() | {"cases": results, "scope": "map routing, non-silence, clipping, cry/fanfare completion; no qualified auditory/artistic approval"}, indent=2) + "\n")
print("Audio signal and contextual engine routing:", len(results), "PASS", flush=True)
