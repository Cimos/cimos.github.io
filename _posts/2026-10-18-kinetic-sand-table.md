---
layout: post
author: Simon Maddison
title:  "Building a Kinetic Sand Table"
date:   2026-10-18
tags: [sand-table, freecad, cad, 3d-printing, build-log]
image: /assets/images/og/kinetic-sand-table.png
---

## Table of contents
- [Overview](#overview)
- [How it moves](#how-it-moves)
- [The table](#the-table)
- [Doing it in CAD first](#doing-it-in-cad-first)
- [What's still open](#whats-still-open)
- [Updates](#updates)

## Overview

A sand table is a coffee table with a layer of sand under glass. A steel ball
rolls through the sand and draws patterns. Under the sand, a magnet on a small
robot arm drags the ball around.

I want to build one. The design I'm basing it on is the
[Dune Weaver](https://github.com/tuanchris/dune-weaver) Pro, an open source
sand table. The problem is the Pro's CAD isn't public. There are STLs, a build
video, a BOM and a lot of photos from the Discord, but no editable model.

So this project is rebuilding the Pro's mechanism in FreeCAD from that
evidence, and fitting it into a cheap IKEA table. This post is the starting
point. I'll add updates at the bottom as the build moves along.

Most of the design work was done with AI agents. I wrote about how that went in
[Designing Hardware with AI When You Don't Have the Time](/designing-with-ai).

## How it moves

The mechanism is polar, not X/Y. Two stepper motors:

- **Theta** turns a big 200 tooth GT2 wheel through a 20 tooth pulley (10:1).
  The wheel sits on a large bearing and carries the arm around.
- **Rho** moves a carriage in and out along an MGN9 rail. The rail *is* the arm.

The catch is that the rho belt runs around pulleys that spin with the arm. So
when the arm turns, the carriage moves too, unless the rho motor turns with it.
To hold a fixed radius, the rho motor has to turn 1:1 with the disc. One disc
turn with the rho motor stopped moves the carriage 40 mm.

I wrote a small kinematic model for this. It takes a pattern file, works out
the motor turns, and animates it:

![Top view animation of the arm and belts following a pattern](/images/kinetic-sand-table/motion.gif)

Red is the rho belt, black is the theta belt, blue is where the ball goes.

## The table

The base is an IKEA VITTSJÖ round coffee table, 75 cm. It's cheap, it's
round, and lots of Dune Weaver builds already use it. The trick most people
use is to flip the whole metal frame upside down. The shelf becomes the board
the sand sits on, and the glass top goes on a printed ring above it.

![The enclosure on the flipped IKEA VITTSJÖ frame](/images/kinetic-sand-table/table-mount.png)

The printed parts are a ring of tank segments to hold the sand, an LED strip
channel, a cover ring for the glass, foot caps (one has the DC jack), and a
vented box under the frame for the electronics.

## Doing it in CAD first

Everything is built from a Python script into FreeCAD, driven by a parameter
file. Nothing is drawn by hand. That means I can change one number, like the
magnet size, and rebuild the whole table.

![First mechanical assembly draft](/images/kinetic-sand-table/assembly.png)

Every rebuild also runs checks. Right now it's a few hundred build checks,
around 700 validation checks and 150-odd tests. The useful ones are:

- **Clearances.** Every moving part is swept through its full travel and
  checked against everything fixed. Minimum running gap is 1 mm.
- **Belts.** The belt paths are worked out properly, with the wrap around each
  pulley, so a belt rubbing on a part gets caught.
- **Motion replay.** A real pattern is run through the clearance checks, not
  just a grid of poses.

Every number is also labelled with where it came from: a datasheet, a photo, a
measurement, or just my own choice. That way I don't fool myself into thinking
a guess is a real Pro dimension.

From the model I can now print out a BOM, a print sheet (about 45 parts, roughly
725 g of PETG) and drawings.

![Printed parts overview](/images/kinetic-sand-table/printed-parts.png)

## What's still open

None of this has been built yet, so a lot is unproven:

- The bare rail droops about 1.2 mm at the tip when the magnet pulls on it.
  The Pro does the same, so I'll measure it on the real arm.
- The IKEA numbers come from IKEA's 3D model and a tape measure. They need a
  real table to confirm.
- The Pro's firmware config has the wrong steps per mm for this drive (533 vs
  640). I've fixed it in my config, but motor direction still needs checking.
- Magnets are bought (N52, 19 x 4 mm). They still need a bench test through
  the board.

Next is ordering parts, test printing the mechanism, and seeing what breaks.

## Updates

### 2026-10-18 - Starting point
CAD model, checks, BOM, print sheet and wiring plan are all drafted. Magnets
bought. Nothing printed yet.

-SM
