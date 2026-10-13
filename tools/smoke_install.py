"""Install the packaged instance twice without using an existing Prism profile."""
import argparse
import functools
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import subprocess
import tempfile
import threading
import zipfile

from build_prism import LOCK, ROOT, build


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


class PackServer(ThreadingHTTPServer):
    # The installer fetches mod metadata concurrently.
    request_queue_size = 32


def smoke(java, pack_url=None, profile=LOCK["default_profile"]):
    settings = LOCK["profiles"][profile]
    mods = [mod for mod in LOCK["mods"] if mod["id"] in settings["mods"]]
    archive = build(profile)
    handler = functools.partial(QuietHandler, directory=str(ROOT / settings["pack_dir"]))
    server = None
    if pack_url is None:
        server = PackServer(("127.0.0.1", 0), handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        pack_url = "http://127.0.0.1:" + str(server.server_port) + "/pack.toml"
    try:
        with tempfile.TemporaryDirectory(prefix="prism-smoke-", dir=ROOT / "build") as directory:
            instance = Path(directory)
            assert instance.resolve().is_relative_to((ROOT / "build").resolve())
            with zipfile.ZipFile(archive) as source:
                source.extractall(instance)
                saved_world_files = {
                    entry.filename: source.read(entry) for entry in source.infolist()
                    if not entry.is_dir() and entry.filename.startswith("minecraft/saves/")
                }
            minecraft = instance / "minecraft"
            markers = [minecraft / "saves" / LOCK["assets"][key]["directory"] / "player-edit-sentinel.txt"
                       for key in settings["worlds"]]
            env = os.environ.copy()
            env["INST_DIR"] = str(instance)
            env["INST_MC_DIR"] = str(minecraft)
            args = [java, "-Djava.awt.headless=true", "-jar", str(minecraft / "packwiz-installer-bootstrap.jar"),
                    "--bootstrap-no-update", "--bootstrap-main-jar", str(minecraft / "packwiz-installer.jar"),
                    "-g", "-s", "client", pack_url]
            for phase in (1, 2):
                result = subprocess.run(args, cwd=minecraft, env=env,
                                        capture_output=True, text=True, timeout=180)
                (ROOT / "build" / ("installer-smoke-" + profile + "-" + str(phase) + ".log")).write_text(
                    result.stdout + result.stderr, encoding="utf-8"
                )
                result.check_returncode()
                assert {path.name for path in (minecraft / "mods").glob("*.jar")} == {mod["filename"] for mod in mods}
                for mod in mods:
                    actual = hashlib.sha256((minecraft / "mods" / mod["filename"]).read_bytes()).hexdigest()
                    assert actual == mod["sha256"], mod["filename"]
                components = json.loads((instance / "mmc-pack.json").read_text(encoding="utf-8"))
                installed_versions = {c["uid"]: c["version"] for c in components["components"]}
                assert installed_versions["net.minecraft"] == LOCK["minecraft"]
                assert installed_versions["net.neoforged"] == LOCK["neoforge"]
                for name, data in saved_world_files.items():
                    assert (instance / name).read_bytes() == data, name
                if phase == 1:
                    for marker in markers:
                        marker.write_text("Keep this player's world edits.\n", encoding="utf-8")
                    config = minecraft / "config/powergrid-server.toml"
                    config.write_text(config.read_text(encoding="utf-8") + "# Player config note\n", encoding="utf-8")
                else:
                    for marker in markers:
                        assert marker.read_text(encoding="utf-8") == "Keep this player's world edits.\n"
                    assert "# Player config note" in config.read_text(encoding="utf-8")
            print(f"{profile} installation and relaunch passed: {len(mods)} matching jars, both worlds and configuration preserved")
    finally:
        if server is not None:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--java", default="java")
    parser.add_argument("--pack-url")
    parser.add_argument("--profile", choices=LOCK["profiles"], default=LOCK["default_profile"])
    args = parser.parse_args()
    smoke(args.java, args.pack_url, args.profile)
