#!/usr/bin/env python3
"""Regenerate obtainium-import.json and aurora-checklist.md from apps.py."""

from __future__ import annotations

import json
from pathlib import Path

from apps import AURORA, BOOTSTRAP, OBTAINIUM

HERE = Path(__file__).parent

SOURCE_OVERRIDE = {
    "github": "GitHub",
    "fdroid": "F-Droid",
    "html": "HTML",
}

# Minimal viable additionalSettings. Obtainium fills in the rest on import.
DEFAULT_SETTINGS = {
    "includePrereleases": False,
    "fallbackToOlderReleases": True,
    "trackOnly": False,
    "versionDetection": True,
    "autoApkFilterByArch": True,
    "apkFilterRegEx": "",
    "invertAPKFilter": False,
}


def obtainium_entry(app: dict) -> dict:
    settings = dict(DEFAULT_SETTINGS)
    if app.get("apk_asset_filter"):
        settings["apkFilterRegEx"] = app["apk_asset_filter"]
    return {
        "id": app["id"],
        "url": app["url"],
        "name": app["name"],
        "author": app.get("author", ""),
        "preferredApkIndex": 0,
        "additionalSettings": json.dumps(settings),
        "categories": [],
        "allowIdChange": True,
        "overrideSource": SOURCE_OVERRIDE[app["source"]],
    }


def write_obtainium() -> None:
    apps = [obtainium_entry(a) for a in BOOTSTRAP + OBTAINIUM]
    out = HERE / "obtainium-import.json"
    out.write_text(json.dumps({"apps": apps}, indent=2) + "\n")
    print(f"wrote {out.name}: {len(apps)} apps")


def write_aurora_checklist() -> None:
    lines = [
        "# Aurora Store tap-through checklist",
        "",
        "Open Aurora Store → search by name (or paste the package id into the",
        "URL bar of your browser at `market://details?id=<pkg>` if you prefer).",
        "Check each off as you install. **SGP** marks apps that will want",
        "Sandboxed Google Play for push/Play-Integrity.",
        "",
    ]
    for pkg, name, sgp in AURORA:
        tag = " **[SGP]**" if sgp else ""
        lines.append(f"- [ ] `{pkg}` — {name}{tag}")
    lines.append("")
    out = HERE / "aurora-checklist.md"
    out.write_text("\n".join(lines))
    print(f"wrote {out.name}: {len(AURORA)} apps")


if __name__ == "__main__":
    write_obtainium()
    write_aurora_checklist()
