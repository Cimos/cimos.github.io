---
layout: post
author: Simon Maddison
title:  "Sand Table Update: Parts on the Bench"
date:   2026-11-22
tags: [sand-table, freecad, 3d-printing, build-log]
pcb3d: /assets/models/dune-weaver.glb
pcb3d_caption: "The whole table out of FreeCAD, glass on. Drag to orbit, scroll to zoom. Go underneath for the mechanism."
---

Quick update on the [kinetic sand table](/kinetic-sand-table). Last time it was all CAD. Now there's plastic, motors and a flashed controller on the bench.

The model up top is the whole table straight out of the FreeCAD model: the IKEA legs (simplified), the sand ring, wood trims, LED strip, glass, and the mechanism hanging under the board. Spin it over to see the arm.

## The table side

First prints went on 19 October. The leg pocket slides onto the real IKEA leg with 0.3 mm a side and no wobble, once you pull IKEA's screw foot off. My tape measurements matched IKEA's 3D model to within 3 mm, which was a nice surprise.

A few things needed a tweak:

- **Side trims** rattled at 0.2 mm dovetail clearance. Down to 0.1 and they're snug.
- **Cover and outer ring** puzzle joints were loose. The knobs grew 0.1 mm a side and the sockets stayed put, so parts already printed still work.
- **Sand ring** went from screwed joint plates to built-in tabs. Two part types, 4 leg pieces and 8 LED segments, one M3 screw per joint. 12 screws instead of 24 and no plates to print.
- **Wood grain** on the trims now repeats once per trim, so it lines up across every seam.

The ring is printing in PLA for now. It was drawn for PETG because the LED strip sits inside it, so the LEDs stay turned down until I know it won't soften.

## The mechanism

Hardware turned up on 30 October. Straight away two things didn't match the model: the idlers (18 mm flange, 8.5 mm wide) and the heat-set inserts. Measured them, put the real numbers in, rebuilt.

Then the bench build, and the stuff you only find by holding it:

- The **home magnet lug** snapped off the first printed wheel. It only hung on the rim by 2.1 mm. The rough build carries on and it gets fixed before the final wheel.
- The **belt clamp** was too tight and fragile. Opened the slot up from 0.1 to 0.35 mm and thickened the walls.
- The **far idler** bound up. The tension screw hit the axle 11 mm below the belt, so the axle tilted. It's now on a printed yoke that slides in guides, pulled by one M3 screw at belt height.

The controller is an MKS DLC32 running [Dune Weaver firmware](https://github.com/tuanchris/dune-weaver-firmware) v0.2.2. First moves sorted out the rho coupling. Set one way, the carriage drifted outward as the disc turned. Flipped, it held still for a full turn.

## Next

Reprint the far end and the wheel, finish the mechanism, then power it up on the bare frame with a ball and a magnet and see if it actually draws something.

-SM
