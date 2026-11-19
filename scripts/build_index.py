#!/usr/bin/env python3
"""Scans projects/*/ and writes projects/index.json for the website.

Folder layout (see README.md):
  projects/<anything-sortable>/info.txt
  projects/<...>/photo.(jpg|png|webp|svg)
  projects/<...>/media/*  (screenshots, gifs, mp4s -- shown in filename order)
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = ROOT / "projects"
IMG = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".avif"}
VID = {".mp4", ".webm", ".mov"}


def parse_info(path):
    """Header lines `key: value`, then a line of `---`, then the story text."""
    text = path.read_text(encoding="utf-8-sig")
    head, _, body = text.partition("\n---")
    if not _:  # no separator: treat whole file as header-less story
        head, body = "", text
    data = {"links": []}
    for line in head.splitlines():
        m = re.match(r"\s*([A-Za-z_]+)\s*:\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1).lower(), m.group(2).strip()
        if key in ("download", "link"):
            label, sep, url = val.rpartition("|")
            if not sep:
                label, url = ("Download" if key == "download" else "Visit"), val
            data["links"].append({"label": label.strip(), "url": url.strip(),
                                  "kind": key})
        else:
            data[key] = val
    data["story"] = body.strip().lstrip("-").strip()
    return data


def rel(p):
    return p.relative_to(ROOT).as_posix()


def main():
    items = []
    for d in sorted(PROJECTS.iterdir()):
        if not d.is_dir() or d.name.startswith((".", "_")):
            continue
        info_file = d / "info.txt"
        if not info_file.exists():
            print(f"skip {d.name}: no info.txt", file=sys.stderr)
            continue
        info = parse_info(info_file)
        photo = next((f for f in sorted(d.glob("photo.*"))
                      if f.suffix.lower() in IMG), None)
        media = []
        mdir = d / "media"
        if mdir.is_dir():
            for f in sorted(mdir.iterdir(), key=lambda f: f.name.lower()):
                ext = f.suffix.lower()
                if ext in IMG:
                    media.append({"type": "image", "src": rel(f)})
                elif ext in VID:
                    media.append({"type": "video", "src": rel(f)})
        items.append({
            "id": d.name,
            "name": info.get("name", d.name),
            "app": info.get("app", ""),
            "tagline": info.get("tagline", ""),
            "date": info.get("date", ""),
            "story": info["story"],
            "links": info["links"],
            "photo": rel(photo) if photo else "",
            "media": media,
            "_sort": info.get("date") or d.name,
        })
    # newest first (by `date:` if given, else by folder name)
    items.sort(key=lambda i: i["_sort"], reverse=True)
    for i in items:
        del i["_sort"]
    out = PROJECTS / "index.json"
    out.write_text(json.dumps(items, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    print(f"wrote {rel(out)} with {len(items)} project(s)")


if __name__ == "__main__":
    main()
