# scripts/

Build-time asset tooling. **Not run by Jekyll** — run by hand when adding
content, then commit the generated files. Requires Node + a one-time install:

```bash
npm install
```

| Command | What it does | When to run |
|---|---|---|
| `npm run og` | Generate a social-share (OG) card per post from its title, and inject the `image:` front-matter line if missing. | After adding/renaming a blog post. |
| `npm run images` | Recompress everything under `images/` to ≤1600px (mozjpeg / palette PNG), in place. Filenames unchanged. | After adding photos/renders. |
| `npm run icons` | Regenerate the favicon set, `logo.svg`, and `assets/images/og-default.png` from the chip monogram. | Only if the brand mark changes. |

All three are safe to re-run; they overwrite their generated outputs and skip
front-matter that's already set.
