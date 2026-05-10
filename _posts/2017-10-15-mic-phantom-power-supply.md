---
layout: post
author: Simon Maddison
title:  "Mic Phantom Power Supply"
date:   2017-10-15
tags: [audio, phantom-power, analog, veroboard, power-supply]
---

## Overview

Little box I put together in my final year of uni. Our group design project needed a condenser mic and we’d already gone and bought one — then realised none of us had a way to actually power the thing. Commercial phantom boxes weren’t happening on a student budget, so I threw one together on Veroboard over a weekend and stuffed it in an ABS jiffy box.

## The Circuit

Two stages, nothing clever.

Front end is a 25–30VAC transformer into a full-wave bridge (1N4004s), 1000µF bulk caps, then a discrete BJT regulator — BD139 pass, BC546 error amp, 24V zener reference. Gives a clean rail for the next stage.

Phantom side is a soft-start regulator. BC639 pass transistor with its base pulled up through a string of 1N914s and a 47V zener. The 100µF on the base ramps the output gently up to +48V instead of slamming it on the moment you flip the switch — last thing you want is to cook a brand new mic. 6k8 1% resistors on the XLR pins for the standard phantom feed.

<div style="display: flex; gap: 1.5rem; justify-content: center; flex-wrap: wrap; margin: 2rem 0;">
  <div style="flex: 1 1 100%; text-align: center;">
    <img src="../images/phantom-power/48v-power-supply.gif"
         alt="48V power supply schematic"
         style="max-width: 90%; height: auto; border-radius: 12px; box-shadow: 0 6px 20px rgba(0,0,0,0.15);">
  </div>
  <div style="flex: 1 1 100%; text-align: center;">
    <img src="../images/phantom-power/phantom-soft-start.jpg"
         alt="Soft-start phantom power regulator schematic"
         style="max-width: 90%; height: auto; border-radius: 12px; box-shadow: 0 6px 20px rgba(0,0,0,0.15);">
  </div>
</div>

## Final Thoughts

Did the job. Powered the mic the whole way through the project and never made a peep on the audio.

-SM
