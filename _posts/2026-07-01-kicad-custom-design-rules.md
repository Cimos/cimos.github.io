---
layout: post
author: Simon Maddison
title:  "KiCad Design Rules That Match Your Fab House"
date:   2026-07-01
tags: [kicad, kicad-dru, design-rules, drc, jlcpcb, pcbway, pcb, eda]
---

## Table of contents
- [Overview](#overview)
- [Why this exists](#why-this-exists)
- [What's in it](#whats-in-it)
- [How to use it](#how-to-use-it)
- [How the rules are validated](#how-the-rules-are-validated)
- [Caveats](#caveats)

## Overview

A set of custom design rules for KiCad that match the manufacturing capabilities of common PCB fab houses. The rules live in `.kicad_dru` files and each set is validated against a paired test board (`.kicad_pcb`). Source: [Cimos/KiCad-CustomDesignRules](https://github.com/Cimos/KiCad-CustomDesignRules). MIT-licensed.

This is the most-used thing I've put on GitHub, which tells you how much of a gap it fills.

## Why this exists

KiCad's default DRC checks that your board is internally consistent. It does not know that JLCPCB wants a minimum 0.127 mm trace on their cheap process, or that PCBWay's annular ring floor is different again. Every fab publishes a capability table; almost nobody transcribes it into KiCad's custom-rules syntax, so boards get to the fab, fail review, and bounce back.

These are that transcription — done once, checked, and reusable. Drop the right file in, run DRC, and the checker flags anything your chosen fab would reject before you pay for it.

## What's in it

The rules are authored against the KiCad 8 custom-rules syntax and are forward-compatible with **KiCad 9 and 10**. There's a folder per fab:

- `JLCPCB/` — `JLCPCB.kicad_dru` plus its test board
- `PCBWay/` — `PCBWay.kicad_dru` plus its test board

Each fab folder ships the rule file alongside a matching `.kicad_pcb`, `.kicad_sch` and `.kicad_pro`, so the rules never exist without a board to prove them on.

## How to use it

1. Copy the relevant `.kicad_dru` into your project folder.
2. Rename it to match your project name.
3. Open *File → Board Setup → Design Rules → Custom Rules*.
4. Run the checker with **F8** (or *Inspect → Design Rules Checker*).

## How the rules are validated

Every rule has at least one footprint on the paired test board that passes or fails exactly as intended, so a rule that silently stops matching gets caught. On top of that there's a Python linter for CI syntax checking, and the boards run through KiCad 8+ headless command-line DRC — so the whole set is machine-verifiable, not just eyeballed.

## Caveats

Many rules ship with alternates commented out for different layer counts or copper weights. Those aren't automatic — you pick the variant that matches the board you're actually ordering. Read the comments before you trust the green tick.
