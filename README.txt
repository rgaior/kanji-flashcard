# Kanji Flashcards iPhone App

This is a Progressive Web App (PWA).

## Range selection
Enter a first and last KANJIDAMAGE number, e.g.:
- First 1, Last 20 → randomizes cards 1–20
- First 101, Last 200 → randomizes cards 101–200
- First 1, Last 1700 → randomizes the full range (if the current KANJIDAMAGE list contains that many entries)

The numbers refer to the ordering in the KANJIDAMAGE listing currently loaded by the app.

## Install on iPhone
The app must be served from HTTPS for Safari's Add to Home Screen/PWA behavior and service worker caching to work.
Once hosted:
1. Open the site in Safari.
2. Tap Share.
3. Tap Add to Home Screen.
4. Open it from the new Home Screen icon.

The app can then cache the interface for offline use. The KANJIDAMAGE update itself requires internet access.
