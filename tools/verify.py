"""Check the release lock, packwiz hashes, solver settings and Prism templates."""
import configparser
import hashlib
import json
from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify():
    lock = json.loads((ROOT / "dependencies.json").read_text(encoding="utf-8"))
    pack_root = ROOT / "pack"
    pack = tomllib.loads((pack_root / "pack.toml").read_text(encoding="utf-8"))
    assert pack["version"] == lock["version"]
    assert pack["versions"] == {"minecraft": lock["minecraft"], "neoforge": lock["neoforge"]}
    index_path = pack_root / pack["index"]["file"]
    assert pack["index"]["hash-format"] == "sha256"
    assert pack["index"]["hash"] == digest(index_path)
    index = tomllib.loads(index_path.read_text(encoding="utf-8"))
    assert index["hash-format"] == "sha256"
    expected = {"mods/" + mod["id"] + ".pw.toml" for mod in lock["mods"]}
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
    assert {m["id"] for m in lock["mods"]} == {"wwpg", "cee", "pg", "create", "architectury"}
    for mod in lock["mods"]:
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
    cfg.read(ROOT / "prism/instance.cfg", encoding="utf-8")
    settings = cfg["General"]
    assert settings["InstanceType"] == "OneSix"
    assert settings.getboolean("AutomaticJava")
    assert settings.getboolean("OverrideCommands")
    command = settings["PreLaunchCommand"].replace('\\"', '"')
    assert command.startswith('"$INST_JAVA" ')
    assert '--bootstrap-no-update' in command
    assert '-g -s client' in command
    assert command.endswith(
        "https://raw.githubusercontent.com/" + lock["repository"] + "/" + lock["version"] + "/pack/pack.toml"
    )
    for asset in lock["assets"].values():
        assert len(asset["sha256"]) == 64
    world_directories = []
    for key in ("example_world", "expanded_world"):
        asset = lock["assets"][key]
        assert asset["url"].startswith("https://")
        directory = asset["directory"]
        assert directory and directory not in (".", "..")
        assert not any(character in directory for character in "/\\:")
        world_directories.append(directory)
    assert len(set(world_directories)) == len(world_directories)
    print("Packwiz index, five pinned mods, Prism versions and native/16 solver settings verified")


if __name__ == "__main__":
    verify()
