# CMOS Foundry — cimos.github.io

Simon Maddison's personal site and blog. Electronics & software engineer
(UAV avionics, PCB design, mechanical keyboards). Dark "Jinx / Zaun"
cyberpunk neon identity.

---

## Stack

- **Jekyll 4** static site, deployed on **GitHub Pages** (default branch build from `master`).
- Started on the Moonwalk remote theme, but **every layout/include/sass file is now overridden locally** — Moonwalk is effectively vestigial (see *Open threads* below).
- Plugins: `jekyll-feed`, `jekyll-seo-tag`, `jekyll-sitemap`.
- Fonts are **self-hosted** (Inter variable + Roboto Mono, latin subset) in `assets/fonts/` — no Google Fonts request.

## Local development

```bash
bundle install
bundle exec jekyll serve      # http://localhost:4000
```

The Node scripts in `scripts/` are **build-time tooling, not part of the Jekyll build** — run them by hand when needed (see below). They need `npm install` first.

---

## Repo layout

```
_config.yml            site config, theme_config, analytics, front-matter defaults
_data/home.yml         nav, portfolio cards, archive cards, footer/social links
_layouts/              default · home · post · blog
_includes/             head, terminal, pcb_viewer, site_scripts, analytics,
                       card_list, date_and_social_share, post_list, …
_sass/                 moonwalk.scss (main styles) · list.scss (cards) · syntax.scss
_posts/                blog posts (Markdown)
assets/fonts/          self-hosted woff2
assets/images/og/      per-post social cards (generated — see scripts/)
assets/js/vendor/      vendored three.js + OrbitControls + GLTFLoader
scripts/               asset tooling (OG cards, image compression, icons)
about.md tags.md blog.html 404.html
```

---

## How to add content

### A blog post
Create `_posts/YYYY-MM-DD-slug.md`:

```yaml
---
layout: post
author: Simon Maddison
title:  "Post Title"
date:   2026-07-01
tags: [tag-a, tag-b]
image: /assets/images/og/slug.png   # ← run `npm run og` to generate this
---
```

Then **`npm run og`** to generate the social card and inject the `image:` line
if missing. The tags page (`/tags`) and RSS pick it up automatically.

### A portfolio project card
Edit `_data/home.yml` under `project_entries` (or `old_project_entries` for
Archive). Fields:

```yaml
- title: Project Name
  desc: One factual sentence.
  url: post-slug            # internal write-up (omit if none)
  href: https://…           # external link (used only if no url; shows a ↗)
  repo: Cimos/RepoName      # optional — live ★ star pill (shown at ≥2 stars)
  highlight: SOON           # optional — SOON or WIP badge; a bare card with
                            #   neither url nor href renders non-clickable
```

The **terminal** and any data-driven UI read these automatically — no second place to update.

---

## Design system

Palette lives as CSS custom properties in `_sass/moonwalk.scss`
(`@mixin dark-appearance` / `light-appearance`). Theme is `auto` by default
(follows OS), toggle stamps `data-theme` on `<html>`.

| Token | Dark | Light | Use |
|---|---|---|---|
| `--blue` | `#35D6EA` | `#0E8FA6` | links, primary accent (Jinx hair) |
| `--pink` | `#FF2E88` | `#D6156A` | secondary accent, badges (Jinx) |
| `--violet` | `#9A6BFF` | `#6D3BE0` | ambient glow, grid haze |
| `--bg` | `#0B0912` | `#F4F1FA` | page ground |
| `--head` `--text` `--muted` `--edge` | … | … | headings / body / secondary / borders |
| `--glow` | `0.70` | `0.35` | neon intensity multiplier |
| `--gx` | `0.55` | `0.55` | glitch intensity multiplier |

Fonts: **Inter** (headings + body), **Roboto Mono** (labels, eyebrows, dates, code, terminal).

---

## Custom features (and where they live)

- **Bootable terminal** — `_includes/terminal.html` + `.term-*` in `moonwalk.scss`.
  Backtick or the bottom-right chip opens it. Command data (projects, posts,
  socials) is **generated from Jekyll**, so it stays in sync. `open`/`theme`
  do real navigation / theme switching.
- **3D PCB viewer** — `_includes/pcb_viewer.html`, vendored three.js. Enabled per
  post via front matter `pcb3d: true` (procedural placeholder) or
  `pcb3d: /assets/models/foo.glb` (real model; GLTFLoader path already wired).
  Loads only on pages that set the flag.
- **Live ★ counts** — client-side GitHub API fetch (`site_scripts.html`),
  6h cache, pill shown at ≥2 stars.
- **Per-post OG cards** — generated PNGs in `assets/images/og/`; each post's
  `image:` front matter points at its card.
- **Reading UX** — copy-code buttons, hover heading anchors, image lightbox,
  lazy-loaded images (all `site_scripts.html`, article pages only).
- **Animated hero** — faint PCB-trace canvas behind the homepage hero
  (`#hero-canvas`, `site_scripts.html`).
- **Print CV** — `about.md` "Save as PDF" button + `@media print` block flips
  the whole site to a clean printable light palette.
- **Analytics** — GoatCounter (`_includes/analytics.html`), production-only,
  configured via `analytics.goatcounter` in `_config.yml`.

---

## Asset tooling (`scripts/`)

Not run by Jekyll — run manually after `npm install`:

- **`npm run og`** — generate a social card per post + inject `image:` front matter. **Run this whenever you add a post.**
- **`npm run images`** — recompress everything under `images/` to ≤1600px (mozjpeg / palette PNG). Run after adding photos.
- **`npm run icons`** — regenerate the favicon set, `logo.svg`, and the default OG image from the chip monogram.

---

## Gotchas / maintenance

- ⚠️ **OG cards are not automatic.** New posts need `npm run og` (there is no
  build-time hook yet — see *CI + auto-OG* below).
- **Moonwalk is dead weight.** `remote_theme` is still declared but nothing
  depends on it; `moonwalk.gemspec`, `_screenshots/`, `_examples/`,
  `moonwalk_on_windows.md`, `github_pages.md` are leftover theme-repo files.
- `site.url` has **no trailing slash** (keeps absolute URLs from doubling up).
- Images are large photos — keep them run through `npm run images`.

---

## Open threads (state as of this commit)

1. **Layout redesign — decision pending.** Review concluded the single 720px
   column is the weak point (no header, no hierarchy, blog as bare bullets).
   A restructured homepage was mocked up (sticky header, two-column hero with a
   featured-flagship panel, wider project grid, styled blog rows). **Not yet
   built.** Recommendation: drop Moonwalk, stay on Jekyll, build the new layout.
   Astro migration considered but not needed.
2. **CI + auto-OG — queued.** A GitHub Actions workflow to build, link-check
   (html-proofer), and auto-generate OG cards so new posts never miss one.
3. **Etchy** — teased on the portfolio with a SOON badge; flip to a real card +
   write-up when the repo goes public.
4. **Real Mad_RP2040 3D model** — currently a procedural placeholder. Export a
   GLB (`kicad-cli pcb export glb Mad_RP2040.kicad_pcb -o madrp2040.glb`), drop
   in `assets/models/`, set the post's `pcb3d:` to that path.
