# Myth Puppet Theatre Style: Hindi Mythology Shorts

Learned from 2 reference shorts. Both are folk/Puranic stories told as an animated **leather shadow-puppet
show** (Tholu Bommalata / Togalu Gombeyata look), with calm Hindi storytelling, karaoke-style
romanised captions, and a comment-bait question at the end.

| # | Story | Length | Words | Hook type |
|---|-------|--------|-------|-----------|
| 1 | Shiva hides from Shani for 7.5 years (origin of *saadhesaati*) | 2:05 | ~260 | "He hid, yet got caught. How?" |
| 2 | Barbarik: the warrior who could end Kurukshetra in a minute (Khatu Shyam) | 1:55 | ~280 | "He could end it. Why didn't he fight?" |

Reference frames are in `reference/puppet-*.jpg`. Full reconstructed scripts are in section 9.

**How this differs from the Field Notebook style (`PLAYBOOK.md`):** it's slower and warmer and runs on
story, not facts. There are pauses between lines, no fact props or stamps, a single illustrated world
instead of a collage, dissolves instead of cuts, and full romanised captions instead of keyword headlines.

---

## 1. Technical format (measured)

| Spec | Value |
|------|-------|
| Aspect / res | 9:16, 720×1280, 30 fps (export 1080×1920) |
| Length | **1:55–2:05** |
| Script | **200–280 words** of Hindi |
| Overall pace | **105–140 wpm**, much slower than Field Notebook (170–200) |
| Pace inside a line | 2.6–2.8 words/s; lines are **2.2–3.4 s** |
| Pause between lines | **0.5–0.9 s, on purpose**. One 3 s breath before the final moral/CTA |
| First word | 0.0 s. Voice and picture start together with no intro |
| Loudness | **-14 LUFS integrated**, true peak about -1.3 dBFS (both videos) |
| Silence | none: a drone bed fills every pause (gaps measure about -17 dB, close to voice level) |
| Hard cuts | **1–2 per video in total.** Every other scene change is a slow cross-dissolve |
| Visual change | something moves or appears on every caption chunk (~2 s); new scene every 5–10 s |

---

## 2. Visual style: the animated shadow-puppet stage

### 2.1 Characters (the signature)
- Built like **Andhra leather puppets**: **head in profile** with a big almond eye, torso facing forward,
  flat colour fills, thin dark outline.
- **Visible joints** at shoulder, elbow, wrist, hip and knee (small rivet dots). Limbs rotate on those pivots,
  which gives you puppet motion for free.
- **Puppet rods**: thin, faint vertical lines run from the hands and feet down off the bottom of the frame.
  It's subtle, but it's what makes the frame read as a puppet show rather than a cartoon.
- **Dotted ornament lines** (like punched-leather perforations) along the dhoti, crown, jewellery and trim.
- **Warm backlit glow**: every puppet has a soft orange/amber outer glow, as if a lamp is behind the screen.
  Characters are slightly translucent during dissolves.
- Iconography carries identity: Shiva is pale grey-blue with a jata bun, crescent, snake, trident and
  tiger-skin dhoti. Shani is deep blue with a tall gold crown, crow and Saturn. Krishna is blue with a
  peacock feather and yellow dhoti. Barbarik is brown-skinned with an orange dhoti and three arrows.
- **Silhouette version** of a character (solid black, backlit halo) for mystery. The hook shows the hero
  as a silhouette and the next scene **dissolves him into full colour** when he's named.

### 2.2 Stage and backgrounds
- **Red theatre curtain** with a gold top border, a pelmet of hanging tassels and lamps, small sun and moon
  icons in the corners, and a row of **diyas along the stage edge**.
  - The curtain **opens** when the story proper starts ("Lokkatha kehti hai…", v1 at 0:19) or when the
    source is named (v2 at 1:45).
  - The curtain **closes** on the CTA. The final 3–4 s are the curtain sliding shut, then a closed curtain
    with a deep boom. This is the outro: no logo and no "subscribe".
- Background worlds are **flat, layered, softly lit gradients with grain**:
  - Night/cosmic: indigo-purple `#3A3157 → #1E1A2E` with gold stars and Saturn
  - Underwater: teal `#2E6E67` with light shafts, bubbles, small fish, reeds and pebbles
  - Desert/battlefield: amber-sepia `#7A4A22 → #2A1A10` with low dune lines
  - Lamp-lit story space: warm brown `#4A3020` with a glowing diya in the corner
  - Mountains: grey-slate Kailash with cream snow caps
- A thin **gold horizon line** and faint perspective lines on the floor, like the edge of a stage.

### 2.3 Caption system (on every line)
- Romanised Hinglish (Hindi written in Latin letters: "Jawab Ganga ki gehrai mein chhipa hai"), **not
  Devanagari**, so non-Hindi-script readers can follow.
- Font: **Cinzel** (classical small-caps serif). Cream-white `#F3EBDD` with a soft dark drop shadow.
- **Karaoke highlight**: the word being spoken turns **mint/aqua `#8FE3CF`**; earlier words go back to
  cream. Names and key nouns (Shanidev, Mahadev, Ganga, Krishna, daan) are usually the ones highlighted.
- 2–6 words per chunk, so each line splits into 2–3 chunks. The chunk fades to about 40% opacity as the
  next one fades in (no hard pops).
- Position moves with the composition: **top band (8–35% height)** when characters stand low, and
  **bottom band (~88%)** when the scene is tall. Captions never cover a face.
- Small, about 26–30 px at 720 wide. Captions add to the art; they don't shout over it.

### 2.4 Story props (each abstract idea becomes one object)
| Idea | Prop / device |
|------|---------------|
| Time passing | **Sun and moon icons swap** in the sky; a row of suns multiplies (7, then 8) for years |
| 7.5 years / astrology | **Zodiac wheel** whose sectors fill in amber as the narrator counts |
| Shani's gaze (*drishti*) | **Searchlight beam** from Saturn sweeping the scene |
| Flashback / "what you did" | **Pearl-bordered thought bubble** showing the earlier scene |
| Divine moment / realisation | **Radial light rays** rotating behind the character |
| "Scriptures / granth" | Stack of glowing **palm-leaf manuscripts** with lamps |
| Shifting loyalty | **Balance scale** with armies on each pan, tipping back and forth |
| Cold / held breath | Falling snowflakes, rising bubbles, a stillness close-up |
| Moral: you can't outrun it | Man running while **his shadow on the wall grows bigger** |
| Moral: sacrifice bears fruit | **Seed → sprout → sapling → big tree shading village huts** |
| Present-day payoff | **Temple** (Khatu Shyam) with saffron flags and the deity inside |

### 2.5 Motion and editing
- **Cross-dissolve / double exposure** between every scene (0.6–1.0 s). The previous scene stays visible
  as a ghost for a moment.
- **Puppet articulation**: an arm rotates up from the shoulder pivot, the head tilts, a bow is drawn. Small
  idle bob and sway, plus a slow push-in on most shots.
- **Vertical camera pans** link worlds, for example from the mountain down a cliff into the river, then
  underwater.
- **Close-up inserts** for proof details: a giant bust of meditating Shiva ("ruki hui saans"), or
  Krishna's foot covering the leaf with an arrow circling it.
- Particles everywhere: dust motes in lamp light, stars twinkling, fish swimming.
- **Light does the drama**: the scene dims to near-black on "pareeksha ban jaati hai", and glow swells on
  reveals.

---

## 3. Voice-over

- **Language:** simple spoken Hindi with very little English (only words like "minute" and "comment").
  It's more traditional than Field Notebook's Hinglish, because myth should sound timeless.
- **Register:** a calm, wise storyteller (*kathavachak* / grandparent) with gravitas, not hype. Median pitch
  is about 200 Hz with about a 10-semitone range. Expressive, but never shouting.
- **Pauses are part of the performance.** A beat after each line, and a longer breath before the moral.
- **Short declarative lines, 4–9 words each.** Many are fragments: "Thanda paani. Ruki hui saans. Saadhe
  saat baras." Three-beat lists like this are a signature.
- **Characters speak in quoted dialogue**, introduced with "Shiv ne kaha," / "Bole," / "Unhone kaha,".
- **One-word punchlines**: "Uff." / "Shyam." Say each one alone, after a pause.
- **Phrases you can reuse:**
  - `Jawab ___ mein chhipa hai.` (used in both videos at 0:10)
  - `Lokkatha kehti hai, …` / `___ Puran ki parampara kehti hai, …`
  - `Phir bhi ___. Kaise?` / `Phir woh ___ kyon nahi?`
  - `Par saar ek hi hai…`
  - `Yeh lokkatha hai, kisi ek granth ki nahi.` / `Mool paath mein uska naam nahi. Yeh katha Puran aur lok parampara ki hai.`
  - `Ab aap bataiye, ___ ya ___? Comment mein likhiye.`

---

## 4. Script blueprint (both videos follow this exactly)

```
0:00–0:10  HOOK         Paradox in 2 lines: impossible feat + "phir bhi / phir kyon?"
                        End on a one-word question: "Kaise?" / "Kyon nahi?"
0:10–0:13  TEASE        "Jawab ___ mein chhipa hai."   (names the key object, explains nothing)
0:13–0:19  THEME*       v1 only: the moral line, said once up front (it returns at the end)
0:17–0:25  FRAME        Source + who: "Lokkatha kehti hai…" / "Naam tha Barbarik. Ghatotkach ka
                        beta, Bheem ka pota." Curtain opens or the silhouette becomes colour.
0:25–1:10  STORY        6–10 beats, 1 visual per line, dialogue in quotes.
                        Rule of three where possible (3 arrows, 3 beats of "thanda paani…").
                        A test or trick sets up the turn (the hiding place, the peepal leaf).
1:10–1:30  TWIST        The other character reveals what really happened, in ONE line:
                        "Yahi to meri saadhesaati thi." / "Maine bas Krishna ka chakra dekha."
                        Then a one-word beat: "Uff." / "Shyam."
1:30–1:40  TODAY        Link to the present: "Saadhesaati bhi itne hi baras chalti hai" /
                        "Aaj wahi Khatu Shyam kehlate hain."
1:40–1:48  HONESTY      Name the source and its limits: lokkatha / not in the original text.
                        This earns trust and heads off "this isn't in the scripture" comments.
1:48–1:55  MORAL        A one-image metaphor (shadow you can't outrun / seed becomes a tree),
                        often echoing the THEME line from the opening.
1:55–2:05  CTA          "Ab aap bataiye: A ya B? Comment mein likhiye." Curtain closes, boom.
```

### 4.1 Hook rules
- The first frame is already the story's most striking image: Shiva meditating underwater with sun and
  moon cycling overhead, or two armies with a silhouetted warrior between them.
- State a **number** (saadhe saat saal, atthaarah din, ek minute) and an **impossible contrast**.
- Keep the name/identity back (Barbarik is named at 0:18) or the mechanism back (*how* Shani caught him).
- The hook question gets answered at the TWIST, about 75% of the way in. The whole video is one open loop.

### 4.2 CTA rule
Ask a **binary values question with no wrong answer**, so both sides comment:
- "Karm se koi bhaag nahi sakta, ya har kisi ki shakti ka sammaan karna chahiye?"
- "Barbarik ka sabse bada daan sir tha, ya apna vachan?"

---

## 5. Sound design

From the spectrograms and loudness measurements:
- **Drone bed**: a sustained Indian tonal drone (tanpura/sitar-like, strongest around 700–800 Hz) runs for
  the whole video, so there's never silence. It sits only a few dB under the voice in the pauses and is
  ducked under speech.
- **Low hits / thumps** on beats and scene changes (deep drum or *dhol* boom, energy below 120 Hz), and a
  big boom when the curtain closes. Use soft swells, not sharp risers.
- Suggested SFX palette:

| Visual | SFX |
|--------|-----|
| Curtain open/close | cloth swish + deep boom |
| Dissolve to new scene | soft airy whoosh / reverse cymbal swell |
| Divine reveal (light rays) | shimmering bell / ghungroo, temple bell |
| Arrow released / hits | bow twang, arrow whizz, soft thock |
| Underwater | muffled bubbles |
| Searchlight gaze | low tonal hum |
| One-word punchline ("Uff.", "Shyam.") | everything drops to drone, then one bell |

- Mix: voice on top (about -16 to -17 LUFS short-term), drone bed about 6–10 dB under it, master **-14 LUFS**,
  true peak -1 dBTP.

---

## 6. Topic method

A good topic has:
1. **A paradox in one sentence**: "even the gods couldn't escape", or "the strongest warrior never fought".
2. **One clever trick or test at its centre**: the hiding place, the leaf under the foot.
3. **A present-day hook**: a ritual, temple, festival, astrology belief, or saying people still use.
4. **A source you can name** (Purana, regional lokkatha) and say so honestly on air.
5. **A moral you can show with one image.**

Story ideas in the same vein (check the versions and sources first):
- Ganesha and the moon: why we don't look at the moon on Ganesh Chaturthi
- Ekalavya's thumb
- Why Brahma has (almost) no temples: the Pushkar curse
- Shani and Hanuman: why Saturday oil is offered to Hanuman
- Karna's last daan: gold teeth on the battlefield
- Why Jagannath's idol is unfinished
- Bhasmasur: the boon that turned on its owner
- Why the crow is fed during Shraddh
- Abhimanyu and the chakravyuh he learned in the womb
- Kumbhakarna's slip of the tongue: Nidrasan instead of Indrasan

---

## 7. Production recipe (HyperFrames)

1. **Script**: 200–280 words, one line per row, each marked with chapter (HOOK / TEASE / FRAME / STORY / TWIST / TODAY / HONESTY / MORAL / CTA).
2. **Voice**: record it or use TTS (`audio-lab/scripts/tts.py`, edge `hi-IN-MadhurNeural` / `hi-IN-SwaraNeural`,
   rate -5% to 0%). **Keep 0.5–0.9 s pauses between lines.** Don't tighten them the way the Field Notebook
   style does.
3. **Word timings**: run faster-whisper with `word_timestamps=True` and drive the karaoke captions from them.
   Write the romanised caption text by hand. Don't auto-transliterate.
4. **Puppets**: build each character as an **SVG rig**: head, torso, upper arm, forearm, thigh, shin as
   separate `<g>` groups, each with `transform-origin` on its rivet. Add dotted `stroke-dasharray` trim,
   rivet circles, 1 px vertical rod lines down to the bottom edge, and `filter: drop-shadow(0 0 18px #ffb35a88)`
   for the backlit glow. Reuse the same rig in every scene.
5. **Sets**: layered SVG/CSS gradients plus a grain overlay. Build one reusable **curtain component** (open/close
   timeline) and one **diya row**.
6. **Timeline**: one GSAP timeline. Scenes overlap by 0.8 s with opacity dissolves. Puppet poses are tweened
   on the line where the action is spoken.
7. **Audio**: drone bed, ducking, a boom per scene change, then master to -14 LUFS.
8. **Export**: 1080×1920, 30 fps.

---

## 8. Checklist

- [ ] Paradox hook with a number, ending in "Kaise?/Kyon?" by 0:10
- [ ] "Jawab ___ mein chhipa hai" tease
- [ ] Curtain opens on the story and closes on the CTA
- [ ] Every character is a jointed profile puppet with glow and rod lines
- [ ] Romanised Cinzel captions with a mint karaoke word, placed clear of faces
- [ ] Only dissolves (≤2 hard cuts); something moves on every caption chunk
- [ ] Twist line + one-word punchline around 75%
- [ ] Present-day link + honest source line
- [ ] One-image moral, then a binary "Ab aap bataiye… comment mein likhiye"
- [ ] Drone bed with no silence; 0.5–0.9 s pauses kept; -14 LUFS

---

## 9. Reference scripts (reconstructed from audio + on-screen captions)

### 9.1 Shiva and Shani (saadhesaati)
| t | Beat | Line |
|---|------|------|
| 0:00 | HOOK | Saadhe saat saal Mahadev aisi jagah chhipe rahe, jahan koi unhe dhoondh na sake. |
| 0:06 | HOOK | Phir bhi Shanidev unhe pakad le gaye. Kaise? |
| 0:11 | TEASE | Jawab Ganga ki gehrai mein chhipa hai. |
| 0:14 | THEME | Jahan chhipkar aap bachna chahte hain, wahi jagah aapki pareeksha ban jaati hai. |
| 0:20 | FRAME | Lokkatha kehti hai, ek din Narad Muni Bhagwan Shiv ke paas pahunche aur bole, |
| 0:25 | STORY | "Shanidev aapki or aa rahe hain, apni drishti daalne ke liye." |
| 0:30 | STORY | Shiv ne kaha, "Shani, mujh par nazar rakhega? Main aisi jagah chhip jaunga jahan woh mujhe dhoondh bhi nahi payega." |
| 0:38 | STORY | Aur ve Ganga ki gehrai mein jaakar ekagra baith gaye. |
| 0:42 | STORY | Thanda paani. Ruki hui saans. Saadhe saat baras. |
| 0:48 | TODAY (early) | Maanyata hai ki Shani ki saadhesaati bhi itne hi baras chalti hai. |
| 0:53 | STORY | Phir Mahadev baahar aaye aur seedhe Shanidev ke paas pahunche. Bole, |
| 0:58 | STORY | "Main aisi jagah chhip gaya tha ki tum mujhe dhoondh bhi nahi paaye." |
| 1:02 | TWIST | Shanidev muskuraaye aur haath jodkar bole, "Itni thand mein aap saadhe saat saal saans rokkar paani ke neeche baithe rahe. Yahi to meri saadhesaati thi." |
| 1:14 | PUNCH | Shiv ne bas itna kaha, "Uff." |
| 1:18 | HONESTY | Yeh lokkatha hai, kisi ek granth ki nahi, aur sunane wale ise apne dhang se sunate hain. |
| 1:26 | MORAL | Par saar ek hi hai: Shani ki drishti se koi nahi bachta. Bhagwan bhi nahi. |
| 1:32 | MORAL | Parchhai se bhaagne wala jitna tez daudta hai, woh utni hi paas chalti hai. |
| 1:38 | MORAL (echo) | Aur jahan chhipkar aap bachna chahte hain, wahi jagah aapki pareeksha ban jaati hai. |
| 1:44 | CTA | Ab aap bataiye, karm se koi bhaag nahi sakta, ya har kisi ki shakti ka sammaan karna chahiye? Comment mein likhiye. |

### 9.2 Barbarik / Khatu Shyam
| t | Beat | Line |
|---|------|------|
| 0:00 | HOOK | Kurukshetra ka yuddh atthaarah din chala. |
| 0:03 | HOOK | Par kehte hain ek yoddha use ek minute mein khatam kar sakta tha. Phir woh lada kyon nahi? |
| 0:10 | TEASE | Jawab ek daan mein chhipa hai. Jiske paas sabse badi jeet thi, usne wahi jeet daan kar di. |
| 0:18 | FRAME | Naam tha Barbarik. Ghatotkach ka beta, Bheem ka pota. |
| 0:23 | FRAME | Skand Puran ki parampara kehti hai, Devi se use teen achook baan mile. |
| 0:29 | STORY | Pehla baan nishaan lagata, doosra bachane walon ko chunta, teesra nishaan walon ko mita deta. |
| 0:37 | STORY | Woh maa ko vachan de chuka tha: kamzor paksh se hi ladoonga. |
| 0:41 | STORY | Yuddh se pehle Brahmin ke vesh mein Krishna uske paas aaye. Unhone kaha, "Is peepal ke saare patte ek baan se beendho." |
| 0:50 | STORY | Baan ne har patta beendh diya, par ek patta Krishna ne pair ke neeche chhipa liya tha, aur baan usi ke chaaron or ghooma. |
| 0:59 | STORY | Krishna samajh gaye: kamzor ka saath dene wala kabhi idhar jayega, kabhi udhar. Haarta paksh badalta rahega, aur ant mein dono senayein mit jayengi. |
| 1:10 | STORY | Tab Krishna ne daan mein maanga: tumhara sir. Barbarik ne bina jhijhke haan keh diya. |
| 1:18 | STORY | Usne bas itna maanga ki woh yuddh dekh sake. Aur uska sir pahadi par rakha gaya. |
| 1:24 | TWIST | Yuddh khatam hua to Pandav jeet ka shrey lene lage. Sir ne kaha, "Maine bas Krishna ka chakra dekha." |
| 1:32 | STORY | Krishna ne vardaan diya, "Kaliyug mein tum mere hi naam se pooje jaoge." |
| 1:37 | PUNCH | Shyam. |
| 1:38 | TODAY | Aaj wahi Khatu Shyam kehlate hain, jisne jeet daan kar di. |
| 1:43 | HONESTY | Mahabharat ke mool paath mein uska naam nahi. Yeh katha Puran aur lok parampara ki hai. |
| 1:50 | MORAL | Jo beej mitti mein dab jaata hai, wahi ped bankar poore gaon ko chhaya deta hai. |
| 1:56 | CTA | Ab aap bataiye, Barbarik ka sabse bada daan sir tha ya apna vachan? Comment mein likhiye. |
