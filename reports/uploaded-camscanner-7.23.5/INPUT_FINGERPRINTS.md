# Input Fingerprints

- CamScanner APKM: `APK.apkm` — 202 MB — SHA-256 `2f62abc367c8e34c6234bde6108c5b317aec027e132237a8673cf43c11cb0a52`
- CamScanner base APK: version `7.23.5.2608050000`, package `com.intsig.camscanner` — SHA-256 `801514f2226f4cf35ee1992260b456c221847d8f8a212c4d0e06d17b1b31f973`
- CamScanner arm64 split — SHA-256 `30cffd606771e917e197eecd7fb0742253584fb9fc2c81d6b088ae7bd26b3b1b`
- DocVault APK: `Docvault.apk` — 65 MB — SHA-256 `87b20d4e423dcbffc7442cf30076762c22e878f713703c6e6efe4b0621097286`

The CamScanner bundle is an APKM with a 152.77 MB base APK and ABI/language splits. The normal GitHub 100 MB per-file limit prevents committing the base APK directly; use a runtime downloader, Git LFS, or Actions artifact for the binary.
