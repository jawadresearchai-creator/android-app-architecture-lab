# Uploaded APK Provenance

## Reference application

- User-supplied file: `APK.apkm`
- Identified application: CamScanner
- Android package: `com.intsig.camscanner`
- Version name: `7.23.5.2608050000`
- Version code: `72351`
- Bundle size: `211,194,345` bytes
- Bundle SHA-256: `2f62abc367c8e34c6234bde6108c5b317aec027e132237a8673cf43c11cb0a52`
- Bundle MD5: `f0aa6ed8db0f0b8f9e311d5ad27426f0`
- Bundle composition: base APK plus ABI/resource/language split APKs
- ABI variants observed: arm64-v8a and armeabi
- Base APK size: `160,190,739` bytes
- Base APK SHA-256: `801514f2226f4cf35ee1992260b456c221847d8f8a212c4d0e06d17b1b31f973`
- Base APK MD5: `9ac9500c7d7062a2a501d05fe0434dd7`
- Base APK DEX files: 15
- Total class definitions across base DEX files: 92,274

The base APK hash is the preferred identity check for alternate public bundle packaging. If a public source wraps the same signed `base.apk` in XAPK/APKM differently, the outer archive hash can differ while the executable base APK remains byte-identical.

## Target application

- User-supplied file: `Docvault.apk`
- Target namespace observed: `com.example`
- File size: `67,152,965` bytes
- SHA-256: `87b20d4e423dcbffc7442cf30076762c22e878f713703c6e6efe4b0621097286`
- MD5: `3cfb24e4b05d84e123d2ff50761b5334`
- DEX files: 14
- Total class definitions: 42,073

## Analysis policy

The reference application is used as a behavioral and architectural benchmark. Proprietary source code, branding, assets, credentials, and private service implementations are not to be copied into DocVault. Equivalent features should be implemented independently with Android platform APIs, permissively licensed libraries, and independently designed code.
