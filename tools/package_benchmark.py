"""Package the existing native 10,000-tier export with its requested public label."""
import argparse
import gzip
import hashlib
from io import BytesIO
import json
from pathlib import Path, PurePosixPath
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA256 = "1b93bfcff2f4584370deb150b1a6a718b9ccc1d302ac1ccd6b03aaa4a3b00c61"
SOURCE_DIRECTORY = "WWPG Benchmark - MIXED - 10000 nodes"
NAME = "14,650 node benchmark"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def rename_level(data):
    raw = gzip.decompress(data)
    marker = b"\x08\x00\x09LevelName"
    if raw.count(marker) != 1:
        raise ValueError("Expected one LevelName tag")
    start = raw.index(marker) + len(marker)
    length = int.from_bytes(raw[start:start + 2], "big")
    name = NAME.encode("utf-8")
    return gzip.compress(raw[:start] + len(name).to_bytes(2, "big") + name
                         + raw[start + 2 + length:], mtime=0)


def package(source):
    data = source.read_bytes()
    if digest(data) != SOURCE_SHA256:
        raise ValueError("Unexpected benchmark source checksum")
    files = {}
    with zipfile.ZipFile(BytesIO(data)) as archive:
        for line in archive.read("SHA256SUMS.txt").decode("utf-8").splitlines():
            expected, name = line.split("  ", 1)
            if digest(archive.read(name)) != expected:
                raise ValueError("Source member checksum mismatch: " + name)
        for entry in archive.infolist():
            if entry.filename == "SHA256SUMS.txt" or entry.is_dir():
                continue
            path = PurePosixPath(entry.filename)
            if (path.is_absolute() or ".." in path.parts or "\\" in entry.filename
                    or path.parts[0] != SOURCE_DIRECTORY):
                raise ValueError("Unexpected source path: " + entry.filename)
            relative = PurePosixPath(*path.parts[1:]).as_posix()
            files[relative] = archive.read(entry)
    grid = json.loads(files["WWPG_BENCHMARK.json"])
    if (grid["requested_tier"] != 10000 or grid["variant"] != "MIXED"
            or grid["audit"]["electrical_nodes"] != 14650 or grid["audit"]["edges"] != 20637):
        raise ValueError("Unexpected saved benchmark workload")
    files["level.dat"] = rename_level(files["level.dat"])
    original = json.loads(files["WWPG_BENCHMARK_RUNTIME.json"])
    provenance = {
        "schema": 1,
        "source_export_sha256": SOURCE_SHA256,
        "generated_with_wwpg": original["generated_with_wwpg"],
        "generation_runtime_sha256": original["runtime"]["sha256"],
        "generation_profile": original["profile"]["name"],
        "generation_heap_gib": original["profile"]["heap_gib"],
        "requested_tier": grid["requested_tier"],
        "electrical_nodes": grid["audit"]["electrical_nodes"],
        "connections": grid["audit"]["edges"],
        "native_circuit_files_changed": False,
        "packaging_changes": ["Save folder and LevelName", "Public instructions and provenance"],
        "capacity_certified": False,
    }
    files["WWPG_BENCHMARK_RUNTIME.json"] = (json.dumps(provenance, indent=2) + "\n").encode("utf-8")
    files["BENCHMARK_README.txt"] = (
        NAME + "\n\n"
        "Open this save from Singleplayer in the WWPG 0.2.2-beta.2 test pack.\n"
        "Minecraft 1.21.1, NeoForge 21.1.248, Java 21; PG native engine, 16 substeps.\n"
        "Use an 8 GiB maximum heap; leave sufficient memory for the operating system.\n"
        "Creative spawn: 1038, 64, 1038. Loading this large grid can take several minutes.\n\n"
        "This is the nominal 10,000-tier mixed benchmark: 14,650 actual electrical nodes,\n"
        "20,637 connections, 1,050 stateful devices and 50 factories across 953 chunks.\n"
        "Native wires, panels, boards and stored state are retained. The original save\n"
        "was generated with WWPG 0.2.2-dev.2; the test pack supplies beta.2.\n"
        "An optional separate helper records timed trials; it is not required to inspect\n"
        "the existing CEE and PG circuits. This pack does not run a timed trial automatically.\n"
        "The large-network 20 TPS goal remains open. Inclusion is not capacity certification.\n"
        "Keep a clean instance for comparisons; edits change the workload.\n"
    ).encode("utf-8")
    files["PACK_SHA256SUMS.txt"] = "".join(
        digest(content) + "  " + name + "\n" for name, content in sorted(files.items())
    ).encode("utf-8")
    output = ROOT / "worlds/wwpg-benchmark-14650-v1.zip"
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, content in sorted(files.items()):
            entry = zipfile.ZipInfo(NAME + "/" + name, (2026, 10, 14, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, content)
    print(str(output))
    print(digest(output.read_bytes()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    args = parser.parse_args()
    package(args.source)
