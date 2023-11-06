# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/tallybark/easy-as-pypi-config#🍐
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
# License: MIT

"""Top-level package for the easy-as-pypi-config library."""

# Convenience import(s).

from .dec_wrap import decorate_and_wrap  # noqa: F401
from .defaults import register_conf_filename  # noqa: F401
from .fileboss import (  # noqa: F401
    create_configobj,
    default_config_path,
    default_config_path_abbrev,
    echo_config_obj,
    load_config_obj,
    warn_user_config_errors,
    write_config_obj,
)
from .urable import ConfigUrable  # noqa: F401
