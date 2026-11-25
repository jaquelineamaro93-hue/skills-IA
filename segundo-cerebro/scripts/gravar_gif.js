// Grava os quadros da primeira tela do cérebro 3D girando (uma volta completa).
// Uso: node gravar_gif.js <pagina.html> <pasta_quadros>
// Depois: ffmpeg -framerate 16 -i <pasta_quadros>/f%03d.png -vf "scale=960:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=200[p];[b][p]paletteuse=dither=bayer:bayer_scale=4" -loop 0 cerebro.gif
const path = require('path');
const { chromium } = require('playwright');
(async () => {
  const [pagina, pasta] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 810 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(pagina));
  await page.waitForTimeout(1500);
  await page.evaluate(() => { velY = 0; });
  const N = 72;
  for (let i = 0; i < N; i++) {
    await page.evaluate(a => { rotY = 0.45 + a; }, i * 2 * Math.PI / N);
    await page.waitForTimeout(70);
    await page.screenshot({ path: path.join(pasta, 'f' + String(i).padStart(3, '0') + '.png'), clip: { x: 0, y: 0, width: 1440, height: 810 } });
  }
  await browser.close();
  console.log(N + ' quadros em ' + pasta);
})();
