#!/usr/bin/env python3
"""Construye la pagina HTML del plan a partir de data/plan.json."""
import json, os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(BASE,"data","plan.json")))
S = D["semanas"]

FASE_META = {
 "F0": ("Reconstrucción", "z0", "Arreglar el tejido antes de pedirle velocidad. Cero series duras."),
 "F1": ("Base y umbral", "z1", "El bloque que más marca te baja. Entra el trabajo de umbral."),
 "F2": ("Específico", "z2", "Ritmo maratón, nutrición ensayada, calor de Medellín."),
 "F3": ("Taper", "z3", "Menos volumen, misma intensidad."),
 "RACE": ("Carrera", "z4", "Carga de carbohidratos y correr."),
}
HITOS = {1:"Test 30′", 8:"Test 10K", 15:"21K control", 21:"Pico", 22:"Simulación", 26:"MARATÓN"}

# ---------------- grafico de carga ----------------
W,H = 720,266
ML,MR,MT,MB = 38,10,26,34
PW = W-ML-MR
BW, GAP = 22.0, 4.0
YMAX = 70
def bx(i): return ML + i*(BW+GAP)
def by(km): return (H-MB) - km/YMAX*((H-MB)-MT)

svg = [f'<svg viewBox="0 0 {W} {H}" class="chart" role="img" aria-label="Volumen semanal de carrera a lo largo de las 26 semanas, con pico de 64 kilometros en la semana 21">']
# bandas de fase
fase_runs, cur = [], None
for i,s in enumerate(S):
    if s["fase"] != cur:
        cur = s["fase"]; fase_runs.append([cur,i,i])
    else: fase_runs[-1][2] = i
for f,a,b in fase_runs:
    x0 = bx(a)-GAP/2; x1 = bx(b)+BW+GAP/2
    svg.append(f'<rect class="band {FASE_META[f][1]}" x="{x0:.1f}" y="{MT}" width="{x1-x0:.1f}" height="{H-MB-MT}"/>')
    svg.append(f'<text class="bandlab" x="{(x0+x1)/2:.1f}" y="{MT-9}">{FASE_META[f][0]}</text>')
# grid
for g in (0,20,40,60):
    y = by(g)
    svg.append(f'<line class="grid" x1="{ML}" y1="{y:.1f}" x2="{W-MR}" y2="{y:.1f}"/>')
    svg.append(f'<text class="ytick" x="{ML-7}" y="{y+3.5:.1f}">{g}</text>')
# barras
for i,s in enumerate(S):
    km, y = s["km"], by(s["km"])
    cls = "bar race" if s["fase"]=="RACE" else ("bar hito" if s["semana"] in (21,22) else "bar")
    svg.append(f'<rect class="{cls}" x="{bx(i):.1f}" y="{y:.1f}" width="{BW}" height="{(H-MB)-y:.1f}" rx="1.5"><title>Semana {s["semana"]}: {km} km</title></rect>')
    if s["semana"] in HITOS:
        svg.append(f'<circle class="dot" cx="{bx(i)+BW/2:.1f}" cy="{y-7:.1f}" r="2.6"/>')
    if s["semana"] in (1,5,10,15,20,26):
        svg.append(f'<text class="xtick" x="{bx(i)+BW/2:.1f}" y="{H-MB+15}">{s["semana"]}</text>')
svg.append(f'<text class="xlab" x="{ML}" y="{H-6}">semana</text>')
svg.append(f'<text class="ylab" x="{ML-7}" y="{MT-9}">km</text>')
svg.append('</svg>')
SVG = "\n".join(svg)

# ---------------- filas de semanas ----------------
rows, cur = [], None
for s in S:
    if s["fase"] != cur:
        cur = s["fase"]; n,c,desc = FASE_META[cur]
        rows.append(f'<tr class="phasehead {c}"><th colspan="5"><span class="pname">{n}</span><span class="pdesc">{desc}</span></th></tr>')
    m = s["largo_min"]
    largo = f'{m//60}h{m%60:02d}' if m and m%60 else (f'{m//60}h' if m else '42,195 km')
    hito = f'<span class="pill">{HITOS[s["semana"]]}</span>' if s["semana"] in HITOS else ''
    rows.append(
      f'<tr class="{FASE_META[s["fase"]][1]}">'
      f'<td class="wk"><b>{s["semana"]}</b><span>{s["etiqueta"]}</span></td>'
      f'<td class="km"><b>{s["km"]}</b></td>'
      f'<td class="lng"><b>{largo}</b><span>{s["largo_desc"]}</span></td>'
      f'<td class="qty">{s["calidad"]}</td>'
      f'<td class="fcs">{hito}{s["foco"]}</td></tr>')
ROWS = "\n".join(rows)
open("/tmp/claude-0/-home-user-training/a7cf7ce3-b7b3-56e7-b793-4b98c8a437f5/scratchpad/_frag.json","w").write(json.dumps({"svg":SVG,"rows":ROWS}))
print("svg:", len(SVG), "chars · rows:", len(ROWS), "chars")
