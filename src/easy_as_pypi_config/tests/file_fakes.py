# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/tallybark/easy-as-pypi-config#🍐
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

"""Useful generic file fixtures."""

import os
import py
import tempfile

import fauxfactory
import pytest


@pytest.fixture
def filename():
    """Provide a filename string."""
    return fauxfactory.gen_utf8()


@pytest.fixture
def filepath(tmpdir, filename):
    """Provide a fully qualified pathame within our tmp-dir."""
    return os.path.join(tmpdir.strpath, filename)


@pytest.fixture(scope="session")
def tmpdir_ro(request):
    # https://stackoverflow.com/questions/25525202/py-test-temporary-folder-for-the-session-scope
    # Make a temporary directory, and wrap the path string in a Path object,
    # so that `.remove` works, and so test fixtures can treat it same as a
    # `tmpdir` builtin pytest fixture.
    _tmpdir = py.path.local(tempfile.mkdtemp())
    request.addfinalizer(lambda: _tmpdir.remove(rec=1))
    return _tmpdir
