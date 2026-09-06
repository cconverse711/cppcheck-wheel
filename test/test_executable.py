import os
import sys
import tempfile
from pathlib import Path

import pytest

EXECUTABLES = (
    "cppcheck",
    "cppcheck-htmlreport",
)


@pytest.fixture(autouse=True)
def ensure_cppcheck_from_wheel(monkeypatch):
    """Test the installed cppcheck package, not the local one."""
    this_dir = Path(__file__).resolve().parent

    paths_to_remove = {
        this_dir,
        this_dir.parent,
    }

    sys.path[:] = [
        path for path in sys.path if Path(path).resolve() not in paths_to_remove
    ]

    monkeypatch.delitem(sys.modules, "cppcheck", raising=False)


@pytest.mark.parametrize("executable", EXECUTABLES)
def test_executable_file(capsys, executable):
    import cppcheck

    cppcheck._get_executable.cache_clear()
    exe = cppcheck.get_executable(executable)
    assert os.path.exists(exe)
    assert os.access(exe, os.X_OK)
    assert capsys.readouterr().out == ""


def test_verbose_output(capsys, monkeypatch):
    import cppcheck

    monkeypatch.setenv("CPPCHECK_WHEEL_VERBOSE", "1")
    # need to clear cache to make sure the function is run again
    cppcheck._get_executable.cache_clear()
    cppcheck.get_executable("cppcheck")
    assert capsys.readouterr().out


def test_cppcheck():
    import cppcheck

    with tempfile.TemporaryDirectory() as tmpdir:
        compilation_unit = Path(tmpdir) / "dummy.cpp"
        with open(compilation_unit, "w") as ostr:
            ostr.write("int main() { return 0;}\n")

        # Verify that the addon and library files can be found.
        xml_path = Path(tmpdir) / "report.xml"
        assert (
            cppcheck._run(
                "cppcheck",
                "--enable=all",
                "--addon=naming",
                "--library=std",
                "--xml",
                f"--output-file={xml_path!s}",
                str(compilation_unit),
            )
            == 0
        )

        assert (
            cppcheck._run_python(
                "cppcheck-htmlreport",
                f"--file={xml_path!s}",
                f"--report-dir={tmpdir}/html",
            )
            == 0
        )
