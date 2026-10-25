---
message: "AI doesn't read words, it reads tokens: small chunks of text. They set what AI costs, how much it can remember at once, and why it used to miscount the R's in 'strawberry'."
destination: reels / shorts
aspect: 1080x1920
length: 66.3s
---

## Intent

The owner sent a reference reel (a kid asks an AI to "explain tokens like I'm five") and asked for the same
video in their pixel style, with a voiceover. This is a new take on that topic. The script, characters, jokes and
art are all new: a kid with hair buns in a red hoodie, and a little white hover-robot with a screen face. The only
things kept from the reference are the topic and the "explain it like I'm five" setup. It's narrated as a two-voice
dialogue because the owner asked for a voice. Small centred captions follow the words, both characters' mouths move
with their own voice, and the SFX duck under the speech.

## Story (line → picture)

| Time | Beat |
|---|---|
| 0–2.7 | Cold open: "HELLO! HOW ARE YOU?" slams down and shatters into its **6 tokens**. Robot: "I don't read your words. I read… these." Rewind glitch |
| 2.7–7.4 | Kid at her desk types to the laptop and the robot pops out: "Hey AI! What's a token? Explain it like I'm five." |
| 7.4–13.3 | The robot buries her in jargon (sub-word unit, byte-pair encoding, integer ID…) on a hologram. Her eyes spiral |
| 13.3–14.6 | Record scratch. Deadpan close-up with five fingers up: "I'm five." |
| 14.6–17.4 | "Right. Okay. Think of building blocks." Alphabet blocks stack up |
| 17.4–22.1 | Her message is typed, then snapped into 6 blocks: EXPLAIN / IT / LIKE / I'M / FIVE / . |
| 22.1–27.8 | CAT = 1 block. JELLYFISH splits into JELLY + FISH |
| 27.8–34.0 | "Ooh! Do Tyrannosaurus!" A T-rex stomps in and roars. The word splits into TYR / ANN / OS / AURUS |
| 34.0–37.7 | 1 token ≈ ¾ of a word (100 tokens ≈ 75 words) |
| 37.7–43.4 | "Why does that matter?" Blocks ride a belt into a meter and a coin pops out for each one: AI is priced by the token |
| 43.4–47.6 | A literal window fills with blocks: the **context window**. FULL! |
| 47.6–52.2 | "What happens when it's full?" The oldest blocks get pushed out and the robot forgets |
| 52.2–60.5 | "So you don't see letters?" STRAWBERRY fuses into one block, which is a big reason AI used to say 2 R's |
| 60.5–66.3 | "So how many R's are in strawberry?" Drum roll. "Three. I checked." The 3 R's light up gold. Loops back to the cold open |

## Voice

Microsoft neural voices via `edge-tts` (`scripts/make_voices.py`): robot **en-US-AndrewMultilingualNeural** (+12%),
kid **en-US-AnaNeural** (child voice, +6%). `synth_audio.py` trims pauses longer than 0.42 s, cuts the robot off
mid-word when the kid interrupts, levels every line the same, and lays the lines end to end. It writes `captions.js`
(captions, word timings, mouth flaps), and every scene keys off those word times, so a re-voice stays in sync.
To swap a voice: `SSL_CERT_FILE=… python3 scripts/make_voices.py assets/audio/vo <ai_voice> <kid_voice>`, then
`python3 scripts/synth_audio.py`, update `DUR` / `data-duration` in index.html if the printed DUR changed, then render again.

## Facts (checked with OpenAI's tiktoken: o200k_base = GPT-4o, cl100k_base = GPT-4)

- "Hello! How are you?" → Hello / ! / How / are / you / ? = 6 tokens in both tokenizers
- " cat" = 1 token; " jellyfish" = " jelly" + "fish"; " Tyrannosaurus" = " Tyr" + "ann" + "os" + "aurus" (same in both)
- "Explain it like I'm five." = 6 tokens in o200k (8 in cl100k), so the video says **"splits vary by model"**
- " strawberry" (as it appears mid-sentence) is a single token in both. The model never sees its letters, and that
  is widely cited as a main reason chatbots answered "2 R's" in 2024. The video hedges with "a big reason"
- Rule of thumb: 1 token ≈ ¾ of an English word, 100 tokens ≈ 75 words (OpenAI help centre, "What are tokens and how to count them")
- API usage is billed per token (priced per million input/output tokens, e.g. Anthropic and OpenAI pricing pages). The on-screen meter counts tokens, not real prices
- Context window = the most tokens a model can take at once. When a chat outgrows it, apps drop or summarise the
  oldest messages, so the model loses them ("I can start to forget")
- Byte-pair encoding (BPE) builds the sub-word vocabulary; each token maps to an integer ID, then to an embedding vector (the jargon joke is accurate)
