"""Thin PEP 517 backend wrapper around scikit-build-core.

Ensures cppcheck's source is vendored into third_party/ before the
sdist is actually assembled, so `python -m build --sdist` (and anything
that calls this hook -- pip, cibuildwheel, twine, CI) always produces a
self-contained sdist without a manual pre-step.
"""

import subprocess
import sys
from pathlib import Path

from scikit_build_core.build import build_editable as _build_editable
from scikit_build_core.build import build_sdist as _build_sdist
from scikit_build_core.build import build_wheel as _build_wheel

# Re-export everything scikit-build-core provides; we only override
# build_sdist. Anything not overridden here still needs to exist as an
# attribute for setuptools/pip's PEP 517 hook lookup to find it.
from scikit_build_core.build import (  # noqa: F401
    get_requires_for_build_editable,
    get_requires_for_build_sdist,
    get_requires_for_build_wheel,
    prepare_metadata_for_build_editable,
    prepare_metadata_for_build_wheel,
)

_ROOT = Path(__file__).resolve().parent


def _vendor_cppcheck():
    vendor_script = _ROOT / "scripts" / "vendor_cppcheck.py"
    print(f"[backend_wrapper] running {vendor_script}", file=sys.stderr)
    subprocess.check_call([sys.executable, str(vendor_script)])


def build_editable(editable_directory, config_settings=None, metadata_directory=None):
    _vendor_cppcheck()
    return _build_editable(editable_directory, config_settings, metadata_directory)


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    _vendor_cppcheck()
    return _build_wheel(wheel_directory, config_settings, metadata_directory)


def build_sdist(sdist_directory, config_settings=None):
    _vendor_cppcheck()
    return _build_sdist(sdist_directory, config_settings)
