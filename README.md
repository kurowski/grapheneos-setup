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
   In Obtainium: Settings → Import/Export → Obtainium Import → pick the file.
   Tap the "Install All" button.
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

## Known issues / verify-in-Obtainium

A few URLs in `apps.py` are best-guess; if Obtainium fails to resolve them,
fix the URL in the Obtainium UI (it'll offer to auto-detect):

- `com.liamcottle.meshcore.android`
- `de.schliweb.makeacopy`
- `com.seafile.seadroid2`
- `com.anthropic.claude` (may not publish an APK — fall back to Aurora)
