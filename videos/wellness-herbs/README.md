# Find the Plant — wellness reel (9:16, 23 s)

A HyperFrames edit of the client's wellness interview, using the "Interest Media" reference's editing approach. B-roll, music and SFX all come from Mixkit (free licence).

## Rebuild

```bash
tools/prep.sh /path/to/client.mp4      # crops, trims, cut-out, Mixkit downloads, audio mix
npx hyperframes@0.9.38 check
npx hyperframes@0.9.38 render -o renders/find-the-plant.mp4
```

Client footage, and anything made from it, is kept out of git (see `.gitignore`).

## Edit map (output seconds)

| Time | Beat | Picture |
|---|---|---|
| 0.00–2.92 | Hook: "Right now, wellness is in a precarious place" | Cam A, 112%→100% settle, name tag, terracotta accent pill |
| 2.92–4.99 | "…losing the plot" | Mixkit pill pile + "losing the plot" pill |
| 4.99–8.27 | "The point is to be healthy and well, right?" | Flash and blur into Cam B wide shot, cut to the interviewer on "right?" |
| 8.27–11.69 | "Not necessarily to consume or over-consume" | Phone shopping clip, cart counter 1→27, zoom out to a wall of products, ticking audio |
| 11.69–14.79 | "There is an herb for everything. So for anxiety," | Flash into the ocean angle; ticking stops |
| 14.79–18.25 | "…nervines. Lavender is a perfect example." | Linen gradient world, herbal-tea card then lavender card, definition pills |
| 18.25–23.00 | "Chamomile, valerian, kava, rose, passionflower." | Her cut-out over a blurred lavender field, five herb pills joined by a growing stem, ending in a bloom |

Name tag text is a placeholder (`[Client Name]`); edit it in `index.html`.

## Mixkit sources

- **B-roll:** various-medications-16448, woman-exploring-an-online-sales-page-on-her-cell-phone-42136, different-medications-5697, lot-of-pills-and-capsules-turning-34235, medications-piled-up-2856, prescription-bottles-and-medication-16420, woman-with-red-led-mask-in-a-spa-52163, couple-opening-a-package-with-an-alarm-clock-42122, parcels-on-a-conveyor-belt-20770, capsules-falling-on-a-table-20509, creating-herbal-tea-22670, lavender-flowers-close-up-1244, lavender-in-the-field-close-up-24990
- **Music:** "Serene View" (443)
- **SFX:** 3005, 2357, 1489, 645, 2573, 1125, 1474, 1185, 1107, 3108
