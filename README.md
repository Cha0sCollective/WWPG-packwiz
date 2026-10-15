# WWPG Test Pack

Import these packs into **Prism Launcher** to try **WWPG 0.2.2-beta.3** with the exact required mods and ready-made circuits. Choose the **Base** edition for ordinary factories or **Pinout** for computer control. Each includes its matching Stationary Test Yard, a smaller historical factory demo, and **14,650 node benchmark**. This repository is separate from the [WWPG mod](https://github.com/Cha0sCollective/World-Wide-Power-Grid).

Beta.3 reduces repeated work preparing circuits and storing results, and includes disconnected-wire and repeated-diagnostics corrections. API 1.0.0 and saved-world compatibility are retained. The large-network 20 TPS goal remains open; see the [beta.3 release notes](https://github.com/Cha0sCollective/World-Wide-Power-Grid/releases/tag/0.2.2-beta.3).

## Play

| Edition | Download | Mods and world |
| --- | --- | --- |
| Pinout | [Pinout Prism ZIP](https://github.com/Cha0sCollective/WWPG-packwiz/releases/download/0.2.2-beta.3/WWPG-Test-Pack-0.2.2-beta.3-Pinout-Prism.zip) | Seven mods, including Pinout and CC:Tweaked; **Stationary Test Yard — Pinout**. |
| Base | [Base Prism ZIP](https://github.com/Cha0sCollective/WWPG-packwiz/releases/download/0.2.2-beta.3/WWPG-Test-Pack-0.2.2-beta.3-Prism.zip) | Five required mods; **Stationary Test Yard**. |

1. Download the ZIP for your chosen edition.
2. In a current Prism Launcher, choose **Add Instance → Import**, select the ZIP, and create the instance. Allow the included installer command if Prism asks.
3. Launch the instance. Prism installs Minecraft and NeoForge; packwiz downloads and verifies the five or seven pinned mods. Internet access and a Minecraft account are required. Automatic Java selection is enabled; use Java 21 if your launcher asks you to select Java.
4. Choose **Singleplayer → Stationary Test Yard** in Base, or **Stationary Test Yard — Pinout** in Pinout. You start in Creative mode at `(8, 64, 16)`. The smaller **WWPG - Panel Relay Demo** and separate **14,650 node benchmark** are also in the world list.

Earlier [pack releases](https://github.com/Cha0sCollective/WWPG-packwiz/releases) and their fixed tags remain available. Both new editions use the exact published **wwpg-0.2.2-beta.3.jar**.

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

Use the [current station guide](https://github.com/Cha0sCollective/World-Wide-Power-Grid/blob/0.2.2-beta.3/docs/STATIONARY_YARD.md) for expected readings and resets. Goggles show precise readings when meter needles barely move. Cabinets contain spares; their contents are not counted as working demonstrations. If PG's design editor is cut off, reduce **Options → Video Settings → GUI Scale**; scale 2 fits its controls in a 1280 × 720 window.

In the **Pinout edition**, at **S80 or S81**, open the computer and enter:

```text
wwpg start
wwpg stop
wwpg pattern 85
```

`wwpg start` lights all eight pin lamps; `wwpg stop` turns them off. The separate board RUN lamp stays on briefly as its capacitor discharges, then OFF lights. Allow about three seconds for the relay to respond. `wwpg demo` runs a lamp sequence, `wwpg volts` shows readings, and `wwpg layout` explains the pins. Both computers' programs and startup files are included in the save.

The smaller **panel-relay demo** uses a CEE panel to control a PG relay and capacitor board, which switches power to CEE lamps. Turn **Factory enable** off: the green RUNNING lamp stays on for roughly three seconds, then red OFF lights. Turn it on again to recharge and switch back. Southern circuits use a 300 V PG supply for CEE lighting and a water pump, plus a separate 600 V supply for the heater under a Create basin. Both factory demos include meters and wire tools at spawn. The input water is finite; refill it if the pump has already moved it.

## 14,650 node benchmark

Choose **Singleplayer → 14,650 node benchmark** to open the large mixed CEE/PG save. You spawn in Creative mode near `(1038, 64, 1038)`. It contains **14,650 electrical nodes**, **20,637 connections**, **1,050 stateful devices**, and **50 factories** across **953 chunks**. The original builder called this its 10,000-tier workload; the pack label uses the audited actual node count.

Both editions use **NeoForge 21.1.248** and an **8 GiB maximum Java heap**, matching this save's benchmark setup. Leave enough RAM for your operating system and other programs. Initial grid loading can take several minutes. PG starts with the native engine and 16 substeps.

The circuits use the ordinary required mods. Timed measurements use a separate optional helper; opening this world does not start an automatic timed trial. The save was generated with a historical `0.2.2-dev.2` candidate, and its generation checksum is retained in the save's provenance. This pack supplies the published beta.3 jar. The benchmark archive is unchanged from the beta.2 pack so the workload stays identical for version comparisons. Its inclusion demonstrates the saved workload, not certified 20 TPS capacity. Keep a clean instance for comparisons; edits change the workload.

## Included versions

| Component | Version |
| --- | --- |
| Minecraft | 1.21.1 |
| NeoForge | 21.1.248 |
| Java | 21 |
| Create | 6.0.10-280, full release |
| Create: Electro Energetics | 1.21.1-1.1.3 |
| Power Grid | 0.6.2 |
| Architectury API | 13.0.8 |
| World-Wide Power Grid | 0.2.2-beta.3 |
| CC:Tweaked, Pinout edition | 1.120.2 |
| CC;CPG: Pinout, Pinout edition | 0.2.1 |

Power Grid is configured for the native backend with 16 electrical substeps. WWPG supplies its required native resources. Native support was tested on Windows x86-64 and Ubuntu 24.04 x86-64; Linux requires glibc 2.38 or newer. PG retains its Java fallback. Use `/wwpg` to check the active backend; enable cheats for commands if needed.

WWPG 0.2.2-beta.3 reuses unchanged terminal identities and CEE circuit descriptions, reduces temporary result allocations, and includes the wire and diagnostics fixes since beta.2. Stored energy, electrical models, 16 substeps, and extension API 1.0.0 remain compatible. Read [supported content](https://github.com/Cha0sCollective/World-Wide-Power-Grid/blob/0.2.2-beta.3/docs/SUPPORT.md) and [current status](https://github.com/Cha0sCollective/World-Wide-Power-Grid/blob/0.2.2-beta.3/docs/STATUS.md) for the declared stationary scope.

The **Base** pack uses WWPG's base profile; **Pinout** includes the two computer-control mods. The separate Extension API Workshop uses two additional example add-ons described in [WWPG's installation guide](https://github.com/Cha0sCollective/World-Wide-Power-Grid/blob/0.2.2-beta.3/docs/INSTALL.md). The runtime WWPG jar already supplies the APIs; developer API jars belong in build dependencies.

## Saves and updates

Each ZIP includes three worlds once on import. Packwiz manages only the mod downloads and initial solver configuration; it does not manage `saves/`, so launching again preserves your world edits and computer programs. Both editions use the pack's fixed Git tag with separate managed pack directories. A future pack release requires a new import; keep your old instance to retain its worlds. The small panel demo retains its beta.2 archive filename and historical verification; each Stationary Yard comes from beta.3's published world bundle.

## Maintain the pack

All downloads have SHA-256 checksums in [dependencies.json](dependencies.json). Upstream mods are downloaded from their original distribution URLs; their jars are not committed here. Create already bundles Ponder, Flywheel, and Registrate.

The two yards are read from their named inner archives inside the published `wwpg-0.2.2-beta.3-example-worlds.zip` bundle. Both the bundle and inner archives have pinned checksums. Each edition copies only its own named yard into the Prism instance. The authorized benchmark save is committed separately in `worlds/wwpg-benchmark-14650-v1.zip`, with a pinned checksum and public provenance. `tools/package_benchmark.py` reproduces its label and instructions from the recorded source export; native circuit files are retained byte for byte.

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

WWPG pack code and documentation use [MIT](LICENSE). Each ZIP retains the packwiz bootstrap and installer licenses. WWPG's 0.2.2-beta.3 jar includes its MIT license. Power Grid's bundled native resources and the other upstream dependencies retain their own licenses.
