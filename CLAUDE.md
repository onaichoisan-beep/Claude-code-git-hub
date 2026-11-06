# Project notes

The user is a freelance UGC video editor.

## B-roll library
`broll-library/` catalogues the user's client B-roll. Before suggesting or cutting B-roll for a client, read `broll-library/<brand>/CATALOG.md` and refer to clips by their IDs (e.g. `USE-05`). To pull files: `pip install gdown && python3 broll-library/fetch.py <brand> [--id X] [--tag Y] [--category Z]`. To add a new brand, follow `broll-library/README.md`. Never commit video files: `media/` is gitignored.
