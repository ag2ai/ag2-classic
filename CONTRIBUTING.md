# Contributing to AG2 Classic

> [!IMPORTANT]
> **This is AG2 Classic** — the classic AG2 framework built around `ConversableAgent`, published to PyPI as [`autogen`](https://pypi.org/project/autogen/). It is in **maintenance mode**.
>
> **AG2 is the current, actively developed version.** New features, enhancements, and new integrations belong there: [github.com/ag2ai/ag2](https://github.com/ag2ai/ag2) (PyPI: [`ag2`](https://pypi.org/project/ag2/)), docs at [docs.ag2.ai](https://docs.ag2.ai/).

## What we accept

Because this repository is in maintenance mode, we only accept changes that keep the existing framework working and safe:

- **Security fixes** — patches for confirmed vulnerabilities (see [SECURITY.md](.github/SECURITY.md) for how to report privately).
- **Critical bug fixes** — corrections to broken behaviour in existing functionality.
- **Maintenance** — dependency and compatibility updates (e.g. keeping the package installable and passing on supported Python versions), build/packaging fixes, and CI upkeep.
- **Documentation corrections** — fixing inaccurate, broken, or outdated documentation for existing behaviour.

## What we do **not** accept

- **New features or enhancements**.
- **New agents, tools, models, or integrations.**
- **API changes or refactors** that are not required to fix a security issue or critical bug.
- **Behavioural changes** beyond what is needed to restore correct, documented behaviour.
- **New Documentation** beyond what is needed to align with the existing code base.

Rather than generating features or enhancements for this, AG2 Classic, repository, please consider creating them for the active AG2 framework in the [`ag2`](https://github.com/ag2ai/ag2) repository.

## Before you open a pull request

1. **Open an issue first** for anything beyond a trivial fix, so a maintainer can confirm it's in scope for maintenance mode before you invest time.
   - [Report a bug](https://github.com/ag2ai/ag2classic/issues/new?template=bug_report.yml)
   - Report a security vulnerability privately via the process in [SECURITY.md](.github/SECURITY.md) — **do not** open a public issue.
2. **Keep the change focused.** A maintenance PR should fix one thing and touch the minimum surface area needed.
3. **Add or update tests** covering the fix where relevant.
4. **Make sure all automated checks pass**, including pre-commit hooks and the test suite.

## License headers

Please include the following header at the top of each new source file you create:

```python
# Copyright (c) 2023 - 2026, AG2ai, Inc., AG2ai open-source projects maintainers and core contributors
#
# SPDX-License-Identifier: Apache-2.0
```

For files that contain or are derived from the original MIT-licensed code from https://github.com/microsoft/autogen, use this extended header:

```python
# Copyright (c) 2023 - 2026, AG2ai, Inc., AG2ai open-source projects maintainers and core contributors
#
# SPDX-License-Identifier: Apache-2.0
#
# Portions derived from https://github.com/microsoft/autogen are under the MIT License.
# SPDX-License-Identifier: MIT
```

## AI-assisted contributions

AG2 welcomes AI-assisted contributions. Contributors remain responsible for everything they submit — see [.github/AI_POLICY.md](.github/AI_POLICY.md).

## Questions

For questions, discussion, or help getting started with the actively developed version, join the [AG2 community on Discord](https://discord.gg/pAbnFJrkgZ).
