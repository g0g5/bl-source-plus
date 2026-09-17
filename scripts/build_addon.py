"""Package the Blender add-on source into an installable zip.

Usage:
    uv run python scripts/build_addon.py
    python scripts/build_addon.py --out-dir dist

The resulting archive contains a single top-level ``bl_source_plus/`` folder,
which is what Blender expects when installing an add-on from a zip
(Edit > Preferences > Add-ons > Install...).
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
import tomllib
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PACKAGE_DIR = REPO_ROOT / "src" / "bl_source_plus"
DEFAULT_OUT_DIR = REPO_ROOT / "dist"
PYPROJECT_PATH = REPO_ROOT / "pyproject.toml"

EXCLUDED_DIRS = {"__pycache__"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".pyd", ".blend1", ".blend2"}
EXCLUDED_NAMES = {".DS_Store", "Thumbs.db"}


def read_project_version(pyproject: Path) -> str:
    """Read ``[project].version`` from pyproject.toml for the archive filename."""
    with pyproject.open("rb") as fh:
        data = tomllib.load(fh)
    version = data.get("project", {}).get("version")
    if not version:
        raise ValueError(f"No [project].version found in {pyproject}")
    return str(version)


def should_skip(path: Path) -> bool:
    if path.name in EXCLUDED_NAMES:
        return True
    if path.suffix.lower() in EXCLUDED_SUFFIXES:
        return True
    if any(part in EXCLUDED_DIRS for part in path.parts):
        return True
    if any(part.startswith(".") for part in path.parts):
        return True
    return False


def iter_package_files(package_dir: Path):
    for root, dirs, files in os.walk(package_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS and not d.startswith(".")]
        root_path = Path(root)
        for name in files:
            file_path = root_path / name
            if should_skip(file_path.relative_to(package_dir)):
                continue
            yield file_path


def build_zip(package_dir: Path, out_dir: Path) -> Path:
    if not (package_dir / "__init__.py").is_file():
        raise FileNotFoundError(f"Not an add-on package (missing __init__.py): {package_dir}")

    package_name = package_dir.name
    version_str = read_project_version(PYPROJECT_PATH)

    out_dir.mkdir(parents=True, exist_ok=True)
    zip_path = out_dir / f"{package_name}-{version_str}.zip"
    if zip_path.exists():
        zip_path.unlink()

    staging = Path(tempfile.mkdtemp(prefix=f"{package_name}-build-"))
    try:
        for src in iter_package_files(package_dir):
            rel = src.relative_to(package_dir)
            dst = staging / package_name / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

        entries = sorted(
            p for p in (staging / package_name).rglob("*") if p.is_file()
        )
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for file_path in entries:
                zf.write(file_path, file_path.relative_to(staging).as_posix())
    finally:
        shutil.rmtree(staging, ignore_errors=True)

    return zip_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--package-dir",
        type=Path,
        default=DEFAULT_PACKAGE_DIR,
        help="Add-on package folder to package (default: src/bl_source_plus)",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=DEFAULT_OUT_DIR,
        help="Output directory for the zip (default: dist)",
    )
    args = parser.parse_args(argv)

    package_dir = args.package_dir.resolve()
    out_dir = args.out_dir.resolve()

    try:
        zip_path = build_zip(package_dir, out_dir)
    except (FileNotFoundError, ValueError) as err:
        print(f"error: {err}", file=sys.stderr)
        return 1

    print(f"Built {zip_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
