---
layout: post
author: Simon Maddison
title:  "kibot-config: One Push, a Full Fabrication Datapack"
date:   2026-07-01
tags: [kicad, kibot, github-actions, gerbers, bom, blender, panelization, ci-cd]
---

## Table of contents
- [Overview](#overview)
- [What it generates](#what-it-generates)
- [Repo layout it expects](#repo-layout-it-expects)
- [Using it](#using-it)
- [License](#license)

## Overview

**kibot-config** is a GitHub Action and a library of KiBot configs that turn a KiCad project into a complete datapack — drawings, gerbers, BOM, pick-and-place, 3D STEP, Blender renders, panels, and visual diffs — on every push. Source: [Cimos/kibot-config](https://github.com/Cimos/kibot-config).

This is the pipeline behind [Mad_RP2040]({{ '/madrp2040-anything-keypad' | relative_url }}); I pulled the configs out into their own repo so any board could reuse them.

## What it generates

Each config is a self-contained job:

- **`build-pcb-kibot.yaml`** — schematics, PCB PDFs, gerbers, BOMs, pick-and-place, KiCost data, and stencils
- **`build-3d_model-kibot.yaml`** — 3D STEP exports (simple and full)
- **`build-2d_images-kibot.yaml`** — four Blender renders (top/bottom × angled/straight)
- **`build-video-kibot.yaml`** — a rotating-board Blender frame sequence
- **`build-diff-kibot.yaml`** — KiRi + git-based PCB/SCH visual diffs
- **`build-panel-kibot.yaml`** — drawings for panelized boards

## Repo layout it expects

The action auto-detects a single top-level `*.kicad_pro`, then reads:

- `options.yaml` — required, for preflight overrides, filters, and variants
- `panelization.yaml` — optional, only if you're panelizing

## Using it

Add a workflow that checks out both your project and this config repo, then invokes the action with the config you want:

```yaml
# .github/workflows/build-pcb.yaml
- uses: Cimos/kibot-config@main
  with:
    config: build-pcb-kibot.yaml
```

Swap `config` for any of the jobs above to run just that stage.

## License

BSD-3-Clause — deliberately permissive, so anyone can lift the configs into their own boards without thinking about it.
