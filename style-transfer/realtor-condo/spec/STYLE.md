# STYLE — reference summary

## Palette
- cyan: ['#5fd8ff', '#1dc3f2', '#139fdc']
- blue: ['#4aa8ff', '#2687e6', '#1f5fd6']
- green: #7cf13e
- studio: ['#e8a26e', '#da996f', '#d1466f']
- violet: ['#3f6bff', '#6a3cff']
- pillText: ['#c2189b', '#2d5be3']
- white: #ffffff
- ring: ['#7cf13e', '#7a3cff']
- labelGreen: #58e04a

## Typography (Bricolage Grotesque, NCC 0.78 = best of 20 Google candidates; ref is soft 720p)
| role | family | wt | px@1080 | note |
|---|---|---|---|---|
| accent big word | Bricolage Grotesque | 800 | 220 | cap 145px, tracking -0.03em, gradient fill |
| headline white | Bricolage Grotesque | 800 | 125 | So if you (xh 66) |
| line bold white | Bricolage Grotesque | 800 | 98 | Aur best part (xh 52), mein apna 81 |
| sub bold white | Bricolage Grotesque | 700 | 75 | Start hoti hai (xh 40) |
| light caption | Bricolage Grotesque | 300 | 62 | chala rahe ho 79 / humari services 62 / want to boost 57 |
| colour accent mid | Bricolage Grotesque | 800 | 132 | Your business (cap 87) |
| CAPS CTA | Bricolage Grotesque | 800 | 133 | DM US RIGHT NOW (cap 88) |
| counter | Bricolage Grotesque | 800 | 188 | 30000 (cap 124) + Rs 70px |
| side word | Bricolage Grotesque | 800 | 72 | Business (green) |
| pill text | Bricolage Grotesque | 700 | 44 | Performance marketing, pill h 64, pad 30 |

## Components (canonical motion)
- **slideX**: {"what": "big accent word, gradient fill, BEHIND the subject (head occludes it)", "from_px": -745, "axis": "x", "ease": "expo.out", "dur_f": 20.9, "t0": "word spoken -0..2f", "blur": "motion blur while moving (~18px at peak)", "src": "S01 Dehradun right edge 250->990, rms 7.6px"}
- **riseWord**: {"what": "word-by-word rise, used for big behind-head words", "from_px": 64, "axis": "y", "ease": "circ.out", "dur_f": 21.4, "opacity": "0->1 in ~4f", "stagger": "per spoken word", "src": "S03 Aaj top 760->696, rms 0.4px"}
- **snapRise**: {"what": "very fast snap-up of a big word + per-letter random reveal", "from_px": 218, "axis": "y", "ease": "power2.out", "dur_f": 3, "letters": "random-order fade over ~5f", "src": "S02 Social media top 669->452"}
- **springRise**: {"what": "coloured accent word springs up", "from_px": 127, "axis": "y", "ease": "back.out(1.7)", "dur_f": 5.7, "overshoot_px": -12, "src": "S09 Your business 1066->939, settles f657"}
- **sideSlide**: {"what": "small coloured side word slides in from the right", "from_px": 309, "axis": "x", "ease": "expo.out", "dur_f": 9.5, "src": "S01 Business x0 1014->705"}
- **typeOn**: {"what": "light captions / labels / CAPS CTA typed letter by letter", "rate": "~1.2 chars per frame", "cursor": false, "src": "S01 chala rahe ho f37-47, S04 labels, S10 DM US"}
- **letterRTL**: {"what": "giant word revealed letter by letter from the right", "dur_f": 11, "src": "S05 Studio x0 493->55 f284-295"}
- **cameraPunchOut**: {"what": "whole frame (footage+graphics) zooms out", "scale_from": 1.15, "scale_to": 1.0, "ease": "circ.out", "dur_f": 4.7, "at": "~0.9s into hook (f27)", "src": "S01 Dehradun width 896->779, rms 1.3"}
- **pageExit**: {"what": "caption page leaves: scale 1->0.92, blur 0->10px, opacity 1->0", "dur_f": 5, "src": "S01->S02 f49-54"}
- **iconRow**: {"what": "3 app-icon tiles slide in L->R staggered, settle", "stagger_f": 1, "dur_f": 5, "src": "S02 f55-60"}
- **cardDrop**: {"what": "post cards drop in from above one by one on a dark panel", "stagger_f": 4, "dur_f": 6, "ease": "back.out(1.7)", "src": "S03 f150-160"}
- **mediaCard**: {"what": "rounded media card slides in from the side with a green tint flash; green label types on above; thin white arc links cards", "dur_f": 8, "src": "S04 f196-240"}
- **logoDrop**: {"what": "white disc badge drops from above with one bounce", "dur_f": 8, "ease": "back.out(1.7)", "src": "S05 f282-290"}
- **uiCardPop**: {"what": "glassy UI card scales 0.6->1 with overshoot", "dur_f": 6, "ease": "back.out(1.7)", "src": "S06 f336-346"}
- **pillChart**: {"what": "white pill (r=full) with gradient text + white line chart drawn behind the subject", "chart_draw_f": 40, "pill_pop_f": 5, "src": "S07 f379-460"}
- **counter**: {"what": "big number counts 0->N with a circular progress ring and small suffix", "dur_f": 27, "ease": "power2.out", "ring": "green->purple stroke 0->100%", "src": "S08 f540-573"}
- **coinRoll**: {"what": "3D coin rolls in from the left", "dur_f": 8, "src": "S09 f640-650"}
- **lightLeak**: {"what": "screen-blended light leak sweeps in from right to white-out, cut underneath, decays", "build_f": 12, "white_f": 2, "decay_f": 8, "colors": {"blue": ["#1a6cff", "#7fd3ff", "#ffffff"], "warm": ["#ff2d6a", "#ff9a3c", "#ffffff"]}, "src": "f108-126, f319-335, f465-478, f599-610"}

## Global rules
- 100% speaker footage; every section = one caption "page"; page swaps by blur-exit (5f) or a light-leak at shot changes.
- Big accent words sit BEHIND the subject (depth layer), around forehead/hair height; small text sits at chest, never over the face.
- Words appear word-by-word/letter-by-letter in sync with speech; light captions type on.
- A new page every 2-3 s; light-leak at each location change (4 of 5 cuts).
- Grade: untouched footage, slight warm, no vignette.
