# STYLE: fraym.fx "After" edit, measured (canvas 1080x1920)

## Palette (measured hex)
| role | hex | where |
|---|---|---|
| cream card bg | `#F4E0A5` | S02, S04, S08 full cards (BGR 165,224,244, flat with fine paper grain) |
| polaroid card bg | `#F1E9D4` | S06 |
| maroon ink | `#5F0100` (core), AA ~`#73240A` | type card, polaroid text |
| brick red ink | `#B02A12` (measured #BB2D15 / #A92209 / #9E2409) | collage + video card text |
| white type | `#FFFEF5` | everything on the speaker |
| lime word | `#F3F83D` | "Ice-creams" |
| pale yellow | `#E5CF74` | "Kya khaana hain??" |
| side-note yellow | `#EDEB6A` (est.) | "Aaj main kya pehnu", "Save" |
| type box | `rgba(78,60,53,0.55)` over the wall (measured #4E3C35 vs wall #634B3F) | TypeBox |
| pink frame | `#CCB1AC` to `#B6848A` glitter + hearts | PinkFrame |
| camera body | `#9C736D` / highlight `#E3BEA6`, bg `#F3F2E2` | Digicam |

## Typography (font matched by NCC on the ink, Chromium render)
| role | font | NCC | size px | tracking | measured box |
|---|---|---|---|---|---|
| bold card word ("Decisions") | **Familjen Grotesk 700** | 0.886 | 122 | -0.05em | x 315-774, y 918-999 |
| card small lines ("as a girl") | Familjen Grotesk 700 | (same family) | ~78 | -0.05em | h 65 incl. descender |
| card script ("To make") | **Pinyon Script** | 0.365 (closest of 40 scripts) | 149 | -0.05em | x 190-609, y 796-902 |
| serif accent ("travel", "Career", "working") | **Libre Bodoni Italic** | 0.741 | 127 | -0.08em | x 574-840, y 159-262 |
| white top words ("Mujhe har dinn") | **Syne 600** | 0.33 | 69 (line 2 bolder ~84) | -0.03em | x 300-793, y 375-512 |
| bottom caption | **Space Grotesk 500** | 0.585 | 49 | -0.05em | x 268-818, y 1523-1564 |
| hook script ("Literally") | Pinyon Script, white | visual | ~120 | 0 | x 372-698, y 364-478 |
| product script ("Cafe Mocha") | **Alex Brush**, white | visual | ~104 | -0.03em | x 290-712, y 406-496 |
| lime word ("Ice-creams") | Familjen Grotesk 700 italic (skew -10deg) | visual | ~88 | -0.06em | x 328-768, y 415-487 |
| yellow italic ("Kya khaana hain??") | Familjen Grotesk 600 italic | visual | ~60 | 0 | x 275-824, y 418-465 |

## Global rules (measured)
- **Text zones on the speaker:** TOP = just above the head (ref y 364-512, centred x~540); MID = chest (ref y 1177-1245); BOTTOM caption (ref y 1523-1564; **we raise it to <=1520 for the IG safe zone**).
- **Timing:** text appears **~4 frames AFTER** the word is spoken (measured +1 to +6 f, mean +4.3 f over 9 words). Not before.
- **Entrances:** almost everything is a **hard pop** (full size, full opacity on one frame; template tracking shows scale 1.00, dx 0 for "Decisions" over 49 f and "Literally" over 25 f). No exits: hard swaps on the next word/phrase or on the cut.
- Exceptions (the only animated things): TypeBox typewriter (~2 f per char + cursor), ScriptFade/LimeWord letter cascade (letter fade ~6 f, stagger ~1.2 f, L->R), PinkFrame zoom-in (inset 34->64->84->92 px over 4 f, expo.out), Digicam pop (scale 0.96 -> 1.02 at +2 f -> 1.00 by +16 f, back.out).
- Cards/collage clips: pop on hard, tilted -6..+4 deg, inner video keeps playing.
- Camera on the speaker: none (no punch-ins measured on the After footage).

## Components (canonical)
| id | what | numbers |
|---|---|---|
| TopScript | one white script word above head | Pinyon 120px, pop, +4f |
| PopWord | single white word on chest, replaced per word | Syne 600 ~84px, pop, +4f |
| SubCap | bottom phrase caption | Space Grotesk 500 49px white, ls -0.05em, baseline <=1520, phrase swap |
| SideNote | small yellow note top-left/right | Space Grotesk 500 ~36px #EDEB6A, x 62 or right-aligned 900, y ~400 |
| TypeBox | typewriter in translucent box | box rgba(78,60,53,.55) r6, text Space Grotesk 500 caps 44px white, 2 f/char, cursor bar |
| TopWords | 1-2 white lines above head | Syne 600 69px + line 2 Syne 700 84px, pop per word |
| SerifStack | small white sans + big serif italic | Syne 600 46px over Libre Bodoni Italic 120px |
| YellowItalic | pale yellow italic line top | Familjen 600 italic 60px #E5CF74 |
| LimeWord | lime bold italic word top | Familjen 700 italic 88px #F3F83D, letter cascade |
| ScriptFade | white script product word | Alex Brush 104px, letter fade 6f stagger 1.2f |
| ArcText | curved white small text over head | Space Grotesk 500 40px on a 420px-radius arc, word by word |
| TypeCard | full cream card, stacked maroon type | bg #F4E0A5, Pinyon 149 + Familjen 700 122 / 78, word by word, hard cut in |
| Collage | cream card with 2-3 tilted clip cards, pins | clip cards ~440x600 rot -6/+4, red Familjen 700 62px lines + red Libre Bodoni Italic accent |
| Polaroid | cream card, white polaroid (inset clip), heart sticker | card #F1E9D4, polaroid #F1DCC6 x 50-1030, clip 70-1010 x 230-1690; text maroon Familjen 700 60px + Libre Bodoni 84px |
| VideoCard | cream card, clip panel 912x1580 centre, red text top/bottom | red Syne 600 64px + Libre Bodoni Italic 127px |
| PinkFrame | pink glitter heart frame, speaker inset | inner window x 92-988 y 166-1754, zoom-in 4f; white Syne 700 72px + Libre Bodoni Italic 72px accent |
| Digicam | retro camera on floral cream | body #9C736D, screen 760x620, pop scale .96->1.02->1.00 16f |

```json
{"canvas":[1080,1920],"fps":30,"textLagFrames":4,
 "palette":{"cream":"#F4E0A5","polaroidBg":"#F1E9D4","maroon":"#5F0100","red":"#B02A12","white":"#FFFEF5","lime":"#F3F83D","paleYellow":"#E5CF74","noteYellow":"#EDEB6A","typeBox":"rgba(78,60,53,0.55)","pink":"#CCB1AC","camBody":"#9C736D","camBg":"#F3F2E2"},
 "fonts":{"bold":"Familjen Grotesk 700","script":"Pinyon Script","serifItalic":"Libre Bodoni Italic","top":"Syne 600","caption":"Space Grotesk 500","productScript":"Alex Brush"},
 "sizes":{"cardBold":122,"cardSmall":78,"cardScript":149,"serifAccent":127,"topWords":69,"caption":49,"hookScript":120,"productScript":104,"lime":88,"yellowItalic":60},
 "zones":{"top":[364,512],"mid":[1177,1245],"captionBaseline":1500},
 "motion":{"pop":"0f","typewriterFramesPerChar":2,"letterFade":{"dur":6,"stagger":1.2},"pinkFrameInset":[34,64,84,92],"digicamScale":[[0,0.96],[2,1.02],[16,1.0]]}}
```
