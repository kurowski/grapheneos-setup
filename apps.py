"""Source of truth for phone provisioning.

Every entry declares:
  id      — package name (used by ADB / Aurora / Obtainium)
  name    — display name
  source  — one of: github | fdroid | html | aurora | aurora_sgp
  url     — for obtainium-fed sources; ignored for aurora*
  notes   — freeform; ends up in generated checklists

Optional:
  apk_asset_filter    — regex over release asset names (Obtainium apkFilterRegEx)
  preferred_apk_index — pick the Nth APK after arch filtering; default 0
  extra_settings      — raw Obtainium additionalSettings overrides

URL heuristics (verify inside Obtainium after import):
  github → https://github.com/<owner>/<repo>
  fdroid → https://f-droid.org/packages/<package>/
  html   → vendor download page
"""

# Obtainium normally reads the version out of the APK and compares it to the
# release tag; when the two legitimately disagree the app is flagged as
# "update available" forever. Turning versionDetection off makes Obtainium
# trust the tag instead.
VERSION_FROM_TAG = {"versionDetection": False}

BOOTSTRAP = [
    # First-time install is via `adb install`; the entry below lets Obtainium
    # track itself for future self-updates.
    {"id": "dev.imranr.obtainium",
     "name": "Obtainium",
     "source": "github",
     "url": "https://github.com/ImranR98/Obtainium",
     # Pick the standard release, not the *-fdroid-*.apk variant (different
     # applicationId for F-Droid's channel; would refuse to update over our
     # adb-installed copy).
     "apk_asset_filter": "^(?!.*fdroid).*\\.apk$"},
]

OBTAINIUM = [
    # Obtainium installs these after import of obtainium-import.json.
    # Includes F-Droid + Aurora so they get managed + auto-updated by Obtainium.

    {"id": "org.fdroid.fdroid", "name": "F-Droid",
     "source": "fdroid", "url": "https://f-droid.org/packages/org.fdroid.fdroid/",
     "notes": "package manager for FOSS"},
    {"id": "com.aurora.store", "name": "Aurora Store",
     "source": "fdroid", "url": "https://f-droid.org/packages/com.aurora.store/",
     "notes": "anonymous Play proxy; used for the tap-through apps below"},

    # FOSS
    {"id": "app.pachli", "name": "Pachli",
     "source": "github", "url": "https://github.com/pachli/pachli-android",
     "notes": "Mastodon client; used alongside the official app"},
    {"id": "at.bitfire.davdroid", "name": "DAVx5",
     "source": "github", "url": "https://github.com/bitfireAT/davx5-ose"},
    {"id": "ch.protonvpn.android", "name": "Proton VPN",
     "source": "github", "url": "https://github.com/ProtonVPN/android-app"},
    {"id": "com.capyreader.app", "name": "Capy Reader",
     "source": "github", "url": "https://github.com/jocmp/capyreader"},
    {"id": "com.chiller3.rsaf", "name": "RSAF",
     "source": "github", "url": "https://github.com/chenxiaolong/RSAF",
     "notes": "rclone as a Storage Access Framework provider"},
    {"id": "com.flipperdevices.app", "name": "Flipper Zero",
     "source": "github", "url": "https://github.com/flipperdevices/Flipper-Android-App"},
    {"id": "com.geeksville.mesh", "name": "Meshtastic",
     "source": "github", "url": "https://github.com/meshtastic/Meshtastic-Android",
     # Releases also carry a `-google-` build plus desktop artifacts, but arch
     # filtering alone lands on androidApp-fdroid-<arch>-release.apk at index 0,
     # so no asset filter is needed.
     "extra_settings": VERSION_FROM_TAG},
    {"id": "com.tailscale.ipn", "name": "Tailscale",
     "source": "github", "url": "https://github.com/tailscale/tailscale-android",
     "extra_settings": VERSION_FROM_TAG},
    {"id": "com.termux", "name": "Termux",
     "source": "github", "url": "https://github.com/termux/termux-app"},
    {"id": "com.termux.styling", "name": "Termux Styling",
     "source": "github", "url": "https://github.com/termux/termux-styling"},
    {"id": "com.wirelessalien.android.moviedb", "name": "ShowCase",
     "source": "github", "url": "https://github.com/WirelessAlien/MovieDB",
     # Assets are [showcase-vX-plus.apk, showcase-vX.apk]; index 1 is the
     # standard build (the "plus" flavour pulls in proprietary GDrive backup).
     "preferred_apk_index": 1},
    {"id": "io.ente.photos.independent", "name": "Ente Photos",
     "source": "github", "url": "https://github.com/ente-io/ente",
     # The monorepo also releases auth/locker; `photos` picks the right asset.
     # Note the `.independent` applicationId — that's the GitHub/F-Droid build,
     # distinct from the Play build's `io.ente.photos`.
     "apk_asset_filter": "photos"},
    {"id": "io.music_assistant.client", "name": "Music Assistant",
     "source": "github", "url": "https://github.com/music-assistant/mobile-app",
     "notes": "repo interleaves ios-* and android-* releases; "
              "fallbackToOlderReleases walks back to the newest android-* tag"},
    {"id": "net.waterfox.android.release", "name": "Waterfox",
     "source": "github", "url": "https://github.com/BrowserWorks/Waterfox-Android",
     "extra_settings": VERSION_FROM_TAG},
    {"id": "org.breezyweather", "name": "Breezy Weather",
     "source": "github", "url": "https://github.com/breezy-weather/breezy-weather"},
    {"id": "org.fairscan.app", "name": "FairScan",
     "source": "github", "url": "https://github.com/pynicolas/FairScan",
     "notes": "document scanner; replaced MakeACopy"},
    {"id": "org.futo.inputmethod.latin", "name": "FUTO Keyboard",
     "source": "github", "url": "https://github.com/futo-org/android-keyboard"},
    {"id": "org.joinmastodon.android", "name": "Mastodon",
     "source": "github", "url": "https://github.com/mastodon/mastodon-android"},
    {"id": "org.tasks", "name": "Tasks.org",
     "source": "github", "url": "https://github.com/tasks/tasks",
     "apk_asset_filter": "-fdroid-",  # not -googleplay-
     "extra_settings": VERSION_FROM_TAG},
    {"id": "xyz.blueskyweb.app", "name": "Bluesky",
     "source": "github", "url": "https://github.com/bluesky-social/social-app"},

    # Direct-vendor (sensitive / security-critical: pull from the source of truth)
    {"id": "org.thoughtcrime.securesms", "name": "Signal",
     "source": "github", "url": "https://github.com/signalapp/Signal-Android",
     "notes": "Signal now ships APKs to GitHub releases"},
    {"id": "md.obsidian", "name": "Obsidian",
     "source": "github", "url": "https://github.com/obsidianmd/obsidian-releases",
     "extra_settings": VERSION_FROM_TAG},
    {"id": "com.liamcottle.meshcore.android", "name": "MeshCore",
     "source": "html", "url": "https://files.liamcottle.net/MeshCore/",
     "notes": "closed source, no GitHub releases; vendor file index. The "
              "intermediateLink hop descends into the newest vX.Y/ directory, "
              "then the APK is picked from there.",
     "extra_settings": {
         "versionDetection": False,
         "intermediateLink": [{
             "customLinkFilterRegex": "v[0-9]+\\.",
             "autoLinkFilterByArch": False,
             "filterByLinkText": False,
             "matchLinksOutsideATags": False,
             "skipSort": False,
             "reverseSort": False,
             "sortByLastLinkSegment": False,
         }],
         "customLinkFilterRegex": "",
         "filterByLinkText": False,
         "skipSort": False,
         "reverseSort": False,
     }},
]

AURORA = [
    # Tap-through list in Aurora Store. `sgp=True` means the app also needs
    # Sandboxed Google Play installed (from GOS Apps) for push / Play Integrity.

    # Google (SGP mandatory)
    ("com.google.android.gm", "Gmail", True),
    ("com.google.android.calendar", "Google Calendar", True),
    ("com.google.android.apps.maps", "Google Maps", True),
    ("com.google.android.apps.messaging", "Google Messages", True),
    ("com.google.android.apps.tycho", "Google Fi", True),
    ("com.google.android.GoogleCamera", "Pixel Camera", True),
    ("com.google.android.apps.wear.companion", "Wear OS", True),
    ("com.google.android.apps.wearables.maestro.companion", "Pixel Buds", True),

    # Play-only (no FOSS / direct-vendor distribution)
    ("com.anthropic.claude", "Claude", False),
    ("com.seafile.seadroid2", "Seafile", False),  # F-Droid build is stale (v4.0.6)

    # Banking / financial
    ("com.infonow.bofa", "Bank of America", True),
    ("com.wf.wellsfargomobile", "Wells Fargo", True),
    ("com.venmo", "Venmo", True),
    ("me.greenlight", "Greenlight", True),

    # Health
    ("com.cerner.iris.play", "Cerner HealtheLife", False),

    # Travel / rides / food
    ("com.airbnb.android", "Airbnb", False),
    ("com.ubercab", "Uber", True),
    ("me.lyft.android", "Lyft", True),
    ("com.dd.doordash", "DoorDash", False),
    ("com.instacart.client", "Instacart", False),
    ("com.main.gopuff", "GoPuff", False),
    ("com.opentable", "OpenTable", False),
    ("com.resy.android.prod", "Resy", False),
    ("com.touchtunes.android", "TouchTunes", False),
    ("me.highest.aviate", "Aviate: Flight Companion", False),

    # Streaming / media
    ("de.danoeh.antennapod", "AntennaPod", True),  # Play build for Android Auto
    ("com.spotify.music", "Spotify", False),
    ("com.getchannels.dvr.app", "Channels DVR", False),
    ("com.sonos.acr2", "Sonos", False),

    # Home / IoT
    ("io.homeassistant.companion.android", "Home Assistant", True),  # Play build: FCM push
    ("com.mcu.reolink", "Reolink", False),
    ("com.midea.ai.overseas", "SmartHome (MSmartHome)", False),
    ("com.birdbuddy.app", "Bird Buddy", False),
    ("com.pushd.client", "Aura Frames", False),
    ("com.mixtiles.oasis", "Mixtiles", False),

    # Work / productivity
    ("com.atlassian.android.jira.core", "Jira", False),
    ("com.backblaze.android", "Backblaze", False),
    ("com.github.android", "GitHub", False),
    ("com.azure.authenticator", "Microsoft Authenticator", True),
    ("com.duosecurity.duomobile", "Duo Mobile", True),
    ("com.microsoft.office.outlook", "Outlook", True),
    ("com.microsoft.skydrive", "OneDrive", True),
    ("com.microsoft.teams", "Teams", True),
    ("us.zoom.videomeetings", "Zoom", False),
    ("com.fastmail.app", "Fastmail", False),
    ("com.onepassword.android", "1Password", True),
    ("com.dayoneapp.dayone", "Day One", False),
    ("com.readermobile", "Readwise Reader", False),
    ("org.kde.kdeconnect_tp", "KDE Connect", False),

    # Retail / misc
    ("com.amazon.mShop.android.shopping", "Amazon", False),
    ("com.usablenet.mobile.walgreen", "Walgreens", False),
    ("com.planetfitness", "Planet Fitness", False),
    ("com.strava", "Strava", False),
    ("com.ipsgroupinc.parksmarter", "ParkSmarter", False),
    ("net.sharewire.parkmobilev2", "ParkMobile", False),
    ("org.bookshop.app", "Bookshop.org", False),
    ("com.kagi.search", "Kagi Search", False),
    ("com.powerschool.portal", "PowerSchool", False),
    ("com.valvesoftware.android.steam.community", "Steam", False),
    ("com.PalmCourt.Wavelength", "Wavelength", False),
    ("com.windyty.android", "Windy.com", False),
    ("bitpit.launcher", "Niagara Launcher", False),
    ("com.subaru.telematics.app.remote", "Subaru STARLINK", True),
    ("com.toyota.oneapp", "Toyota", True),
]
