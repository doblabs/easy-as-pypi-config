############
Installation
############

.. vim:tw=0:ts=3:sw=3:et:norl:nospell:ft=rst

.. |virtualenv| replace:: ``virtualenv``
.. _virtualenv: https://virtualenv.pypa.io/en/latest/

.. |workon| replace:: ``workon``
.. _workon: https://virtualenvwrapper.readthedocs.io/en/latest/command_ref.html?highlight=workon#workon

To install system-wide, run as superuser::

    $ pip3 install easy-as-pypi-config

To install user-local, simply run::

    $ pip3 install -U easy-as-pypi-config

To install within a |virtualenv|_, try::

    $ cd "$(mktemp -d)"

    $ python3 -m venv .venv

    $ . ./.venv/bin/activate

    (easy-as-pypi-config) $ pip install easy-as-pypi-config

To develop on the project, link to the source files instead::

    (easy-as-pypi-config) $ deactivate
    $ git clone git@github.com:doblabs/easy-as-pypi-config.git
    $ cd easy-as-pypi-config
    $ python3 -m venv easy-as-pypi-config
    $ . ./.venv/bin/activate
    (easy-as-pypi-config) $ make develop

After creating the virtual environment, it's easy to start
developing from a fresh terminal::

    $ cd easy-as-pypi-config
    $ . ./.venv/bin/activate
    (easy-as-pypi-config) $ ...

