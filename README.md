# GrapheneOS phone provisioning

Curated install list for a fresh GrapheneOS phone.

## Files

- `apps.py` — source of truth; edit when your app list changes
- `build.py` — regenerates the two artifacts below
- `obtainium-import.json` — Obtainium import (FOSS + direct-vendor apps)
- `aurora-checklist.md` — tap-through list for Aurora Store apps

## Procedure for a new phone

1. **Flash GrapheneOS** via the web installer.
2. **Enable ADB**: Settings → About → tap build number 7×, then Developer
   options → USB debugging.
3. **Install Obtainium** (only true bootstrap):
   ```sh
   # Get the latest APK from https://github.com/ImranR98/Obtainium/releases
   # Grab `app-release.apk` (universal) — the `*-fdroid-*.apk` files are
   # the same code under a different applicationId for F-Droid's update
   # channel; either works, but the standard build is the simplest path.
   adb install ~/Downloads/app-release.apk
   ```
4. **Push the import file** and open Obtainium:
   ```sh
   adb push obtainium-import.json /sdcard/Download/
   ```
   In Obtainium: Settings → Import/Export → Obtainium Import → pick the
   file. The apps now show in the list flagged as "Update available" (since
   they're not yet installed). To install them in bulk: long-press any app
   to enter selection mode → use the "Select All" action in the top bar →
   tap the install/update action in the bottom bar. Approve the install
   prompt for each (Android requires per-install consent on the first run;
   after that you can grant Obtainium "install unknown apps" permission to
   make subsequent installs silent).
5. **Install Sandboxed Google Play** (only if you want any SGP-flagged apps
   in the checklist to work properly):
   - Open the GOS **Apps** app (pre-installed)
   - Install "GrapheneOS Sandboxed Google Play"
   - Open Play Store and sign in (or don't — up to you)
6. **Tap through `aurora-checklist.md`**. Open Aurora Store (installed via
   Obtainium in step 4), choose "Anonymous", then search each app and
   install. Check entries off as you go.

## When your app list changes

1. Edit `apps.py`
2. `python3 build.py`
3. Commit the two generated files so they're in sync.

## Re-deriving the list from a current phone

```sh
adb shell pm list packages -3 | sort | sed 's/^package://' > packages-current.txt
# Diff against apps.py to see what drifted
```

## When something fails in Obtainium

The error "could not find a suitable release" means Obtainium found the
source but couldn't match a downloadable APK. Common causes:

- The project doesn't publish APK assets to GitHub Releases (they only
  ship via F-Droid or Play). Fix: change source to F-Droid in `apps.py`.
- The project is Play-only (no FOSS or direct-vendor distribution). Fix:
  move it to the `AURORA` list.
- The vendor's HTML page renders APK links via JavaScript and Obtainium
  can't see them (e.g. Signal). Fix: use the "Direct APK Link" source
  with a stable URL, or the `HTML` source with a custom regex.

To check whether a GitHub project actually ships APKs:

```sh
gh release view --repo OWNER/NAME --json assets --jq '.assets[].name'
```
