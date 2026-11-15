# SFX library (from "Free Sfx Pack")

52 sounds, renamed to safe filenames. `catalog.json` has measurements for every file:

| Field | Meaning |
|---|---|
| `sync_at_s` | **Where the hit or peak is inside the file.** Put the file so this point lands on the cut or word: `start = event_time - sync_at_s`. Most files have silence or a build-up before the peak (up to 2 s). |
| `audible_s` | How long it's actually audible |
| `lufs` | Loudness of the raw file |
| `gain_db_for_minus14_voice` | Gain to place it at about −24 LUFS, roughly 10 dB under a −14 LUFS voice. Add +4 dB for a big moment and −4 dB for something subtle. |
| `bass_energy_pct` | Share of energy below 150 Hz. Over 90% is mostly felt as a thump on phone speakers. |

`Lit sword slice.mp3` was empty (no audio stream) and is left out.

## Shortlist: the ones that suit talking-head and budget vlogs

| Job | Pick | sync_at | Notes |
|---|---|---|---|
| **Caption or text pop-in** (subtle) | `Quick_whoosh` | 0.62 | Shortest whoosh (0.4 s), clean. Use at −4 dB from the catalog gain. |
| **Cut whoosh** (fast montage) | `Whoosh_2`, `My_fav_whoosh`, `Whoosh_4` | 0.60 / 0.82 / 0.60 | Rotate them so repeats don't sound copy-pasted |
| **Big reveal / number slam** | `THE_Boom_Sound_Effect` | 0.38 | Sub-heavy cinematic boom, 2.2 s tail |
| **Build into a reveal** | `Reverse_Bass` | 1.03 | Rises into the peak. Land 1.03 s exactly on the punch word, then cut it. |
| **Heavy hit (smaller than a boom)** | `Bass_Explosion` | 0.12 | Near-instant attack, good on a number |
| **Punchline / "ouch" moment** | `Lit_body_punch`, `Lit_whoosh+punch` | 0.09 / 0.58 | Short and dry, comedic |
| **Tension / suspense beat** | `Lit_heartbeat1` | 1.19 | A single heartbeat. Fits the med-student theme. |
| **"Danger" / shock joke** | `Lit_shock` | 0.77 | Short electric zap |
| **Counting / calculating** | `Beeping_Sound_Effect` | 0.09 (first beep) | ~1 kHz beeps about 6 per second for 1.9 s. Works as a calculator or "adding it up" sound. Trim to taste. |
| **Glass-shatter twist** | `Lit_window_break` | 0.40 | Expectation shattered |
| **Drama / villain entrance** | `Dark_whoosh5`, `Lit_dark_whoosh_2` | 2.13 / 1.19 | Long, dark swells |
| **Avoid in vlogs** | gunshot, shotgun, sword, blood/bone, `Thunder_Sfx` (9 s), the two 30 s compilations | | Too violent or too long for this format. The compilations are about 13 (`Punch…`) and 26 (`Fighting…`) separate hits joined together. Cut out single hits if needed. |

## Rules for using them
1. **Use them sparingly.** The reference budget vlog used none at all. In a 60 s
   vlog, use 6–10 SFX total, only on hook, twists, reveals and the final montage.
   Don't put a whoosh on every cut; it starts to sound cheap.
2. **Line up the peak, not the file start.** Use `sync_at_s`.
3. **Keep the voice on top.** Put normal accents about 10 dB under the voice and big
   booms about 6 dB under. Never cover a word you need to hear, and place booms on
   the word *after* the key word or in a breath.
4. **Low booms on phones**: anything with >90% bass energy is mostly felt, not
   heard. Layer it with a short bright hit (`Lit_body_punch`) if it has to read
   on phone speakers.
5. **Fade the tails** of long files (booms, swells) over 0.3–0.5 s at the next cut.
