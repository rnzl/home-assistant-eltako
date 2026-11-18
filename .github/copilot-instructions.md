# Repository instructions

- Make focused changes and preserve existing behavior and identifiers.
- Read relevant code and tests before editing; reuse existing patterns.
- Run the smallest relevant tests first, then broader checks when needed.
- On POSIX, use the offline runner for automated tests:
  - Integration: `python -m tests.run_offline unittest discover tests -v`
  - Standalone: `python -m tests.run_offline pytest eltako_standalone/tests -q`
- Run the suites in separate processes: standalone uses a Home Assistant shim.
- Use `ruff check custom_components tests` for the CI lint baseline.
- CI uses Python 3.14 and Node.js for frontend tests; report local differences.
- Do not read, upload, or commit personal configuration or device lists without
  explicit approval.
- Never access, scan, probe, send to, teach in, or modify real hardware without
  explicit approval for that specific operation.
- The offline runner is not a security sandbox and does not protect subprocesses.
  The standalone UI/CLI test launcher and direct pytest/unittest commands do not
  install its guard.
