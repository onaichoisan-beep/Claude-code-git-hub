# B-roll library

Catalogued B-roll for UGC edits, one folder per brand. The video files stay on Google Drive. This folder holds:

- `<brand>/CATALOG.md`: read this first. It has a story map (which clip fits which ad beat), a quick index, and every clip with frame strips, a description, best section, notes and tags.
- `<brand>/catalog.json`: the same data in machine-readable form (Drive file IDs, duration, resolution, fps, HDR flag, tags).
- `<brand>/thumbs/`: a 6-frame strip for each clip.
- `build_catalog.py`: regenerates `CATALOG.md` from `catalog.json` after you edit the JSON.
- `fetch.py`: downloads clips from Drive into `<brand>/media/NN_category/ID_name.ext` (gitignored).

| Brand | Clips | Drive |
|---|---|---|
| [Pacagen](pacagen/CATALOG.md) | 210 (shoots A, B, C) | [1](https://drive.google.com/drive/folders/1-7sQpKl0AAn6fOKnXBuczjWl4ajC3mjG) · [2](https://drive.google.com/drive/folders/1Rzp2KmpcLtVEMqLZSZA92K9N5ShiA36Q) · [3](https://drive.google.com/drive/folders/1dcrdbOeYrqY_jpALUPfBRYTECSPseL0h) |

## Adding a new brand
Share the Drive folder link with Claude and ask it to "add it to the B-roll library". Claude downloads the clips, watches frame strips, removes duplicates, and writes a new `<brand>/` folder in the same format.

When new footage for an existing brand arrives, Claude adds it to that brand's catalog.json with a new shoot letter and the next free IDs, then runs `build_catalog.py`. Files are downloaded by Drive file ID, because folders often contain several different files with the same name.
