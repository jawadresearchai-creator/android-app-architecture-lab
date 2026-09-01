# APK input

Upload the Android package to this folder through the GitHub web interface.

Supported targets for this lab are primarily `.apk`, with `.xapk`, `.apkm`, `.dex`, and `.jar` accepted when JADX can open them.

For the simplest automatic run, keep only **one** analyzable package in this folder. A push that adds or changes a package triggers the analysis workflow automatically.

If several packages are present, open **Actions → Analyze Android Package → Run workflow** and provide the repository-relative path, for example:

`input/reference-app.apk`

Do not upload keystores, signing passwords, API credentials, or other secrets.
