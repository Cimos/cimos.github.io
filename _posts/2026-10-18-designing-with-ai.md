---
layout: post
author: Simon Maddison
title:  "Designing Hardware with AI When You Don't Have the Time"
date:   2026-10-18
tags: [ai, cad, freecad, workflow, sand-table]
image: /assets/images/og/designing-with-ai.png
---

## Table of contents
- [Overview](#overview)
- [The problem is time](#the-problem-is-time)
- [What the AI actually did](#what-the-ai-actually-did)
- [What I still do](#what-i-still-do)
- [Rules that make it work](#rules-that-make-it-work)
- [Where it goes wrong](#where-it-goes-wrong)
- [Why it matters](#why-it-matters)

## Overview

I have a long list of projects I want to do and not much time to do them. Work,
life, the usual. Most ideas never get past a note on my phone.

The [kinetic sand table](/kinetic-sand-table) is the first hardware project
where I leaned on AI agents for most of the design work. It went from nothing to
a full parametric CAD model, BOM, print sheet, wiring plan and firmware config
in about two days. That would have taken me months of evenings on my own,
if it happened at all.

This post is about how that worked, and what it means for people like me who
are short on time.

## The problem is time

The hard part of a hobby project isn't usually the skill. It's the hours.

A sand table sounds simple. In practice it's a lot of small jobs: read through
build videos and Discord photos, work out belt lengths, check every part clears
every other part through a full turn, find a magnet, find a rail, figure out how
to fit it in a table, write a BOM. Each one is an evening. Most of them are
boring. That's where projects die.

## What the AI actually did

I used coding agents (Claude and Codex) with FreeCAD driven from Python. No
clicking around in the GUI. The agent writes the script, the script builds the
model, and checks run on every build.

In about two days and 30 commits it:

- Went through the photos, build video and Discord images and wrote up what each
  one showed.
- Built the mechanism, the table mount and the enclosure as a parametric model.
- Wrote clearance checks that sweep every moving part through its travel, plus
  belt path checks.
- Wrote a kinematic model that animates a real pattern.
- Generated the BOM, a shopping list, a print sheet and drawings.
- Wrote a FluidNC config and a wiring plan, and caught that the original config
  had the wrong steps per mm for this drive.

It also kept working while I was busy. I could give it a job, go do something
else, and come back to a result with checks run.

## What I still do

I didn't hand the project over. My job changed.

- **Decisions.** Should the rail be the arm, or use a tube? Which magnet? Flip
  the IKEA frame or not? The agent laid out the options; I picked.
- **Real world.** Buying magnets, measuring the actual table with a tape,
  sending it photos from Discord.
- **Saying no.** When something looked wrong, or didn't match the photos, I
  pushed back.

It's less like having a tool and more like having a fast junior engineer who
never gets bored.

## Rules that make it work

Left alone, AI will happily make up a plausible number and move on. In hardware
that's how you end up with a part that doesn't fit. So the project has a short
rules file the agent reads first. The main ones:

- **Label every number.** Each dimension says where it came from: a datasheet,
  a photo, a measurement, a calculation, or a guess. A guess is never shown as a
  real dimension.
- **Unknown stays unknown.** If a value isn't known, it's left empty. No filling
  in something that looks about right.
- **Checks, not claims.** Every change has to pass the build, validate and test
  run. Failures get reported word for word.
- **No exports until it's ready.** Production STLs stay switched off until the
  open questions are closed.

These rules are what turn it from a toy into something I trust.

## Where it goes wrong

It's not magic. Some things I ran into:

- **It can't see.** It can render images and check numbers, but it doesn't look
  at a model the way you do. Some problems were only caught when I compared it
  to photos.
- **It's confidently wrong sometimes.** The first arm design used a tube and
  counterweight. Discord videos showed the real one doesn't. That was a full
  rework.
- **Usage limits.** One agent hit its limit halfway through a job, and another
  had to pick it up. Having everything written down in the repo made that easy.
- **Still unbuilt.** None of it has been printed yet. The real test is whether
  it works on the bench.

## Why it matters

For me the big change is which projects are possible at all. Things I'd have
written off as "not enough time" are now a few evenings of decisions instead of
months of grind.

You still need to know enough to tell when it's wrong. But if you do, AI turns
the boring 80% into something that happens in the background, and leaves you
with the fun part: making the calls and building the thing.

-SM
