# Reference reels: sound-design analysis (demucs stem split + cut-by-cut spectrograms)

| | Ref 1 (Df6oWnOydeU, 44s) | Ref 2 (DeA_qVESaQ9, 60s) |
|---|---|---|
| Music | warm lo-fi hip-hop bed (sustained bass + soft keys, light drums) | 97 BPM hip-hop/trap, 808 slides |
| Level | ~17 dB under voice, steady | ~15 dB under voice, steady |
| Ducking | none | ~2 dB |
| Cuts | mostly free | land ON the 808 kick |
| SFX | almost none | almost none; cut "hits" are the kick itself |
| Big move | dead silence at 8.25s, music OUT under the black pocket-watch line, music swells back at 10.9s | soft intro (no drums), music jumps to full on wordless B-roll montages (4.0s, 6.9s), beat DROP at 7.9s when the main talk starts |
| Ending | sweep into end card, 4s music fade | music runs ~3.5s past the last word, hard stop into a silent end card |

## Applied to the UMM Growth reel (v13)
- 0–11.7s: C.B.P.D soft intro under the hook / card section (−29.5 LUFS, 15 dB under voice)
- 11.7–13.0s: music OUT (designed silence) under "Our goal is simple."; only film burn + typewriter
- 13.0s: beat drop, first 808 kick measured at 13.005s on the cut to full frame
- 13–28.5s: beat at −29.5 LUFS, light ducking, fades with the picture
- SFX pulled back so the music dynamics lead: booms −5 dB, burn whooshes −2.5 dB, accents −3 dB; typewriter unchanged
- Mix: `edit-data/mix-music.sh renders/<base>.mp4 renders/<out>.mp4`
