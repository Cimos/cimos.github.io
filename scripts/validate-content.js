// Pre-merge content checks (no dependencies). Run: node scripts/validate-content.js
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const postsDir = path.join(root, '_posts');
const errors = [];

for (const file of fs.readdirSync(postsDir).filter((f) => /\.(md|markdown)$/.test(f))) {
  const rel = `_posts/${file}`;
  if (!/^\d{4}-\d{2}-\d{2}-.+\.(md|markdown)$/.test(file)) {
    errors.push(`${rel}: filename must be YYYY-MM-DD-slug.md`);
  }
  const text = fs.readFileSync(path.join(postsDir, file), 'utf8').replace(/^\uFEFF/, '');
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!m) {
    errors.push(`${rel}: missing YAML front matter`);
    continue;
  }
  const fm = m[1];
  for (const key of ['layout']) {
    if (!new RegExp(`^${key}:`, 'm').test(fm)) errors.push(`${rel}: missing "${key}" in front matter`);
  }
  const img = fm.match(/^image:\s*["']?([^"'\r\n]+?)["']?\s*$/m);
  if (!img) {
    errors.push(`${rel}: missing "image:" (run npm run og)`);
  } else if (img[1].startsWith('/') && !fs.existsSync(path.join(root, img[1]))) {
    errors.push(`${rel}: image not found: ${img[1]}`);
  }
}

// Keep photos small; run `npm run images` if this fails.
const MAX_IMAGE_BYTES = 1.5 * 1024 * 1024;
function* walk(dir) {
  if (!fs.existsSync(dir)) return;
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) yield* walk(p);
    else yield p;
  }
}
for (const dir of ['images', 'assets/images']) {
  for (const f of walk(path.join(root, dir))) {
    if (/\.(png|jpe?g|gif|webp)$/i.test(f) && fs.statSync(f).size > MAX_IMAGE_BYTES) {
      errors.push(`${path.relative(root, f).replace(/\\/g, '/')}: over 1.5MB (run npm run images)`);
    }
  }
}

if (errors.length) {
  console.error(errors.map((e) => `✗ ${e}`).join('\n'));
  process.exit(1);
}
console.log('Content validation passed.');
