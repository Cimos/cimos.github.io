---
layout: post
author: Simon Maddison
title:  "kibot-config: One Push, a Full Fabrication Datapack"
date:   2026-07-01
tags: [kicad, kibot, github-actions, gerbers, bom, blender, panelization, ci-cd]
image: /assets/images/og/kibot-config.png
---

## Table of contents
- [Overview](#overview)
- [A board isn't done when the layout is](#a-board-isnt-done-when-the-layout-is)
- [The jobs](#the-jobs)
- [What it expects from your repo](#what-it-expects-from-your-repo)
- [Why it's its own repo](#why-its-its-own-repo)

## Overview

[Cimos/kibot-config](https://github.com/Cimos/kibot-config) is a GitHub Action and a small library of KiBot configs that turn a KiCad project into a complete fabrication datapack — drawings, gerbers, BOM, pick-and-place, 3D STEP, Blender renders, panels, visual diffs — on every push.

## A board isn't done when the layout is

Finishing the layout feels like the end. It isn't. Then you export gerbers, generate the drill files, produce a BOM in whatever format the assembler wants this week, a pick-and-place with the right origin, a STEP for the mechanical team, a render for the pull request, and a panel drawing for the fab. Do that by hand, from menus, every time you change a resistor, and you'll eventually ship the *old* gerbers by accident.

The fix is the same one CI applies to software: never generate release artefacts by hand. Let a machine rebuild the whole datapack from source on every push, deterministically, so what you hand to the fab always matches the commit.

## The jobs

Each config is a self-contained stage you can run on its own:

- **`build-pcb`** — schematics, PCB PDFs, gerbers, BOMs, pick-and-place, KiCost data, stencils
- **`build-3d_model`** — STEP exports, simple and full
- **`build-2d_images`** — four Blender renders (top/bottom × angled/straight)
- **`build-video`** — a rotating-board frame sequence
- **`build-diff`** — KiRi and git-based visual diffs of the PCB and schematic
- **`build-panel`** — drawings for panelized boards

## What it expects from your repo

Almost nothing, on purpose. It auto-detects a single top-level `*.kicad_pro`, reads an `options.yaml` for preflight overrides, filters and variants, and an optional `panelization.yaml` if you're panelizing. Add a workflow that checks out your project and this repo, then names the config you want:

```yaml
- uses: Cimos/kibot-config@main
  with:
    config: build-pcb-kibot.yaml
```

## Why it's its own repo

This started life inside [Mad_RP2040]({{ '/madrp2040-anything-keypad' | relative_url }}) as that board's pipeline. It was obviously not board-specific — nothing in "export the gerbers" cares which board it is — so I pulled it out so any project could reuse it without copy-pasting a `.github` folder around. It's BSD-3-Clause for the same reason: I'd rather people lift these into their own boards without having to think about the licence.

-SM
