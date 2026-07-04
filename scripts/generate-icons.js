#!/usr/bin/env node
// Regenerate the CMOS Foundry favicon set, logo.svg, and the default OG image
// from the chip-monogram SVG.  npm install && npm run icons
const sharp = require('sharp');
const pngToIcoMod = require('png-to-ico');
const pngToIco = pngToIcoMod.default || pngToIcoMod;
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const FAV = path.join(ROOT, 'assets', 'images', 'favicon');
fs.mkdirSync(FAV, { recursive: true });

// chip-die "C" monogram — cyan/magenta on dark
const icon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <defs>
    <radialGradient id="bg" cx="35%" cy="25%" r="90%"><stop offset="0%" stop-color="#1b1330"/><stop offset="100%" stop-color="#0B0912"/></radialGradient>
    <linearGradient id="stroke" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#35D6EA"/><stop offset="100%" stop-color="#7fe9f4"/></linearGradient>
  </defs>
  <rect x="0" y="0" width="512" height="512" rx="112" fill="url(#bg)"/>
  <rect x="8" y="8" width="496" height="496" rx="108" fill="none" stroke="#2A2440" stroke-width="6"/>
  <g fill="#FF2E88">
    <rect x="150" y="70" width="26" height="34" rx="6"/><rect x="243" y="70" width="26" height="34" rx="6"/><rect x="336" y="70" width="26" height="34" rx="6"/>
    <rect x="150" y="408" width="26" height="34" rx="6"/><rect x="243" y="408" width="26" height="34" rx="6"/><rect x="336" y="408" width="26" height="34" rx="6"/>
  </g>
  <g fill="#35D6EA">
    <rect x="70" y="150" width="34" height="26" rx="6"/><rect x="70" y="243" width="34" height="26" rx="6"/><rect x="70" y="336" width="34" height="26" rx="6"/>
    <rect x="408" y="150" width="34" height="26" rx="6"/><rect x="408" y="243" width="34" height="26" rx="6"/><rect x="408" y="336" width="34" height="26" rx="6"/>
  </g>
  <rect x="104" y="104" width="304" height="304" rx="52" fill="#12101c" stroke="#2A2440" stroke-width="4"/>
  <path d="M 330 190 A 92 92 0 1 0 330 322" fill="none" stroke="url(#stroke)" stroke-width="34" stroke-linecap="round"/>
  <circle cx="332" cy="256" r="20" fill="#FF2E88"/>
</svg>`;

const og = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630">
  <defs>
    <radialGradient id="g1" cx="18%" cy="0%" r="80%"><stop offset="0%" stop-color="#2a1748"/><stop offset="100%" stop-color="#0B0912"/></radialGradient>
    <pattern id="grid" width="44" height="44" patternUnits="userSpaceOnUse"><path d="M 44 0 L 0 0 0 44" fill="none" stroke="#9A6BFF" stroke-opacity="0.08" stroke-width="1"/></pattern>
  </defs>
  <rect width="1200" height="630" fill="url(#g1)"/>
  <rect width="1200" height="630" fill="url(#grid)"/>
  <text x="90" y="250" font-family="monospace" font-size="26" letter-spacing="6" fill="#7E7897">SIMON MADDISON · UAS SYSTEMS ENGINEER</text>
  <text x="86" y="360" font-family="sans-serif" font-weight="bold" font-size="120" fill="#EDEAF6">CMOS Foundry</text>
  <text x="90" y="430" font-family="monospace" font-size="30" fill="#35D6EA">// embedded · avionics · keyboards that clack in minor keys</text>
  <rect x="90" y="470" width="120" height="5" fill="#FF2E88"/>
</svg>`;

const pngs = [
  ['favicon-16x16.png', 16], ['favicon-32x32.png', 32], ['apple-touch-icon.png', 180],
  ['android-chrome-192x192.png', 192], ['android-chrome-256x256.png', 256], ['mstile-150x150.png', 150],
];

(async () => {
  fs.writeFileSync(path.join(FAV, 'favicon.svg'), icon);
  fs.writeFileSync(path.join(ROOT, 'logo.svg'), icon);
  for (const [name, size] of pngs) await sharp(Buffer.from(icon)).resize(size, size).png().toFile(path.join(FAV, name));
  const bufs = [];
  for (const s of [16, 32, 48]) bufs.push(await sharp(Buffer.from(icon)).resize(s, s).png().toBuffer());
  const ico = await pngToIco(bufs);
  fs.writeFileSync(path.join(FAV, 'favicon.ico'), ico);
  fs.writeFileSync(path.join(ROOT, 'favicon.ico'), ico);
  await sharp(Buffer.from(og)).resize(1200, 630).png().toFile(path.join(ROOT, 'assets', 'images', 'og-default.png'));
  console.log('icons + og-default generated');
})().catch((e) => { console.error(e); process.exit(1); });
