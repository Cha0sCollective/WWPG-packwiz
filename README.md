# WWPG Test Pack

Import these packs into **Prism Launcher** to try **WWPG 0.2.2-alpha.1** with the exact required mods and ready-made circuits. Choose the **Base** edition for ordinary factories or **Pinout** for computer control. Each includes its matching Stationary Test Yard and a smaller historical factory demo. This repository is separate from the [WWPG mod](https://github.com/Cha0sCollective/World-Wide-Power-Grid).

This is an alpha for circuit-loading fixes and SDK improvements. Large-network performance remains under investigation; see [current status](https://github.com/Cha0sCollective/World-Wide-Power-Grid/blob/0.2.2-alpha.1/docs/STATUS.md).

## Play

| Edition | Download | Mods and world |
| --- | --- | --- |
| Pinout | [Pinout Prism ZIP](https://github.com/Cha0sCollective/WWPG-packwiz/releases/download/0.2.2-alpha.1/WWPG-Test-Pack-0.2.2-alpha.1-Pinout-Prism.zip) | Seven mods, including Pinout and CC:Tweaked; **Stationary Test Yard — Pinout**. |
| Base | [Base Prism ZIP](https://github.com/Cha0sCollective/WWPG-packwiz/releases/download/0.2.2-alpha.1/WWPG-Test-Pack-0.2.2-alpha.1-Prism.zip) | Five required mods; **Stationary Test Yard**. |

1. Download the ZIP for your chosen edition.
2. In a current Prism Launcher, choose **Add Instance → Import**, select the ZIP, and create the instance. Allow the included installer command if Prism asks.
3. Launch the instance. Prism installs Minecraft and NeoForge; packwiz downloads and verifies the five or seven pinned mods. Internet access and a Minecraft account are required. Automatic Java selection is enabled; use Java 21 if your launcher asks you to select Java.
4. Choose **Singleplayer → Stationary Test Yard** in Base, or **Stationary Test Yard — Pinout** in Pinout. You start in Creative mode at `(8, 64, 16)`. The smaller **WWPG - Panel Relay Demo** is also included as a historical example.

Earlier [pack releases](https://github.com/Cha0sCollective/WWPG-packwiz/releases) and their fixed tags remain available. Both new editions use the exact published **wwpg-0.2.2-alpha.1.jar**.

## Explore the worlds

In either **Stationary Test Yard**, take the guidebooks, Engineer's Goggles, meters, and tools from the spawn chest at `(8, 64, 16)`. Follow the white paths or fly between the labeled stations. Each exhibit explains its controls, expected readings, and reset action. The earlier factory, board and panel galleries, transformers, and meter banks remain on the west side; the east side has 79 additional base exhibits. Pinout adds two computer stations.

| Area | Where | What to try |
| --- | --- | --- |
| Factory and galleries | West side | Toggle **Factory enable**, try the board and panel controls, and compare transformer and meter readings. |
| Core and radiator | Follow the exhibit signs | Inspect generation, the mixed load, and cooling. |
| Plotter and CRTs | S15, S24–S26 | Change the input to move the graph trace or glowing CRT dot. |
| Saved circuit design | S61 | Load, edit, save, copy, and assemble the supplied design through PG's native menus. |
| Nether link | S65 | Enter the portal and compare the powered equipment at both ends. |
| Wire families and duplex cable | S68–S77 | Switch the feed and measure the load; the duplex example powers a red 12 V bulb. |
| Wire attachments and energy meter | S78–S79 | Use native wire attachments and compare the lamps with the three-pole meter. |
| Pinout computer controls | S80–S81, Pinout edition | Use each upstream power supply to run eight computer-controlled lamps, a board relay, and a panel gauge. |

Use the [current station guide](https://github.com/Cha0sCollective/World-Wide-Power-Grid/blob/0.2.2-alpha.1/docs/STATIONARY_YARD.md) for expected readings and resets. Goggles show precise readings when meter needles barely move. Cabinets contain spares; their contents are not counted as working demonstrations. If PG's design editor is cut off, reduce **Options → Video Settings → GUI Scale**; scale 2 fits its controls in a 1280 × 720 window.

In the **Pinout edition**, at **S80 or S81**, open the computer and enter:

```text
wwpg start
wwpg stop
wwpg pattern 85
```

`wwpg start` lights all eight pin lamps; `wwpg stop` turns them off. The separate board RUN lamp stays on briefly as its capacitor discharges, then OFF lights. Allow about three seconds for the relay to respond. `wwpg demo` runs a lamp sequence, `wwpg volts` shows readings, and `wwpg layout` explains the pins. Both computers' programs and startup files are included in the save.

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
| World-Wide Power Grid | 0.2.2-alpha.1 |
| CC:Tweaked, Pinout edition | 1.120.2 |
| CC;CPG: Pinout, Pinout edition | 0.2.1 |

Power Grid is configured for the native backend with 16 electrical substeps. WWPG supplies its required native resources. Native support was tested on Windows x86-64 and Ubuntu 24.04 x86-64; Linux requires glibc 2.38 or newer. PG retains its Java fallback. Use `/wwpg` to check the active backend; enable cheats for commands if needed.

WWPG 0.2.2-alpha.1 improves circuit loading, preserves stored energy while affected circuits load, and fixes a single-player buzzer crash. Extension API 1.0.0 remains compatible. Read [supported content](https://github.com/Cha0sCollective/World-Wide-Power-Grid/blob/0.2.2-alpha.1/docs/SUPPORT.md) and [current status](https://github.com/Cha0sCollective/World-Wide-Power-Grid/blob/0.2.2-alpha.1/docs/STATUS.md) for the declared stationary scope.

The **Base** pack uses WWPG's base profile; **Pinout** includes the two computer-control mods. The separate Extension API Workshop uses two additional example add-ons described in [WWPG's installation guide](https://github.com/Cha0sCollective/World-Wide-Power-Grid/blob/0.2.2-alpha.1/docs/INSTALL.md). The runtime WWPG jar already supplies the APIs; developer API jars belong in build dependencies.

## Saves and updates

Each ZIP includes two worlds once on import. Packwiz manages only the mod downloads and initial solver configuration; it does not manage `saves/`, so launching again preserves your world edits and computer programs. Both editions use the pack's fixed Git tag with separate managed pack directories. A future pack release requires a new import; keep your old instance to retain its worlds. The small panel demo retains its beta.2 archive filename and historical verification; each Stationary Yard comes from the current alpha's published world bundle.

## Maintain the pack

All downloads have SHA-256 checksums in [dependencies.json](dependencies.json). Upstream mods are downloaded from their original distribution URLs; their jars are not committed here. Create already bundles Ponder, Flywheel, and Registrate.

The two yards are read from their named inner archives inside the published `wwpg-0.2.2-alpha.1-example-worlds.zip` bundle. Both the bundle and inner archives have pinned checksums. Each edition copies only its own named yard into the Prism instance.

Use Python 3.11 or newer:

```sh
python tools/verify.py
python tools/build_prism.py
python tools/smoke_install.py --profile BASE --java /path/to/java
python tools/smoke_install.py --profile PINOUT --java /path/to/java
```

Verification and building cover both profiles by default; use `--profile BASE` or `--profile PINOUT` to select one. The build writes both Prism ZIPs and checksums to `build/distributions/`. Each smoke check installs its pack twice into an isolated instance and verifies the exact mod set, loader metadata, every packaged save file, and preservation of a world-edit marker in each world. It does not launch Minecraft, sign in, or modify an existing Prism installation.

The Pinout metadata is in `pack/`; Base is in `pack-base/`. After editing managed files, run `packwiz refresh` in each affected directory, then verify both profiles. Keep shared mod metadata consistent between editions. Each index covers only its own directory. Keep worlds and launcher templates outside the indices. For a new version, update the shared lock, both pack versions, both instance names and tag URLs, and README together. Never rewrite a published tag.

The [official packwiz installer guide](https://packwiz.infra.link/tutorials/installing/packwiz-installer/) and [Prism import guide](https://prismlauncher.org/wiki/help-pages/Zip-import/) describe the installation flow.

## License

WWPG pack code and documentation use [MIT](LICENSE). Each ZIP retains the packwiz bootstrap and installer licenses. WWPG's 0.2.2-alpha.1 jar includes its MIT license. Power Grid's bundled native resources and the other upstream dependencies retain their own licenses.
