# Voice casting: every video is narrated, every character gets a voice that fits

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
