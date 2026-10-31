# Print-Aware Modeling

**Consider FDM printing constraints while modeling, and review existing CAD/STL designs.**

[中文完整说明](README.md) · [Skill instructions](SKILL.md) · [Contributing](CONTRIBUTING.md)

This instruction-based Agent Skill guides an AI assistant through requirements, dimensions, assembly, print orientation, local geometry and removable supports. It supports both designing from a brief or sketch and improving an existing model.

The skill instructions and detailed references are currently written in Chinese. This page is an English overview, not a separate English edition.

## What it does

- Consider orientation, splitting and self-supporting geometry before adding detail.
- Design manual supports when useful, including contact gaps, stability, tool access and removal paths.
- Review overhangs, bridges, thin features, fit and accessible sharp edges.
- Preserve functional surfaces and editable sources during local changes.
- Separate geometry measurements, slicer observations, physical print feedback and engineering inference.

The repository contains a standalone modeling skill. It does not require a separate slicing skill. CAD or mesh editing requires tools supplied by the host environment; slicing and physical verification remain separate steps. No CAD engine, slicer or printer controller is bundled.

## Install

Ask Codex:

```text
$skill-installer Install the skill at the root of
https://github.com/tank-long/print-aware-modeling
using the name print-aware-modeling.
```

Or clone the repository into `~/.agents/skills/print-aware-modeling` if that directory does not already exist. See [OpenAI's skill documentation](https://learn.chatgpt.com/docs/build-skills) for discovery and invocation details. Compatibility with other skill hosts has not been independently verified.

Example request:

```text
Use $print-aware-modeling to design an FDM enclosure from this brief.
Compare print orientations before detailing the model. If removable supports
are needed, parameterize them separately and explain how they can be removed.
Preserve the specified interfaces and report only verification actually performed.
```

## Evidence and limits

The [manual-support walkthrough](references/modeling-with-supports.md) is a hypothetical design exercise, not a print-tested model. P001 and P002 are historical maintainer case summaries; their original model files and verification scripts are not distributed here. P001 includes broad positive print feedback with incomplete process conditions. P002 has recorded geometry checks but no physical print validation.

No universal support gap, wall thickness, fit allowance or overhang angle is promised. The skill does not automatically upload files, publish feedback or run background updates.

Contribute reproducible successes and failures through the [contribution guide](CONTRIBUTING.md). Run `python3 tools/validate.py` for repository checks; these checks do not establish printability.

Original repository content is available under the [MIT License](LICENSE). External references and models retain their own licensing terms.
