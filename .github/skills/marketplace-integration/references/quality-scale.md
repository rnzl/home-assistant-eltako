# Grading a custom integration against the quality scale

Home Assistant's integration quality scale is the project's written
definition of a well-made integration: 54 rules in four cumulative tiers
(20 Bronze, 10 Silver, 21 Gold, 3 Platinum, as of November 2026). This file
is how this skill applies it to an integration that lives outside core.

## What a tier means outside core

- Core gives custom integrations no tier. Its manifest value for them is
  `custom`, and nobody in the project reviews or awards one. Do not add
  `quality_scale` to a custom integration's `manifest.json`, and do not tell
  the user their integration "is Silver" as if that were official. Say it
  "meets the Silver rules".
- The rules are still the best yardstick there is. Hacs/default reviewers
  ask for many of them by name, and they are exactly what core wants if the
  integration is ever proposed for core, where Bronze is the minimum.
- Default target: **Bronze is the floor, Silver is the goal** for anything
  released to other people. Gold and Platinum are worth naming as next
  steps, but only make them part of the work when the user asks.

## The live rule pages

Every rule has its own page at
`https://contributors.home-assistant.io/core/quality-scale/<rule>/`
(Markdown: add `index.md`). The full list per tier is
`https://contributors.home-assistant.io/core/quality-scale/rules/`. Each page
has the reason for the rule, an example, how core checks it and when it does
not apply. Rules get added to tiers over time, so before grading against a
tier, check the rules page still has the counts above. If it does not, grade
against the live list and tell the user this file is out of date. The pages
are written for core: read them through the
[translation table](ha-best-practices.md#reading-the-live-docs-for-a-custom-integration)
before applying them.

## How to grade

Give every rule in the target tier, and in every tier below it, one of:

| Verdict | Meaning |
| --- | --- |
| **Met** | You found the code (or docs) that satisfies it. Cite file:line. |
| **Not met** | It applies and is missing or wrong. Cite where, and give the fix. |
| **N/A** | The rule's own exception covers this integration (it has no actions, does not poll, needs no sign-in…). Say which exception. |
| **Unknown** | Needs something you cannot see: the docs site, GitHub, a run against the device. Say what the user has to confirm. |

A tier is met when every rule in it and below it is Met or N/A. Unknowns
keep it open: report them as such, not as passes. Do not guess a verdict
from file names or from the pre-flight script alone; read the code.

The report starts with one line per tier, then the open rules:

```text
Quality scale (unofficial, custom integrations have no tier)
  Bronze   18/20 met, 1 N/A, 1 not met   -> not met: test-before-setup
  Silver    6/10 met, 1 N/A, 2 not met, 1 unknown
            -> not met: reauthentication-flow, parallel-updates
            -> unknown: integration-owner (are issues answered?)
  Gold      not graded (Silver not met)
```

Stop grading at the first tier that is not met unless the user asked for a
full picture. In the review findings, a Bronze rule that is not met is at
least **Should fix**; a higher-tier rule is **Nice to have** unless the user
set that tier as the target.

## Bronze

| Rule | What it means here | Where to look |
| --- | --- | --- |
| `action-setup` | Actions are registered once, in `async_setup`, and check the entry is loaded before using it. | `__init__.py`, `services.py`: no `hass.services.async_register` inside `async_setup_entry` |
| `appropriate-polling` | The poll interval suits the source: no seconds-long polling of a cloud API. | `SCAN_INTERVAL`, `update_interval=` |
| `brands` | Icon (and ideally logo) in `custom_components/<domain>/brand/`. The brands repository is for core only. | the `brand/` folder; no `ignore: brands` in the HACS workflow |
| `common-modules` | The coordinator lives in `coordinator.py` and the shared base entity in `entity.py`. | file list |
| `config-flow` | UI setup only, `data_description` for each field, connection data in `entry.data` and tunables in `entry.options`. | `config_flow.py`, `translations/en.json` |
| `config-flow-test-coverage` | Tests cover every flow step, every error and recovery from it, and the duplicate abort. | `tests/test_config_flow.py` |
| `dependency-transparency` | Each `requirements` package is open source, on PyPI, released from public CI, tagged, pinned with `==`. N/A with no requirements. | `manifest.json`, the library's repository |
| `docs-actions` | The README (or the `documentation` URL) describes each action. N/A without actions. | README, `services.yaml` |
| `docs-conditions` | Each condition the integration provides is described. N/A without conditions. | README, `conditions.yaml` |
| `docs-high-level-description` | The docs say what the device, product or service is. | README opening |
| `docs-installation-instructions` | Step-by-step install through the Marketplace and manual install, with prerequisites (account, firmware, API key). | README |
| `docs-removal-instructions` | How to remove the integration and anything it leaves behind on the device or account. | README |
| `docs-triggers` | Each trigger the integration provides is described. N/A without triggers. | README, `triggers.yaml` |
| `entity-event-setup` | Subscriptions start in `async_added_to_hass` and end through `async_on_remove`. | entity modules |
| `entity-unique-id` | Every entity has a stable unique ID, not built from a name, IP or title. | `_attr_unique_id` |
| `has-entity-name` | `_attr_has_entity_name = True` on every entity. | base entity |
| `runtime-data` | Per-entry objects in a typed `entry.runtime_data`, not `hass.data`. | `__init__.py`, `data.py` |
| `test-before-configure` | The flow connects before it creates the entry, and maps failures to translated errors. | `config_flow.py` |
| `test-before-setup` | Setup fails with `ConfigEntryNotReady`, `ConfigEntryAuthFailed` or `ConfigEntryError` as fits. A coordinator's first refresh counts. | `async_setup_entry` |
| `unique-config-entry` | The same device or account cannot be added twice: a unique ID or `_async_abort_entries_match`, or `single_config_entry`. | `config_flow.py`, `manifest.json` |

## Silver

| Rule | What it means here | Where to look |
| --- | --- | --- |
| `action-exceptions` | Failing actions raise `ServiceValidationError` (bad input) or `HomeAssistantError` (it went wrong), never return quietly. N/A without actions. | action handlers, entity command methods |
| `config-entry-unloading` | `async_unload_entry` undoes everything setup did, so a reload works without a restart. | `__init__.py`, `async_on_unload` calls |
| `docs-configuration-parameters` | Each options-flow field is documented. N/A without an options flow. | README |
| `docs-installation-parameters` | Each field asked for during setup is documented, including where to find it. | README |
| `entity-unavailable` | Lost contact shows as unavailable, never as a stale or zero value. | `available`, `CoordinatorEntity` |
| `integration-owner` | `codeowners` names the maintainer, and issues get answered. The second half is Unknown from code alone. | `manifest.json`, the issue tracker |
| `log-when-unavailable` | One log line when the connection is lost and one when it returns, not one per poll. | coordinator, push handlers |
| `parallel-updates` | Every platform module sets `PARALLEL_UPDATES`. | each platform file |
| `reauthentication-flow` | Credentials can be replaced from the UI without removing the entry, and a different account cannot take over. N/A without sign-in. | `async_step_reauth*` |
| `test-coverage` | Over 95% per module. Run it with `pytest --cov=custom_components.<domain> --cov-report term-missing` on `pytest-homeassistant-custom-component`. | `tests/`, CI |

## Gold

| Rule | What it means here | Where to look |
| --- | --- | --- |
| `devices` | Entities sit on devices with full `DeviceInfo`. | base entity |
| `diagnostics` | A diagnostics download with secrets redacted. | `diagnostics.py`, `async_redact_data` |
| `discovery` | The device is found by zeroconf, DHCP, SSDP, USB or Bluetooth. N/A when it cannot be discovered (most cloud services). | manifest matchers, `async_step_<source>` |
| `discovery-update-info` | Rediscovery updates the stored address of a known device. | discovery steps: `_abort_if_unique_id_configured(updates=…)` |
| `docs-data-update` | The docs say how and how often data updates (poll interval, push). | README |
| `docs-examples` | Automation examples or blueprints. | README |
| `docs-known-limitations` | What the integration does not do or does badly. | README |
| `docs-supported-devices` | Known working and known not-working models. | README |
| `docs-supported-functions` | Each entity and what it does. | README |
| `docs-troubleshooting` | Common problems and their fixes, including how to enable debug logs. | README |
| `docs-use-cases` | What people can do with it. | README |
| `dynamic-devices` | A device added to the account or hub later shows up on its own, with no reload or re-setup. | coordinator listener adding entities |
| `entity-category` | Config and diagnostic entities carry an `entity_category`. | entity descriptions |
| `entity-device-class` | A device class wherever one fits. | entity descriptions |
| `entity-disabled-by-default` | Noisy or rarely wanted entities are off by default. | `entity_registry_enabled_default` |
| `entity-translations` | Names via `translation_key` in `translations/en.json` (core says `strings.json`). | entities, `translations/en.json` |
| `exception-translations` | User-facing errors use `translation_domain` / `translation_key`. | `raise` sites |
| `icon-translations` | Custom icons, including state-based ones, in `icons.json`, not `_attr_icon`. | `icons.json` |
| `reconfiguration-flow` | Host or connection details can be changed without re-adding. | `async_step_reconfigure` |
| `repair-issues` | Problems the user must fix raise a repair issue. N/A when there are none. | `ir.async_create_issue` |
| `stale-devices` | Devices that disappear are removed, or the user can delete them. | `async_remove_config_entry_device`, device registry cleanup |

## Platinum

| Rule | What it means here | Where to look |
| --- | --- | --- |
| `async-dependency` | The library is asyncio-native, with no executor jobs for its I/O. | the library, `async_add_executor_job` calls |
| `inject-websession` | The library accepts Home Assistant's `aiohttp` or `httpx` session. | client construction |
| `strict-typing` | The integration passes `mypy --strict` (configured in the repository; core's `.strict-typing` file does not apply), the library ships `py.typed`, and the typed config entry is used everywhere. | `mypy.ini` / `pyproject.toml`, CI |

## What the tiers do not cover

The scale says nothing about several things hacs/default reviewers do check:
security (secrets, admin-only actions, escaping in bundled frontend code),
staying inside the integration's own namespace, and the catalog
requirements. A Gold-grade integration can still be closed on those, so a
review grades the scale *and* goes through
[review-rounds.md](review-rounds.md) and
[marketplace-requirements.md](marketplace-requirements.md).
