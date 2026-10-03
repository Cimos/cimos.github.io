---
layout: post
author: Simon Maddison
title:  "eV+ in VS Code: Language Support for Omron Robot Programs"
date:   2026-10-03
tags: [vscode, omron, robotics, automation, ev-plus, extension]
image: /assets/images/og/vscode-evplus-extension.png
---

## Table of contents
- [Overview](#overview)
- [Why bother](#why-bother)
- [What you get](#what-you-get)
- [Built from the manual](#built-from-the-manual)
- [Trying it](#trying-it)

## Overview

Omron Adept robots are programmed in **eV+** (and its older sibling V+), a
language that dates back decades and shows it. The official editor does the job,
but it's a long way from a modern code editor.
[**vscode-evplus**](https://github.com/Cimos/vscode-evplus) brings eV+ / V+
programs (`.pg`, `.v2`) into VS Code: highlighting, hover help, completion,
diagnostics and navigation. MIT-licensed.

## Why bother

eV+ has a few traps that bite anyone coming from another language. The big one:
everything after a `;` is a comment. So this line

```
a = 1 ; b = 2
```

only assigns `a`. Nothing warns you, the robot just doesn't do the second half.
Add a large program split across many `.PROGRAM` blocks, `GOTO` labels, and a
reference manual you have to keep open in another window, and small mistakes are
easy to make and slow to find. An editor that knows the language catches most of
them before the program ever reaches the controller.

## What you get

- **Highlighting** for control flow, instructions, functions, system switches and
  parameters, radix numbers (`^HFF`, `^B1010`), precision points (`#pick`), string
  variables (`$name`), labels and `.PROGRAM` / `.END` blocks, with folding.
- **Hover** shows the manual's syntax line for the keyword under the cursor.
- **Completion** for 260+ keywords with their type and syntax, and **signature
  help** that tracks which parameter you're on.
- **Diagnostics** for code hiding after a `;`, `GOTO` targets that don't exist,
  and unpaired `.PROGRAM` / `.END`.
- **Navigation**: every program in the Outline panel, go-to-definition and find
  references across the workspace, and Ctrl+T to jump to any program by name.
- Snippets and auto-indent for the usual blocks (IF, WHILE, DO/UNTIL, FOR, CASE).

## Built from the manual

The keyword data isn't typed in by hand. A script reads an extraction of the eV+
Language Reference Guide and generates both the keyword list (name, type and
syntax for each entry) and the keyword patterns in the grammar. When the manual
changes, the extension is regenerated rather than patched. Only the syntax lines
are committed. If you own the manual you can regenerate locally with the fuller
descriptions for richer hover text.

The grammar is covered by tokenisation snapshot tests, so a change that breaks
highlighting on an existing construct fails the test run.

## Trying it

It isn't on the marketplace yet. Build it from source:

```
npm install
npm run package
./install.sh
```

`install.sh` installs the extension on both the WSL and Windows sides of VS Code.
Reload, open a `.pg` file, and go.

Source is on [GitHub](https://github.com/Cimos/vscode-evplus).

-SM
