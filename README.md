# Cppcheck Python distribution

[![PyPI Release](https://img.shields.io/pypi/v/cppcheck-py.svg)](https://pypi.org/project/cppcheck-py)

This project packages the `cppcheck` utility as a Python package. It allows you to install `cppcheck` directly from PyPI:

```
python -m pip install cppcheck-py
```

The tools provided are:

cppcheck: performs static analysis of C/C++ source code
cppcheck-htmlreport: generates an html report of a XML file produced by cppcheck

This projects intends to release a new PyPI package for each major and minor release of `cppcheck`.

## Use with pipx

You can use `pipx` to run cppcheck, as well. For example, `pipx run cppcheck <args>` will run cppcheck without any previous install required on any machine with pipx (including all default GitHub Actions / Azure runners, avoiding requiring a pre-install step or even `actions/setup-python`).

## Building new releases

The [cppcheck-wheel repository](https://github.com/cconverse711/cppcheck-wheel) provides the logic to build and publish binary wheels of the `cppcheck` utility.

In order to add a new release, the following steps are necessary:

* Edit the [version file](https://github.com/cconverse711/clang-format-wheel/blob/main/cppcheck_version.txt)
  * In the form `cppcheck_version.wheel_version`, e.g. `2.21.0.1`
* Tag the commit with this version to trigger the [GitHub Actions release workflow](https://github.com/cconverse711/cppcheck-wheel/actions/workflows/release.yml)
  * e.g. `git tag v2.21.0.1 && git push origin v2.21.0.1`

Alternatively, the workflow can be triggered manually:

On manual triggers, the following input variables are available:
* `cppcheck_version`: Override the LLVM version (default: `""`)
* `wheel_version`: Override the wheel packaging version (default `"0"`)
* `skip_emulation`: Set which emulation builds to skip, e.g. `"qemu"` (default: `""`)
* `deploy_to_testpypi`: Whether to deploy to TestPyPI instead of PyPI (default: `false`)

The repository with the precommit hook is automatically updated using a scheduled Github Actions workflow.

## Acknowledgements

This repository extends the great work of several other projects:

* `cppcheck` itself is [provided by the Cppcheck project](https://github.com/cppcheck-opensource/cppcheck) under the Apache 2.0 License with LLVM exceptions.
* The repository is inspired by [clang-format-wheel](https://github.com/ssciwr/clang-format-wheel) and [clang-tidy-wheel](https://github.com/ssciwr/clang-tidy-wheel) which are in turn based on [scikit-build-core](https://github.com/scikit-build/scikit-build-core) which greatly reduces the amount of low level code necessary to package `cppcheck`.
* The `scikit-build` packaging examples of [CMake](https://github.com/scikit-build/cmake-python-distributions) and [Ninja](https://github.com/scikit-build/ninja-python-distributions) were very helpful in packaging `cppcheck`.
* The CI build process is controlled by [cibuildwheel](https://github.com/pypa/cibuildwheel) which makes building wheels across a number of platforms a pleasant experience (!)

We are grateful for the generous provisioning with CI resources that GitHub currently offers to Open Source projects.

## Troubleshooting

To see which cppcheck binary the package is using
you can set `CPPCHECK_WHEEL_VERBOSE` to `1` in your environment.
