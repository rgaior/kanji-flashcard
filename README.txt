# Kanji Flashcards — GitHub Pages / iPhone

This is a Progressive Web App (PWA) designed for Safari on iPhone.

## Range selection
Enter a first and last KANJIDAMAGE listing number, for example:
- First 1, Last 20 → randomizes the actual kanji entries numbered 1–20 on KANJIDAMAGE
- First 101, Last 200 → randomizes the actual kanji entries numbered 101–200
- First 1, Last 1760 → covers the numbered kanji portion currently visible on the site

KANJIDAMAGE also has numbered rows that are images/radicals rather than kanji. Those rows keep their website numbers but are skipped as flashcards. Therefore a numeric range can contain fewer flashcards than its width.

## GitHub Pages
Upload the contents of this folder to the root of a GitHub repository. The repository should contain index.html at the top level. In Settings → Pages, choose "Deploy from a branch", select the main branch and the root folder, then Save.

GitHub Pages publishes static HTML/CSS/JavaScript files. A project site normally appears at:
https://YOUR-USERNAME.github.io/YOUR-REPOSITORY/

## Install on iPhone
Open the published HTTPS address in Safari, tap Share → Add to Home Screen, then open the new icon.

The app can cache its interface for offline use. Updating the KANJIDAMAGE list requires internet access.
