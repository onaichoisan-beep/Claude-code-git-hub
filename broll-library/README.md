# B-roll library

Catalogued B-roll for UGC edits, one folder per brand. The video files stay on Google Drive. This folder holds:

- `<brand>/CATALOG.md`: read this first. It has a story map (which clip fits which ad beat), a quick index, and every clip with frame strips, a description, best section, notes and tags.
- `<brand>/catalog.json`: the same data in machine-readable form (Drive file IDs, duration, resolution, fps, HDR flag, tags).
- `<brand>/thumbs/`: a 6-frame strip for each clip.
- `fetch.py`: downloads clips from Drive into `<brand>/media/NN_category/ID_name.ext` (gitignored).

| Brand | Clips | Drive |
|---|---|---|
| [Pacagen](pacagen/CATALOG.md) | 56 | [folder](https://drive.google.com/drive/folders/1-7sQpKl0AAn6fOKnXBuczjWl4ajC3mjG) |

## Adding a new brand
Share the Drive folder link with Claude and ask it to "add it to the B-roll library". Claude downloads the clips, watches frame strips, removes duplicates, and writes a new `<brand>/` folder in the same format.
