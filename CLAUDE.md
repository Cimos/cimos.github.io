# CMOS Foundry — cimos.github.io

Simon Maddison's personal site and blog. Electronics & software engineer
(UAV avionics, PCB design, mechanical keyboards). Dark "Jinx / Zaun"
cyberpunk neon identity.

---

## Stack

- **Jekyll 4** static site on **GitHub Pages**, built and deployed by
  **GitHub Actions** (`.github/workflows/ci.yml`; Pages source = "GitHub Actions").
  The `Gemfile` is what production uses — the artifact CI checks is the one deployed.
- **No theme.** Moonwalk has been fully removed — all layouts/includes/sass are local; the main stylesheet is `_sass/foundry.scss`.
- Plugins: `jekyll-feed`, `jekyll-seo-tag`, `jekyll-sitemap`, plus the local
  `_plugins/og_image.rb` (points each post's `image` at its generated OG card).
- Fonts are **self-hosted** (Inter variable + Roboto Mono, latin subset) in `assets/fonts/` — no Google Fonts request.

## Local development

```bash
bundle install
bundle exec jekyll serve      # http://localhost:4000
```

No local Ruby? Build in Docker:

```bash
docker run --rm -v "$PWD":/site -w /site -e JEKYLL_ENV=development ruby:3.3 \
  bash -c "bundle config set path vendor/bundle && bundle install && bundle exec jekyll build"
python3 scripts/dev-server.py    # serves _site on http://localhost:4000
```

Development builds (`JEKYLL_ENV=development`) include a floating **feedback
widget** (bottom-left, adapted from etchy's demo widget). `scripts/dev-server.py`
serves `_site/` and collects `POST /feedback` into `.feedback/feedback.jsonl`
(gitignored — contains IP/UA/names). Production builds never include the widget.

The Node scripts in `scripts/` are **asset tooling, not part of the Jekyll build** — CI runs `npm run og` before every build; the rest are run by hand (see below). They need `npm install` first.

---

## Repo layout

```
_config.yml            site config, theme_config, analytics, front-matter defaults
_data/home.yml         nav, portfolio cards, archive cards, footer/social links
_layouts/              default · home · post · blog
_includes/             head, terminal, pcb_viewer, site_scripts, analytics,
                       card_list, date_and_social_share, post_list, …
_sass/                 foundry.scss (main styles) · list.scss (cards) · syntax.scss
_plugins/              og_image.rb (default post `image` → generated OG card)
_posts/                blog posts (Markdown)
assets/fonts/          self-hosted woff2
assets/images/og/      per-post social cards (generated in CI, gitignored)
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
---
```

That's it — CI generates the social card on every build and the post's
`image` defaults to it (set `image:` only to override with a custom picture).
The tags page (`/tags`) and RSS pick it up automatically.

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

Palette lives as CSS custom properties in `_sass/foundry.scss`
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

- **Bootable terminal** — `_includes/terminal.html` + `.term-*` in `foundry.scss`.
  Backtick or the bottom-right chip opens it. Command data (projects, posts,
  socials) is **generated from Jekyll**, so it stays in sync. `open`/`theme`
  do real navigation / theme switching.
- **3D PCB viewer** — `_includes/pcb_viewer.html`, vendored three.js. Enabled per
  post via front matter `pcb3d: true` (procedural placeholder) or
  `pcb3d: /assets/models/foo.glb` (real model; GLTFLoader path already wired).
  Loads only on pages that set the flag.
- **Live ★ counts** — client-side GitHub API fetch (`site_scripts.html`),
  6h cache, pill shown at ≥2 stars.
- **Per-post OG cards** — PNGs generated into `assets/images/og/` by CI
  (`npm run og`, gitignored); `_plugins/og_image.rb` makes each post's `image`
  default to its card.
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

Not run by Jekyll — run after `npm install`:

- **`npm run og`** — generate any missing social cards. CI runs it before every build; run it locally only to preview cards.
- **`npm run images`** — recompress everything under `images/` to ≤1600px (mozjpeg / palette PNG). Run after adding photos.
- **`npm run icons`** — regenerate the favicon set, `logo.svg`, and the default OG image from the chip monogram.

---

## Gotchas / maintenance

- **Deploys only happen through CI.** A push to `master` deploys after `lint`
  and `build-and-check` pass; a red build means nothing ships. Re-run via
  *Actions → CI → Run workflow* if a deploy fails transiently.
- `site.url` has **no trailing slash** (keeps absolute URLs from doubling up).
- Images are large photos — keep them run through `npm run images`.

---

## Open threads (state as of this commit)

1. **Layout redesign — DONE.** Moonwalk dropped; homepage restructured: sticky
   header, two-column hero with the flagship boot-readout panel (data-driven from
   the `flagship: true` entry in `_data/home.yml`), project card grid, styled blog
   rows, real footer. Reading pages keep a ~47rem prose measure; the homepage uses
   `shell: wide` front matter for the 74rem shell.
2. **CI + Actions deploy — DONE.** One workflow builds, generates OG cards,
   link-checks (html-proofer), and deploys the checked artifact to Pages.
3. **Etchy — DONE.** Published write-up + flagship card.
4. **Real Mad_RP2040 3D model — DONE.** `assets/models/mad-rp2040.glb` (~15 MB,
   already quantized; further shrinking would need meshopt/Draco decoders vendored).
