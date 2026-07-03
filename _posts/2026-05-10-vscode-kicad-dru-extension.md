---
layout: post
author: Simon Maddison
title:  "A Tiny VS Code Extension for KiCad Custom Design Rules"
date:   2026-05-10
tags: [kicad, vscode, kicad-dru, design-rules, pcb, eda, extension]
image: /assets/images/og/vscode-kicad-dru-extension.png
---

## Table of contents
- [Overview](#overview)
- [Why this exists](#why-this-exists)
- [What it does](#what-it-does)
- [What it doesn't do](#what-it-doesnt-do)
- [Install](#install)
- [Pairing it with KiCad](#pairing-it-with-kicad)
- [What's next](#whats-next)

## Overview

Just shipped a small Visual Studio Code extension: **[KiCad Custom Design Rules](https://marketplace.visualstudio.com/items?itemName=cimos.kicad-dru)**. Source on GitHub at [Cimos/vscode-kicad-dru](https://github.com/Cimos/vscode-kicad-dru). It adds proper syntax highlighting and snippets for `.kicad_dru` files in VS Code, and nothing else. Specifically nothing else — more on that below.

Marketplace ID: `cimos.kicad-dru`. MIT-licensed. Currently v0.0.1.

## Why this exists

KiCad's only built-in editor for custom design rules is the single-line textbox in *Board Setup → Custom Rules*, plus a *Check Rule Syntax* button. That's fine for a one-liner. The moment your DRU file has more than two or three rules — multi-class clearance, manufacturer-specific via stacks, a stack of `disallow` constraints — you want a real editor. Multi-cursor. Search. Folding. Colour that distinguishes a `condition` operator from an `A.NetClass` accessor from a layer name from a string literal.

The KiCad forums make the demand obvious. There's a long-running megathread where people post DRU snippets and ask grammar questions, and at least one user spelled it out plainly: *"externally I have a better text editor with syntax highlight and the possibility to search things and multiple cursors."* They were clearly already editing in VS Code; the editor just wasn't doing anything useful.

The closest existing extension is `DanielMeza.kicad-syntax-highlighter`. It declares `.kicad_dru` in its file-extension list, but the underlying grammar is a generic KiCad s-expression highlighter — keywords like `condition`, `constraint`, `disallow`, `A.NetClass`, `intersectsArea` all colour as plain atoms. Functionally you get matched parens and not much else. `oaslananka.kicadstudio` is the heavyweight all-in-one, and it does great workspace-level things, but it doesn't ship a TextMate grammar that knows the DRU sub-language either.

Nobody had bothered to write a grammar tuned to DRU specifically. So I did.

## What it does

- **Syntax highlighting** scoped to `.kicad_dru`. Top-level keywords (`version`, `rule`, `constraint`, `condition`, `layer`, `severity`, `disallow`), every constraint type (`clearance`, `hole_clearance`, `track_width`, `length`, `assertion`, …), the token-expression accessors used inside `condition` strings (`A.NetClass`, `B.intersectsArea`, …), operators, severities, layer names, comments, and numbers with units all colour distinctly.
- **Snippets** for the rule shapes you keep re-typing: starter `rule` block, clearance by netclass, disallow, length matching, via and track sizing, hole-to-hole, assertion. Type the prefix in a paren context, hit tab.
- **Editor niceties**: `#` line comments toggle with Ctrl+/, parens match, top-level `(rule …)` blocks fold, brackets auto-close.

That's the entire v0.0.1 surface. No `extension.js`, no activation event, no LSP, no telemetry. Just static JSON contributions: a TextMate grammar, a snippet file, and a language config. It loads when you open a `.kicad_dru` and does nothing the rest of the time.

## What it doesn't do

Worth being explicit, because the existing KiCad extensions on the marketplace tend to over-promise:

- **No validation.** This is a highlighter, not a parser. KiCad's *Check Rule Syntax* button remains the source of truth for whether a rule is valid. If your file colours nicely but KiCad rejects it, KiCad is right.
- **No schematic / PCB / symbol / footprint support.** Those have their own grammar and their own existing extensions. Staying out of that territory is the whole point — DRU support there is incidental; here it's first-class.
- **No hover docs, completion, or diagnostics yet.** All worth doing once the grammar settles. For v0.0.1 they would have meant shipping a real `extension.js` for what is currently three static JSON files. Tracked as future work.

## Install

From the VS Code Marketplace:

```
ext install cimos.kicad-dru
```

…or search for **"KiCad Custom Design Rules"** in the Extensions view.

A `.vsix` is also attached to each GitHub release if you'd rather sideload:

```
code --install-extension vscode-kicad-dru-<version>.vsix
```

## Pairing it with KiCad

KiCad ≥ 7 has *Preferences → Configure Paths → External Tools*. Point it at VS Code's executable and you get one-click round trips: open the `.kicad_dru` file from the PCB editor, edit it here, save, switch back, re-run *Check Rule Syntax*. That's the workflow this extension is built around.

## What's next

The big-ticket items for v0.1.x:

- **Hover docs** scraped from the KiCad documentation, so hovering on `clearance` or `intersectsArea` surfaces the constraint type's docs without leaving the editor.
- **Layer-name catalogue refresh** — KiCad 9 added user-defined Cu layers and renamed some display strings, and the v0.0.1 grammar isn't fully aware of them yet.
- **Open VSX publish** so VSCodium / Cursor / Theia users can install without bouncing through the MS marketplace.

If you hit a real `.kicad_dru` file the highlighter mangles, [open an issue](https://github.com/Cimos/vscode-kicad-dru/issues) with a minimal snippet and I'll take a look. PRs welcome too — DRU corner cases are exactly the kind of thing a small fixture catches and prose review misses.

-SM
