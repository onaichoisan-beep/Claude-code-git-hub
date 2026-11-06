# Pacagen B-roll library

**Brand:** Pacagen: cat allergen neutralizing spray, cat allergen reducing supplement, WhiskerBlock powder
**Source:** [Google Drive folder](https://drive.google.com/drive/folders/1-7sQpKl0AAn6fOKnXBuczjWl4ajC3mjG) ("Pacagen B ROLL extras")
**Clips:** 56 unique (87 files on Drive: 21 were uploaded twice, and 10 renamed files are copies of `IMG_xxxx` files) · 8 min 5 s total
**Format:** all vertical 9:16. 55 are 4K 2160×3840; only `FEED-05` is 720p.
**Cats:** **Siamese** (seal/lynx point, short hair) and **Ragdoll** (grey-blue, long fluffy hair). **Creator:** one woman with dark hair.
**Audio:** room sound only, no talking. Mute it or use it as a quiet ambience bed.

> ⚠ `USE-02`, `USE-03` and `USE-04` (IMG_1108/1109/1110) are **HDR (HLG) HEVC at 60fps**. Convert them to Rec.709/SDR in your NLE or they will look washed out next to the other clips.

Get the files: `python3 broll-library/fetch.py pacagen` downloads every clip into category folders with clear names.
Filter by tag: `python3 broll-library/fetch.py pacagen --tag hook`, or one clip: `--id USE-05`.

---

## Story map: which clip for which beat

| Ad beat | Go-to clips |
|---|---|
| **Hook / scroll-stopper** | `RAG-01` ragdoll stares into lens · `FEED-06` ragdoll walks up to the camera · `PROB-01` handful of cat hair · `RAG-02` judgy close-up |
| **Problem: hair everywhere** | `PROB-01` hair in the cat bed · `PROB-02` lint-rolling clothes · `PROB-03` brushing hair off, frustrated |
| **Problem: allergy symptoms** | `FEED-03` at 0:13 (creator rubs her nose) · `PROB-03` |
| **Problem: cat shut out** | `DOOR-01` opening the door to a waiting cat · `DOOR-03` door closing on her · `DOOR-02` |
| **What I tried before** | `AIR-02` air purifier display · `AIR-01` / `AIR-03` pan between the purifier and the cat · `PROB-02` lint roller |
| **Product reveal** | `PRD-01` lineup push-in · `PRD-03` creator presents each item · `PRD-02` |
| **How it works (3 steps)** | `PRD-08` powder (activate) → `USE-01` / `USE-02` spraying (neutralize) → `PRD-06` box-back steps → `USE-05` relax |
| **Supplement** | `PRD-04` tub rotating to the logo · `FEED-01` / `FEED-02` cat eating beside the tub · `PRD-05` back label |
| **Spray demo** | `USE-01` cat tree · `USE-02` / `USE-03` couch · `USE-04` play mats · `USE-05` 0:00–0:12 |
| **Pet-safe / cat-approved** | `USE-06` Siamese sniffs the bottle · `FEED-01` |
| **After / result** | `USE-05` 0:45–1:28 reading with the cat · `BOND-01` to `BOND-04` petting · `RAG-08` relaxed |
| **CTA / end card** | `PRD-01`, `PRD-02` (lineup), `PRD-04` (ends on the logo) |
| **Filler / pacing** | `SIA-*` (play, climbing, window) · `RAG-*` (bed, couch, hiding) · `FEED-07` / `FEED-08` feeding station |
| **Funny beat** | `RAG-12` hides under the trampoline · `RAG-02` judgy stare |

## Quick index

| ID | Clip | Length | Cat |
|---|---|---|---|
| `PRD-01` | Full lineup on counter — slow push-in | 6.3s | none |
| `PRD-02` | Full lineup on counter — slide left→right | 3.4s | none |
| `PRD-03` | Creator unboxes / presents each product | 21.9s | none |
| `PRD-04` | Supplement tub in hand — rotate to logo | 9.2s | none |
| `PRD-05` | Supplement tub back label | 3.4s | none |
| `PRD-06` | Spray box back — 3-step instructions | 3.8s | none |
| `PRD-07` | Dark-blue box back — 'Inside this pack' | 2.0s | none |
| `PRD-08` | WhiskerBlock powder stick in hand | 8.0s | none |
| `USE-01` | Spraying the cat tree | 10.7s | none |
| `USE-02` | Spraying the couch (sectional) | 6.2s | none |
| `USE-03` | Spraying the couch — leaning across | 4.4s | none |
| `USE-04` | Spraying cat climbing mats / play area | 5.0s | none |
| `USE-05` | Spray couch → sit and read WITH the cat (88s) | 87.8s | siamese |
| `USE-06` | Siamese sniffing the spray bottle on windowsill | 6.2s | siamese |
| `FEED-01` | Siamese eats from bowl next to supplement tub | 5.2s | siamese |
| `FEED-02` | Siamese eats next to tub — push-in | 7.2s | siamese |
| `FEED-03` | Creator sets out bowls — then rubs nose | 17.7s | none |
| `FEED-04` | Ragdoll eating at feeding tray | 4.7s | ragdoll |
| `FEED-05` | Ragdoll eating — wide, low-res | 5.8s | ragdoll |
| `FEED-06` | Ragdoll walks up to camera past food tray | 3.5s | ragdoll |
| `FEED-07` | Feeding station tray — slow pan | 3.0s | none |
| `FEED-08` | Kibble bowls + water fountain push-in | 2.9s | none |
| `PROB-01` | Picking cat hair out of cat bed | 7.3s | none |
| `PROB-02` | Lint-rolling cat hair off shirt | 13.6s | none |
| `PROB-03` | Brushing hair off shirt, waving it away | 8.2s | none |
| `AIR-01` | Air purifier → pan up to Siamese on cat tree | 8.6s | siamese |
| `AIR-02` | Air purifier display push-in | 4.6s | none |
| `AIR-03` | Siamese on tree → pan down to air purifier | 6.2s | siamese |
| `DOOR-01` | Open door → Siamese sitting waiting outside | 4.4s | siamese |
| `DOOR-02` | Siamese walking outside door gap | 4.2s | siamese |
| `DOOR-03` | Door closing on Siamese | 5.1s | siamese |
| `BOND-01` | Petting ragdoll on bed | 10.7s | ragdoll |
| `BOND-02` | Scratching ragdoll's head | 11.9s | ragdoll |
| `BOND-03` | Belly rubs — ragdoll on back | 13.6s | ragdoll |
| `BOND-04` | Petting ragdoll — cat closes eyes | 14.9s | ragdoll |
| `SIA-01` | Siamese playing with feather wand | 5.7s | siamese |
| `SIA-02` | Siamese rolling with feather toy | 3.8s | siamese |
| `SIA-03` | Siamese play session (14s) | 14.2s | siamese |
| `SIA-04` | Siamese on windowsill about to jump down | 2.1s | siamese |
| `SIA-05` | Siamese leaves window bed, walks the room | 6.2s | siamese |
| `SIA-06` | Siamese walking wall shelves → cat tree | 13.0s | siamese |
| `SIA-07` | Siamese stepping onto wall hammock | 3.2s | siamese |
| `SIA-08` | Siamese on wall hammock, looks at camera | 5.0s | siamese |
| `SIA-09` | Siamese on cat tree by clock → jumps to shelf | 8.8s | siamese |
| `RAG-01` | Ragdoll on bed — stares into camera | 9.9s | ragdoll |
| `RAG-02` | Ragdoll close-up — judgy stare | 5.1s | ragdoll |
| `RAG-03` | Ragdoll on bed — profile then front | 7.9s | ragdoll |
| `RAG-04` | Ragdoll loaf on bed, wooden dresser behind | 5.0s | ragdoll |
| `RAG-05` | Ragdoll on bed — handheld around | 10.6s | ragdoll |
| `RAG-06` | Ragdoll lying → sits up, looks away | 6.9s | ragdoll |
| `RAG-07` | Ragdoll grooming on bed | 7.0s | ragdoll |
| `RAG-08` | Ragdoll stretched out — push-in to face | 4.3s | ragdoll |
| `RAG-09` | Ragdoll in fabric cube on cat shelf | 8.8s | ragdoll |
| `RAG-10` | Ragdoll on couch in sunlight stripes | 2.8s | ragdoll |
| `RAG-11` | Ragdoll by window → walks to camera | 9.0s | ragdoll |
| `RAG-12` | Ragdoll hides under trampoline | 4.0s | ragdoll |

---

## Product packshots & details  (8 clips)

### `PRD-01` Full lineup on counter — slow push-in
![](thumbs/PRD-01.jpg)

- **File:** `showing product on counter.mov`
- **Length:** 6.3s · 2160x3840 · 30fps · wide → medium, slow push-in
- **What's in it:** All Pacagen products lined up on granite counter (spray bottle, stabilizing solution pouch, Cat Allergen Neutralizing Spray box, supplement tub). Slow handheld push-in from wide to the boxes.
- **Use for:** Brand reveal, 'this is the whole kit', CTA end card background
- **Tags:** lineup, packshot, counter, spray, supplement, box

### `PRD-02` Full lineup on counter — slide left→right
![](thumbs/PRD-02.jpg)

- **File:** `showing product on counter 2.mov`
- **Length:** 3.4s · 2160x3840 · 30fps · medium close, lateral slide
- **What's in it:** Same lineup, closer, lateral slide across the pouch, powder stick and supplement tub.
- **Use for:** Quick product flash, transition between sections
- **Tags:** lineup, packshot, counter

### `PRD-03` Creator unboxes / presents each product
![](thumbs/PRD-03.jpg)

- **File:** `showing each product.mov`
- **Length:** 21.9s · 2160x3840 · 30fps · static medium, creator on camera
- **What's in it:** Creator behind kitchen counter holds up each item: spray box front (0:03-0:05), box back 'Inside this pack' (0:06-0:08), opens supplement tub (0:09-0:13), spray box again (0:14-0:16), instructions card (0:16-0:18). Ends on products alone (0:19-0:22).
- **Use for:** 'Here's what you get', unboxing beat, product-explainer section
- **Best section:** 0:03-0:18
- **Note:** Best single clip to explain the kit
- **Tags:** creator, unboxing, talking-head-style, kitchen, box, supplement

### `PRD-04` Supplement tub in hand — rotate to logo
![](thumbs/PRD-04.jpg)

- **File:** `supplement side view.mov`
- **Length:** 9.2s · 2160x3840 · 30fps · close-up, handheld rotate
- **What's in it:** Hand holds Cat Allergen Reducing Supplement tub, rotates from side label to front 'Pacagen' logo. Spray + pouch blurred behind.
- **Use for:** Supplement mention, 'just add a scoop to food'
- **Note:** Ends on logo, good hold frame
- **Tags:** supplement, tub, hand, closeup, logo

### `PRD-05` Supplement tub back label
![](thumbs/PRD-05.jpg)

- **File:** `back side of package supplement.mov`
- **Length:** 3.4s · 2160x3840 · 30fps · close-up handheld
- **What's in it:** Hand holds supplement tub showing back label / barcode.
- **Use for:** Ingredients / 'it's safe' claims
- **Tags:** supplement, back-label, closeup

### `PRD-06` Spray box back — 3-step instructions
![](thumbs/PRD-06.jpg)

- **File:** `showing the back side of package 1.mov`
- **Length:** 3.8s · 2160x3840 · 30fps · close-up, push-in
- **What's in it:** Hand holds box back: Step 1 Activate, Step 2 Neutralize, Step 3 Relax & Repeat. Push-in to Step 2/3 text.
- **Use for:** 'How it works' — 3 steps; pair with on-screen text
- **Tags:** box, instructions, steps, how-it-works

### `PRD-07` Dark-blue box back — 'Inside this pack'
![](thumbs/PRD-07.jpg)

- **File:** `backside of package 2.mov` (also uploaded as `IMG_0102.mov`)
- **Length:** 2.0s · 2160x3840 · 30fps · close-up handheld
- **What's in it:** Hand holds blue box back: 1x WhiskerBlock powder, 1x Stabilizing solution, special video from founder (QR). Short (2s).
- **Use for:** 'What's inside the pack' flash
- **Note:** Same file as IMG_0102
- **Tags:** box, inside-this-pack, closeup

### `PRD-08` WhiskerBlock powder stick in hand
![](thumbs/PRD-08.jpg)

- **File:** `whisker block powder.mov`
- **Length:** 8.0s · 2160x3840 · 30fps · close-up handheld
- **What's in it:** Fingers hold the blue WhiskerBlock powder stick sachet, turn it to show the back. Spray bottle behind.
- **Use for:** Step 1 'pour the powder in'
- **Tags:** powder, whiskerblock, sachet, closeup


## Product in use — spraying  (6 clips)

### `USE-01` Spraying the cat tree
![](thumbs/USE-01.jpg)

- **File:** `IMG_0112.mov`
- **Length:** 10.7s · 2160x3840 · 30fps · static wide
- **What's in it:** Creator walks into frame and sprays the tall cream cat tree with the Pacagen bottle, then smiles at camera.
- **Use for:** 'Spray where your cat hangs out', application demo
- **Tags:** spray, cat-tree, creator, application

### `USE-02` Spraying the couch (sectional)
![](thumbs/USE-02.jpg)

- **File:** `IMG_1109.MOV`
- **Length:** 6.2s · 2160x3840 · 60fps · static wide · ⚠ HDR
- **What's in it:** Creator (brown tee, jeans) sprays a beige sectional couch, walks along it.
- **Use for:** 'Spray the couch', application demo
- **Note:** HDR (HLG) HEVC 60fps — convert to SDR/Rec709 in your NLE
- **Tags:** spray, couch, creator, application

### `USE-03` Spraying the couch — leaning across
![](thumbs/USE-03.jpg)

- **File:** `IMG_1110.MOV`
- **Length:** 4.4s · 2160x3840 · 60fps · static wide · ⚠ HDR
- **What's in it:** Same couch, creator leans across the chaise to spray the back cushions.
- **Use for:** Alt take of USE-02
- **Note:** HDR (HLG) HEVC 60fps
- **Tags:** spray, couch, creator, application

### `USE-04` Spraying cat climbing mats / play area
![](thumbs/USE-04.jpg)

- **File:** `IMG_1108.MOV`
- **Length:** 5.0s · 2160x3840 · 60fps · static wide · ⚠ HDR
- **What's in it:** Creator sprays stacked gym-mat climbing structure (yellow pyramid), turns to camera.
- **Use for:** 'Spray anywhere they nap or play'
- **Note:** HDR (HLG) HEVC 60fps
- **Tags:** spray, play-area, creator, application

### `USE-05` Spray couch → sit and read WITH the cat (88s)
![](thumbs/USE-05.jpg)

- **File:** `IMG_0165.MOV`
- **Length:** 87.8s · 2160x3840 · 30fps · static wide, long take
- **What's in it:** Hand sprays couch (0:00-0:12), empty couch (0:12-0:28), creator brings in Siamese and sits (0:28-0:40), reads a book with cat cuddled beside her (0:45-1:28).
- **Use for:** Before→after in one shot; 'now I can actually sit with my cat'; happy ending
- **Best section:** 0:00-0:12 spray / 0:45-1:28 cuddle
- **Note:** Long — trim to beats; key 'solution' clip
- **Tags:** spray, couch, creator, cuddle, reading, after, solution, ending

### `USE-06` Siamese sniffing the spray bottle on windowsill
![](thumbs/USE-06.jpg)

- **File:** `IMG_0114.mov`
- **Length:** 6.2s · 2160x3840 · 30fps · static close
- **What's in it:** Pacagen spray bottle on sunny windowsill; Siamese walks over and sniffs it, looks up.
- **Use for:** Cute product+cat moment, 'cat-approved', safe for pets
- **Tags:** spray-bottle, siamese, window, sniff, cute, cat-approved


## Feeding & supplement  (8 clips)

### `FEED-01` Siamese eats from bowl next to supplement tub
![](thumbs/FEED-01.jpg)

- **File:** `Cat eating the supplements .mov` (also uploaded as `IMG_0126.mov`)
- **Length:** 5.2s · 2160x3840 · 30fps · static medium
- **What's in it:** On kitchen counter: supplement tub left, Siamese eating from white bowl, looks at camera mid-way.
- **Use for:** 'I just add a scoop to her food', supplement proof
- **Note:** Same file as IMG_0126
- **Tags:** supplement, eating, siamese, counter, bowl

### `FEED-02` Siamese eats next to tub — push-in
![](thumbs/FEED-02.jpg)

- **File:** `Cat next to supplement while eating.mov`
- **Length:** 7.2s · 2160x3840 · 30fps · push-in
- **What's in it:** Same set-up, slow push-in from wide to close on cat's face eating.
- **Use for:** Alt of FEED-01, more cinematic
- **Tags:** supplement, eating, siamese, push-in

### `FEED-03` Creator sets out bowls — then rubs nose
![](thumbs/FEED-03.jpg)

- **File:** `IMG_0107.mov`
- **Length:** 17.7s · 2160x3840 · 30fps · static wide
- **What's in it:** Creator places three white bowls on kitchen counter (0:02-0:12), then rubs face/nose (0:13-0:14, allergy moment) and walks off.
- **Use for:** Food prep / routine; 0:13 nose-rub doubles as allergy-symptom beat
- **Best section:** 0:02-0:14
- **Tags:** creator, bowls, kitchen, routine, allergy-symptom, sneeze

### `FEED-04` Ragdoll eating at feeding tray
![](thumbs/FEED-04.jpg)

- **File:** `Cat eating .mov` (also uploaded as `IMG_0171.mov`)
- **Length:** 4.7s · 2160x3840 · 30fps · static close
- **What's in it:** Fluffy ragdoll eating from white bowl on black feeding tray, water fountain beside.
- **Use for:** Daily routine, supplement-in-food B-roll
- **Note:** Same file as IMG_0171
- **Tags:** ragdoll, eating, feeding-tray, bowl

### `FEED-05` Ragdoll eating — wide, low-res
![](thumbs/FEED-05.jpg)

- **File:** `cat eating.MOV` (also uploaded as `IMG_8761.MOV`)
- **Length:** 5.8s · 720x1280 · 30fps · static wide · ⚠ 720x1280
- **What's in it:** Ragdoll eating at tray from a wide angle, door behind.
- **Use for:** Backup only
- **Note:** 720p only — low quality; same file as IMG_8761
- **Tags:** ragdoll, eating, feeding-tray

### `FEED-06` Ragdoll walks up to camera past food tray
![](thumbs/FEED-06.jpg)

- **File:** `IMG_0170.mov`
- **Length:** 3.5s · 2160x3840 · 30fps · static, subject walks in
- **What's in it:** Ragdoll walks down the hallway towards camera past the food tray, ends in tight face close-up.
- **Use for:** Hook / attention grab, 'meet my cat'
- **Note:** Great hook opener
- **Tags:** ragdoll, walk-to-camera, face, closeup, hook

### `FEED-07` Feeding station tray — slow pan
![](thumbs/FEED-07.jpg)

- **File:** `IMG_0169.MOV`
- **Length:** 3.0s · 2160x3840 · 30fps · pan
- **What's in it:** Pan across black tray: wet food bowls, kibble, water fountain.
- **Use for:** Routine / setting the scene
- **Tags:** feeding-tray, bowls, fountain, establishing

### `FEED-08` Kibble bowls + water fountain push-in
![](thumbs/FEED-08.jpg)

- **File:** `IMG_0151.MOV`
- **Length:** 2.9s · 2160x3840 · 30fps · push-in
- **What's in it:** Close push-in over kibble bowls to stainless water fountain.
- **Use for:** Routine / transitional
- **Tags:** kibble, fountain, closeup


## Problem — cat hair / allergy  (3 clips)

### `PROB-01` Picking cat hair out of cat bed
![](thumbs/PROB-01.jpg)

- **File:** `Cat hair everywhere grabbing the hair.MOV` (also uploaded as `IMG_0144.MOV`)
- **Length:** 7.3s · 2160x3840 · 30fps · static close
- **What's in it:** Hand pinches clumps of cat hair from a fluffy round cat bed by a sunny window and shows it to camera.
- **Use for:** 'Cat hair EVERYWHERE', pain point / hook
- **Note:** Same file as IMG_0144
- **Tags:** cat-hair, cat-bed, hand, problem, hook

### `PROB-02` Lint-rolling cat hair off shirt
![](thumbs/PROB-02.jpg)

- **File:** `Lint rolling Cat hair.MOV` (also uploaded as `IMG_0146.MOV`)
- **Length:** 13.6s · 2160x3840 · 30fps · handheld selfie-style
- **What's in it:** Creator in green tee lint-rolls cat hair off her shirt and pants, then shows the hairy roller close to camera.
- **Use for:** 'I was lint rolling 5 times a day', pain point
- **Note:** Same file as IMG_0146
- **Tags:** lint-roller, cat-hair, creator, clothes, problem

### `PROB-03` Brushing hair off shirt, waving it away
![](thumbs/PROB-03.jpg)

- **File:** `IMG_0145.MOV`
- **Length:** 8.2s · 2160x3840 · 30fps · handheld selfie-style
- **What's in it:** Creator in striped window-light brushes cat hair off shirt, flicks hand, shrugs — frustrated vibe.
- **Use for:** Pain point, frustration reaction
- **Best section:** 0:01-0:07
- **Tags:** cat-hair, creator, clothes, frustrated, problem


## Air purifier — 'what I tried before'  (3 clips)

### `AIR-01` Air purifier → pan up to Siamese on cat tree
![](thumbs/AIR-01.jpg)

- **File:** `Air filter.MOV` (also uploaded as `IMG_0153.MOV`)
- **Length:** 8.6s · 2160x3840 · 30fps · pan / tilt up
- **What's in it:** Starts on air purifier, pans up wall past hammock and clock to Siamese lounging on top of cat tree.
- **Use for:** 'I tried air purifiers…', 'other solutions didn't work'
- **Note:** Same file as IMG_0153
- **Tags:** air-purifier, siamese, cat-tree, clock, pan

### `AIR-02` Air purifier display push-in
![](thumbs/AIR-02.jpg)

- **File:** `IMG_0152.MOV`
- **Length:** 4.6s · 2160x3840 · 30fps · push-in / pull-out
- **What's in it:** Push-in to the air purifier's green ring display, then pull back out.
- **Use for:** 'Running my purifier 24/7' — what I tried before
- **Tags:** air-purifier, display, closeup

### `AIR-03` Siamese on tree → pan down to air purifier
![](thumbs/AIR-03.jpg)

- **File:** `IMG_0154.MOV`
- **Length:** 6.2s · 2160x3840 · 30fps · pan / tilt down
- **What's in it:** Reverse of AIR-01: starts on Siamese by clock, pans down the wall to the air purifier.
- **Use for:** Alt of AIR-01
- **Tags:** air-purifier, siamese, cat-tree, pan


## Problem — cat locked out of the room  (3 clips)

### `DOOR-01` Open door → Siamese sitting waiting outside
![](thumbs/DOOR-01.jpg)

- **File:** `Cat waiting at door.MOV` (also uploaded as `IMG_0164.MOV`)
- **Length:** 4.4s · 2160x3840 · 30fps · handheld POV
- **What's in it:** Hand opens bedroom door to reveal Siamese sitting on the carpet waiting.
- **Use for:** 'I had to lock her out of my bedroom', emotional pain point
- **Note:** Same file as IMG_0164
- **Tags:** door, siamese, waiting, sad, locked-out, pov

### `DOOR-02` Siamese walking outside door gap
![](thumbs/DOOR-02.jpg)

- **File:** `Cat locked out waiting.MOV` (also uploaded as `IMG_0162.MOV`)
- **Length:** 4.2s · 2160x3840 · 30fps · static through door gap
- **What's in it:** Through a door gap, Siamese wanders in the hallway outside.
- **Use for:** Locked-out beat
- **Note:** Same file as IMG_0162
- **Tags:** door, siamese, locked-out

### `DOOR-03` Door closing on Siamese
![](thumbs/DOOR-03.jpg)

- **File:** `IMG_0161.MOV`
- **Length:** 5.1s · 2160x3840 · 30fps · static through door
- **What's in it:** Siamese walks out, hand closes the door on her, door reopens with her outside.
- **Use for:** 'Shutting the door on her every night'
- **Tags:** door, siamese, closing, locked-out


## Bonding / cuddles — the 'after'  (4 clips)

### `BOND-01` Petting ragdoll on bed
![](thumbs/BOND-01.jpg)

- **File:** `IMG_0131.MOV`
- **Length:** 10.7s · 2160x3840 · 30fps · static close
- **What's in it:** Hand reaches in and pets ragdoll who rolls over on bed.
- **Use for:** After / 'now I can cuddle without sneezing'
- **Tags:** ragdoll, petting, hand, bonding, after, solution

### `BOND-02` Scratching ragdoll's head
![](thumbs/BOND-02.jpg)

- **File:** `IMG_0134.MOV`
- **Length:** 11.9s · 2160x3840 · 30fps · static medium
- **What's in it:** Hand strokes and scratches sitting ragdoll's head and chin; cat leans in.
- **Use for:** After / bonding
- **Tags:** ragdoll, petting, hand, bonding, after

### `BOND-03` Belly rubs — ragdoll on back
![](thumbs/BOND-03.jpg)

- **File:** `IMG_0136.MOV`
- **Length:** 13.6s · 2160x3840 · 30fps · static close
- **What's in it:** Ragdoll lying on back, hand rubs belly and chest.
- **Use for:** After / affection
- **Tags:** ragdoll, petting, belly, bonding, after

### `BOND-04` Petting ragdoll — cat closes eyes
![](thumbs/BOND-04.jpg)

- **File:** `IMG_0139.mov`
- **Length:** 14.9s · 2160x3840 · 30fps · static close
- **What's in it:** Hand pets ragdoll's head, cat closes eyes happily.
- **Use for:** After / content cat
- **Tags:** ragdoll, petting, bonding, after, content


## Siamese lifestyle filler  (9 clips)

### `SIA-01` Siamese playing with feather wand
![](thumbs/SIA-01.jpg)

- **File:** `IMG_0122.mov`
- **Length:** 5.7s · 2160x3840 · 30fps · static close
- **What's in it:** Siamese on her back batting a colourful feather wand toy on the carpet.
- **Use for:** Playful filler, 'healthy happy cat'
- **Tags:** siamese, play, feather-toy, cute

### `SIA-02` Siamese rolling with feather toy
![](thumbs/SIA-02.jpg)

- **File:** `IMG_0123.mov`
- **Length:** 3.8s · 2160x3840 · 30fps · static wide
- **What's in it:** Siamese lying on side chewing/rolling with feather toys.
- **Use for:** Playful filler
- **Tags:** siamese, play, feather-toy

### `SIA-03` Siamese play session (14s)
![](thumbs/SIA-03.jpg)

- **File:** `IMG_0124.mov`
- **Length:** 14.2s · 2160x3840 · 30fps · static medium
- **What's in it:** Longer play session: wand dangles, Siamese grabs and kicks the feather toy.
- **Use for:** Playful filler, longer
- **Tags:** siamese, play, feather-toy

### `SIA-04` Siamese on windowsill about to jump down
![](thumbs/SIA-04.jpg)

- **File:** `IMG_0113.mov`
- **Length:** 2.1s · 2160x3840 · 30fps · static
- **What's in it:** Siamese crouched on sunny windowsill above a grey donut bed.
- **Use for:** Quick filler
- **Note:** Short (2s)
- **Tags:** siamese, window, sunlight

### `SIA-05` Siamese leaves window bed, walks the room
![](thumbs/SIA-05.jpg)

- **File:** `cat by window moving around.mov`
- **Length:** 6.2s · 2160x3840 · 30fps · handheld follow
- **What's in it:** Siamese in window bed hops down and walks across the room; handheld follow.
- **Use for:** Day-in-the-life filler
- **Tags:** siamese, window, walk, follow

### `SIA-06` Siamese walking wall shelves → cat tree
![](thumbs/SIA-06.jpg)

- **File:** `IMG_0147.MOV`
- **Length:** 13.0s · 2160x3840 · 30fps · handheld follow
- **What's in it:** Siamese walks along wall-mounted cat shelves then onto top of tall cat tree.
- **Use for:** Filler, 'she's everywhere in the house'
- **Tags:** siamese, wall-shelves, cat-tree, climb

### `SIA-07` Siamese stepping onto wall hammock
![](thumbs/SIA-07.jpg)

- **File:** `IMG_0148.MOV`
- **Length:** 3.2s · 2160x3840 · 30fps · static low angle
- **What's in it:** Siamese steps down onto a wall-mounted hammock shelf, low angle.
- **Use for:** Filler
- **Tags:** siamese, wall-shelves, climb

### `SIA-08` Siamese on wall hammock, looks at camera
![](thumbs/SIA-08.jpg)

- **File:** `IMG_0149.MOV`
- **Length:** 5.0s · 2160x3840 · 30fps · static close low angle
- **What's in it:** Siamese standing on wall hammock, looks at camera, turns.
- **Use for:** Filler / reaction cut
- **Tags:** siamese, wall-shelves, look-at-camera

### `SIA-09` Siamese on cat tree by clock → jumps to shelf
![](thumbs/SIA-09.jpg)

- **File:** `IMG_0150.MOV`
- **Length:** 8.8s · 2160x3840 · 30fps · handheld
- **What's in it:** Siamese on carpeted cat tree next to clock, leaps onto wall perch.
- **Use for:** Filler with action
- **Tags:** siamese, cat-tree, clock, jump


## Ragdoll lifestyle filler  (12 clips)

### `RAG-01` Ragdoll on bed — stares into camera
![](thumbs/RAG-01.jpg)

- **File:** `IMG_0132.MOV`
- **Length:** 9.9s · 2160x3840 · 30fps · push-in, eye-level
- **What's in it:** Grey ragdoll lying on white bed, camera moves in, cat stares straight into lens.
- **Use for:** Hook / reaction / 'meet my other cat'
- **Note:** Strong hero shot
- **Tags:** ragdoll, bed, stare, look-at-camera, hook

### `RAG-02` Ragdoll close-up — judgy stare
![](thumbs/RAG-02.jpg)

- **File:** `IMG_0138.mov`
- **Length:** 5.1s · 2160x3840 · 30fps · push-in close-up
- **What's in it:** Push-in to ragdoll's face, blue eyes, judgy expression.
- **Use for:** Funny reaction cut, hook
- **Tags:** ragdoll, face, closeup, stare, funny, reaction, hook

### `RAG-03` Ragdoll on bed — profile then front
![](thumbs/RAG-03.jpg)

- **File:** `IMG_0133.MOV`
- **Length:** 7.9s · 2160x3840 · 30fps · handheld orbit
- **What's in it:** Ragdoll loaf on bed, camera circles from profile to front.
- **Use for:** Cute filler
- **Tags:** ragdoll, bed, orbit

### `RAG-04` Ragdoll loaf on bed, wooden dresser behind
![](thumbs/RAG-04.jpg)

- **File:** `IMG_0135.MOV`
- **Length:** 5.0s · 2160x3840 · 30fps · static
- **What's in it:** Calm ragdoll lying on bed, subtle movement.
- **Use for:** Calm filler
- **Tags:** ragdoll, bed, calm

### `RAG-05` Ragdoll on bed — handheld around
![](thumbs/RAG-05.jpg)

- **File:** `IMG_0141.mov`
- **Length:** 10.6s · 2160x3840 · 30fps · handheld orbit
- **What's in it:** Camera moves around ragdoll on bed from several angles.
- **Use for:** Filler
- **Tags:** ragdoll, bed, orbit

### `RAG-06` Ragdoll lying → sits up, looks away
![](thumbs/RAG-06.jpg)

- **File:** `IMG_0140.mov`
- **Length:** 6.9s · 2160x3840 · 30fps · static low
- **What's in it:** Ragdoll lying on bed then sits up and turns head.
- **Use for:** Filler
- **Tags:** ragdoll, bed

### `RAG-07` Ragdoll grooming on bed
![](thumbs/RAG-07.jpg)

- **File:** `Grooming on bed.mov` (also uploaded as `IMG_0137.mov`)
- **Length:** 7.0s · 2160x3840 · 30fps · slow pull-back
- **What's in it:** Ragdoll lying on bed grooming / looking around, door behind.
- **Use for:** Calm filler
- **Note:** Same file as IMG_0137
- **Tags:** ragdoll, bed, grooming

### `RAG-08` Ragdoll stretched out — push-in to face
![](thumbs/RAG-08.jpg)

- **File:** `IMG_0130.MOV`
- **Length:** 4.3s · 2160x3840 · 30fps · push-in
- **What's in it:** Ragdoll lying stretched on bed; push-in to relaxed face.
- **Use for:** Relaxed / 'finally calm' beat
- **Tags:** ragdoll, bed, relaxed, push-in

### `RAG-09` Ragdoll in fabric cube on cat shelf
![](thumbs/RAG-09.jpg)

- **File:** `IMG_0127.MOV`
- **Length:** 8.8s · 2160x3840 · 30fps · static low angle
- **What's in it:** Ragdoll lounging inside a black fabric cube bed on top of white furniture, low angle.
- **Use for:** Filler
- **Tags:** ragdoll, cube-bed, lounging

### `RAG-10` Ragdoll on couch in sunlight stripes
![](thumbs/RAG-10.jpg)

- **File:** `cat in house - filler video.mov`
- **Length:** 2.8s · 2160x3840 · 30fps · static
- **What's in it:** Ragdoll on couch with striped window light across fur.
- **Use for:** Aesthetic filler
- **Tags:** ragdoll, couch, sunlight, aesthetic

### `RAG-11` Ragdoll by window → walks to camera
![](thumbs/RAG-11.jpg)

- **File:** `rag doll by window .mov`
- **Length:** 9.0s · 2160x3840 · 30fps · handheld follow
- **What's in it:** Ragdoll on window cubby shelf hops down and walks toward camera past cat trees.
- **Use for:** Filler
- **Tags:** ragdoll, window, walk

### `RAG-12` Ragdoll hides under trampoline
![](thumbs/RAG-12.jpg)

- **File:** `ragdoll hide.mov`
- **Length:** 4.0s · 2160x3840 · 30fps · static low
- **What's in it:** Ragdoll looks at camera then crawls under a mini trampoline to hide.
- **Use for:** Funny beat / 'my cat when I get the lint roller out'
- **Tags:** ragdoll, hide, funny
