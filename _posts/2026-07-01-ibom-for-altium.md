---
layout: post
author: Simon Maddison
title:  "An Interactive HTML BOM for Altium Designer"
date:   2026-07-01
tags: [altium, bom, interactive-html-bom, pcb, assembly, pascal]
---

## Table of contents
- [Overview](#overview)
- [What it does](#what-it-does)
- [Two ways to run it](#two-ways-to-run-it)
- [Output formats](#output-formats)
- [Credit and license](#credit-and-license)

## Overview

An interactive HTML BOM generator for Altium Designer — a self-contained page that lets you search components and visually correlate them with their placements on the board. Source: [Cimos/interactivehtmlbom4altium2](https://github.com/Cimos/interactivehtmlbom4altium2). MIT-licensed.

If you've hand-assembled a dense board, you know why this matters: a clickable BOM that highlights the footprint beats squinting at a paper printout.

## What it does

It reads PCB and schematic data through Altium Designer's Pascal script API and renders silkscreen, footprint pads, text, and drawings. Click a footprint on the board and it highlights the matching BOM row (and back the other way). Optional extras include tracks/zones and a netlist for dynamic net highlighting.

Performance scales with density — roughly 5 seconds for 200 components, and around 50 seconds for 2000 densely-placed parts on a reasonably fast PC.

## Two ways to run it

**As a script:** clone the repo, wire it into Altium per their scripting docs, and run it from the PCB layout — a GUI comes up for configuration.

**As an OutJob output:** add `InteractiveHTMLBOM4Altium2.pas` to your project, create a new Report Output in the OutJob, point it at the script, and generate it as part of your normal output run.

## Output formats

- **HTML** — a self-contained, dependency-free page
- **JS** — a custom JavaScript file
- **JSON** — matches the InteractiveHtmlBom schema, so it drops into that platform

## Credit and license

This extends the excellent [InteractiveHtmlBom](https://github.com/openscopeproject/InteractiveHtmlBom) by the OpenScopeProject, adapting the data-extraction side for Altium Designer. Written in Pascal and JavaScript, MIT-licensed.
