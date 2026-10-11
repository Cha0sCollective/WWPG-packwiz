# WWPG Test Pack

Import this pack into **Prism Launcher** to try WWPG 0.2.0 with **Pinout computer controls**, the Pinout Stationary Test Yard, and a smaller historical factory demo. Pinout and CC:Tweaked are included in the pinned downloads. This repository is separate from the [WWPG mod](https://github.com/Cha0sCollective/World-Wide-Power-Grid).

## Play

1. Download [WWPG-Test-Pack-0.2.0-pinout.1-Prism.zip](https://github.com/Cha0sCollective/WWPG-packwiz/releases/download/0.2.0-pinout.1/WWPG-Test-Pack-0.2.0-pinout.1-Prism.zip).
2. In a current Prism Launcher, choose **Add Instance → Import**, select the ZIP, and create the instance. Allow the included installer command if Prism asks.
3. Launch the instance. Prism installs Minecraft and NeoForge; packwiz downloads and verifies the seven pinned mods. Internet access and a Minecraft account are required. Automatic Java selection is enabled; use Java 21 if your launcher asks you to select Java.
4. Choose **Singleplayer → Stationary Test Yard — Pinout**. You start in Creative mode at `(8, 64, 16)`. The smaller **WWPG - Panel Relay Demo** is also included as a historical example.

The [original base 0.2.0 pack](https://github.com/Cha0sCollective/WWPG-packwiz/releases/tag/0.2.0) remains available. This Pinout edition is pack revision **0.2.0-pinout.1** and uses the same **WWPG 0.2.0** runtime jar.

## Explore the worlds

In the **Pinout Stationary Test Yard**, take the guidebooks, Engineer's Goggles, meters, and tools from the spawn chest at `(8, 64, 16)`. Follow the white paths or fly between the labeled stations. Each exhibit explains its controls, expected readings, and reset action. The earlier factory, board and panel galleries, transformers, and meter banks remain on the west side; the east side has 79 additional base exhibits and two Pinout computer stations.

| Area | Where | What to try |
| --- | --- | --- |
| Factory and galleries | West side | Toggle **Factory enable**, try the board and panel controls, and compare transformer and meter readings. |
| Core and radiator | Follow the exhibit signs | Inspect generation, the mixed load, and cooling. |
| Plotter and CRTs | S15, S24–S26 | Change the input to move the graph trace or glowing CRT dot. |
| Saved circuit design | S61 | Load, edit, save, copy, and assemble the supplied design through PG's native menus. |
| Nether link | S65 | Enter the portal and compare the powered equipment at both ends. |
| Wire families and duplex cable | S68–S77 | Switch the feed and measure the load; the duplex example powers a red 12 V bulb. |
| Wire attachments and energy meter | S78–S79 | Use native wire attachments and compare the lamps with the three-pole meter. |
| Pinout computer controls | S80–S81 | Use each upstream power supply to run eight computer-controlled lamps, a board relay, and a panel gauge. |

Use the [current station guide](https://github.com/Cha0sCollective/World-Wide-Power-Grid/blob/0.2.0/docs/STATIONARY_YARD.md) for expected readings and resets. Goggles show precise readings when meter needles barely move. Cabinets contain spares; their contents are not counted as working demonstrations. If PG's design editor is cut off, reduce **Options → Video Settings → GUI Scale**; scale 2 fits its controls in a 1280 × 720 window.

At **S80 or S81**, open the computer and enter:

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
| World-Wide Power Grid | 0.2.0 |
| CC:Tweaked | 1.120.2 |
| CC;CPG: Pinout | 0.2.1 |

Power Grid is configured for the native backend with 16 electrical substeps. WWPG supplies its required native resources. Native support was tested on Windows x86-64 and Ubuntu 24.04 x86-64; Linux requires glibc 2.38 or newer. PG retains its Java fallback. Use `/wwpg` to check the active backend; enable cheats for commands if needed.

WWPG 0.2.0 adds a public extension API for add-on machines and improves saved terminal ownership, late-loading wires, and unavailable meter readings. The earlier saved-design error is corrected and demonstrated in the current yard. Read [supported content](https://github.com/Cha0sCollective/World-Wide-Power-Grid/blob/0.2.0/docs/SUPPORT.md) and [current status](https://github.com/Cha0sCollective/World-Wide-Power-Grid/blob/0.2.0/docs/STATUS.md) for the declared stationary scope.

This pack uses WWPG's **Pinout profile**. The separate Extension API Workshop uses two additional example add-ons described in [WWPG's installation guide](https://github.com/Cha0sCollective/World-Wide-Power-Grid/blob/0.2.0/docs/INSTALL.md). The runtime WWPG jar already supplies the APIs; developer API jars belong in build dependencies.

## Saves and updates

Both worlds are included once in the import ZIP. Packwiz manages only the mod downloads and initial solver configuration; it does not manage `saves/`, so launching again preserves your world edits and computer programs. The release instance uses the pack's fixed Git tag. A future pack release requires a new import; keep your old instance to retain its worlds. The small panel demo retains its beta.2 archive filename and historical verification; the Pinout Stationary Test Yard is the current 0.2.0 Pinout acceptance world.

## Maintain the pack

All downloads have SHA-256 checksums in [dependencies.json](dependencies.json). Upstream mods are downloaded from their original distribution URLs; their jars are not committed here. Create already bundles Ponder, Flywheel, and Registrate.

The Pinout yard is read from `worlds/wwpg-0.2.0-stationary-yard-pinout.zip` inside the published `wwpg-0.2.0-example-worlds.zip` bundle. Both the bundle and the inner world archive have pinned checksums. Only the named save is copied into the Prism instance.

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

WWPG pack code and documentation use [MIT](LICENSE). The ZIP retains the packwiz bootstrap and installer licenses. WWPG's 0.2.0 jar includes its MIT license. Power Grid's bundled native resources and the other upstream dependencies retain their own licenses.
