#!/usr/bin/env node
// Generate a branded social-share (OG) card per blog post from its title,
// and inject `image:` into the post front matter if missing. Idempotent.
//   npm install && npm run og
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');
const POSTS = path.join(__dirname, '..', '_posts');
const OGDIR = path.join(__dirname, '..', 'assets', 'images', 'og');
fs.mkdirSync(OGDIR, { recursive: true });

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

function wrap(title, max) {
  const words = title.split(/\s+/), lines = []; let cur = '';
  for (const w of words) {
    if ((cur + ' ' + w).trim().length > max && cur) { lines.push(cur); cur = w; }
    else cur = (cur + ' ' + w).trim();
  }
  if (cur) lines.push(cur);
  return lines;
}

function ogSvg(title) {
  const lines = wrap(title, 22).slice(0, 4);
  const base = lines.length >= 4 ? 48 : lines.length === 3 ? 56 : 66;
  const maxLen = Math.max(...lines.map((l) => l.length));
  const size = Math.min(base, Math.floor(1020 / (0.6 * maxLen))); // guarantee fit
  const lh = size * 1.18, blockH = lines.length * lh, startY = 300 - blockH / 2 + size;
  const tspans = lines.map((l, i) =>
    `<text x="90" y="${startY + i * lh}" font-family="sans-serif" font-weight="bold" font-size="${size}" fill="#EDEAF6">${esc(l)}</text>`
  ).join('\n  ');
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630">
  <defs>
    <radialGradient id="g1" cx="18%" cy="0%" r="80%"><stop offset="0%" stop-color="#2a1748"/><stop offset="100%" stop-color="#0B0912"/></radialGradient>
    <radialGradient id="g2" cx="100%" cy="0%" r="70%"><stop offset="0%" stop-color="#3a1030" stop-opacity="0.8"/><stop offset="100%" stop-color="#0B0912" stop-opacity="0"/></radialGradient>
    <pattern id="grid" width="44" height="44" patternUnits="userSpaceOnUse"><path d="M 44 0 L 0 0 0 44" fill="none" stroke="#9A6BFF" stroke-opacity="0.08" stroke-width="1"/></pattern>
  </defs>
  <rect width="1200" height="630" fill="url(#g1)"/>
  <rect width="1200" height="630" fill="url(#grid)"/>
  <rect width="1200" height="630" fill="url(#g2)"/>
  <text x="90" y="110" font-family="monospace" font-size="24" letter-spacing="5" fill="#35D6EA">CMOS FOUNDRY</text>
  ${tspans}
  <rect x="90" y="540" width="120" height="5" fill="#FF2E88"/>
  <text x="90" y="585" font-family="monospace" font-size="24" fill="#7E7897">cimos.github.io</text>
</svg>`;
}

(async () => {
  const files = fs.readdirSync(POSTS).filter((f) => f.endsWith('.md'));
  for (const f of files) {
    const full = path.join(POSTS, f);
    let src = fs.readFileSync(full, 'utf8');
    const fm = src.match(/^---\n([\s\S]*?)\n---/);
    if (!fm) { console.log('skip (no front matter):', f); continue; }
    const titleM = fm[1].match(/^title:\s*"?(.+?)"?\s*$/m);
    const title = titleM ? titleM[1] : f;
    const slug = f.replace(/^\d{4}-\d{2}-\d{2}-/, '').replace(/\.md$/, '');
    await sharp(Buffer.from(ogSvg(title))).png().toFile(path.join(OGDIR, `${slug}.png`));
    if (!/^image:\s*/m.test(fm[1])) {
      src = src.replace(/^(---\n[\s\S]*?\n)(---)/, (m, body, end) => body + `image: /assets/images/og/${slug}.png\n` + end);
      fs.writeFileSync(full, src);
    }
    console.log('og:', slug);
  }
  console.log(`done — ${files.length} posts`);
})().catch((e) => { console.error(e); process.exit(1); });
