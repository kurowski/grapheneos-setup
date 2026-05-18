"""Source of truth for phone provisioning.

Every entry declares:
  id      — package name (used by ADB / Aurora / Obtainium)
  name    — display name
  source  — one of: github | fdroid | html | aurora | aurora_sgp
  url     — for obtainium-fed sources; ignored for aurora*
  notes   — freeform; ends up in generated checklists

URL heuristics (verify inside Obtainium after import):
  github → https://github.com/<owner>/<repo>
  fdroid → https://f-droid.org/packages/<package>/
  html   → vendor download page
"""

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
    {"id": "at.bitfire.davdroid", "name": "DAVx5",
     "source": "fdroid", "url": "https://f-droid.org/packages/at.bitfire.davdroid/"},
    {"id": "ch.protonvpn.android", "name": "Proton VPN",
     "source": "github", "url": "https://github.com/ProtonVPN/android-app"},
    {"id": "com.capyreader.app", "name": "Capy Reader",
     "source": "github", "url": "https://github.com/jocmp/capyreader"},
    {"id": "com.flipperdevices.app", "name": "Flipper Zero",
     "source": "github", "url": "https://github.com/flipperdevices/Flipper-Android-App"},
    {"id": "com.tailscale.ipn", "name": "Tailscale",
     "source": "github", "url": "https://github.com/tailscale/tailscale-android"},
    {"id": "com.termux", "name": "Termux",
     "source": "github", "url": "https://github.com/termux/termux-app"},
    {"id": "com.termux.styling", "name": "Termux Styling",
     "source": "github", "url": "https://github.com/termux/termux-styling"},
    {"id": "de.danoeh.antennapod", "name": "AntennaPod",
     "source": "fdroid", "url": "https://f-droid.org/packages/de.danoeh.antennapod/"},
    {"id": "de.schliweb.makeacopy", "name": "MakeACopy",
     "source": "fdroid", "url": "https://f-droid.org/packages/de.schliweb.makeacopy/"},
    {"id": "io.ente.photos", "name": "Ente Photos",
     "source": "github", "url": "https://github.com/ente-io/ente",
     "apk_asset_filter": "photos"},
    {"id": "io.homeassistant.companion.android", "name": "Home Assistant",
     "source": "github", "url": "https://github.com/home-assistant/android",
     "apk_asset_filter": "full"},
    {"id": "net.waterfox.android.release", "name": "Waterfox",
     "source": "github", "url": "https://github.com/BrowserWorks/Waterfox-Android"},
    {"id": "org.breezyweather", "name": "Breezy Weather",
     "source": "github", "url": "https://github.com/breezy-weather/breezy-weather"},
    {"id": "org.futo.inputmethod.latin", "name": "FUTO Keyboard",
     "source": "github", "url": "https://github.com/futo-org/android-keyboard"},
    {"id": "org.joinmastodon.android", "name": "Mastodon",
     "source": "github", "url": "https://github.com/mastodon/mastodon-android"},
    {"id": "org.kde.kdeconnect_tp", "name": "KDE Connect",
     "source": "fdroid", "url": "https://f-droid.org/packages/org.kde.kdeconnect_tp/"},
    {"id": "org.tasks", "name": "Tasks.org",
     "source": "github", "url": "https://github.com/tasks/tasks",
     "apk_asset_filter": "-fdroid-"},  # not -googleplay-
    {"id": "xyz.blueskyweb.app", "name": "Bluesky",
     "source": "github", "url": "https://github.com/bluesky-social/social-app"},

    # Direct-vendor (sensitive / security-critical: pull from the source of truth)
    {"id": "org.thoughtcrime.securesms", "name": "Signal",
     "source": "github", "url": "https://github.com/signalapp/Signal-Android",
     "notes": "Signal now ships APKs to GitHub releases"},
    {"id": "md.obsidian", "name": "Obsidian",
     "source": "github", "url": "https://github.com/obsidianmd/obsidian-releases"},
]

AURORA = [
    # Tap-through list in Aurora Store. `sgp=True` means the app also needs
    # Sandboxed Google Play installed (from GOS Apps) for push / Play Integrity.

    # Google (SGP mandatory)
    ("com.google.android.apps.googlevoice", "Google Voice", True),
    ("com.google.android.apps.wear.companion", "Wear OS", True),

    # Play-only (no FOSS / direct-vendor distribution)
    ("com.anthropic.claude", "Claude", False),
    ("com.liamcottle.meshcore.android", "MeshCore", False),
    ("com.seafile.seadroid2", "Seafile", False),  # F-Droid build is stale (v4.0.6)
    ("com.whatsapp", "WhatsApp", False),  # vendor URL has expiring tokens

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

    # Streaming / media
    ("com.spotify.music", "Spotify", False),
    ("com.getchannels.dvr.app", "Channels DVR", False),
    ("com.sonos.acr2", "Sonos", False),

    # Home / IoT
    ("com.mcu.reolink", "Reolink", False),
    ("com.tuya.smart", "Tuya Smart", False),
    ("com.birdbuddy.app", "Bird Buddy", False),

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
    ("com.server.auditor.ssh.client", "Termius", False),
    ("com.subaru.telematics.app.remote", "Subaru STARLINK", True),
    ("com.toyota.oneapp", "Toyota", True),
    ("com.pushd.client", "Aura Frames", False),
]
