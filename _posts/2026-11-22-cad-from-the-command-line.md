---
layout: post
author: Simon Maddison
title:  "CAD from the Command Line: CadQuery and FreeCAD on WSL2"
date:   2026-11-22
tags: [cadquery, freecad, wsl, cad, 3d-printing, workflow]
---

The [MadRP2040 case](/madrp2040-case) and the [sand table](/kinetic-sand-table) are both built from Python, not drawn with a mouse. This is the setup they run on: CadQuery and FreeCAD on WSL2, set up so I can rebuild it on another machine and get exactly the same thing.

## What's in it

| Part | Version | Why |
|---|---|---|
| CadQuery | 2.8.0 | Latest on conda-forge |
| OCP / OpenCascade | 7.9.3 | The version CadQuery 2.8 pins |
| Python | 3.12 | Every compiled dependency has builds for it |
| FreeCAD | 1.1.4 | For opening, checking and the bigger assemblies |
| OCP CAD Viewer | 4.1.0 | 3D preview inside VS Code |

Everything lives in one micromamba environment with exact lockfiles. FreeCAD sits outside it because it brings its own Python and OpenCascade. It's the official AppImage, unpacked, since running it directly needs `libfuse2` and that needs sudo.

## How a model works

A model is a Python file plus a JSON parameter file. Change a number, rebuild.

```bash
make build validate test
make preview
```

Every build writes a STEP, an STL and a JSON report: parameters, versions, volume, bounding box, and which checks passed. If anything fails, the old STEP and STL get deleted first, so a stale file can never pass for a current one.

Checks are tight where they can be. Hole centres and bounding boxes to 0.001 mm, volume to a millionth after a STEP round trip. There's also my own STL watertight check: every triangle edge has to be shared by exactly two triangles. That proves the mesh is closed, not that it'll print well.

For printed parts there's `make print-check` for overhangs, bed fit and mass, `make print-pack` for a folder with pictures and print notes, and a calibration coupon for dialling in fits on a new printer or filament.

## The one that bit me

The VS Code viewer has a quick-start button that runs `pip install` into whatever Python you've selected. I pressed it. It pulled in build123d from git, which dragged a different OpenCascade in over the top and broke CadQuery.

Because everything is locked, the fix was to move the broken environment aside and rebuild from the lockfiles. Now `make doctor` fails if OpenCascade ever comes from pip, and warns about any pip package that shouldn't be there.

Same story with old Python packages in my home folder (MAVProxy and friends) leaking into the environment. The Makefile turns that off now.

## Why bother

It's what makes the AI side of things work, which I wrote about in [Designing Hardware with AI When You Don't Have the Time](/designing-with-ai). A script builds the model and the checks say whether it's right, so a change from me or from an AI gets judged the same way. A short rules file in the repo tells coding assistants how to behave in it: run everything through `make`, never pip-install into the environment, keep dimensions in the parameter files, and reject an impossible number instead of quietly fixing it.

-SM
