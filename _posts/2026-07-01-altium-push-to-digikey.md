---
layout: post
author: Simon Maddison
title:  "Altium → DigiKey: BOM to Cart in One Command"
date:   2026-07-01
tags: [altium, digikey, bom, python, procurement, automation]
---

## Table of contents
- [Overview](#overview)
- [How it works](#how-it-works)
- [No auth, and the caveat that comes with it](#no-auth-and-the-caveat-that-comes-with-it)
- [Install and use](#install-and-use)
- [Limitations](#limitations)

## Overview

A small Python tool that takes an Altium BOM and turns it into a DigiKey shopping list. Source: [Cimos/Altium-Push-to-DigiKey](https://github.com/Cimos/Altium-Push-to-DigiKey). MIT-licensed.

## How it works

It reads a BOM emitted by Altium — either the raw CSV from a BOM Output Job, or the normalised JSON from a review-pack pipeline — and POSTs it to DigiKey's anonymous `mylists/api/thirdparty` endpoint. You get back a short URL (`https://www.digikey.com/short/<code>`) that you open in a browser to claim the list under your account.

Parsing is deliberately tolerant: it auto-detects headers (case-insensitive) for manufacturer part number, quantity, and designator, then skips `DNP` rows and anything with an empty MPN or zero quantity.

## No auth, and the caveat that comes with it

There are no API keys or OAuth to set up. The model is *anonymous on the way in, account-tied when you open the returned URL* — the same endpoint Digi-Key's own official KiCad plugin uses. A future authenticated direct-to-account mode (OAuth2, via DigiKey's Developer API) is on the roadmap so lists can land straight in your account without the shareable link.

## Install and use

Needs Python 3.8+.

```bash
pip install git+https://github.com/Cimos/Altium-Push-to-DigiKey.git
```

That gives you an `altium-push-to-digikey` command. Typical runs:

```bash
# from review-pack JSON
python digikey_push.py path\to\review-pack\bom.json

# from raw CSV, with a name
python digikey_push.py path\to\bom.csv --list-name "MyBoard rev B"
```

Useful flags: `--dry-run` (parse and report, don't POST), `--open` (launch the browser), `--tags "tag1,tag2"`.

## Limitations

Worth knowing before you lean on it:

- The returned short URL is **link-shareable until you claim it** — treat it like a secret.
- The endpoint is not formally documented as a public API, and there's no per-user authentication on the POST.
- No compliance filtering — NDAA and any regulatory concerns are yours to handle upstream.
