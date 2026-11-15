# GNX Ver.12.0 — Firebase account foundation

Based on the user-supplied GNX-main.zip (Ver.11.9). Home visuals, hero, sidebar hover behavior and GA4 code are preserved.

## Deploy
Copy **all** files (index.html, assets/, robots.txt, sitemap.xml and the Google verification HTML) to the GNX GitHub repository root. Commit and push. Do not copy the outer GNX_Ver12_0 directory itself.

## Features
- Google popup sign-in and sign-out using Firebase Authentication.
- Cloud Firestore progress storage under `users/{uid}/progress/{gameId}`.
- Existing local progress migrates on first sign-in when no cloud document exists.
- If cloud progress already exists, it is loaded instead of overwriting it; differing local data is backed up in browser localStorage under `gnx:backup:{uid}:{gameId}:{timestamp}`.
- Progress saved through the existing guide UI is debounced and uploaded to Firestore.
- Guest mode remains local-only. JSON export/import remains available.

## Important limitations
- This version uses a lightweight last-write-wins model, not real-time multi-device conflict resolution. When changing progress on two devices simultaneously, the last save may win. Reload to get latest cloud data.
- Google login needs popups enabled and `popochan0547-creator.github.io` in Firebase Authentication authorized domains.
- Firebase SDK is loaded from Google's CDN; it needs an internet connection.
- Cloud sync requires Firestore rules restricting `/users/{uid}/**` to the signed-in user.
- Account management and data deletion UX, privacy policy, automated tests, offline queue and production-grade schema validation should be completed before broad public launch.
- Firebase Analytics measurement ID differs from GNX's existing GA4 ID. The new Firebase module does **not** initialize Firebase Analytics or change the existing GA4 measurement ID.
