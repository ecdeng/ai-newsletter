const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const shots = [
    ['index.html',       'landing',      1280, 900,  'light'],
    ['index.html',       'landing-dark', 1280, 900,  'dark'],
    ['exercises.html',   'catalogue',    1280, 1000, 'light'],
    ['modules/m13.html', 'module',       1280, 1000, 'light'],
    ['case-engine.html', 'case-engine',  1280, 900,  'light'],
    ['index.html',       'mobile',       390,  844,  'light'],
  ];
  const errors = [];
  for (const [path, name, w, h, scheme] of shots) {
    const ctx = await browser.newContext({
      viewport: { width: w, height: h },
      deviceScaleFactor: 2,
      colorScheme: scheme,
    });
    const page = await ctx.newPage();
    page.on('console', m => { if (m.type() === 'error') errors.push(`${name}: ${m.text()}`); });
    page.on('pageerror', e => errors.push(`${name}: PAGEERROR ${e.message}`));
    await page.goto(`http://localhost:8077/${path}`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(250);
    await page.screenshot({ path: `shots/${name}.png` });
    // measure horizontal overflow — the classic mobile bug
    const over = await page.evaluate(() =>
      document.documentElement.scrollWidth - document.documentElement.clientWidth);
    if (over > 2) errors.push(`${name}: horizontal overflow ${over}px`);
    await ctx.close();
  }
  // functional check: the filter actually filters
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 1000 } });
  const page = await ctx.newPage();
  await page.goto('http://localhost:8077/exercises.html', { waitUntil: 'networkidle' });
  const before = await page.locator('.exrow:not([hidden])').count();
  await page.selectOption('#f-build', 'Low');
  await page.waitForTimeout(150);
  const afterLow = await page.locator('.exrow:not([hidden])').count();
  await page.check('#f-flagship');
  await page.waitForTimeout(150);
  const afterFlag = await page.locator('.exrow:not([hidden])').count();
  await page.click('#f-reset');
  await page.waitForTimeout(150);
  const afterReset = await page.locator('.exrow:not([hidden])').count();
  console.log(`filter: all=${before}  build:Low=${afterLow}  +flagship=${afterFlag}  reset=${afterReset}`);
  if (!(before === 58 && afterLow < before && afterFlag <= afterLow && afterReset === 58))
    errors.push('filter behaviour unexpected');
  await ctx.close();
  await browser.close();
  console.log(errors.length ? 'ISSUES:\n' + errors.join('\n') : 'no console errors, no overflow');
})();
