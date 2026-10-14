"""Build a reproducible Prism import ZIP from pinned published assets."""
import argparse
import hashlib
from io import BytesIO
import json
from pathlib import Path, PurePosixPath
from urllib.request import Request, urlopen
import zipfile

ROOT = Path(__file__).resolve().parents[1]
LOCK = json.loads((ROOT / "dependencies.json").read_text(encoding="utf-8"))


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def download(asset):
    if "path" in asset:
        path = (ROOT / asset["path"]).resolve()
        if not path.is_relative_to(ROOT.resolve()) or sha256(path.read_bytes()) != asset["sha256"]:
            raise ValueError("Local asset checksum/path mismatch: " + asset["filename"])
        return path
    path = ROOT / "build/cache" / asset["filename"]
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file() and sha256(path.read_bytes()) == asset["sha256"]:
        return path
    request = Request(asset["url"], headers={"User-Agent": "WWPG-packwiz/" + LOCK["version"]})
    with urlopen(request, timeout=60) as response:
        data = response.read()
    if sha256(data) != asset["sha256"]:
        raise ValueError("Checksum mismatch: " + asset["filename"])
    path.write_bytes(data)
    return path


def world_archive(asset):
    path = download(asset)
    if "member" not in asset:
        return zipfile.ZipFile(path)
    with zipfile.ZipFile(path) as bundle:
        data = bundle.read(asset["member"])
    if sha256(data) != asset["member_sha256"]:
        raise ValueError("Checksum mismatch: " + asset["member"])
    return zipfile.ZipFile(BytesIO(data))


def archive_path(profile):
    suffix = LOCK["profiles"][profile]["archive_suffix"]
    return ROOT / "build/distributions" / ("WWPG-Test-Pack-" + LOCK["version"] + suffix + "-Prism.zip")


def build(profile=LOCK["default_profile"]):
    from verify import verify
    verify(profile)
    settings = LOCK["profiles"][profile]
    files = {
        "instance.cfg": (ROOT / settings["instance_file"]).read_bytes(),
        "mmc-pack.json": (ROOT / "prism/mmc-pack.json").read_bytes(),
        "LICENSE": (ROOT / "LICENSE").read_bytes(),
        "README.md": (ROOT / "README.md").read_bytes(),
        "minecraft/WWPG-LICENSE.txt": (ROOT / "LICENSE").read_bytes(),
    }
    for key in ("bootstrap", "installer", "bootstrap_license", "installer_license"):
        asset = LOCK["assets"][key]
        files["minecraft/" + asset["filename"]] = download(asset).read_bytes()
    # Include the configuration on import; packwiz preserves later user edits.
    files["minecraft/config/powergrid-server.toml"] = (
        ROOT / settings["pack_dir"] / "config/powergrid-server.toml"
    ).read_bytes()
    for key in settings["worlds"]:
        asset = LOCK["assets"][key]
        with world_archive(asset) as world:
            for entry in world.infolist():
                path = PurePosixPath(entry.filename)
                if (path.is_absolute() or ".." in path.parts or not path.parts
                        or path.parts[0] != asset["directory"] or "\\" in entry.filename):
                    raise ValueError("Unexpected example-world path: " + entry.filename)
                if not entry.is_dir():
                    files["minecraft/saves/" + path.as_posix()] = world.read(entry)
        if "minecraft/saves/" + asset["directory"] + "/level.dat" not in files:
            raise ValueError("Missing level.dat: " + asset["filename"])
    output = ROOT / "build/distributions"
    output.mkdir(parents=True, exist_ok=True)
    archive = archive_path(profile)
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as target:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, (2026, 10, 9, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            target.writestr(info, data)
    (output / "SHA256SUMS.txt").write_text(
        "".join(sha256(path.read_bytes()) + "  " + path.name + "\n"
                for path in sorted(archive_path(name) for name in LOCK["profiles"])
                if path.is_file()),
        encoding="utf-8", newline="\n",
    )
    print(str(archive))
    return archive


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=LOCK["profiles"])
    args = parser.parse_args()
    for profile in ([args.profile] if args.profile else LOCK["profiles"]):
        build(profile)
