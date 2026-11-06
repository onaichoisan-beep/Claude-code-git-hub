# Audio Lab

Tools to pull audio out of reference videos, learn how it is built, and
generate narration voices for new videos in the 3D realistic style
(`../video-playbook/3D_REALISTIC_STYLE.md`).

## Setup
```bash
./setup.sh            # venv at /opt/alab, tools + ~1 GB of offline voice models
P=/opt/alab/bin/python
```

## Pipeline
| Step | Command | Output |
|---|---|---|
| 1. Extract audio | `ffmpeg -i video.mp4 -vn -ac 1 -ar 44100 reference_audio/name.wav` | wav |
| 2. Transcribe + word timings + loudness | `$P scripts/analyze_audio.py reference_audio/*.wav > analysis.json` | `analysis.json` |
| 3. Split voice / background | `$P -m demucs --two-stems=vocals -n htdemucs -o stems reference_audio/*.wav` | `stems/htdemucs/<name>/{vocals,no_vocals}.wav` |
| 4. Profile clean stems | `$P scripts/stem_profile.py` | `stem_profile.json` |
| 5. Score TTS voices against the narrator | `$P scripts/voice_shootout.py` | `voice_scores.json`, `samples/` |
| 6. Generate narration | `$P scripts/tts.py ...` (see below) | wav |

## What the reference audio taught us
Measured on the clean Demucs voice stem:

| | Ear hack | Store riddle | DIY projector |
|---|---|---|---|
| Narration | yes | yes | **none (music only)** |
| Pace | 180 wpm (3.0 words/s) | 141 wpm | — |
| First word | 0.00 s | 0.00 s | — |
| Narrator pitch (median) | 164 Hz | 167 Hz | — |
| Pitch spread (p10–p90) | 16 semitones | 20 semitones | — |
| Voice loudness | −17.7 LUFS | −17.7 LUFS | — |
| Background vs voice | −20.6 dB | −25.1 dB | music at −27 LUFS |
| Long pauses (>0.4 s) | 1 | 5 (around the riddle question) | — |

Rules to copy:
- **The voice starts on frame 1.** No intro, no music lead-in.
- **The voice does almost all the work.** The background (soft SFX hits and a
  faint bed) sits 20–25 dB under the voice. Mix voice ≈ −17 LUFS, bed ≈ −40 LUFS.
- **Fast, very expressive delivery:** 140–180 wpm, and the pitch swings more
  than an octave. Flat TTS sounds wrong; push rate and use expressive voices.
- **Pause only on purpose.** Riddles pause before and after the question;
  hacks run straight through.
- **DIY/process videos have no voice at all,** just an upbeat ~130 BPM track
  with foley.

## Voices
`tts.py` drives three engines:

```bash
# Edge (online, most natural, Microsoft neural voices, free)
$P scripts/tts.py --engine edge --voice en-US-GuyNeural --rate +2% --pitch +8Hz --text-file script.txt -o vo.wav
# Kokoro (offline, 54 voices, good quality)
$P scripts/tts.py --engine kokoro --voice am_eric --speed 0.85 --text-file script.txt -o vo.wav
# Piper (offline, very fast, 7 English voices downloaded)
$P scripts/tts.py --engine piper --voice en_US-ryan-high --speed 1.1 --text-file script.txt -o vo.wav
$P scripts/tts.py --list edge|kokoro|piper
```

Tuned presets (ear-hack script, in `presets/`):

| Preset | Command flags | Pitch | Notes |
|---|---|---|---|
| **A_guy_energetic** (default) | edge `en-US-GuyNeural --rate +2% --pitch +8Hz` | 164 Hz | pitch matches the narrator exactly |
| B_andrew_bright | edge `en-US-AndrewNeural --rate +2% --pitch +30Hz` | 132 Hz | warmer, younger male |
| C_emma_female | edge `en-US-EmmaNeural` | 175 Hz | female option |
| D_kokoro_eric_offline | kokoro `am_eric --speed 0.85` | 154 Hz | works with no internet |

Full ranking of 26 voices: `voice_scores.json` (lower score = closer to the
narrator on pitch, expressiveness and pace). The score measures numbers, not
how a voice sounds, so listen to the presets before choosing.

Don't clone the real narrator's voice from these stems: it's someone else's
voice and content. Use the stock voices above.
