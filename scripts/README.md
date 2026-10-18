# scripts/

Asset tooling. **Not run by Jekyll.** Requires Node + a one-time install:

```bash
npm install
```

| Command | What it does | When to run |
|---|---|---|
| `npm run og` | Generate a social-share (OG) card for any post **missing** one into `assets/images/og/` (gitignored). Pass `-- --force` to regenerate all after a template change. | Automatic — CI runs it before every build. Run locally only to preview cards. |
| `npm run images` | Recompress everything under `images/` to ≤1600px (mozjpeg / palette PNG), in place. Filenames unchanged. | After adding photos/renders. |
| `npm run icons` | Regenerate the favicon set, `logo.svg`, and `assets/images/og-default.png` from the chip monogram. | Only if the brand mark changes. |
| `node scripts/validate-content.js` | Post filename/front-matter checks and image size limits (also run in CI). | Optional pre-push check. |
| `python3 scripts/dev-server.py` | Serve `_site/` locally and collect feedback-widget posts into `.feedback/`. | Local review of a development build. |

All are safe to re-run.