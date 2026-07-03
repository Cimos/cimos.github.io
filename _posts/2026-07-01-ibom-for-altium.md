---
layout: post
author: Simon Maddison
title:  "An Interactive HTML BOM for Altium Designer"
date:   2026-07-01
tags: [altium, bom, interactive-html-bom, pcb, assembly, pascal]
image: /assets/images/og/ibom-for-altium.png
---

## Table of contents
- [Overview](#overview)
- [Why hand-assembly needs this](#why-hand-assembly-needs-this)
- [Standing on the OpenScopeProject's shoulders](#standing-on-the-openscopeprojects-shoulders)
- [Getting it out of Altium](#getting-it-out-of-altium)

## Overview

[Cimos/interactivehtmlbom4altium2](https://github.com/Cimos/interactivehtmlbom4altium2) generates an interactive HTML BOM from an Altium Designer project — a single self-contained page where you can search a part and have its footprint light up on the board, and click a footprint to jump to its BOM row. MIT-licensed.

## Why hand-assembly needs this

If you've ever hand-populated a dense board, you know the loop: find the next line on the BOM, find that reference designator on the board, place the part, repeat two hundred times. On paper that means squinting between a printout and the PCB, losing your place, and occasionally soldering a 4.7k where the 47k goes.

An interactive BOM collapses that. Search or step through the list, the matching footprint highlights on a rendered board, and you never lose which parts are already down. For the KiCad crowd this has been a solved problem for years. Altium users have mostly been left doing it the paper way.

## Standing on the OpenScopeProject's shoulders

I didn't invent the good part here. The [InteractiveHtmlBom](https://github.com/openscopeproject/InteractiveHtmlBom) project by the OpenScopeProject is the tool everyone means when they say "iBOM," and its output format is the thing worth being compatible with. What was missing was the front half for Altium — the bit that reads the design and produces data in that shape.

So this is that half. It pulls PCB and schematic data through Altium's Pascal scripting API, renders silkscreen, pads, text and drawings, and writes out HTML, a JS bundle, and JSON that matches the InteractiveHtmlBom schema — so it slots straight into the ecosystem that already exists. Optional tracks, zones and a netlist get you live net highlighting on top.

It's quick enough to live in your workflow: roughly five seconds for a 200-component board, around fifty for a genuinely dense 2000-part one.

## Getting it out of Altium

Two ways in, depending on how you work. Run it as a script from the PCB layout and a configuration GUI comes up — good for one-offs. Or add the `.pas` to an OutJob as a Report Output, and the interactive BOM gets generated as part of your normal output run, right next to the gerbers and the assembly drawings, every time.

-SM
