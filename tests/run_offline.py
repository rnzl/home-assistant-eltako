"""Run either test suite in its own guarded process.

Usage: python -m tests.run_offline unittest [unittest arguments]
       python -m tests.run_offline pytest [pytest arguments]
"""

import sys

from tests.offline_guard import install


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in {"unittest", "pytest"}:
        raise SystemExit(__doc__)
    suite, arguments = sys.argv[1], sys.argv[2:]
    install()
    if suite == "unittest":
        from tests.offline_guard import isolate_port_discovery
        isolate_port_discovery()
        import unittest
        unittest.main(module=None, argv=["unittest", *arguments])
    else:
        import pytest
        raise SystemExit(pytest.main(arguments))


if __name__ == "__main__":
    main()
