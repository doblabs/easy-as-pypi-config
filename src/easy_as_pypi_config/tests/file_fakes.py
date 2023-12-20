# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/easy-as-pypi-config#🍐
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

"""Useful generic file fixtures."""

import os
import sys
import tempfile
import unicodedata
from pathlib import Path

import fauxfactory
import py
import pytest

# 2023-11-13: GHA macOS py3.12 will sometimes reject gen_utf8 filenames, e.g.,:
#   tests/test_fileboss.py:227: in simple_config_obj
#     with open(filepath, "w") as conf_file:
#   OSError: [Errno 92] Illegal byte sequence:
#     '/private/var/folders/3s/vfzpb5r/T/pytest-of-runner/pytest-0/
#      test_load_config_obj_fail_dupl0/胆작〳ޖ㩋蠌쟲嵁𘀢𞁗'
# - It failed this test most recently (and the first time):
#       def test_load_config_obj_fail_duplicate_error
#   - Though it passed when I re-ran the test (sorta as I expected).
# - TRACK/2023-11-13 01:29: This was the first time I've seen this failure.
#   - Keep an eye on it... maybe there's a filename-safe gen_utf8 generator.
# - One suggestion:
#       filename = unicodedata.normalize(
#           'NFC', unicode(filename, 'utf-8')
#       ).encode('utf-8')
#   except that snipped is from 2012, and what's unicode()?
# - REFER: "MacOS X uses a special kind of decomposed UTF-8 to store filenames."
# https://web.archive.org/web/20120423075412/http://boodebr.org/main/python/all-about-python-and-unicode#PLAT_WIN
# - BEGET:
# https://stackoverflow.com/questions/9757843/unicode-encoding-for-filesystem-in-mac-os-x-not-correct-in-python
# - REFER: *HFS Plus Volume Format*
# https://developer.apple.com/library/archive/technotes/tn/tn1150.html#UnicodeSubtleties
# - REFER: "The Unicode Decomposition table contains a list of characters
#   that are illegal as part of an HFS Plus string"
#   https://developer.apple.com/library/archive/technotes/tn/tn1150table.html

# 2023-12-20: Failed again. I've add a `Path()` check, let's see if that works!
# REFER: Some blather on OS path and Unicode, from Apple's perspective:
# https://opensource.apple.com/source/subversion/subversion-52/subversion/notes/unicode-composition-for-filenames.auto.html


@pytest.fixture
def filename():
    """Provide a filename string."""
    filename = fauxfactory.gen_utf8()
    if sys.platform.startswith("darwin"):
        # FIXME/2023-12-20 05:10: Design test to fail on macOS again.
        # - I'm trying to think how I'd generate output from pytest on CI,
        #   other than raising an error and having CI dump the message.
        # - Though I want the job to fail so I think to look at this trace!
        trace_msgs = []

        def validate_filename(fname, context):
            trace_msg = f"Path({fname})"
            try:
                Path(fname)
                trace_msgs.append(f"{context}: {trace_msg} passed")
            except OSError as err:
                fname = None
                trace_msgs.append(f"{context}: {trace_msg} failed: {repr(err)}")

            return fname

        raw_valid = validate_filename(filename, "raw")

        nfc_fname = unicodedata.normalize("NFC", filename)
        nfc_valid = validate_filename(nfc_fname, "NFC")

        nfd_fname = unicodedata.normalize("NFD", filename)
        nfd_valid = validate_filename(nfd_fname, "NFD")

        if filename != nfc_fname:
            trace_msgs.append("filename != nfc_fname")
        if filename != nfd_fname:
            trace_msgs.append("filename != nfd_fname")
        if nfc_fname != nfd_fname:
            trace_msgs.append("nfc_fname != nfd_fname")

        if not raw_valid:
            if not nfc_valid:
                if not nfd_valid:
                    raise RuntimeError(" / ".join(trace_msgs))
                else:
                    filename = nfd_fname
            else:
                filename = nfc_fname

        # 2023-12-20: I want to see this failure when it happens next.
        # - Then only do this error if none are valid.
        if not (raw_valid and nfc_valid and nfd_valid):
            raise RuntimeError(" / ".join(trace_msgs))

    return filename


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
