# My App Showcase

## Adding a project

1. Copy the `projects/000-example-person` folder and rename it, e.g. `projects/2026-12-acme-co`.
   Newest first: folders sort by the optional `date:` line in `info.txt`, otherwise by folder name.
2. Edit `info.txt`.
3. Replace `photo.*` with their photo (any of jpg/png/webp/svg; must be named `photo`).
4. Put screenshots / GIFs / mp4s in `media/`. They show in filename order (`01-home.png`, `02-settings.png`, ...).
5. Commit and push. A GitHub Action rebuilds `projects/index.json` automatically and the site updates in about a minute.

## info.txt

```
name: Jane Example                 <- shown under the photo
app: Recipe Keeper                 <- the app's name (optional)
tagline: One line about the app    (optional)
date: 2026-11-01                   (optional, used for ordering)
download: Download for Windows | https://link    <- green-ish primary button, add as many as you like
link: Source on GitHub | https://link            <- secondary button
---
Everything after the dashes is the "idea" text box. Blank line = new paragraph.
```

## Local preview

```
python scripts/build_index.py
python -m http.server
```
then open http://localhost:8000. (Running the script locally is optional; the Action does it on push.)

The previous page lives in `archive/old-index.html`.
