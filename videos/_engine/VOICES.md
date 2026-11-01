# Voice casting: every character gets a voice that fits

**Default engine (owner, Nov 2026: the edge-tts voices sound robotic): Kokoro-82M** — open source, runs locally,
`python3 scripts/make_voices_kokoro.py .` with `scripts/voices_kokoro.json` = `{speaker: [voice, speed]}` (copy the script
from `videos/_engine/`). Best voices (Kokoro's own grades): narrator `af_heart` (A) at speed 1.08-1.12; women `af_bella` (A-),
`af_nicole` (B-, soft/whispery), `bf_emma` (B-, British); men `am_fenrir` / `am_michael` / `am_puck` (C+), `bm_george` /
`bm_fable` (C, British). Don't speed narration past ~1.15 and don't squeeze natural pauses below 0.45 s. Example:
`videos/memory-loss-except-you`. edge-tts (below) is the fallback, e.g. for Indian-accented characters (`hi-IN-MadhurNeural`).

# (edge-tts casting, fallback)

House rule: **narrate everything.** Each speaking character gets their **own** voice, matched to who they are
(age, gender, culture, personality, size). The narrator matches the story's mood and setting. Never reuse one
voice for two characters in the same video.

Engine: Microsoft neural voices via `edge-tts` (`scripts/make_voices.py`, free, with word timings for the
synced captions). In this container run it with `SSL_CERT_FILE=/root/.ccr/ca-bundle.crt`.
`scripts/voices.json` = `{speaker: [voice, rate, pitch]}`; `scripts/lines.json` = `[[speaker, text], ...]`.

## Narrators by story mood

| Story | Voice | Rate / pitch | Notes |
|---|---|---|---|
| Indian legend, mythology, festival | `en-IN-PrabhatNeural` | −3% / −3 Hz | Warm older storyteller (Fisherman Who Caught the Sun) |
| Indian story, female narrator | `en-IN-NeerjaExpressiveNeural` | +0% | Expressive; also good for mothers, queens |
| Hindi narration (if the owner asks for Hindi) | `hi-IN-MadhurNeural` / `hi-IN-SwaraNeural` | +0% | Write the lines in Hindi |
| Dark fairy tale, epic, trailer | `en-US-ChristopherNeural` | −4% / −4 to −12 Hz | Add a low boost + hall reverb in synth (Clockmaker) |
| Mysterious, intimate, eerie | `en-GB-SoniaNeural` | −6% / −2 Hz | Hushed librarian; light room reverb (Library of Unlived Lives) |
| Science explainer, upbeat | `en-US-AndrewMultilingualNeural` | +6 to +12% | Warm, confident, playful insider |
| Calm awe (space, nature) | `en-US-AvaMultilingualNeural` | +0 to +6% | Caring, soft |
| News / documentary | `en-US-GuyNeural`, `en-US-AriaNeural` | +0% | Punchy, authoritative |
| Casual friend | `en-US-BrianMultilingualNeural`, `en-US-EmmaMultilingualNeural` | +4% | Conversational |

## Characters

| Character | Voice | Rate / pitch |
|---|---|---|
| Little girl | `en-GB-MaisieNeural` (UK child) or `en-US-AnaNeural` (US child) | −4 to +6% |
| Little boy | `en-US-AnaNeural` | +6% / −4 Hz (a touch lower) |
| Teen | `en-US-EmmaNeural` / `en-US-BrianNeural` | +8% |
| Mother, wife, queen | `en-IN-NeerjaExpressiveNeural` (Indian), `en-US-JennyNeural`, `en-GB-LibbyNeural` | +0 to +6% |
| Father, old man, sage | `en-IN-PrabhatNeural`, `en-GB-ThomasNeural`, `en-US-ChristopherNeural` | −4% / −4 Hz |
| Smug cat, posh animal | `en-GB-RyanNeural` | +12% / −2 Hz (Mittens) |
| Small cute creature | `en-US-AnaNeural` | +10% / +10 Hz |
| Big beast, demon, villain | `en-US-ChristopherNeural` | −8% / −15 Hz, low boost + reverb |
| God, divine voice | `en-US-ChristopherNeural` or `en-IN-PrabhatNeural` | −6% / −6 Hz, big hall reverb |
| Robot, AI | `en-US-AndrewMultilingualNeural` | +12% (optionally bitcrush in synth) |
| Shouty boss, director | `en-US-GuyNeural` | +10% |
| Australian, Irish, Kenyan, Nigerian… | `en-AU-WilliamMultilingualNeural`, `en-IE-ConnorNeural`, `en-KE-ChilembaNeural`, `en-NG-AbeoNeural` | to match the character's home |

`python3 -c "import asyncio, edge_tts; print([v['ShortName'] for v in asyncio.run(edge_tts.list_voices()) if v['Locale'].startswith('en-')])"`
lists every voice. When a character doesn't fit any row, pick by age + gender + accent, then tune rate
(energy) and pitch (size: lower = bigger and older, higher = smaller and younger).
