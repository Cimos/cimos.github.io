---
layout: post
author: Simon Maddison
title:  "KiCad Design Rules That Match Your Fab House"
date:   2026-07-01
tags: [kicad, kicad-dru, design-rules, drc, jlcpcb, pcbway, pcb, eda]
---

## Table of contents
- [Overview](#overview)
- [The check KiCad doesn't do](#the-check-kicad-doesnt-do)
- [Rules that can't quietly rot](#rules-that-cant-quietly-rot)
- [Using it](#using-it)
- [The one gotcha](#the-one-gotcha)

## Overview

KiCad's DRC will happily tell you your board is perfect. Your fab house may disagree. [Cimos/KiCad-CustomDesignRules](https://github.com/Cimos/KiCad-CustomDesignRules) is a set of `.kicad_dru` files that teach KiCad what a given manufacturer will actually accept — right now, JLCPCB and PCBWay. MIT-licensed, and by some distance the most-used thing I've put on GitHub, which tells you how common the problem is.

## The check KiCad doesn't do

Default DRC checks that your board is internally consistent: nets don't short, clearances match the netclasses *you* set, courtyards don't overlap. What it has no opinion on is whether the 0.1 mm trace you just routed is below your fab's floor on their cheap process, or whether your annular ring survives their drill tolerance.

Every fab publishes a capability table. Almost nobody transcribes it into KiCad's custom-rules syntax, because the syntax is fiddly and the table is long. So the board passes DRC, gets to the fab, fails their review, and bounces back with a note about minimum annular ring — usually after you've already paid and started waiting.

These files are that transcription, done once and checked, so the failure happens on your screen instead of in their inbox.

## Rules that can't quietly rot

The failure mode for a project like this is subtle: KiCad changes a token, a rule silently stops matching anything, and the file still "passes" because it's now checking nothing. Green tick, zero coverage.

So every fab folder ships its `.kicad_dru` next to a paired test board — a real `.kicad_pcb` with footprints placed to trip each rule on purpose. If a rule stops biting, the test board stops failing where it should, and that's caught. On top of that there's a Python linter for syntax and a headless KiCad 8+ command-line DRC pass, so the whole set is machine-verified rather than eyeballed. Authored against KiCad 8 syntax, forward-compatible with 9 and 10.

## Using it

Copy the relevant file into your project, rename it to match, then *Board Setup → Design Rules → Custom Rules*, and run the checker with **F8**. That's the whole workflow.

## The one gotcha

A lot of rules ship with alternates commented out — different values for different layer counts or copper weights. Those aren't automatic. Pick the variant that matches the board you're actually ordering, and read the comments before you trust the result. A green tick against the wrong copper weight is just a different way to be wrong.

Found a capability the rules get wrong, or want a fab I haven't added? [Open an issue](https://github.com/Cimos/KiCad-CustomDesignRules/issues) — a fab's spec sheet plus a failing example is exactly what makes these better.

-SM
