---
name: eltako-hardware-testing
description: "Use when validating real ELTAKO or EnOcean hardware, probing serial gateways, scanning a bus or memory, running device tests, or testing discovery against a live gateway. Requires operation-specific approval before hardware access."
---

# Real-hardware validation

1. Prefer simulation and offline tests. Follow the [offline-testing skill](../eltako-offline-testing/SKILL.md) and [simulation guide](../../../docs/simulation/readme.md) unless the question specifically requires real hardware.
2. Before touching hardware, get explicit approval for the specific operation, gateway or port, and expected effects. Approval to diagnose is not approval to probe, read a bus, transmit, teach in, write memory, or change configuration. If approval is absent or ambiguous, do not run the operation.
3. Classify the operation before choosing a command. The [hardware-testing guide](../../../docs/hardware-testing/readme.md) and [device-test guide](../../../docs/device-tests/readme.md) are the detailed references. In particular:
   - `scan` reads USB descriptors; `detect` actively opens ports and probes gateways.
   - The `devicetest config` test sends no telegrams, but can rely on live bus or memory data. Do not describe it as hardware-free.
   - Plug-and-play bus reads, actuator tests, bus-burst tests, cover tests, teach-in, and memory writes can access or change real devices. Confirm their exact scope and effects before proceeding.
4. Ensure only one process owns a serial port. Check for Home Assistant, standalone servers, test processes, PCT14, or other gateway tools before connecting. Do not stop another process or take over its port without approval. For FAM14 bus work, use the standalone runtime or a Linux host with direct device pass-through; the TCP bridge is not reliable for bus scans.
5. Use a minimal, dedicated test configuration. Do not read personal configuration or device lists without explicit approval. Do not run standalone UI/CLI tests or direct pytest/unittest against a real configuration expecting the offline runner to protect hardware; it is not a security sandbox.
6. Bound any approved active test to the named devices and requested action. Device tests may switch actuators or drive covers; bus-burst tests transmit test telegrams. Confirm acceptable device state changes and duration, and do not assume a default sequence leaves devices in their original state.
7. Report the exact operation and scope, results, side effects, and any unverified behavior. Keep hardware observations distinct from offline or simulated results.