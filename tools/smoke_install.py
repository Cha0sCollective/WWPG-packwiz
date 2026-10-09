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


def smoke(java, pack_url=None):
    archive = build()
    handler = functools.partial(QuietHandler, directory=str(ROOT / "pack"))
    server = None
    if pack_url is None:
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        pack_url = "http://127.0.0.1:" + str(server.server_port) + "/pack.toml"
    try:
        with tempfile.TemporaryDirectory(prefix="prism-smoke-", dir=ROOT / "build") as directory:
            instance = Path(directory)
            assert instance.resolve().is_relative_to((ROOT / "build").resolve())
            with zipfile.ZipFile(archive) as source:
                source.extractall(instance)
            minecraft = instance / "minecraft"
            env = os.environ.copy()
            env["INST_DIR"] = str(instance)
            env["INST_MC_DIR"] = str(minecraft)
            args = [java, "-Djava.awt.headless=true", "-jar", str(minecraft / "packwiz-installer-bootstrap.jar"),
                    "--bootstrap-no-update", "--bootstrap-main-jar", str(minecraft / "packwiz-installer.jar"),
                    "-g", "-s", "client", pack_url]
            for phase in (1, 2):
                result = subprocess.run(args, cwd=minecraft, env=env, check=True,
                                        capture_output=True, text=True, timeout=180)
                (ROOT / "build" / ("installer-smoke-" + str(phase) + ".log")).write_text(
                    result.stdout + result.stderr, encoding="utf-8"
                )
                for mod in LOCK["mods"]:
                    actual = hashlib.sha256((minecraft / "mods" / mod["filename"]).read_bytes()).hexdigest()
                    assert actual == mod["sha256"], mod["filename"]
                components = json.loads((instance / "mmc-pack.json").read_text(encoding="utf-8"))
                installed_versions = {c["uid"]: c["version"] for c in components["components"]}
                assert installed_versions["net.minecraft"] == LOCK["minecraft"]
                assert installed_versions["net.neoforged"] == LOCK["neoforge"]
                if phase == 1:
                    marker = minecraft / "saves/WWPG Example/player-edit-sentinel.txt"
                    marker.write_text("Keep this player's world edits.\n", encoding="utf-8")
                    saved_level = (minecraft / "saves/WWPG Example/level.dat").read_bytes()
                    config = minecraft / "config/powergrid-server.toml"
                    config.write_text(config.read_text(encoding="utf-8") + "# Player config note\n", encoding="utf-8")
                else:
                    assert marker.read_text(encoding="utf-8") == "Keep this player's world edits.\n"
                    assert (minecraft / "saves/WWPG Example/level.dat").read_bytes() == saved_level
                    assert "# Player config note" in config.read_text(encoding="utf-8")
            print("Actual packwiz installation and relaunch passed: five matching jars, world and configuration preserved")
    finally:
        if server is not None:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--java", default="java")
    parser.add_argument("--pack-url")
    args = parser.parse_args()
    smoke(args.java, args.pack_url)
