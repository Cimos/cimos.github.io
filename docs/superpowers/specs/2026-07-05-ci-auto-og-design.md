# CI + auto-OG — design (issue #11)

## Goal
On every pull request, automatically make sure each blog post has its social (OG)
card and that the site has no broken internal links — without changing how the
site deploys.

## Decisions (from review 2026-07-05)
- **Architecture A:** a CI-check workflow only. GitHub's automatic Pages builder
  keeps deploying `master` exactly as now. We do **not** take over deploy.
- **Auto-OG A1:** on a PR, CI runs `npm run og`; if it created a card or injected
  an `image:` line, it commits those back to the PR branch. GitHub's auto-deploy
  then publishes them on merge. Truly automatic — no manual step.
- **Link check:** html-proofer on the built site, internal links/anchors/images
  only (external link checking is flaky/rate-limited — out of scope).

## The workflow — `.github/workflows/ci.yml`

Triggers: `pull_request` → `master`, and `push` → `master`.

Permissions: `contents: write` (needed for the A1 commit-back).

Single job `ci` on `ubuntu-latest`:
1. **Checkout** — for a PR, check out `github.head_ref` so the commit-back can be
   pushed to the PR branch.
2. **Ruby** — `ruby/setup-ruby` with `bundler-cache: true` (uses our Gemfile,
   Jekyll 4.3).
3. **Node** — `actions/setup-node` (Node 20). No npm cache (no committed lockfile).
4. **`npm install`** — installs the OG tooling deps (sharp).
5. **`npm run og`** — generate any missing cards + inject `image:` front matter.
   Idempotent; a no-op when everything already has a card.
6. **Commit back (PR only, `if: github.event_name == 'pull_request'`)** — if
   `git status --porcelain` shows changes, commit them (author: Cimos) limited to
   `assets/images/og/` and `_posts/`, and push to the PR branch.
   - *No loop:* pushes made with the default `GITHUB_TOKEN` do not trigger new
     workflow runs, so the commit-back can't re-fire CI.
7. **Build** — `JEKYLL_ENV=production bundle exec jekyll build` (production =
   no dev feedback widget, analytics on — matches what GitHub deploys). The build
   already includes the cards generated in step 5.
8. **Link check** — `bundle exec htmlproofer ./_site` with:
   - `--disable-external` (internal links, anchors, images only)
   - `--allow-hash-href` (for `href="#"` controls: theme toggle, copy buttons)
   - `--ignore-urls` for anything that legitimately 404s at check time (none known yet).

On `push` to `master` the same job runs build + link-check as a verification pass;
the commit-back step is skipped (not a PR).

## Gemfile change
Add `gem "html-proofer", "~> 5.0"` to the development group so
`bundle exec htmlproofer` is available.

## What this deliberately does NOT do
- Does not deploy (GitHub's auto-build still owns deploy).
- Does not check external links (flaky; revisit later if wanted).
- Does not switch the Pages source to GitHub Actions (that was Option B, not chosen).
- No spellcheck / Lighthouse / accessibility gates (out of scope for #11).

## Edge cases
- **Fork PRs:** `GITHUB_TOKEN` can't push to a fork branch, so the commit-back
  would fail. Not a concern (solo repo, no forks); if it ever happens, the step is
  guarded to no-op rather than fail hard.
- **Post with an OG card already:** `npm run og` is idempotent → no changes → no
  commit → clean pass.
- **html-proofer false positives:** tune via `--ignore-urls` / `--swap-urls` if the
  first real run surfaces any; start strict.

## Verification
- Add the workflow on a branch, open the PR, watch the CI run go green.
- Confirm: a test post with no `image:` gets a card generated and committed back by CI.
- Confirm: an intentionally broken internal link turns the check red.
- Confirm: `master` push runs build + link-check with no commit-back.
- Leave issue #11 open for Simon to close after reviewing a real run (per house rule).
