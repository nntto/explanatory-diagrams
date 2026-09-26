// 架空の管理画面を、テーマの前後で撮影する。
// node shoot.js <outdir>
// tpl-* は skill の見本 design-before-after に、status-* はケース design-token-change の
// input/screenshots/{before,after}/{orders,delivery-form}.png に使った。
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const out = process.argv[2] || 'shots';
fs.mkdirSync(out, { recursive: true });
const base = 'file://' + path.resolve(__dirname, 'app.html');

// [出力名, view, theme, 撮影範囲（セレクタか clip:x,y,幅,高さ）]
const SHOTS = [
  ['tpl-before-picker', 'picker', 'tpl-before', 'clip:0,0,330,430'],
  ['tpl-after-picker', 'picker', 'tpl-after', 'clip:0,0,330,430'],
  ['tpl-before-buttons', 'buttons', 'tpl-before', '#buttons'],
  ['tpl-after-buttons', 'buttons', 'tpl-after', '#buttons'],
  ['status-before-orders', 'orders', 'status-before', '#root'],
  ['status-after-orders', 'orders', 'status-after', '#root'],
  ['status-before-form', 'form', 'status-before', '#root'],
  ['status-after-form', 'form', 'status-after', '#root'],
];

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 2 });
  for (const [name, view, theme, sel] of SHOTS) {
    await page.goto(`${base}?view=${view}&theme=${theme}`);
    await page.waitForSelector('#root > *');
    await page.waitForTimeout(800);
    if (sel.startsWith('clip:')) {
      const [x, y, width, height] = sel.slice(5).split(',').map(Number);
      await page.screenshot({ path: path.join(out, name + '.png'), clip: { x, y, width, height } });
      console.log('shot', name);
      continue;
    }
    // 撮影範囲を中身に合わせる（#root は最も外側の子要素まで）
    const el = await page.$(sel);
    if (sel === '#root') {
      const box = await page.evaluate(() => {
        const r = document.getElementById('root');
        let right = 0, bottom = 0;
        r.querySelectorAll('*').forEach((n) => {
          const b = n.getBoundingClientRect();
          if (b.width && b.height) { right = Math.max(right, b.right); bottom = Math.max(bottom, b.bottom); }
        });
        return { x: 0, y: 0, width: Math.ceil(right + 24), height: Math.ceil(bottom + 24) };
      });
      await page.screenshot({ path: path.join(out, name + '.png'), clip: box });
    } else {
      await el.screenshot({ path: path.join(out, name + '.png') });
    }
    console.log('shot', name);
  }
  await browser.close();
})();
