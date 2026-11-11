#!/usr/bin/env node
/* =========================================================
   Promo-agent renderer for bang-motion pages (Playwright port of
   .claude/skills/bang-motion/scripts/snap.mjs + export-frames.mjs).

   Why a port:
     - the cloud container ships Playwright + Chromium, not puppeteer;
     - cdn.jsdelivr.net is not reachable from the container, so GSAP /
       Three.js requests are served from tools/node_modules instead
       (the HTML itself keeps the normal CDN URLs and still works when
       double-clicked on a laptop);
     - frames are piped straight into ffmpeg (no thousands of PNGs on disk);
     - the stage size comes from window.OPENER.W/H, so 1920x1080 (16:9)
       and 1080x1920 (9:16) pages render with the same script.

   Usage:
     node tools/render.mjs snap   <page.html> <outDir> <t1> [t2 ...] [--query ratio=9x16]
     node tools/render.mjs export <page.html> <out.mp4> [--fps 30] [--audio a.m4a] [--max 30] [--query ratio=16x9]

   The page must expose window.OPENER = { W, H, DURATION, ready, seek(t),
   [seekFrame(t)], [clipsReady()] } — every bang-motion starter does.
   ========================================================= */
import { createRequire } from 'node:module';
import { spawn } from 'node:child_process';
import { mkdir, readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

// The container's Playwright is installed globally (resolved through NODE_PATH),
// which ESM `import` ignores — require() honours it.
const { chromium } = createRequire(import.meta.url)('playwright');

const HERE = path.dirname(fileURLToPath(import.meta.url));
const NM = path.join(HERE, 'node_modules');

const [mode, page_, out, ...rest] = process.argv.slice(2);
if (!['snap', 'export'].includes(mode) || !page_ || !out) {
  console.log('usage:\n  node tools/render.mjs snap <page.html> <outDir> <t1> [t2 ...]\n  node tools/render.mjs export <page.html> <out.mp4> [--fps 30] [--audio file] [--max 30]');
  process.exit(1);
}
const opt = (name, def) => { const i = rest.indexOf(`--${name}`); return i >= 0 ? rest[i + 1] : def; };
const FPS = Number(opt('fps', 30));
const AUDIO = opt('audio', '');
const MAX = Number(opt('max', 30));
const QUERY = opt('query', '');   // e.g. ratio=9x16 — one page, two formats

if (process.env.RENDER_DEBUG) console.log('[render] start');
const pageUrl = pathToFileURL(path.resolve(page_)).href + '?clean=1' + (QUERY ? '&' + QUERY : '');

// --- CDN → local node_modules -------------------------------------------
// https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js  -> node_modules/gsap/dist/gsap.min.js
// https://cdn.jsdelivr.net/npm/three@0.161.0/build/...       -> node_modules/three/build/...
// https://unpkg.com/<pkg>@<ver>/<file>                       -> same mapping
function localFor(url) {
  const m = url.match(/^https:\/\/(?:cdn\.jsdelivr\.net\/npm|unpkg\.com)\/((?:@[^/]+\/)?[^@/]+)(?:@[^/]+)?\/(.+?)(?:\?.*)?$/);
  if (!m) return null;
  const file = path.join(NM, m[1], m[2]);
  return existsSync(file) ? file : null;
}
const MIME = { '.js': 'application/javascript', '.mjs': 'application/javascript', '.css': 'text/css', '.json': 'application/json', '.wasm': 'application/wasm' };

const proxy = process.env.HTTPS_PROXY || process.env.https_proxy;
const browser = await chromium.launch({
  args: ['--autoplay-policy=no-user-gesture-required', '--ignore-gpu-blocklist', '--enable-unsafe-swiftshader'],
  ...(proxy ? { proxy: { server: proxy } } : {}),
});
const ctx = await browser.newContext({ ignoreHTTPSErrors: true, viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
await ctx.route(/^https:\/\/(cdn\.jsdelivr\.net|unpkg\.com)\//, async (route) => {
  const file = localFor(route.request().url());
  if (!file) { console.warn('CDN miss (add the package to tools/package.json):', route.request().url()); return route.abort(); }
  await route.fulfill({ body: await readFile(file), contentType: MIME[path.extname(file)] || 'application/octet-stream', headers: { 'access-control-allow-origin': '*' } });
});
const page = await ctx.newPage();
page.on('pageerror', (e) => console.log('PAGEERROR', e.message));
page.on('console', (m) => { if (m.type() === 'error') console.log('CONSOLE', m.text()); });

const log = (...a) => process.env.RENDER_DEBUG && console.log('[render]', ...a);
log('goto', pageUrl);
await page.goto(pageUrl, { waitUntil: 'load', timeout: 120000 });
log('loaded');
await page.waitForFunction('window.OPENER && window.OPENER.ready && (!window.OPENER.clipsReady || window.OPENER.clipsReady())', null, { timeout: 120000 });
log('OPENER ready');
await page.evaluate(() => document.fonts.ready);
const { W, H, DURATION } = await page.evaluate(() => ({ W: window.OPENER.W || 1920, H: window.OPENER.H || 1080, DURATION: window.OPENER.DURATION || window.OPENER.tl.duration() }));
await page.setViewportSize({ width: W, height: H });
log('size', W, H, DURATION);
await page.evaluate(() => { window.OPENER.tl.pause(0); });   // braces: never return the timeline (Playwright would try to serialise it)
log('paused');

async function seek(t) {
  await page.evaluate(async (time) => {
    const O = window.OPENER;
    if (O.seekFrame) { await O.seekFrame(time); O.seek && O.seek(time); }
    else { (O.seek || O.tl.time.bind(O.tl))(time); }
    await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
    if (!O.seekFrame && O.seek) O.seek(time);
  }, t);
}

if (mode === 'snap') {
  await mkdir(out, { recursive: true });
  const times = rest.filter((v, i) => !v.startsWith('--') && !(i > 0 && rest[i - 1].startsWith('--')));
  for (const ts of times) {
    const t = Number(ts);
    await seek(t);
    await page.screenshot({ path: `${out}/t${t.toFixed(2).replace('.', '_')}.png`, clip: { x: 0, y: 0, width: W, height: H } });
    process.stdout.write(`${t} `);
  }
  console.log(`\nsnap done: ${W}x${H}, duration ${DURATION}s -> ${out}/`);
} else {
  if (DURATION > MAX + 0.01) { console.error(`Timeline is ${DURATION}s, limit is ${MAX}s. Shorten the page before exporting.`); await browser.close(); process.exit(2); }
  const total = Math.round(DURATION * FPS);
  await mkdir(path.dirname(path.resolve(out)), { recursive: true });
  const args = ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-'];
  if (AUDIO) args.push('-i', AUDIO, '-map', '0:v', '-map', '1:a', '-c:a', 'aac', '-b:a', '192k', '-af', `afade=t=out:st=${Math.max(0, DURATION - 0.8)}:d=0.8`, '-shortest');
  args.push('-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', String(FPS), '-movflags', '+faststart', out);
  const ff = spawn('ffmpeg', args, { stdio: ['pipe', 'inherit', 'inherit'] });
  const done = new Promise((res, rej) => ff.on('close', (c) => (c === 0 ? res() : rej(new Error('ffmpeg exit ' + c)))));
  console.log(`${total} frames @ ${FPS} fps, ${W}x${H}, ${DURATION}s -> ${out}`);
  for (let i = 0; i < total; i++) {
    await seek(i / FPS);
    const buf = await page.screenshot({ clip: { x: 0, y: 0, width: W, height: H }, type: 'png' });
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
    if (i % FPS === 0) process.stdout.write(`\r${i}/${total}`);
  }
  ff.stdin.end();
  await done;
  console.log(`\nexport done -> ${out}`);
}
await browser.close();
