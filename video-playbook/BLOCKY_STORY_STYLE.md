# Blocky Toy-World Story Style

Learned from 2 reference Shorts (720×1280, 30 fps, about 2:15–2:30 each):

| # | Story | Length | Shots | Words |
|---|-------|--------|-------|-------|
| A | The midnight ice cream truck that steals kids | 2:28 | ~66 | 398 |
| B | The town where everyone picks a gold or black pill | 2:16 | ~82 | 365 |

Reference strips: `reference/blocky-icecream-truck.jpg`, `reference/blocky-two-pills.jpg`.

**In one line:** a first-person spooky/mystery "story time" told by a narrator
in a cute blocky toy world, cut every ~2 seconds, with one bright yellow word
on screen at a time.

---

## 1. Why it looks "a little 2D" and why it is cheap to make

The trick is that the characters are 3D, but their **faces are flat 2D drawings
stuck on a cube**. Everything that carries emotion is 2D, and everything else is
simple boxes.

| Element | How it is built | Why it is cheap |
|---|---|---|
| Characters | Cube head, box torso, 4 box limbs. No fingers, no neck. | Every character uses the same rig. You only swap colours, hair and face. |
| Faces | A flat texture on the front of the head: two dot or oval eyes, a line mouth, sometimes eyebrows, freckles or a sweat drop. | You show emotion by **swapping a face image**, not by animating it. Keep 8–10 faces: smile, grin, shocked "o", worried, angry brows, sleeping, creepy wide grin, crying. |
| Hair | One chunky low-poly mesh (spiky brown, bob, slicked back, blonde). | Hair is the main way to tell characters apart. |
| Clothes | Flat colour plus 1–2 details (denim jacket, hoodie strings, striped apron, gold chain). | These are textures, not modelled cloth. |
| Sets | Kit-bashed boxes: houses with blue windows, picket fences, round "lollipop" trees, roads with yellow dashes, floating islands. | Build a set once and use it for 10–20 shots. |
| Look | Soft global light, strong **bloom/glow** on neon, lamps and magic objects, light fog, saturated colours. | Bloom and fog hide low detail and make cheap scenes look polished. |
| Animation | Stiff limb swings, simple walk cycles, characters sliding into place, small head turns. Many shots are **almost still** and rely on the camera moving. | Little or no character acting is needed. |

**The camera does most of the work.** Typical moves are a slow push-in on a face,
an orbit around an object, a fly-through down a corridor, a dolly behind a
walking character, an overhead drone shot of the street, and a dutch tilt for
danger.

### Tool options (from easiest to most work)
1. **A blocky game-engine sandbox plus a camera/keyframe plugin.** This is how
   most channels in this genre do it. Pose avatars, place them in a built
   world, keyframe the camera, and record.
2. **Blender** with one blocky rig and a library of face PNGs. Use Eevee with
   Bloom, Fog and AO turned on, then render 720×1280.
3. **This repo's HyperFrames + Three.js stack** (like `videos/malaria`). Build the
   characters from `BoxGeometry`, draw the faces onto a `CanvasTexture`, add
   `UnrealBloomPass` and fog, and animate the camera with GSAP. The whole
   video can be generated from code.

> Keep it original: use your own characters, sets and logos. Use a *generic
> blocky toy look*, and don't copy a specific game's avatars, UI or branding.

---

## 2. Story formula (both videos follow it beat for beat)

Both videos are told in **first person** ("My name is Mason…", "So, I took it.")
by a kid or teen hero. The tone is a spooky-cute mystery with a happy rescue
and a twist sting at the end.

| Time | Beat | Ice cream truck (A) | Two pills (B) |
|---|---|---|---|
| 0–8 s | **"In this town…" premise**, an impossible rule about the world | "In this town, the ice cream truck only comes at midnight, and every kid knows three rules." | "In this town, everyone must choose between two pills." |
| 8–20 s | **Stakes / rules**, often as a list of 2–3 | Never buy, never follow, never look. "Every kid who broke these rules has disappeared." | Gold = rich for life, black = the darkest secret. |
| ~20 s | **The hero breaks the rule** (the inciting choice) | "My name is Mason, and last night I broke all three." | "70% of you voted for the black pill. So, I took it." ← an **audience-vote hook** that sets up a series |
| 20–50 s | **The first strange thing**, slowly escalating | Midnight melody, a truck with no driver, the friend's call cuts off | Vision changes, red lines connect people, a rich man is "controlled" |
| ~50 s | **Personal stake**: a missing friend or family member | Oliver's little brother followed the truck | Sister Ruby disappeared 5 years ago |
| 50–75 s | **Enter the impossible place** | The inside of the truck is an endless ice cream shop | A hidden elevator leads to an underground room of screens |
| ~75 s | **Reveal of the system** plus the villain's line | Frozen kids in glass; "Once you take a bite, you stay forever." | The gold pill puts a chip in brains; Dad invented it |
| 75–100 s | **The hero notices the weakness** (one clear rule) | The music keeps them trapped, so smash the music box | Only his children can unlock the machine |
| 100–120 s | **Action climax**: alarms, collapse, a run for the exit | Glass shatters, the shop collapses, "You can't escape!" | Guards rush in, hand on the scanner, ACCESS GRANTED, a big red button |
| 120–130 s | **Resolution**: everyone freed, a hug | Every missing child is home | Millions are finally free, "You saved them, little brother." |
| Last 10 s | **Twist / sting** that opens a sequel | 11:59 PM, a pink box on the doorstep: "But who's going to free me?" | "The gold pill could buy you everything, except freedom." (a moral one-liner) |

### Writing rules
- **Open with "In this town,"** and state a rule that could not exist in real life. The first word is spoken at 0.00 s and there is no intro.
- **Short, plain sentences** of 6–12 words. One action per sentence, so each sentence can be one shot.
- **Use exact numbers and times**: "exactly midnight", "11:59 PM", "70%", "five years ago", "thousands of screens". Show each one as a big glowing on-screen prop.
- **Use "Suddenly," and "Then"** about every 15 seconds to restart momentum. Each video uses "suddenly" 3–4 times.
- **Quoted dialogue in short bursts** ("Help me!", "Everyone run!", "Free ice cream, Mason."). The narrator voices every character with little change of tone.
- **Name 2–3 characters only** (hero, ally, villain). Repeat the names often.
- **One clear magic rule** that the hero figures out and breaks. The audience should be able to guess it a second before the hero says it.
- **Length: about 360–400 words, which plays at about 2:15–2:30.**

---

## 3. Editing and pacing

| Spec | Measured value |
|---|---|
| Format | 9:16, 720×1280, 30 fps |
| Shot length | **median 1.6–2.0 s** (A: 2.0 s, B: 1.6 s); longest shot about 4–6 s; 65–80 cuts per video |
| Narration | **~160 wpm**, continuous, with a short breath at full stops only |
| Loudness | **-14 LUFS** integrated (both videos) |
| Transitions | Almost all **hard cuts**. Sometimes a quick flash/whiteout when entering a magic place (the truck door glows white). |
| Shot = line | Every sentence gets a new shot, and long sentences get 2–3 shots. The picture always shows **exactly** the noun being spoken: "phone rang", then a phone on the floor with "OLIVER incoming call". |

### Shot vocabulary (use the same set again and again)
- **Establishing wide**: a night street with a moon, or a sunny floating city. Use it at the start and whenever the location changes.
- **Face close-up**: the cube face fills the frame and the expression swap *is* the beat (shocked, angry, creepy grin).
- **Over-the-shoulder / follow-from-behind**: the hero walks toward the danger.
- **Big text prop**: a giant glowing clock "12:00 AM", a red "LOCKED" panel, a green "ACCESS GRANTED" scanner, a phone caller ID, a chalkboard ("PILL SYSTEM V1"), or a handwritten note. Text is part of the world, not a graphic overlay.
- **Insert of the magic object**: an ice cream cone, a music box, a pill on a pedestal, a red button, with bloom glowing on it.
- **Crowd / scale shot**: hundreds of frozen kids, thousands of screens, an endless corridor (a mirrored, repeated set).
- **Destruction**: shatter, collapse, money raining, with fast cuts of 0.5–1 s.

### Colour storytelling
- Each video has **two worlds with opposite palettes**:
  - A: a cool **blue/indigo night** suburb against the **hot pink** candy interior.
  - B: a warm **beige/brick** poor town and **sky-blue/gold** rich city against a **neon purple/cyan/red** underground lab.
- The villain's world glows (pink, red, neon). Safety is shown in natural light (green grass, blue sky, sunset).
- The final shot returns to the calm world, sometimes at sunset.

---

## 4. Captions

- **One word at a time**, synced to the voice (word-level timestamps).
- Font: heavy **rounded** sans (Fredoka Bold, Nunito Black or Baloo 2 ExtraBold).
- Colour: **neon yellow-lime `#E8FF1A`**, a thick **black outline** (about 6 px at 720 wide) and a soft dark drop shadow.
- Lower case, as spoken, with no punctuation. Proper nouns are capitalised ("Mason", "Golden City", "70%").
- Position: centred horizontally at **~72–75% of frame height**, so it stays out of the way of faces and props.
- Animation: each word **pops in** from about 40% to 100% scale in 3–4 frames, with a slight overshoot. Key words ("impossible", "escape", "like") are drawn about 15% larger.
- No other on-screen graphics: no title card, logo or progress bar.

---

## 5. Audio

- **Narrator**: a young, friendly, slightly breathless storyteller voice. It is clear and fast, and dialogue is only lightly acted.
- **Music bed**: quiet, playing all the way through. Use a music-box/eerie lullaby for spooky parts and a pulsing synth for action, kept well under the voice.
- **SFX on beats**: a phone ring, a door creak, a glass shatter, alarms, a rumble, a whoosh on the flash into the magic place, and a soft "ding" on the final sting.
- No silence. The music carries across every cut.

---

## 6. Production checklist for a new episode

1. **Premise**: "In this town, ___." Write one impossible rule and 2–3 sub-rules or choices.
2. **Script** of ~380 words using the beat table in section 2. End on a twist line or moral.
3. **Cast**: the hero (always the same recurring character, which builds a channel mascot), an ally or missing relative, and a villain with a creepy grin face.
4. **Sets**: 2 locations with opposite palettes, plus 4–6 hero props that show text (clock, phone, sign, note, panel).
5. **Shot list**: one row per sentence, choosing from the shot vocabulary. Aim for ~70 shots.
6. **Voice**: record or generate TTS, then get word timestamps (faster-whisper; see `../audio-lab`).
7. **Build and render** shots with a slow camera move each, plus bloom and fog.
8. **Edit**: hard-cut on sentence boundaries, then add the one-word captions, music and SFX. Master to -14 LUFS.
9. **Hook check**: the first 3 seconds must contain "In this town" plus a striking visual (a truck's headlights, a glowing pill).
10. **Optional series hook**: "I asked you guys which one I should pick… 70% of you voted…" This sets up comment-driven sequels.
