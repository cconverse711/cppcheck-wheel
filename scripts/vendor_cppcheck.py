#!/usr/bin/env python3
"""Run before building an sdist or wheel: vendors cppcheck's source so the sdist
is self-contained and doesn't require network access to build."""

import pathlib
import re
import urllib.request

from scikit_build_core.metadata.regex import dynamic_metadata

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

ROOT = pathlib.Path(__file__).resolve().parent.parent

with open(ROOT / "pyproject.toml", "rb") as f:
    pyproject = tomllib.load(f)

    version_entry = next(
        e for e in pyproject["tool"]["dynamic-metadata"] if e["field"] == "version"
    )
    settings = {
        k: v for k, v in version_entry.items() if k not in ("provider", "field")
    }
    project_version = dynamic_metadata("version", settings)

cppcheck_version = re.match(r"^(\d+\.\d+\.\d+)", project_version).group(1)
url = f"https://github.com/cppcheck-opensource/cppcheck/archive/refs/tags/{cppcheck_version}.tar.gz"
archive_path = ROOT / "third_party" / f"cppcheck-{cppcheck_version}.tar.gz"
if archive_path.exists():
    print(f"{archive_path} already exists, skipping download.")
else:
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {url}")
    urllib.request.urlretrieve(url, archive_path)
