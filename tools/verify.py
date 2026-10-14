"""Check the release lock, packwiz hashes, solver settings and Prism templates."""
import argparse
import configparser
import gzip
import hashlib
import json
from pathlib import Path
import tomllib
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _verify_profile(lock, profile):
    settings = lock["profiles"][profile]
    pack_root = (ROOT / settings["pack_dir"]).resolve()
    assert pack_root.is_relative_to(ROOT.resolve())
    pack = tomllib.loads((pack_root / "pack.toml").read_text(encoding="utf-8"))
    assert pack["version"] == lock["version"]
    assert pack["versions"] == {"minecraft": lock["minecraft"], "neoforge": lock["neoforge"]}
    index_path = pack_root / pack["index"]["file"]
    assert pack["index"]["hash-format"] == "sha256"
    assert pack["index"]["hash"] == digest(index_path)
    index = tomllib.loads(index_path.read_text(encoding="utf-8"))
    assert index["hash-format"] == "sha256"
    expected = {"mods/" + mod_id + ".pw.toml" for mod_id in settings["mods"]}
    expected.add("config/powergrid-server.toml")
    assert {entry["file"] for entry in index["files"]} == expected
    for entry in index["files"]:
        path = (pack_root / entry["file"]).resolve()
        assert path.is_relative_to(pack_root.resolve())
        assert entry["hash"] == digest(path), entry["file"]
        assert not entry["file"].startswith("saves/")
        if entry["file"].endswith(".pw.toml"):
            assert entry["metafile"]
        else:
            assert entry.get("preserve"), "Solver configuration must preserve player edits"
    expected_mods = {"wwpg", "cee", "pg", "create", "architectury"}
    if profile == "PINOUT":
        expected_mods.update(("computercraft", "pinout"))
    assert set(settings["mods"]) == expected_mods
    assert len(settings["mods"]) == len(expected_mods)
    for mod in lock["mods"]:
        if mod["id"] not in settings["mods"]:
            continue
        metadata = tomllib.loads((pack_root / "mods" / (mod["id"] + ".pw.toml")).read_text(encoding="utf-8"))
        assert metadata["filename"] == mod["filename"]
        assert metadata["pin"] and metadata["side"] == "both"
        assert metadata["download"] == {
            "url": mod["url"], "hash-format": "sha256", "hash": mod["sha256"]
        }
        assert mod["url"].startswith("https://")
        assert len(mod["sha256"]) == 64
    solver = tomllib.loads((pack_root / "config/powergrid-server.toml").read_text(encoding="utf-8"))
    assert solver["configVersion"] == 5
    assert solver["electricity"]["solver"] == {"solverBackend": "NATIVE", "multiTicks": 16}
    components = json.loads((ROOT / "prism/mmc-pack.json").read_text(encoding="utf-8"))
    assert components["formatVersion"] == 1
    assert {c["uid"]: c["version"] for c in components["components"]} == {
        "net.minecraft": lock["minecraft"], "net.neoforged": lock["neoforge"]
    }
    cfg = configparser.ConfigParser(interpolation=None)
    instance_file = (ROOT / settings["instance_file"]).resolve()
    assert instance_file.is_relative_to(ROOT.resolve())
    cfg.read(instance_file, encoding="utf-8")
    launcher = cfg["General"]
    assert launcher["InstanceType"] == "OneSix"
    assert launcher.getboolean("AutomaticJava")
    assert launcher.getboolean("OverrideCommands")
    assert launcher.getint("MaxMemAlloc") == 8192
    command = launcher["PreLaunchCommand"].replace('\\"', '"')
    assert command.startswith('"$INST_JAVA" ')
    assert '--bootstrap-no-update' in command
    assert '-g -s client' in command
    assert command.endswith(
        "https://raw.githubusercontent.com/" + lock["repository"] + "/" + lock["version"]
        + "/" + settings["pack_dir"] + "/pack.toml"
    )
    for asset in lock["assets"].values():
        assert len(asset["sha256"]) == 64
    world_directories = []
    assert len(settings["worlds"]) == 3
    assert "benchmark_world" in settings["worlds"]
    for key in settings["worlds"]:
        asset = lock["assets"][key]
        assert ("url" in asset) != ("path" in asset)
        if "path" in asset:
            source = (ROOT / asset["path"]).resolve()
            assert source.is_relative_to(ROOT.resolve())
            assert digest(source) == asset["sha256"]
        else:
            assert asset["url"].startswith("https://")
        directory = asset["directory"]
        assert directory and directory not in (".", "..")
        assert not any(character in directory for character in "/\\:")
        assert ("member" in asset) == ("member_sha256" in asset)
        if "member" in asset:
            assert len(asset["member_sha256"]) == 64
            assert asset["member"].endswith(".zip")
        world_directories.append(directory)
    assert len(set(world_directories)) == len(world_directories)
    benchmark = lock["assets"]["benchmark_world"]
    assert benchmark["directory"] == "14,650 node benchmark"
    with zipfile.ZipFile(ROOT / benchmark["path"]) as world:
        raw = gzip.decompress(world.read(benchmark["directory"] + "/level.dat"))
        marker = b"\x08\x00\x09LevelName"
        assert raw.count(marker) == 1
        start = raw.index(marker) + len(marker)
        length = int.from_bytes(raw[start:start + 2], "big")
        assert raw[start + 2:start + 2 + length].decode("utf-8") == benchmark["directory"]
        grid = json.loads(world.read(benchmark["directory"] + "/WWPG_BENCHMARK.json"))
        assert grid["audit"]["electrical_nodes"] == 14650
    print(f"{profile}: index, {len(settings['mods'])} pinned mods, benchmark label/count and native/16 settings verified")


def verify(profile=None):
    lock = json.loads((ROOT / "dependencies.json").read_text(encoding="utf-8"))
    assert lock["schema"] == 2
    assert set(lock["profiles"]) == {"BASE", "PINOUT"}
    assert lock["default_profile"] in lock["profiles"]
    mod_ids = [mod["id"] for mod in lock["mods"]]
    assert set(mod_ids) == {"wwpg", "cee", "pg", "create", "architectury", "computercraft", "pinout"}
    assert len(mod_ids) == len(set(mod_ids))
    for name in ([profile] if profile else lock["profiles"]):
        _verify_profile(lock, name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=("BASE", "PINOUT"))
    args = parser.parse_args()
    verify(args.profile)
