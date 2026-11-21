---
name: eltako-telegram-debugging
description: "Use when debugging EnOcean or ELTAKO telegrams, EEP encoding or decoding, sender addressing, gateway routing, or entity state from telegrams."
---

# Telegram and EEP debugging

1. Identify the expected and observed behavior, direction, gateway type and EEP.
   Use synthetic data or existing approved, sanitized fixtures; do not read
   personal configuration or device lists without explicit approval.
2. For reception, trace the raw frame and message type through
   `core/gateway.py` and `core/entity.py` to the affected platform's
   `decode_message` and state update. Check local versus global addresses,
   gateway base ID and subscribed addresses. Do not assume every telegram is
   dispatched: reception depends on message type and a known base ID.
3. For sending, trace the platform's EEP encoding and sender ID through the
   dispatcher and gateway, including additional senders and bus-busy behavior
   where applicable. Distinguish a generated telegram from one actually sent or
   acknowledged.
4. Check EEP definitions and relevant existing tests rather than guessing from
   a decoded value. The [telegram analysis guide](../../../docs/telegram-analysis/readme.md)
   is a reference; verify its claims against current code.
5. Reproduce the issue with the smallest relevant offline test using a fake bus,
   simulated gateway or synthetic telegram. Follow the offline-testing skill;
   never use a real gateway for simulation without explicit approval.
6. Report the failing boundary, evidence and any unverified hardware behavior.
   Do not access, scan, probe, send to, teach in, or modify real hardware without
   explicit approval for that specific operation.
