---
layout: post
author: Simon Maddison
title:  "Cube SD Reader: A CubeOrange+ as a USB Card Reader"
date:   2026-11-22
tags: [ardupilot, chibios, usb, firmware, stm32, flight-controller]
---

Getting the microSD card out of a flight controller is a pain. It's tiny and usually buried somewhere in the airframe. So I wrote a firmware that turns a CubeOrange+ into a USB card reader. Flash it, plug in USB, and the card shows up on your computer as a disk called **Cube USB Drive**. Flash ArduPilot back when you're done.

It's on GitHub at [Cimos/cube-sd-reader](https://github.com/Cimos/cube-sd-reader), v0.1.0 out now. It's my own project, not an official CubePilot or ArduPilot release.

## How it works

It's a small standalone app built from pinned ArduPilot and ChibiOS sources. No flight stack and no filesystem on the board, it just passes raw SD card blocks over USB.

- **Keeps the bootloader.** It goes on through the normal ArduPilot bootloader like any other APJ (Mission Planner, QGroundControl or `uploader.py`), so ArduPilot can always go back on.
- **Two USB functions.** A mass storage disk, and a serial control port for `info`, `status`, `bootloader` and `reboot`.
- **Its own USB ID.** `2DAE:1158`, so Windows uses its built-in disk and serial drivers. Nothing to install.
- **Small.** The whole image is about 46 KB.

## The driver gotcha

The first build used the CubeOrange+'s own USB ID (`2DAE:1058`). Windows matched it to CubePilot's serial driver and bound the storage side as "Cube Orange+ Mavlink (COM21)". No disk, even though the reader said the card was ready. A separate ID fixed it with no driver changes at all.

Eject was the other one. The first Windows eject helper reset the board. Keeping the serial port and the locked volume open while sending the cache sync and eject, then asking for the bootloader, sorted it.

## Bench results

One CubeOrange+, one 64 GB FAT32 card, Windows:

| Test | Result |
|---|---|
| 32 MiB write, including flush | 0.81 MB/s |
| 32 MiB read | 1.13 MB/s, SHA-256 matched |
| Read again after reboot and reflash | 1.13 MB/s, matched |
| CHKDSK | No errors |
| Eject, back to bootloader, reflash ArduPlane | Passed, no replug |
| Parameters after restoring ArduPlane | 983 present, only counters and startup calibration changed |

It's USB Full Speed, so about 1 MB/s is the ceiling. Fine for logs, not for dumping a full card.

## What's not done

One board, one card, one host so far. Linux and exFAT, more cards, pulling the card mid-transfer, power loss and a pile of reconnect cycles are all still to test. Use a bench Cube with the outputs disconnected and a card you've backed up.

-SM
