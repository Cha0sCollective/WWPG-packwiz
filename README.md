# WWPG Test Pack

Import this pack into **Prism Launcher** to try WWPG beta.4 with the exact required mods, an expanded test yard, and a smaller factory demo. This repository is separate from the [WWPG mod](https://github.com/Cha0sCollective/World-Wide-Power-Grid).

## Play

1. Download [WWPG-Test-Pack-0.1.0-beta.4-Prism.zip](https://github.com/Cha0sCollective/WWPG-packwiz/releases/download/0.1.0-beta.4/WWPG-Test-Pack-0.1.0-beta.4-Prism.zip).
2. In a current Prism Launcher, choose **Add Instance → Import**, select the ZIP, and create the instance. Allow the included installer command if Prism asks.
3. Launch the instance. Prism installs Minecraft and NeoForge; packwiz downloads and verifies the five pinned mods. Internet access and a Minecraft account are required. Automatic Java selection is enabled; use Java 21 if your launcher asks you to select Java.
4. Choose **Singleplayer → WWPG - Expanded Test Yard**. You start in Creative mode at `(8, 64, 16)`. The smaller **WWPG - Panel Relay Demo** is also included.

## Explore the worlds

In the **expanded yard**, take the guidebook, Engineer's Goggles, meters, and wrench from the chest at `(6, 64, 16)`. Follow the white path or fly between the labeled stations:

| Area | Where | What to try |
| --- | --- | --- |
| Factory | Near spawn | Flip **Factory enable** to change the green RUN and red OFF lamps; watch the water pump and heater beneath the basin. |
| Board gallery | x32–112, z8–81 | Try switches, relays, storage, diodes, transistors, tubes, lights, gauges, and displays. |
| Panel gallery | x32–112, z94–115 | Press buttons, switch lamps, trip and reset a breaker, read gauges, and control wireless lamps. |
| Transformers and variacs | x32–112, z124–145 | Compare input/output voltage and adjust ratios or cranks. |
| Meter banks | x32, 64, or 96; z156 | Compare both mods' readings; the AC station uses 50 Hz. |
| Devices and storage | x32–112, z176–237 | Try motors, controls, connectors, battery charging, and the accumulator. |
| Parts cabinets | x6–10, z48 onward | Take spares and supported parts for your own builds. |

The yard has live examples for all 28 built-in PG board component types and all 11 CEE panel attachment types. It demonstrates 85 of the 134 declared behavior groups; cabinet contents are parts, not working exhibits. See the [full station guide](https://github.com/Cha0sCollective/World-Wide-Power-Grid/blob/0.1.0-beta.4/docs/FIXTURE_WORLD.md) for controls and expected readings. Goggles show numeric readings when meter needles barely move.

The smaller **panel-relay demo** uses a CEE panel to control a PG relay and capacitor board, which switches power to CEE lamps. Turn **Factory enable** off: the green RUNNING lamp stays on for roughly three seconds, then red OFF lights. Turn it on again to recharge and switch back. Southern circuits use a 300 V PG supply for CEE lighting and a water pump, plus a separate 600 V supply for the heater under a Create basin. Both worlds include meters and wire tools at spawn. The input water is finite; refill it if the pump has already moved it.

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
| World-Wide Power Grid | 0.1.0-beta.4 |

Power Grid is configured for the native backend with 16 electrical substeps. WWPG supplies its required native resources. Native support was tested on Windows x86-64 and Ubuntu 24.04 x86-64; Linux requires glibc 2.38 or newer. PG retains its Java fallback. Use `/wwpg` to check the active backend; enable cheats for commands if needed.

Beta.4 fixes premature wire removal during chunk loading and capacitor charge loss on restored circuit boards. It cannot recover wires or charge already lost and saved by an older version. PG's saved-design load error remains open; the expanded yard excludes a placed circuit design table. This is a stationary beta demonstration; read WWPG's [supported content](https://github.com/Cha0sCollective/World-Wide-Power-Grid/blob/0.1.0-beta.4/docs/SUPPORT.md) and [known issues](https://github.com/Cha0sCollective/World-Wide-Power-Grid/blob/0.1.0-beta.4/docs/STATUS.md) for its limits.

## Saves and updates

Both worlds are included once in the import ZIP. Packwiz manages only the mod downloads and initial solver configuration; it does not manage `saves/`, so launching again preserves your world edits. The release instance uses the pack's fixed Git tag. A future pack release requires a new import; keep your old instance to retain its worlds. The world archives retain their beta.2 filenames because those saves are unchanged and work with beta.4.

## Maintain the pack

All downloads have SHA-256 checksums in [dependencies.json](dependencies.json). Upstream mods are downloaded from their original distribution URLs; their jars are not committed here. Create already bundles Ponder, Flywheel, and Registrate.

Use Python 3.11 or newer:

```sh
python tools/verify.py
python tools/build_prism.py
python tools/smoke_install.py --java /path/to/java
```

The build writes the Prism ZIP and checksums to `build/distributions/`. The smoke check installs the real pack twice into an isolated instance and verifies mod hashes, loader metadata, every packaged save file, and preservation of a world-edit marker in each world. It does not launch Minecraft, sign in, or modify an existing Prism installation.

After editing managed files, run `packwiz refresh` from `pack/`, then run verification. The index covers only that directory. Keep the example world and launcher templates outside the index. For a new pack version, update the lock, pack version, instance name, fixed tag URL, and README together. Never rewrite a published tag.

The [official packwiz installer guide](https://packwiz.infra.link/tutorials/installing/packwiz-installer/) and [Prism import guide](https://prismlauncher.org/wiki/help-pages/Zip-import/) describe the installation flow.

## License

WWPG pack code and documentation use [MIT](LICENSE). The ZIP retains the packwiz bootstrap and installer licenses. WWPG's beta.4 jar includes its MIT license. Power Grid's bundled native resources and the other upstream dependencies retain their own licenses.
