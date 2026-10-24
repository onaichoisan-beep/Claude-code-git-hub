# SPEC: How malaria infects you

GOAL:    The viewer can retell the path: bite → liver (hidden a week) → red blood cells burst in waves → fever → next mosquito.
OUTPUT:  HyperFrames, 1080 x 1920, 30 fps
TIME:    49.5 s x 30 = 1485 frames. Narrated; the voice (assets/audio/vo.wav, transcript.json) is the clock.

LOOK:    3D realistic explainer (video-playbook/3D_REALISTIC_STYLE.md).
         Two grounds only: real macro skin (warm, #d9a184 base, pores + fine lines, sheen 0.6)
         and anatomy cutaways on flat cyan #34c3df → #1fa6c9 radial (the reference films' cross-section ground).
         Tissue palette from the references: dermis #e8a49a, fat #f2cf45 (yellow lobules), blood #b3121f,
         vessel wall #c9545c, parasite #6fd36a (green, the one accent: it marks the enemy in every shot).
         Captions: Montserrat 800, 78 px, white, shadow 0 4px 10px rgba(0,0,0,.55), 1-3 words, centre y = 1250.
         Labels in the scene: Montserrat 800, 54 px, white with the same shadow, appear on the part they name.
         Light: warm key (#fff1e0, upper left), cool rim (#9fe6ff, behind), env made of 3 soft strips (PMREM).
OBJECTS: Anopheles mosquito (body tilted ~40° head-down, spotted wings, long palps + proboscis, 6 jointed legs,
         abdomen that swells red when it drinks); skin block cutaway (epidermis, dermis, yellow fat, open capillary);
         biconcave red blood cells; sporozoites (slender curved green worms); liver (glossy maroon lobe);
         hepatocytes (rounded honeycomb cells); merozoites (small green teardrops); 3D glass thermometer; sweat drops.
MOTION:  Enter expo.out, camera power2.inOut, zoom-through / burst power3.in. One hero move per shot.
         Cuts are whips (0.2 s smear) or dives into an object (the next world is inside it). Camera never static.
SHOTS:
  s1  0.0-3.0   mosquito on skin, macro; proboscis bends down and pierces at 0.82 "bite"; buzz then squish
  s2  3.0-8.4   skin cutaway on cyan; proboscis through layers into the open capillary; green worms pour out 5.2-6.6; label SPOROZOITES 6.2
  s3  8.4-14.4  ride inside the vessel with cells streaming past (label UNDER 1 HOUR 8.6); 11.0 liver lobe; 11.7 dive to hepatocytes; worm slips into one cell 12.3-13.2
  s4  14.4-21.2 one liver cell, cut open; DAY 1→7 counter 14.6-16.6; merozoites multiply to hundreds by 19.8
  s5  21.2-27.0 cell swells, bursts 22.08; whip into blood 23.4; merozoite burrows into a red cell 25.0-26.2
  s6  27.0-35.3 one red cell, translucent; ring parasite eats red haemoglobin 28.1; splits into 16 at 29.2; explodes 30.98; pull back, they hit new cells 33.0
  s7  35.3-43.1 field of cells bursting in a wave 36.5; brown waste spreads 37.8; thermometer 37→40 °C 38.6-41.2 (label 40°C at 40.74); skin: goosebumps 41.24, sweat 41.84
  s8  43.1-49.5 new mosquito lands on the sweaty skin, bites 44.16, abdomen fills red, green dots ride up the proboscis 45.5; push in; last frame echoes frame 0
BANNED:  dark void ground; glow/bloom/lens flares; floating decorative particles; corner labels / HUD;
         text moving while read; every shot entering the same way; legends and bullet lists.
QA:      t=0.2 (thumbnail: mosquito on skin), 6.4 (worms + label), 12.6 (liver cells), 19.5 (full cell),
         22.2 (burst), 30.9 (red cell burst), 40.8 (40°C), 42.2 (sweat), 45.8 (abdomen red), 49.3 (loop frame).
