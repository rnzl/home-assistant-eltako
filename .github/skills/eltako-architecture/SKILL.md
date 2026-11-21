---
name: eltako-architecture
description: "Use when changing or refactoring gateway, bus, EnOcean, device, CLI, or Home Assistant architecture."
---

# Eltako architecture

1. Read the relevant sections of the [architecture guide](../../../docs/architecture/readme.md)
   and [requirements](../../../docs/requirements/readme.md), then verify the
   affected claims against current code and tests. The guide describes the
   existing system, not all desired boundaries; either document can drift.
2. Keep the intended boundaries explicit:
   - Gateway and ELTAKO bus: transport, framing, discovery, addressing and memory.
   - Device and EnOcean model: EEPs, telegrams, identity, state and commands,
     independent of Home Assistant.
   - Home Assistant adapter: config entries, entities, availability and services.
3. Refactor incrementally alongside concrete behavior changes; avoid a broad rewrite.
4. Preserve sender IDs, gateway base IDs and Home Assistant entity identifiers.
   Trace affected configuration, Store and config-entry persistence paths before
   changing storage or migrations; never assume deleting stored data is harmless.
5. Keep one gateway owner coordinating bus operations.
6. Treat the standalone runtime as a Home Assistant shim adapter, not yet an
   independent core.
7. Test behavior at the affected boundary and update directly related documentation.
