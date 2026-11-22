---
layout: post
author: Simon Maddison
title:  "Sand Table Update: Parts on the Bench"
date:   2026-11-22
tags: [sand-table, freecad, 3d-printing, build-log]
pcb3d: /assets/models/dune-weaver.glb
pcb3d_caption: "The whole table out of FreeCAD, glass on. Drag to orbit, scroll to zoom."
pcb3d_hide: "board,sand,glass,ball"
---

Quick update on the [kinetic sand table](/kinetic-sand-table). Last time it was all CAD. Now there's plastic, motors and a flashed controller on the bench, and a fair bit of the mechanism has changed because of it.

The model up top is the whole table as it stands today, straight out of the FreeCAD model: the IKEA legs and steel top ring, the sand ring, wood trims, LED strip, glass, and the mechanism hanging under the board. Hit **show mechanism** to lift the board off and see the arm.

## The table side

First prints went on 19 October. The leg pocket slides onto the real IKEA leg with 0.3 mm a side and no wobble, once you pull IKEA's screw foot off. My tape measurements matched IKEA's 3D model to within 3 mm, which was a nice surprise.

A few things changed after that:

- **Top ring.** The printed outer ring is gone. IKEA's own steel top ring goes back on, sitting on the deck and held by an M5 screw through each leg piece. The leg pieces were reprinted with a pocket for it and fitted on 16 November.
- **Sand ring** went from screwed joint plates to built-in tabs. Two part types, 4 leg pieces and 8 LED segments, one M3 screw per joint. 12 screws instead of 24 and no plates to print.
- **Side trims** rattled at 0.2 mm dovetail clearance. Down to 0.1 and they're snug. The wood grain now repeats once per trim, so it lines up across every seam.

The ring is printing in PLA for now. It was drawn for PETG because the LED strip sits inside it, so the LEDs stay turned down until I know it won't soften.

## The mechanism

Hardware turned up on 30 October. The idlers (18 mm flange, 8.5 mm wide) and the heat-set inserts didn't match the model, so I measured them, put the real numbers in and rebuilt.

Then the bench build, and the stuff you only find by holding it:

- **Wheel lug.** The home magnet lug snapped off the first printed wheel. It only hung on the rim by 2.1 mm. It's now part of a new lip under the teeth, which also stops the belt dropping off. Root stress for the same knock went from 43.7 to 1.2 MPa.
- **Hall sensors.** The boards have mounting holes, so the zip ties are gone. Two M2.5 screws each into inserts in the motor frame.
- **Belt tensioner.** The far end block swung 8.3 mm into the printed leg pieces whenever the arm pointed at a leg. The checks only looked every 30°, so they stepped right over it. Now there's a full-turn sweep, the far end is a fixed idler, and the tensioner lives at the near end on the rail.
- **Magnet arm.** The rail moved out and the magnet now sits 120 mm ahead of the carriage on a straight, springy arm that rides on the board, the way the Pro does it.
- **Belt clamp.** Took a few goes. Too tight, then a wedge, then zip ties. It ended up as one solid printed holder with a toothed slot and no ties.

To stop things wandering, every part's geometry got locked on 16 November, so any change shows up before it gets printed. There's also a motion check now that turns the arm a full circle and runs the carriage end to end, checking every moving part against everything else.

The controller is an MKS DLC32 running [Dune Weaver firmware](https://github.com/tuanchris/dune-weaver-firmware) v0.2.2. First moves sorted out the rho coupling. Set one way, the carriage drifted outward as the disc turned. Flipped, it held still for a full turn.

## Next

Print the last of the locked mechanism parts, check the homing on the bench, then power it up on the bare frame with a ball and a magnet and see if it actually draws something.

-SM
