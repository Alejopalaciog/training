/**
 * Genera el PDF del plan a partir del HTML, via Chromium headless.
 *   node scripts/generar_pdf.mjs [html] [pdf]
 * Requiere:  npm i playwright   (y un Chromium local)
 */
import { chromium } from 'playwright';
import { existsSync, readdirSync } from 'node:fs';
import path from 'node:path';

const BASE = path.resolve(import.meta.dirname, '..');
const SRC = process.argv[2] || path.join(BASE, 'plan-maraton.html');
const OUT = process.argv[3] || path.join(BASE, 'Plan-Maraton-26-Semanas.pdf');

// CSS solo para el PDF: tema claro fijo, tablas desplegadas, cortes de pagina limpios
const PRINT_CSS = `
:root{color-scheme:light}
nav{display:none!important}
body{padding:0!important;font-size:10.5px}
.wrap{max-width:100%!important}
section{break-before:page;page-break-before:always;margin-bottom:20px;padding-top:0}
header.mast{break-after:page;page-break-after:always;padding-top:6px}
.shead,h3,h4{break-after:avoid;page-break-after:avoid}
tr,li,.gloss>div,.grid3>div,.note,.decode,.chartbox,.facts{break-inside:avoid;page-break-inside:avoid}
.scroll{overflow:visible!important;border:1px solid #D3D9D2}
table{min-width:0!important;width:100%!important;font-size:8.3px;table-layout:auto}
.weeks,.pace{min-width:0!important}
th,td{padding:4px 6px!important}
thead{display:table-header-group}
thead th{position:static!important}
tfoot{display:table-footer-group}
.weeks .qty,.weeks .lng span{max-width:none;white-space:normal}
.grid2{gap:12px 20px}
.gloss{grid-template-columns:1fr 1fr!important}
a{text-decoration:none}
`;

function findChromium() {
  const d = '/opt/pw-browsers';
  if (!existsSync(d)) return undefined;
  const hit = readdirSync(d).find(n => n.startsWith('chromium-'));
  const p = hit && path.join(d, hit, 'chrome-linux', 'chrome');
  return p && existsSync(p) ? p : undefined;
}

const exe = findChromium();
const browser = await chromium.launch(exe ? { executablePath: exe } : {});
const page = await browser.newPage();
await page.emulateMedia({ media: 'screen', colorScheme: 'light' });
await page.goto('file://' + path.resolve(SRC), { waitUntil: 'networkidle' });
await page.addStyleTag({ content: PRINT_CSS });
await page.waitForTimeout(1500);
await page.pdf({
  path: OUT, format: 'A4', printBackground: true,
  margin: { top: '14mm', bottom: '14mm', left: '11mm', right: '11mm' },
  displayHeaderFooter: true,
  headerTemplate: '<div></div>',
  footerTemplate: '<div style="width:100%;font-size:7px;color:#8B9793;font-family:sans-serif;'
    + 'padding:0 11mm;display:flex;justify-content:space-between">'
    + '<span>Plan de maratón · 26 semanas · 7 sep 2026 → 7 mar 2027</span>'
    + '<span class="pageNumber"></span></div>',
});
await browser.close();
console.log('escrito', OUT);
