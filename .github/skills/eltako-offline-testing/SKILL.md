---
name: eltako-offline-testing
description: "Use when adding tests, simulation, fake buses, recorded telegrams, or memory fixtures."
---

# Offline testing

1. Prefer existing tests, simulators and fake buses. Use temporary configurations
   containing only simulated or fake gateways. A virtual device on a real
   gateway can transmit to real hardware; it is not an offline test. See
   [simulation](../../../docs/simulation/readme.md).
2. Run tests through `python -m tests.run_offline`; run integration and standalone
   suites in separate processes.
3. Keep discovery, serial access and network access isolated. Preserve loopback
   and test-created PTYs where tests require them. The offline runner is not a
   security sandbox and does not protect subprocesses.
4. Do not assume the current simulator models real actuator memory.
5. For memory fixtures, retain complete raw rows and decoded row, function and
   channel information. Four-channel devices can share rows; never infer that
   an unknown sender is safe to remove.
6. Before enabling memory writes, verify backup and recovery, require a snapshot,
   diff and explicit confirmation, compare the entire current row, and read back.
   Treat timeouts or interruptions as unknown outcomes, not successful writes.
7. Do not access, scan, probe, send to, teach in, or modify real hardware without
   explicit approval for that specific operation. Do not capture new hardware
   data or include personal configuration or identifiable device data in fixtures
   without approval.
8. Report skipped tests, warnings and any validation that could not be performed.
