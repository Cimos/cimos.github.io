---
layout: post
author: Simon Maddison
title:  "kicad-druid: Fab House Design Rules, Generated and Tested"
date:   2026-10-03
tags: [kicad, kicad-dru, design-rules, drc, jlcpcb, pcbway, ci-cd, pcb]
image: /assets/images/og/kicad-druid-design-rules.png
---

## Table of contents
- [Overview](#overview)
- [What changed from the old rules](#what-changed-from-the-old-rules)
- [One source of truth per fab](#one-source-of-truth-per-fab)
- [Generic: design before you pick a fab](#generic-design-before-you-pick-a-fab)
- [The green DRC that checked nothing](#the-green-drc-that-checked-nothing)
- [Using it](#using-it)

## Overview

[**kicad-druid**](https://github.com/Cimos/kicad-druid) is a set of KiCad custom
design rules (`.kicad_dru`) that match what JLCPCB and PCBWay can actually make.
Drop the file for your order into your project and KiCad's DRC flags anything the
fab would bounce, on your screen instead of in their review queue.

It replaces my earlier [KiCad Custom Design Rules](/kicad-custom-design-rules)
repo, which is now in the archive. Same idea, rebuilt properly: the rules are
generated rather than hand-edited, every variant is checked by KiCad in CI, and
there is a new set of rules that works for either fab. MIT-licensed, works on
KiCad 8, 9 and 10.

## What changed from the old rules

| | Old repo | kicad-druid |
|---|---|---|
| Rule files | hand-edited | generated |
| Variants | comment blocks | one file per build |
| Fabs | JLCPCB, PCBWay | + Generic (both) |
| CI | lint | lint + full DRC |
| Silent failures | possible | sentinel rule |

## One source of truth per fab

Each fab's published capabilities live in one TOML file
(`capabilities/JLCPCB.toml`, `capabilities/PCBWay.toml`). A small Python script
generates every `.kicad_dru` from it, plus a side-by-side comparison table of the
two fabs. CI regenerates the files and fails if anyone hand-edits the output, so
the rules can't drift away from the capability table they came from.

That also killed the old "uncomment the right block for your layer count" step,
which was the easiest way to get these files wrong. You now pick the whole file
that matches what you're ordering:

| File | Layers | Copper |
|------|--------|--------|
| `<FAB>.kicad_dru` | 4 (default) | 1 oz |
| `<FAB>-2L-1oz.kicad_dru` | 1–2 | 1 oz |
| `<FAB>-4L-2oz.kicad_dru` | 4 | 2 oz |
| `<FAB>-6L-1oz.kicad_dru` | 6 | 1 oz |

PCBWay files also ship impedance net classes (50 Ω single-ended, 60–120 Ω
differential) as starting points for the fab's default stackup.

## Generic: design before you pick a fab

Plenty of boards get designed before anyone has decided where they'll be built.
The `Generic/` rules take the stricter of the two fabs for every limit: the larger
minimum, the smaller maximum, and any rule either fab needs. A board that passes
Generic passes at both. Once the fab is settled, switch to that fab's file and the
limits relax. Generic is derived in code from the two fab files, so it follows any
capability update automatically.

## The green DRC that checked nothing

This is the part I'm happiest with. If KiCad can't compile a rules file (one
typo, one unknown layer name), it drops the rules, and `kicad-cli pcb drc`
reports a clean run with exit code 0. No warning, empty stderr. Your CI goes
green while not a single custom rule ran.

kicad-druid's CI guards against that. It runs KiCad's DRC on a paired test board
for every one of the twelve rule files, and before each run it appends a
*sentinel* rule that must always fire. If the sentinel isn't in the report, the
file didn't compile, and the job fails. It goes at the end of the file because
some errors drop only the rule they're in and everything after it, while others
drop the whole file. Either way, the sentinel goes missing.

The linter also catches the quieter mistakes: lowercase item types like
`'track'` that KiCad silently never matches, and layer display names like
`F.Silkscreen` that stop resolving the moment a board is imported from Altium or
renamed.

## Using it

1. Copy the `.kicad_dru` matching your order from `JLCPCB/`, `PCBWay/` or `Generic/` into your project folder.
2. Rename it to match the project: `your-project.kicad_dru`.
3. Run DRC (F8). Check `Board Setup > Design Rules > Custom Rules` once for errors, since KiCad won't tell you otherwise.

Releases and the full rule comparison are on
[GitHub](https://github.com/Cimos/kicad-druid). It started as a fork of
[labtroll/KiCad-DesignRules](https://github.com/labtroll/KiCad-DesignRules) by
Morten Hattesen, with that history kept.

-SM
