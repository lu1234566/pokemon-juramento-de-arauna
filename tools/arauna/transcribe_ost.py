#!/usr/bin/env python3
"""Best-effort DSP transcription of an instrumental MP3 into a GBA-friendly
multi-track MIDI (melody + bass + chord pad + light percussion).

This is intentionally crude: polyphonic produced audio cannot be transcribed
faithfully. It extracts the dominant pitch contour (melody), the low-band
fundamental (bass), a per-beat chroma chord, and onset-driven percussion, then
quantises to a tempo grid. The result is a *starting point* for manual edit,
not a faithful arrangement.
"""
from __future__ import annotations
import subprocess, struct, sys, math
import numpy as np

SR = 22050
NFFT = 2048
HOP = 512

def decode(path):
    p = subprocess.run(["ffmpeg","-v","error","-i",path,"-ac","1","-ar",str(SR),
                        "-f","f32le","-"], capture_output=True)
    x = np.frombuffer(p.stdout, dtype="<f4").astype(np.float64)
    if x.size == 0:
        raise SystemExit(f"decode failed: {path}\n{p.stderr.decode()[:300]}")
    return x

def stft_mag(x):
    win = np.hanning(NFFT)
    n = 1 + (len(x)-NFFT)//HOP
    n = max(n, 1)
    S = np.empty((NFFT//2+1, n))
    for i in range(n):
        fr = x[i*HOP:i*HOP+NFFT]
        if len(fr) < NFFT: fr = np.pad(fr,(0,NFFT-len(fr)))
        S[:,i] = np.abs(np.fft.rfft(fr*win))
    return S

def freqs():
    return np.fft.rfftfreq(NFFT, 1/SR)

def hz_to_midi(f):
    return 69 + 12*np.log2(np.maximum(f,1e-6)/440.0)

def detect_tempo(x):
    # spectral flux onset envelope
    S = stft_mag(x)
    flux = np.maximum(0, np.diff(S, axis=1)).sum(0)
    flux = flux - flux.mean()
    if flux.std() > 0: flux /= flux.std()
    fps = SR/HOP
    # autocorrelation over lag range for 60..190 BPM
    ac = np.correlate(flux, flux, "full")[len(flux)-1:]
    best_bpm, best_val = 120, -1
    for bpm in range(60,191):
        lag = int(round(60.0/bpm*fps))
        if lag < len(ac) and ac[lag] > best_val:
            best_val, best_bpm = ac[lag], bpm
    return best_bpm, flux, fps

def band_pitch(S, fr, lo, hi, harmonics=1):
    idx = np.where((fr>=lo)&(fr<=hi))[0]
    if len(idx)==0: return None,0
    sub = S[idx,:]
    out_m = np.zeros(S.shape[1]); out_c = np.zeros(S.shape[1])
    for t in range(S.shape[1]):
        col = sub[:,t]
        if harmonics>1:
            # harmonic product spectrum within band via downsampled multiply
            hps = col.copy()
            for h in range(2,harmonics+1):
                ds = col[::h]
                hps[:len(ds)] *= ds
            col = hps
        k = int(np.argmax(col))
        out_m[t] = fr[idx[k]]; out_c[t] = col[k]
    return out_m, out_c

def median_filt(a, k=5):
    if k<3: return a
    pad=k//2; ap=np.pad(a,(pad,pad),mode="edge")
    return np.array([np.median(ap[i:i+k]) for i in range(len(a))])

def contour_to_notes(midi_track, conf, fps, bpm, conf_gate, min_notes=1,
                     lo_note=36, hi_note=96):
    """Quantise a per-frame midi-pitch contour into (start_beat,dur_beat,note,vel)."""
    q = np.round(midi_track).astype(int)
    thr = conf_gate*np.median(conf[conf>0]) if np.any(conf>0) else 0
    voiced = (conf>thr) & (q>=lo_note) & (q<=hi_note)
    notes=[]
    i=0; N=len(q)
    beat = bpm/60.0  # beats per second
    while i<N:
        if not voiced[i]:
            i+=1; continue
        j=i
        while j<N and voiced[j] and q[j]==q[i]:
            j+=1
        t0=i/fps*beat; t1=j/fps*beat
        vel=int(np.clip(40+60*(conf[i:j].mean()/(thr+1e-9)),40,110))
        notes.append([t0,t1-t0,int(q[i]),vel])
        i=j
    # snap to 16th grid, drop ultra-short
    grid=0.25
    out=[]
    for t0,d,nn,v in notes:
        t0=round(t0/grid)*grid; d=max(grid,round(d/grid)*grid)
        out.append([t0,d,nn,v])
    return out

CHORD_TEMPLATES=[]
for root in range(12):
    maj=[root,(root+4)%12,(root+7)%12]
    minr=[root,(root+3)%12,(root+7)%12]
    CHORD_TEMPLATES.append((root,"maj",maj))
    CHORD_TEMPLATES.append((root,"min",minr))

def chroma_chords(S, fr, fps, bpm):
    beat=bpm/60.0
    frames_per_beat=fps/beat
    chroma=np.zeros((12,S.shape[1]))
    midi=hz_to_midi(fr)
    valid=(fr>55)&(fr<2000)
    for t in range(S.shape[1]):
        col=S[:,t]
        for k in np.where(valid)[0]:
            chroma[int(round(midi[k]))%12,t]+=col[k]
    # aggregate per beat
    nbeats=int(S.shape[1]/frames_per_beat)
    chords=[]
    for b in range(nbeats):
        a=int(b*frames_per_beat); z=int((b+1)*frames_per_beat)
        v=chroma[:,a:z].sum(1)
        if v.sum()<=0: chords.append(None); continue
        v=v/np.linalg.norm(v)
        best=None;bv=-1
        for root,q,tones in CHORD_TEMPLATES:
            tv=np.zeros(12); tv[tones]=1; tv/=np.linalg.norm(tv)
            s=float(v@tv)
            if s>bv: bv=s;best=(root,tones)
        chords.append(best)
    return chords  # per beat

def write_midi(path, bpm, tracks, tpqn=480, loop=None):
    """tracks: list of (name, program, channel, notes[start_beat,dur_beat,note,vel]).

    loop: (start_beat, end_beat). mid2agb reads MIDI text events "[" and "]" as
    loop-begin / loop-end, emitting a GOTO so the song repeats forever instead
    of ending on FINE. Every BGM track here needs that."""
    def vlq(n):
        b=[n&0x7f]; n>>=7
        while n: b.insert(0,(n&0x7f)|0x80); n>>=7
        return bytes(b)
    def tk(events):
        # events: list of (abs_tick, bytes)
        events.sort(key=lambda e:e[0])
        out=b""; last=0
        for t,data in events:
            out+=vlq(t-last)+data; last=t
        out+=vlq(0)+b"\xff\x2f\x00"
        return b"MTrk"+struct.pack(">I",len(out))+out
    chunks=[]
    # Conductor track. mid2agb reads this one track's events once and merges
    # them into every AGB track, so the loop markers must live HERE -- markers
    # placed on the instrument tracks are never seen.
    mpqn=int(60_000_000/bpm)
    tempo=[(0,b"\xff\x51\x03"+struct.pack(">I",mpqn)[1:])]
    if loop is not None:
        ls,le=loop
        tempo.append((int(round(ls*tpqn)), b"\xff\x01"+vlq(1)+b"["))
        tempo.append((int(round(le*tpqn)), b"\xff\x01"+vlq(1)+b"]"))
    chunks.append(tk(tempo))
    for name,program,ch,notes in tracks:
        ev=[(0,b"\xff\x03"+vlq(len(name))+name.encode())]
        ev.append((0,bytes([0xC0|ch,program&0x7f])))
        for start,dur,note,vel in notes:
            s=int(round(start*tpqn)); d=max(1,int(round(dur*tpqn)))
            ev.append((s,bytes([0x90|ch,note&0x7f,vel&0x7f])))
            ev.append((s+d,bytes([0x80|ch,note&0x7f,0])))
        chunks.append(tk(ev))
    hdr=b"MThd"+struct.pack(">IHHH",6,1,len(chunks),tpqn)
    open(path,"wb").write(hdr+b"".join(chunks))

def transcribe(path, out_mid, want_perc=True):
    x=decode(path)
    x/=(np.abs(x).max()+1e-9)
    bpm,flux,fps=detect_tempo(x)
    S=stft_mag(x); fr=freqs()
    mel,melc=band_pitch(S,fr,160,1800,harmonics=3)
    bas,basc=band_pitch(S,fr,45,280,harmonics=1)
    mel=median_filt(hz_to_midi(mel),7); bas=median_filt(hz_to_midi(bas),7)
    mnotes=contour_to_notes(mel,melc,fps,bpm,conf_gate=1.2,lo_note=52,hi_note=88)
    bnotes=contour_to_notes(bas,basc,fps,bpm,conf_gate=1.0,lo_note=28,hi_note=55)
    # chords -> pad notes (root+third+fifth, one octave), each lasts 1 beat
    chords=chroma_chords(S,fr,fps,bpm)
    cnotes=[]
    for b,ch in enumerate(chords):
        if ch is None: continue
        root,tones=ch
        for tn in tones:
            note=48+tn
            cnotes.append([float(b),1.0,note,46])
    # program indices into voicegroup_arauna_ost:
    #   0 drumset, 1 piano (warm harmony), 2 & 3 square leads (PSG, cheap)
    tracks=[("melody",2,0,mnotes),     # square lead
            ("bass",3,1,bnotes),       # square, low register
            ("chords",1,2,cnotes)]     # piano-ish pad for harmony
    if want_perc:
        # simple kick on strong beats from flux peaks
        beat=bpm/60.0; spb=fps/beat
        pk=[]
        for b in range(int(len(flux)/spb)):
            a=int(b*spb); z=int((b+1)*spb)
            if z<=a: continue
            seg=flux[a:z]
            if seg.max()>1.0:
                pk.append([float(b),0.25,36,90])  # note ignored on ch9
        tracks.append(("perc",0,9,pk))
    # Loop points, in beats, snapped to whole bars (4/4) so the seam lands on a
    # downbeat. Short masters were written as gameplay loops: repeat entire.
    # Longer ones keep their opening as a one-shot intro and loop the body.
    dur=len(x)/SR
    total_beats=dur*bpm/60.0
    end=math.floor(total_beats/4)*4
    if end<4: end=max(4.0,total_beats)
    start=0.0 if dur<45 else math.floor((total_beats*0.25)/4)*4
    if start>=end: start=0.0
    write_midi(out_mid,bpm,tracks,loop=(start,end))
    stats=dict(bpm=bpm,dur=round(dur,1),loop_start=start,loop_end=end,mel=len(mnotes),bass=len(bnotes),
               chord_beats=sum(1 for c in chords if c),perc=len(tracks[3][3]) if want_perc else 0,
               rms=float(np.sqrt((x**2).mean())))
    return stats

if __name__=="__main__":
    import json
    inp,outp=sys.argv[1],sys.argv[2]
    print(json.dumps(transcribe(inp,outp)))
