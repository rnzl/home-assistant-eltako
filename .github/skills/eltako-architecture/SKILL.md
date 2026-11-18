---
name: eltako-architecture
description: "Use when changing or refactoring gateway, bus, EnOcean, device, CLI, or Home Assistant architecture."
---

# Eltako architecture

1. Read the relevant sections of `docs/architecture/readme.md` and the affected
   code. The guide describes the existing system, not all of the desired boundaries.
2. Keep the intended boundaries explicit:
   - Gateway and ELTAKO bus: transport, framing, discovery, addressing and memory.
   - Device and EnOcean model: EEPs, telegrams, identity, state and commands,
     independent of Home Assistant.
   - Home Assistant adapter: config entries, entities, availability and services.
3. Refactor incrementally alongside concrete behavior changes; avoid a broad rewrite.
4. Preserve sender IDs, gateway base IDs and Home Assistant entity identifiers.
5. Keep one gateway owner coordinating bus operations.
6. Treat the standalone runtime as a Home Assistant shim adapter, not yet an
   independent core.
7. Test behavior at the affected boundary and update directly related documentation.
