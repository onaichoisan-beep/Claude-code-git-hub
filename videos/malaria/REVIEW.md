# Review: How malaria infects you (49.5 s, 1080x1920)

## Creative calls
- Storyline built: **one parasite's journey**, from the bite to the liver to red blood cells to fever and the next mosquito. The ending loops back to the opening frame.
- Not built:
  - **"Inside the outbreak":** the same story told from one infected person's symptoms, working backwards.
  - **"The numbers":** 1 bite → 30,000 merozoites → billions of cells, as rising counters over each stage.
- Look follows `video-playbook/3D_REALISTIC_STYLE.md`: real-looking skin macro shots for the outside world, flat cyan cutaways for anatomy, the parasite always green, labels in the scene, and 1–3 word captions.
- Everything is real-time Three.js inside HyperFrames, not Blender or Unreal, so there are no photoreal human characters. The film keeps the human body implied (skin, blood, liver) instead.

## Science checks
- Anopheles injects dozens of sporozoites with its saliva (the script says "dozens", not "thousands").
- Sporozoites reach the liver within about an hour.
- The liver stage is silent for about a week, and each infected liver cell releases tens of thousands of merozoites.
- In a red cell, the ring stage feeds on haemoglobin, then divides into about 16 merozoites (×16 is shown) before the cell bursts.
- Synchronized bursting releases parasite waste (hemozoin and other byproducts), and the immune response causes fever, chills and sweating.
- A biting mosquito picks up parasites, and the cycle restarts. The script simplifies "gametocytes" to "the parasites".

## Measured vs looked at
- `check`: 0 errors. Lint, layout, motion and contrast all pass.
- Review sheets: the beat frames, the seam strips and the re-snapshots after fixes were all looked at.
- Sound was **measured, not heard**. Voice is −16 LUFS, peaks −1.5 dBTP. Sound-effect hits are placed one frame after their picture.

## Warnings kept on purpose
- `line_unread` on the DAY 3/4 numbers: the day counter is a deliberate fast count-up from 1 to 7.
- `line_unread` "40°C as last line": a misread by the checker. The captions continue after it; the label holds 1.16 s.
- `console_warning` "GPU stall due to ReadPixels": expected with WebGL capture.

## Weakest shot / with more time
- The goosebumps (41.2 s) read weakly. A displaced skin mesh would sell "chills" better than instanced bumps.
- The mosquito is built from primitives; a sculpted model with hairs and scales would be closer to the reference films.
- No music bed: no HeyGen sign-in and no local MusicGen model. The reference films keep their bed about 40 dB under the voice, so the mix is voice plus sound effects.

## Credits (CC BY sounds, include when publishing)
See `assets/sfx/CREDITS.md`: mosquito buzz (CrusaderNella), egg squelch (d.n.audio.uk), bubbling and pop (InspectorJ), slurp (mkoenig).
