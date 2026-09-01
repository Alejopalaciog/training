#!/usr/bin/env python3
"""Semana de carrera: MARATON domingo 6 de septiembre de 2026, 5:00 AM,
Parque de las Luces (Medellin). El atleta vive en Guarne.

Peso 83 kg. Todo en GRAMOS (nada de tazas). Sin proteina en polvo, sin nueces.
Genera data/semana-carrera-nutricion.csv y data/semana-carrera.svg
"""
import csv, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PESO = 83

# alimento -> (gramos de referencia, CHO, PROT) por esa cantidad
F = {
 "arepa":        (100, 33, 4),   "arroz":   (100, 28, 3),   "platano": (100, 30, 1),
 "papa":         (100, 17, 2),   "yuca":    (100, 27, 1),   "pan":     (30,  15, 2),
 "arequipe":     (20,  12, 1),   "panela":  (20,  18, 0),   "bocadillo":(30, 22, 0),
 "banano":       (120, 27, 1),   "miel":    (20,  16, 0),   "avena":   (100, 60, 13),
 "pollo":        (100, 0,  31),  "pescado": (100, 0,  27),  "huevo":   (50,  0,  6),
 "cuajada":      (100, 3,  13),  "leche":   (250, 12, 8),   "yogur":   (100, 5,  9),
 "gel":          (1,   25, 0),   "bebida":  (1000,60, 0),   "datil":   (20,  15, 0),
}
def n(alim, gr):
    ref, c, p = F[alim]; k = gr/ref
    return c*k, p*k

# Cada comida: lista de (alimento, gramos). El texto se genera solo.
NOMBRE = {
 "arepa":"arepa de maíz","arroz":"arroz blanco cocido","platano":"plátano maduro cocido",
 "papa":"papa cocida pelada","yuca":"yuca cocida","pan":"pan blanco tajado",
 "arequipe":"arequipe","panela":"panela","bocadillo":"bocadillo veleño","banano":"banano",
 "miel":"miel","avena":"avena","pollo":"pechuga de pollo","pescado":"pescado (tilapia/salmón)",
 "huevo":"huevo","cuajada":"cuajada","leche":"leche","yogur":"yogur griego",
 "gel":"gel deportivo","bebida":"bebida deportiva","datil":"dátiles",
}
def txt(items, extra=""):
    partes = [f"{NOMBRE[a]} {g} g" for a,g in items]
    s = " + ".join(partes)
    if extra: s = (s+" + " if s else "") + extra
    c = sum(n(a,g)[0] for a,g in items); p = sum(n(a,g)[1] for a,g in items)
    return s, round(c), round(p)

def celda(items, extra="", nota=""):
    s,c,p = txt(items, extra)
    tail = f" · {c} g CHO" + (f", {p} g prot" if p >= 15 else "")
    return s + tail + (f" · {nota}" if nota else ""), c, p

DIAS = ["lunes 31 ago","martes 1 sep","miércoles 2 sep","jueves 3 sep","viernes 4 sep","sábado 5 sep","DOMINGO 6 sep"]

# ---------------------------------------------------------------- comidas
JUGO = "jugo verde (espinaca + manzana + pepino) con fibra en polvo"
JUGO_MED = "jugo verde SIN fibra en polvo (media porción de espinaca)"

comidas = {}
comidas["Al levantarse"] = [
 JUGO, JUGO, JUGO,
 JUGO + " · ÚLTIMA vez con dosis completa de fibra",
 JUGO_MED + " · ÚLTIMA fibra de la semana (solo en la mañana)",
 "Agua de panela tibia 300 ml · NADA de jugo verde, NADA de fibra en polvo",
 "Café solo (el de siempre) al despertar · 2:45 AM",
]
comidas["Desayuno"] = [
 celda([("huevo",150),("arepa",100),("platano",150)], "café", "día normal")[0],
 celda([("huevo",150),("arepa",100),("platano",150)], "café", "día normal")[0],
 celda([("avena",80),("banano",120),("miel",20),("leche",250)], "", "avena cocida o remojada de un día para otro")[0],
 celda([("arepa",200),("arequipe",40),("platano",200),("panela",20)], "café", "CARGA día 1")[0],
 celda([("arepa",200),("arequipe",40),("platano",250),("panela",30)], "café", "CARGA día 2")[0],
 celda([("arepa",200),("arequipe",40),("platano",200),("panela",20)], "café", "CARGA día 3 · sin fibra")[0],
 "3:00 AM (2 h antes) · " + celda([("pan",90),("arequipe",40),("platano",150),("panela",30)], "café solo", "SIN fibra, SIN grasa, SIN lácteos")[0],
]
comidas["Media mañana"] = [
 celda([("yogur",200),("banano",120)])[0],
 celda([("yogur",200),("banano",120)])[0],
 celda([("datil",60)], "café · pre-entreno de fuerza", "está bien, no lo cambies")[0],
 celda([("platano",150)], "café · pre-entreno de fuerza", "cambia los dátiles: tienen mucha fibra")[0],
 celda([("bocadillo",60),("pan",60),("arequipe",20)])[0],
 celda([("pan",120),("arequipe",40),("platano",150)], "", "sin corteza integral")[0],
 "3:30 AM salir de Guarne · 4:10 llegar · 4:45 AM: " + celda([("gel",1)], "sorbo de agua")[0],
]
comidas["Almuerzo"] = [
 celda([("pollo",150),("arroz",250),("papa",150)], "ensalada + ½ aguacate")[0],
 celda([("pollo",150),("arroz",250),("papa",150)], "ensalada + ½ aguacate")[0],
 celda([("pollo",180),("arroz",300),("platano",150)], "verduras cocidas (calabacín + zanahoria + habichuela)")[0],
 celda([("pollo",150),("arroz",400),("platano",150)], "calabacín cocido 100 g", "CARGA")[0],
 celda([("pollo",150),("arroz",450),("platano",200),("panela",30)], "calabacín cocido 100 g", "CARGA")[0],
 celda([("pollo",150),("arroz",450),("papa",200)], "", "CERO verduras · última comida grande del día")[0],
 "DURANTE LA CARRERA · 1 gel cada 35-40 min desde el minuto 20 (8-9 geles ≈ 210 g) + 200 ml de bebida deportiva en cada avituallamiento (≈ 100 g) = 45-55 g/h",
]
comidas["Media tarde"] = [
 celda([("banano",120)], "")[0],
 celda([("banano",120)], "")[0],
 celda([("bocadillo",60)], "")[0],
 celda([("bebida",600),("bocadillo",90)], "", "el agua de panela casera cuenta")[0],
 celda([("bebida",600),("bocadillo",90),("banano",120)])[0],
 celda([("bebida",700),("bocadillo",90),("pan",60)], "", "agua de panela con sal y limón")[0],
 "POST-CARRERA (primeros 60 min): 80-100 g CHO + 30 g proteína + 1 L de líquido con sal. Después, come lo que quieras.",
]
comidas["Cena"] = [
 celda([("pescado",180),("papa",250)], "verduras cocidas")[0],
 celda([("pescado",180),("papa",250)], "verduras cocidas")[0],
 celda([("pescado",180),("arroz",250)], "calabacín + zanahoria + ahuyama cocidos")[0],
 celda([("pescado",150),("arroz",350),("papa",200)], "calabacín cocido 100 g", "CARGA")[0],
 celda([("pescado",150),("arroz",400),("platano",150)], "", "CARGA · CERO verduras desde aquí")[0],
 "18:30 · CENA LIGERA Y TEMPRANA · " + celda([("pollo",120),("arroz",300),("platano",150)], "", "CERO fibra, CERO grasa, CERO frito")[0],
 "Libre. Come y bebe lo que te pida el cuerpo.",
]
comidas["Antes de dormir"] = [
 celda([("cuajada",200)], "", "la cuajada ES caseína")[0],
 celda([("cuajada",200)], "")[0],
 celda([("cuajada",200),("banano",120)])[0],
 celda([("cuajada",200),("banano",120),("leche",250)])[0],
 celda([("cuajada",200),("banano",120),("leche",250)])[0],
 "Agua de panela 300 ml (~30 g CHO) · nada más · acostarse a las 20:00",
 "—",
]
comidas["Entrenamiento"] = [
 "Trote suave 30 min + 4 rectas de 20 s",
 "Trote suave 25-30 min con 2×1 km a ritmo objetivo + 4 rectas",
 "GIMNASIO: solo tren superior, volumen a la mitad, cero fallo · trote 20 min muy suave",
 "GIMNASIO: NO VAYAS, o solo tren superior muy ligero · CERO pierna · trote 15-20 min muy suave",
 "DESCANSO TOTAL · caminata 15 min",
 "Trote 12-15 min MUY suave + 3 rectas · recoger dorsal · preparar todo",
 "🏁 MARATÓN · 5:00 AM · Parque de las Luces",
]
comidas["Hidratación"] = [
 "2,5-3 L de agua","2,5-3 L","2,5-3 L",
 "3-3,5 L · el glucógeno retiene agua: subir de peso es normal y es bueno",
 "3-3,5 L + 2 g de sal extra repartida en las comidas",
 "3 L + 2 g de sal extra · orina amarillo claro, NO transparente",
 "500 ml en las 2 h previas · durante: 400-600 ml/h · NUNCA ganes peso durante la carrera",
]
comidas["Suplementos"] = [
 "Creatina 5 g · Omega 3 · Magnesio 300-400 mg (noche)",
 "Creatina 5 g · Omega 3 · Magnesio","Creatina 5 g · Omega 3 · Magnesio",
 "Creatina 5 g · Omega 3 · Magnesio","Creatina 5 g · Omega 3 · Magnesio",
 "Creatina 5 g · Omega 3 · Magnesio · NADA nuevo",
 "Solo el café que tomas normalmente. NO experimentes con cafeína hoy.",
]
comidas["QUÉ EVITAR"] = [
 "Alcohol","Alcohol","Alcohol · empezar a bajar fibra",
 "Alcohol · frito · exceso de grasa (compite con los carbos) · nueces y frutos secos",
 "Alcohol · frito · legumbres · verduras crudas · brócoli, coliflor, repollo (gases)",
 "TODA la fibra: verduras, legumbres, integrales, cáscaras, semillas, el jugo verde. Nada frito, nada picante, NADA que no hayas comido antes.",
 "Huevo, lácteos, frito, fibra y cualquier alimento nuevo.",
]

# --------- objetivo de carbos por dia (calculado, no inventado) ----------
OBJ = ["~5 g/kg · normal","~5 g/kg · normal","~6 g/kg · bajando fibra",
       f"CARGA 8 g/kg ≈ {8*PESO} g", f"CARGA 9,5 g/kg ≈ {int(9.5*PESO)} g",
       f"CARGA 8,5 g/kg ≈ {int(8.5*PESO)} g", "Pre-carrera ~130 g + 45-55 g/h durante"]

FASE = ["Normal","Normal · activación","Normal · última fibra alta",
        "CARGA día 1","CARGA día 2 (el más alto)","CARGA día 3 + BAJO RESIDUO","🏁 MARATÓN 42,195 km"]

ORDEN = ["OBJETIVO DE CARBOHIDRATOS","Entrenamiento","Al levantarse","Desayuno",
         "Media mañana","Almuerzo","Media tarde","Cena","Antes de dormir",
         "Hidratación","Suplementos","QUÉ EVITAR"]
TABLA = {"FASE":FASE, "OBJETIVO DE CARBOHIDRATOS":OBJ, **comidas}

path = os.path.join(BASE,"data","semana-carrera-nutricion.csv")
with open(path,"w",newline="",encoding="utf-8-sig") as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    w.writerow(["Momento del día"]+DIAS)
    w.writerow(["FASE"]+FASE)                      # en el CSV sí conviene la fila explícita
    for k in ORDEN: w.writerow([k]+TABLA[k])
print("escrito", path)

# comprobacion de carbos por dia
print("\nCarbohidratos calculados por día:")
for i,d in enumerate(DIAS):
    tot = 0
    for k in ["Desayuno","Media mañana","Almuerzo","Media tarde","Cena","Antes de dormir"]:
        cel = TABLA[k][i]
        import re
        m = re.search(r"· (\d+) g CHO", cel)
        if m: tot += int(m.group(1))
    print(f"  {d:<16} {tot:>4} g CHO   (objetivo: {OBJ[i]})")

# =======================  SVG  =======================
import textwrap, html

COL_W, LAB_W, PAD = 268, 148, 9
FS, LH = 11.0, 13.6
HEAD_H, SUB_H = 62, 26
MARGIN_T, MARGIN_L = 96, 22
CPL = 45                     # caracteres por linea a FS=11 en COL_W

PAL = {  # (relleno de columna, color del titulo)
 0:("#F4F6F3","#5C6764"), 1:("#F4F6F3","#5C6764"), 2:("#F4F6F3","#5C6764"),
 3:("#FBF3EA","#A6521E"), 4:("#F8EADC","#A6521E"), 5:("#F5E2CE","#8A4318"),
 6:("#E4EFEE","#0E4F52"),
}
DESTACAR = {"FASE","OBJETIVO DE CARBOHIDRATOS","Entrenamiento","QUÉ EVITAR"}

def wrap(t, w=CPL):
    out = []
    for chunk in t.split(" · "):
        out += textwrap.wrap(chunk, w) or [""]
    return out

# alto de cada fila segun su contenido
alturas = []
for k in ORDEN:
    ln = max(len(wrap(c)) for c in TABLA[k])
    alturas.append(max(ln*LH + 2*PAD, 30))

W = MARGIN_L*2 + LAB_W + COL_W*7
H = MARGIN_T + HEAD_H + SUB_H + sum(alturas) + 54

s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}" font-family="Helvetica Neue, Helvetica, Arial, sans-serif">',
     f'<rect width="{W:.0f}" height="{H:.0f}" fill="#FBFCFA"/>',
     f'<text x="{MARGIN_L}" y="38" font-size="26" font-weight="700" fill="#131A17">Semana de carrera · Maratón Medellín</text>',
     f'<text x="{MARGIN_L}" y="60" font-size="13" fill="#5C6764">Domingo 6 de septiembre de 2026 · 5:00 AM · Parque de las Luces · 83 kg · sin proteína en polvo, sin frutos secos · todo en gramos</text>',
     f'<text x="{MARGIN_L}" y="78" font-size="12" fill="#A6521E" font-weight="600">Sin fase de vaciado. Carga de 3 días. La última fibra es el viernes por la mañana.</text>']

x0 = MARGIN_L + LAB_W
y_head = MARGIN_T
# fondos de columna
for i in range(7):
    fill,_ = PAL[i]
    s.append(f'<rect x="{x0+i*COL_W:.0f}" y="{y_head:.0f}" width="{COL_W}" height="{HEAD_H+SUB_H+sum(alturas):.0f}" fill="{fill}"/>')
# cabecera
for i,d in enumerate(DIAS):
    _,col = PAL[i]
    cx = x0 + i*COL_W + PAD
    s.append(f'<text x="{cx:.0f}" y="{y_head+22:.0f}" font-size="13.5" font-weight="700" fill="{col}">{html.escape(d)}</text>')
    for j,l in enumerate(wrap(FASE[i], 34)):
        s.append(f'<text x="{cx:.0f}" y="{y_head+40+j*13:.0f}" font-size="10.5" font-weight="600" fill="{col}" letter-spacing="0.4">{html.escape(l.upper())}</text>')
# subcabecera de objetivo
y = y_head + HEAD_H
s.append(f'<rect x="{MARGIN_L}" y="{y:.0f}" width="{W-2*MARGIN_L:.0f}" height="{SUB_H}" fill="#131A17"/>')
s.append(f'<text x="{MARGIN_L+PAD}" y="{y+17:.0f}" font-size="10" font-weight="700" fill="#FBFCFA" letter-spacing="0.6">CARBOHIDRATOS/DÍA</text>')
for i,o in enumerate(OBJ):
    s.append(f'<text x="{x0+i*COL_W+PAD:.0f}" y="{y+17:.0f}" font-size="11" font-weight="700" fill="#FBFCFA">{html.escape(o)}</text>')
y += SUB_H

# filas
for k,alto in zip(ORDEN, alturas):
    if k == "OBJETIVO DE CARBOHIDRATOS": continue
    fuerte = k in DESTACAR
    if fuerte:
        s.append(f'<rect x="{MARGIN_L}" y="{y:.0f}" width="{W-2*MARGIN_L:.0f}" height="{alto:.0f}" fill="#EDF0EC" opacity="0.75"/>')
    s.append(f'<line x1="{MARGIN_L}" y1="{y:.1f}" x2="{W-MARGIN_L}" y2="{y:.1f}" stroke="#D3D9D2" stroke-width="1"/>')
    s.append(f'<text x="{MARGIN_L+PAD}" y="{y+PAD+10:.1f}" font-size="11" font-weight="700" fill="#131A17">{html.escape(k)}</text>')
    for i,cel in enumerate(TABLA[k]):
        cx = x0 + i*COL_W + PAD
        peso = "600" if fuerte else "400"
        color = "#131A17" if fuerte else "#2C3835"
        for j,l in enumerate(wrap(cel)):
            s.append(f'<text x="{cx:.0f}" y="{y+PAD+10+j*LH:.1f}" font-size="{FS}" font-weight="{peso}" fill="{color}">{html.escape(l)}</text>')
    y += alto

# lineas verticales y borde
for i in range(8):
    s.append(f'<line x1="{x0+i*COL_W:.0f}" y1="{y_head:.0f}" x2="{x0+i*COL_W:.0f}" y2="{y:.0f}" stroke="#D3D9D2" stroke-width="1"/>')
s.append(f'<line x1="{MARGIN_L}" y1="{y:.1f}" x2="{W-MARGIN_L}" y2="{y:.1f}" stroke="#131A17" stroke-width="1.5"/>')
s.append(f'<rect x="{MARGIN_L}" y="{y_head:.0f}" width="{W-2*MARGIN_L:.0f}" height="{y-y_head:.0f}" fill="none" stroke="#D3D9D2"/>')
s.append(f'<text x="{MARGIN_L}" y="{y+26:.0f}" font-size="10.5" fill="#5C6764">Bebida deportiva casera (1 L): 1 L de agua + 65 g de panela o azúcar + 1,5 g de sal (¼ de cucharadita rasa) + el jugo de 1 limón. · Cuajada = caseína.</text>')
s.append(f'<text x="{MARGIN_L}" y="{y+42:.0f}" font-size="10.5" fill="#5C6764">Domingo: despertar 2:45 · desayuno 3:00 · salir de Guarne 3:30 · llegar 4:10 · gel 4:45 · salida 5:00. Nada nuevo. Sal 15 s/km más lento de lo que crees.</text>')
s.append('</svg>')

svg_path = os.path.join(BASE,"data","semana-carrera.svg")
open(svg_path,"w",encoding="utf-8").write("\n".join(s))
print("escrito", svg_path, f"({W:.0f}x{H:.0f} px)")
