# WWPG Test Pack

Import this pack into **Prism Launcher** to try the WWPG beta with the exact required mods and a ready-made factory world. This repository is separate from the [WWPG mod](https://github.com/Cha0sCollective/World-Wide-Power-Grid).

## Play

1. Download [WWPG-Test-Pack-0.1.0-beta.1-Prism.zip](https://github.com/Cha0sCollective/WWPG-packwiz/releases/download/0.1.0-beta.1/WWPG-Test-Pack-0.1.0-beta.1-Prism.zip).
2. In a current Prism Launcher, choose **Add Instance → Import**, select the ZIP, and create the instance. Allow the included installer command if Prism asks.
3. Launch the instance. Prism installs Minecraft and NeoForge; packwiz downloads and verifies the five pinned mods. Internet access and a Minecraft account are required. Automatic Java selection is enabled; use Java 21 if your launcher asks you to select Java.
4. Choose **Singleplayer → WWPG Example**. You start in Creative mode at `(8, 64, 16)`.

The northern circuit uses a CEE source and a CEE switch/meter panel to power a PG capacitor board. The southern circuit uses a PG source to power CEE lighting, heating, and a water pump connected to Create pipes and tanks. The input water is finite; refill it if the pump has already moved it.

## Included versions

| Component | Version |
| --- | --- |
| Minecraft | 1.21.1 |
| NeoForge | 21.1.231 |
| Java | 21 |
| Create | 6.0.10-280, full release |
| Create: Electro Energetics | 1.21.1-1.1.3 |
| Power Grid | 0.6.2 |
| Architectury API | 13.0.8 |
| World-Wide Power Grid | 0.1.0-beta.1 |

Power Grid is configured for the native backend with 16 electrical substeps. WWPG supplies its required native resources. Native support was tested on Windows x86-64 and Ubuntu 24.04 x86-64; Linux requires glibc 2.38 or newer. PG retains its Java fallback. Use `/wwpg` to check the active backend; enable cheats for commands if needed.

This is a small stationary beta demonstration. Read WWPG's [supported content](https://github.com/Cha0sCollective/World-Wide-Power-Grid/blob/main/docs/SUPPORT.md) and [known issues](https://github.com/Cha0sCollective/World-Wide-Power-Grid/blob/main/docs/STATUS.md), including an unresolved intermittent reload test failure.

## Saves and updates

The example world is included once in the import ZIP. Packwiz manages only the mod downloads and initial solver configuration; it does not manage `saves/`, so launching again preserves your world edits. The release instance uses the pack's fixed Git tag. A future pack release requires a new import; keep your old instance to retain its worlds.

## Maintain the pack

All downloads have SHA-256 checksums in [dependencies.json](dependencies.json). Upstream mods are downloaded from their original distribution URLs; their jars are not committed here. Create already bundles Ponder, Flywheel, and Registrate.

Use Python 3.11 or newer:

```sh
python tools/verify.py
python tools/build_prism.py
python tools/smoke_install.py --java /path/to/java
```

The build writes the Prism ZIP and checksums to `build/distributions/`. The smoke check installs the real pack twice into an isolated instance and verifies mod hashes, loader metadata, and preservation of a world-edit marker. It does not sign in or modify an existing Prism installation.

After editing managed files, run `packwiz refresh` from `pack/`, then run verification. The index covers only that directory. Keep the example world and launcher templates outside the index. For a new pack version, update the lock, pack version, instance name, fixed tag URL, and README together. Never rewrite a published tag.

The [official packwiz installer guide](https://packwiz.infra.link/tutorials/installing/packwiz-installer/) and [Prism import guide](https://prismlauncher.org/wiki/help-pages/Zip-import/) describe the installation flow.

## License

WWPG pack code and documentation use [MIT](LICENSE). The ZIP retains the packwiz bootstrap and installer licenses. WWPG's own beta code is MIT licensed even though its original jar predates that decision and contains older metadata. Power Grid's bundled native resources and the other upstream dependencies retain their own licenses.
