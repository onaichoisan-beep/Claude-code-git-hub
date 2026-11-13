# STYLE: reference
## Canvas / frame
- Background #EDEDED (light grey). Video sits in a floating CARD: x 33-1052, y 30-1847 (1019x1817), corner radius 45 px,
  drop shadow (+14,+22) blur 28 rgba(0,0,0,.45). Dark slab #3F4143 peeks out behind the card left/right, y 380-1440.
- Hook only: bottom crimson gradient (rgba(200,20,60,.85) at y 1847 -> 0 at y 1100), dashed white guide lines (1.5 px, 6/6 dash, 45 % white).
## Palette
| role | hex |
|---|---|
| big word pink (measured median) | #D9335E, highlight top #FF2E6A |
| big word glow | rgba(255,30,85,.55) blur 18 |
| box fill | rgba(28,26,28,.62) (dark) / rgba(90,10,30,.55) (hook maroon) |
| box glow border | #FF2B5E 4 px + glow 16 |
| small text | #FFFFFF, shadow 0 2 8 rgba(0,0,0,.35) |
| card | #FFFFFF 92 %, label #333, numbers #C2264E, bar gradient #C8102E->#F0506E, head #FFD34D glow |
| zigzag line | #FFD23A core, glow #FF7A00 |
| flash | white, peak alpha .75 |
## Typography (NCC/visual match against Google Fonts)
- Small line: **Saira Expanded** 300-400, 59 px (ref "aren't ready for" = 479 px wide), tracking 0, lowercase as spoken.
- Big word: **Saira Expanded Black Italic** 900, 82-100 px, auto-fit to max width 760, UPPERCASE, tracking -0.01 em.
- Card: Saira Expanded 400: label 30 px, number 52 px, axis 28 px.
## Components + canonical motion (measured)
1. **SmallWords**: each word appears on its spoken frame (lead 0-2 f): y -18 -> 0, opacity 0 -> 1, blur 6 -> 0 px, 4 f, power2.out.
2. **BigDrop**: each word y -24 -> 0, opacity 0 -> 1, vertical motion blur, 6 f, power2.out (ref NEW f126 -> settled f132). Lead 2-3 f.
3. **Sweep**: white light streak (3 px, glow) travels L->R across the bottom of the big word 7 f after settle, 6 f, then gone.
4. **HookBar**: maroon box + pink glow edge + corner brackets, opens from centre scaleX 0 -> 1, **quad.out 16 f** (fit error < 1 %), text clipped inside. Final 723 x 61 px.
5. **GlowPill**: dark box radius 20, pink glowing 4 px border; rises +20 px -> 0 in 3 f, opacity 0 -> 1; words inside = SmallWords.
6. **GuideBox**: dark rect grows from centre (both axes) 8 f power3.out, dashed guide lines extend along its edges to the card edges; big pink words drop into it; 5 f after last word, border turns pink glow with corner accents.
7. **ProgressCard**: white card 760 x 190 radius 18, enters with the flash: y +60 -> 0, rotateX 25 -> 0, 10 f power3.out; counter ticks (1 step per 3-4 f), bar fills with yellow glowing head.
8. **Zigzag**: neon polyline drawn L->R (stroke-dashoffset) 10 f linear-ish (power1.out), stays; words placed along it.
9. **FlashCut**: white overlay: alpha .75 held 3 f, decays to 0 over 11 f (power2.inOut); camera punch to the new scale on the flash frame.
10. **Glitch intro** f1-4: RGB split +-14 px, horizontal blur 40 px; f5-15 blue->violet tint fading out.
## Global rules
- Text zone: over the torso, centred on x 540; 1 small line + 1 big accent per page; page 23-90 f; hard swap.
- Never over the face; inside IG safe zone x 84-900... (big words may reach x 166-919 in ref: we clamp to 84-996 card-safe and 760 max width).
