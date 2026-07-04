#!/usr/bin/env node
// Recompress every photo/render under images/ to a web-sane size, in place.
// Filenames are unchanged so post links keep working. Idempotent-ish (only
// writes when it saves bytes).  npm install && npm run images
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..', 'images');
const CAP = 1600; // max long edge

function walk(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else out.push(p);
  }
  return out;
}

(async () => {
  const files = walk(ROOT).filter((f) => /\.(jpe?g|png)$/i.test(f));
  let before = 0, after = 0;
  for (const f of files) {
    const b0 = fs.statSync(f).size; before += b0;
    const isPng = /\.png$/i.test(f);
    const meta = await sharp(f).metadata();
    const long = Math.max(meta.width, meta.height);
    let img = sharp(f).rotate(); // bake EXIF orientation, then drop it
    if (long > CAP) {
      img = img.resize({
        width: meta.width >= meta.height ? CAP : null,
        height: meta.height > meta.width ? CAP : null,
        withoutEnlargement: true,
      });
    }
    const buf = isPng
      ? await img.png({ palette: true, quality: 85, effort: 8 }).toBuffer()
      : await img.jpeg({ quality: 80, mozjpeg: true }).toBuffer();
    if (buf.length < b0) fs.writeFileSync(f, buf);
    after += fs.statSync(f).size;
  }
  console.log(`images: ${(before / 1048576).toFixed(1)} MB -> ${(after / 1048576).toFixed(1)} MB (${(100 * (1 - after / before)).toFixed(0)}% smaller)`);
})().catch((e) => { console.error(e); process.exit(1); });
