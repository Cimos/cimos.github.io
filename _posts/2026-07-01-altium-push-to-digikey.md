---
layout: post
author: Simon Maddison
title:  "Altium → DigiKey: BOM to Cart in One Command"
date:   2026-07-01
tags: [altium, digikey, bom, python, procurement, automation]
image: /assets/images/og/altium-push-to-digikey.png
---

## Table of contents
- [Overview](#overview)
- [The dumb tedious step](#the-dumb-tedious-step)
- [The trick: no auth at all](#the-trick-no-auth-at-all)
- [Running it](#running-it)
- [Know what you're trading](#know-what-youre-trading)

## Overview

[Cimos/Altium-Push-to-DigiKey](https://github.com/Cimos/Altium-Push-to-DigiKey) takes an Altium BOM and turns it into a DigiKey shopping list you can open and buy. One command. MIT-licensed.

## The dumb tedious step

Between "the design is done" and "the parts are on order" sits a chore nobody enjoys: copying manufacturer part numbers out of a BOM and pasting them into a distributor cart, line by line, minding quantities and skipping the DNPs. It's ten boring minutes that's easy to get subtly wrong, and you do it every spin.

This automates exactly that step and nothing more. It reads the BOM Altium already emits — either the raw CSV from a BOM Output Job or the normalised JSON from a review-pack pipeline — parses it tolerantly for part number, quantity and designator, skips `DNP` rows and anything with an empty MPN or zero quantity, and hands you back a link.

## The trick: no auth at all

The neat part is there's nothing to set up. No API key, no OAuth dance. It POSTs to DigiKey's anonymous `mylists/api/thirdparty` endpoint — the same one Digi-Key's own official KiCad plugin uses — and gets back a short URL like `digikey.com/short/<code>`. You open that in a browser and the list drops into whatever account you're logged into. Anonymous on the way out, account-tied the moment you click. An authenticated direct-to-account mode over OAuth2 is on the list, but for the common case the no-auth path is the whole appeal.

## Running it

Python 3.8+, installed straight from the repo:

```bash
pip install git+https://github.com/Cimos/Altium-Push-to-DigiKey.git
```

Then point it at a BOM. `--dry-run` parses and reports without sending; `--open` launches the browser for you; `--tags` labels the list.

## Know what you're trading

Convenience like this always costs something, so here's the bill, stated plainly:

- The short URL is **link-shareable until you claim it** — anyone with the link can grab the list, so treat it like a secret.
- The endpoint isn't formally documented as a public API, and there's no per-user authentication on the POST. It works because the official plugin uses it, not because DigiKey promised it would.
- There's no compliance filtering. NDAA and any regulatory concerns are yours to handle upstream, before the parts ever reach this script.

None of that is a dealbreaker for ordering your own prototypes. It's worth knowing before you wire it into anything that matters.

-SM
