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
   - Install "GrapheneOS Sandboxed Google Play" — this pulls in
     `com.android.vending` (Play Store) and `com.google.android.gms`
     (Play services)
   - While you're in GOS Apps, install **Android Auto**
     (`com.google.android.projection.gearhead`) if you want it; it ships
     there, *not* via Aurora
   - Open Play Store and sign in (or don't — up to you)
6. **Tap through `aurora-checklist.md`**. Open Aurora Store (installed via
   Obtainium in step 4), choose "Anonymous", then search each app and
   install. Check entries off as you go.

## When your app list changes

1. Edit `apps.py`
2. `python3 build.py`
3. Commit the two generated files so they're in sync.

## Re-deriving the list from a current phone

Do this before switching phones, so the new one gets what you actually use.

1. **Which apps are installed, and where each came from.** The `-i` flag
   prints the installer, which is what decides whether an app belongs in
   `OBTAINIUM` or `AURORA`:

   ```sh
   adb shell pm list packages -3 -i | sed 's/^package://' | sort
   ```

   Read the installers as:

   | installer                    | belongs in                             |
   | ---------------------------- | -------------------------------------- |
   | `dev.imranr.obtainium`       | `OBTAINIUM`                            |
   | `com.aurora.store`           | `AURORA`                               |
   | `app.grapheneos.apps`        | neither — it's step 5 (SGP/Android Auto) |
   | `com.android.packageinstaller` | sideloaded by hand                    |

2. **Exact Obtainium sources.** The package list can't tell you *which*
   URL, APK filter, or source type an Obtainium app uses. Export them:
   Obtainium → Settings → Import/Export → "Obtainium Export", then

   ```sh
   adb shell ls /sdcard/Documents /sdcard/Download   # find the export
   adb pull /sdcard/Documents/obtainium-export-*.json
   ```

   That file is authoritative for the `OBTAINIUM` half of `apps.py` —
   `url`, `overrideSource`, `preferredApkIndex`, and `additionalSettings`
   map onto the fields documented at the top of `apps.py`.

3. Diff both against `apps.py`, edit, and re-run `python3 build.py`.

Two entries are deliberately *not* expected to match a phone dump:
`org.fdroid.fdroid` is carried in `OBTAINIUM` so a fresh phone gets
F-Droid from the import even if the old phone had it sideloaded, and the
GOS Apps packages from step 5 never appear in either list.

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
