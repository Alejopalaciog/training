#!/usr/bin/env python3
"""Semana de carrera: MARATON domingo 6 de septiembre de 2026, 5:00 AM,
Parque de las Luces (Medellin). El atleta vive en Guarne. 83 kg.

Restricciones reales del atleta:
  - sin proteina en polvo (le cae mal)   - sin leche (le cae mal)
  - sin frutos secos                     - jugo verde con fibra = su estimulo intestinal
Rutina real de la manana en dias de gimnasio:
  5:40 datiles + cafe -> 6:00 gimnasio -> 7:30 jugo verde -> 8:00 desayuno

Cada celda puede ser un texto (igual en los dos niveles) o una tupla
(PISO, OBJETIVO) para los dias de carga.
Genera: data/semana-carrera-nutricion.csv, data/semana-carrera.svg,
        data/plan-de-carrera.svg
"""
import csv, os, re, textwrap, html
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PESO = 83

F = {  # alimento -> (gramos de referencia, CHO, PROT)
 "arepa":(100,33,4), "arroz":(100,28,3), "platano":(100,30,1), "papa":(100,17,2),
 "yuca":(100,27,1),  "pan":(30,15,2),    "arequipe":(20,12,1), "panela":(20,18,0),
 "bocadillo":(30,22,0),"banano":(120,27,1),"miel":(20,16,0),   "avena":(100,60,13),
 "pollo":(100,0,31), "pescado":(100,0,27),"huevo":(50,0,6),    "cuajada":(100,3,13),
 "yogur":(100,5,9),  "gel":(1,25,0),     "aguapanela":(1000,90,0), "datil":(20,15,0),
}
NOMBRE = {
 "arepa":"arepa de maíz","arroz":"arroz blanco cocido","platano":"plátano maduro cocido",
 "papa":"papa cocida pelada","yuca":"yuca cocida","pan":"pan blanco tajado","arequipe":"arequipe",
 "panela":"panela","bocadillo":"bocadillo veleño","banano":"banano","miel":"miel","avena":"avena",
 "pollo":"pechuga de pollo","pescado":"pescado","huevo":"huevo","cuajada":"cuajada",
 "yogur":"yogur griego","gel":"gel","aguapanela":"agua de panela","datil":"dátiles",
}
def C(items, extra="", nota=""):
    """Construye el texto de una celda y le anexa sus carbohidratos calculados."""
    cho = sum(F[a][1]*g/F[a][0] for a,g in items)
    pro = sum(F[a][2]*g/F[a][0] for a,g in items)
    s = " + ".join(f"{NOMBRE[a]} {g:g} g" for a,g in items)
    if extra: s = (s + " + " if s else "") + extra
    s += f" · {round(cho)} g CHO" + (f", {round(pro)} g prot" if pro >= 10 else "")
    if nota: s += f" · {nota}"
    return s

DIAS = ["lunes 31 ago","martes 1 sep","miércoles 2 sep","jueves 3 sep","viernes 4 sep","sábado 5 sep","DOMINGO 6 sep"]
CARGA = (3,4,5)   # indices de los dias con dos niveles

FASE = ["Normal","Normal","Normal · última fibra alta",
        "CARGA día 1","CARGA día 2 (el más alto)","CARGA día 3 + BAJO RESIDUO","🏁 MARATÓN 42,195 km"]
OBJ = ["~5 g/kg · normal","~5 g/kg · normal","~6 g/kg ≈ 500 g",
       ("PISO 6 g/kg ≈ 500 g","META 8 g/kg ≈ 655 g"),
       ("PISO 7,5 g/kg ≈ 630 g","META 9,5 g/kg ≈ 790 g"),
       ("PISO 6,7 g/kg ≈ 555 g","META 8,6 g/kg ≈ 715 g"),
       "Pre-carrera ~130 g + 47 g/h durante"]

R = {}
R["Entrenamiento"] = [
 "Trote suave 30 min + 4 rectas de 20 s",
 "Trote 25-30 min con 2×1 km a ritmo objetivo + 4 rectas",
 "GIMNASIO 6 AM: solo tren superior, mitad de volumen, cero fallo · trote 20 min muy suave",
 "GIMNASIO 6 AM: mejor NO vayas. Si vas, solo tren superior muy ligero · CERO pierna · trote 15-20 min",
 "DESCANSO TOTAL · caminata 15 min",
 "Trote 12-15 min MUY suave + 3 rectas · recoger dorsal · dejar TODO preparado",
 "🏁 MARATÓN · 5:00 AM · Parque de las Luces",
]
R["Pre-entreno (5:40 AM)"] = [
 "—","—",
 C([("datil",60)], "café", "tu rutina de siempre: no la cambies"),
 (C([("platano",150)], "café"), C([("platano",200)], "café + 20 g de panela")) ,
 "—","—",
 "2:45 AM · café solo, el de siempre",
]
R["Jugo verde (7:30 AM)"] = [
 "jugo verde (espinaca + manzana + pepino) con fibra en polvo",
 "jugo verde con fibra en polvo",
 "jugo verde con fibra en polvo",
 "jugo verde con fibra en polvo · ÚLTIMA vez con dosis completa",
 "jugo verde SIN fibra en polvo, media porción de espinaca · ÚLTIMA fibra de la semana",
 "NADA de jugo verde ni de fibra · en su lugar, agua de panela tibia 300 ml",
 "—",
]
R["Desayuno (8:00 AM)"] = [
 C([("huevo",150),("arepa",100),("platano",150)], "café"),
 C([("huevo",150),("arepa",100),("platano",150)], "café"),
 C([("huevo",100),("arepa",100),("platano",200),("panela",20)], "café"),
 (C([("huevo",150),("arepa",100),("arequipe",20),("platano",200),("panela",20)], "café"),
  C([("huevo",150),("arepa",150),("arequipe",40),("platano",200),("panela",20)], "café")),
 (C([("huevo",150),("arepa",200),("arequipe",20),("platano",200),("panela",20)], "café"),
  C([("huevo",150),("arepa",200),("arequipe",40),("platano",200),("panela",20)], "café")),
 (C([("huevo",150),("arepa",100),("arequipe",40),("platano",200),("panela",20)], "café"),
  C([("huevo",150),("arepa",200),("arequipe",40),("platano",200)], "café")),
 "3:00 AM (2 h antes) · TU RUTINA: " + C([("pan",120),("arequipe",60)], "café solo + 400 ml de agua con sal, limón y 40 g de panela", "en total 132 g CHO · nada nuevo"),
]
R["Media mañana (10:30)"] = [
 C([("yogur",200),("banano",120)]),
 C([("yogur",200),("banano",120)]),
 C([("bocadillo",60),("banano",120)]),
 (C([("bocadillo",60)]), C([("bocadillo",60),("pan",60)])),
 (C([("bocadillo",60),("aguapanela",300)]), C([("bocadillo",120),("pan",60),("arequipe",20)])),
 (C([("bocadillo",60),("aguapanela",300)]), C([("pan",120),("arequipe",40),("platano",150)])),
 "3:30 AM salir de Guarne · 4:10 llegar · 4:45 AM: activación suave 5 min, ropa y vaselina · SIN gel todavía (el nº1 va a las 6:00, ya en carrera)",
]
R["Almuerzo (12:30)"] = [
 C([("pollo",150),("arroz",250),("papa",150)], "ensalada + ½ aguacate"),
 C([("pollo",150),("arroz",250),("papa",150)], "ensalada + ½ aguacate"),
 C([("pollo",180),("arroz",300),("platano",150)], "verduras cocidas: calabacín + zanahoria + habichuela"),
 (C([("pollo",100),("arroz",250),("platano",150)], "calabacín cocido 100 g"),
  C([("pollo",100),("arroz",350),("platano",100)], "calabacín cocido 100 g")),
 (C([("pollo",100),("arroz",300),("platano",200)], "calabacín cocido 100 g"),
  C([("pollo",100),("arroz",400),("platano",150)], "calabacín cocido 100 g")),
 (C([("pollo",150),("arroz",300),("papa",200)], "", "CERO verduras"),
  C([("pollo",150),("arroz",450),("papa",200)], "", "CERO verduras · última comida grande")),
]
R["Almuerzo (12:30)"].append(
 "DURANTE LA CARRERA · REGLA DEL RELOJ: en punto = 1 UP GEL · y media = 1 bocadillo de 30 g · MÁXIMO 6 GELES (tope de cafeína 360 mg) · ≈ 250 g ≈ 45 g/h")
R["Media tarde (16:00)"] = [
 C([("banano",120)]), C([("banano",120)]), C([("bocadillo",60)]),
 (C([("aguapanela",500)]), C([("aguapanela",600),("bocadillo",60)])),
 (C([("aguapanela",600),("bocadillo",60)]), C([("aguapanela",700),("bocadillo",90)])),
 (C([("aguapanela",500),("bocadillo",60)]), C([("aguapanela",700),("bocadillo",60)])),
 "POST-CARRERA (primeros 60 min): 80-100 g CHO + 30 g de proteína + 1 L de líquido con sal",
]
R["Cena (19:00)"] = [
 C([("pescado",180),("papa",250)], "verduras cocidas"),
 C([("pescado",180),("papa",250)], "verduras cocidas"),
 C([("pescado",180),("arroz",250)], "calabacín + zanahoria + ahuyama cocidos"),
 (C([("pescado",100),("arroz",250),("papa",150)], "calabacín 100 g"),
  C([("pescado",100),("arroz",300),("papa",150)], "calabacín 100 g")),
 (C([("pescado",100),("arroz",300),("platano",150)], "", "CERO verduras desde aquí"),
  C([("pescado",100),("arroz",400),("platano",200)], "", "CERO verduras desde aquí")),
 ("18:30 · " + C([("pollo",100),("arroz",250),("platano",150)], "", "CERO fibra, CERO grasa"),
  "18:30 · " + C([("pollo",100),("arroz",300),("platano",200)], "", "CERO fibra, CERO grasa")),
 "Libre. Come y bebe lo que te pida el cuerpo.",
]
R["Antes de dormir"] = [
 C([("cuajada",200)], "", "la cuajada ES caseína"),
 C([("cuajada",200)]),
 C([("cuajada",200),("banano",120)]),
 (C([("cuajada",200),("banano",120)]), C([("cuajada",200),("banano",120)])),
 (C([("cuajada",200),("banano",120)]), C([("cuajada",200),("banano",120)])),
 C([("aguapanela",300)], "", "nada más · a la cama a las 20:00"),
 "—",
]
R["Hidratación"] = [
 "2,5-3 L de agua","2,5-3 L","2,5-3 L",
 "3-3,5 L · el glucógeno retiene agua: subir de peso es normal y es bueno",
 "3-3,5 L · con tu suero hidratante en un par de tomas",
 "3 L · orina amarillo claro, NO transparente",
 "500 ml en las 2 h previas · durante: 400-600 ml/h de TU suero hidratante · lleva 2-3 sobres para rearmar en los avituallamientos",
]
R["Suplementos"] = [
 "Creatina 5 g · Omega 3 · Magnesio 300-400 mg (noche)","Creatina 5 g · Omega 3 · Magnesio",
 "Creatina 5 g · Omega 3 · Magnesio","Creatina 5 g · Omega 3 · Magnesio",
 "Creatina 5 g · Omega 3 · Magnesio","Creatina 5 g · Omega 3 · Magnesio · NADA nuevo",
 "TOPE DE CAFEÍNA: 6 UP GEL = 360 mg (4,3 mg/kg). Tu café de las 2:45 aparte. NO tomes un séptimo gel.",
]
R["QUÉ EVITAR"] = [
 "Alcohol","Alcohol","Alcohol · empezar a bajar fibra",
 "Alcohol · frito · exceso de grasa y proteína (ocupan el espacio de los carbos) · frutos secos",
 "Alcohol · frito · legumbres · verduras crudas · brócoli, coliflor, repollo (gases)",
 "TODA la fibra: verduras, legumbres, integrales, cáscaras, semillas, el jugo verde. Nada frito, nada picante, NADA nuevo.",
 "Huevo, lácteos, frito, fibra y cualquier alimento nuevo. Y NO pases de 6 geles.",
]

# Opciones para llegar al MISMO macro con otros alimentos (dias de carga).
# Muchas vienen del plan del nutricionista: son vehiculos de carbohidrato de
# muy bajo residuo, mejores que el arroz para un colon sensible.
OPC = {
 ("Desayuno (8:00 AM)",3): "o 100 g de crema de arroz con 2 cdas de miel + banano · o 3 tostadas con mermelada sin semillas",
 ("Desayuno (8:00 AM)",4): "o 100 g de crema de arroz con miel + banano + 250 ml de jugo de uva colado",
 ("Desayuno (8:00 AM)",5): "o 100 g de crema de arroz con miel + banano · o 4 tostadas con jalea + isotónica",
 ("Media mañana (10:30)",3): "o 5 galletas de arroz inflado con mermelada · o 500 ml de isotónica + 2 tostadas",
 ("Media mañana (10:30)",4): "o 80 g de cereal de arroz (Nestum) en agua con miel · o 4 tostadas con jalea + 500 ml de isotónica",
 ("Media mañana (10:30)",5): "o 4 tostadas con mermelada sin semillas + 500 ml de bebida deportiva",
 ("Almuerzo (12:30)",3): "el arroz vale igual como pasta blanca cocida (mismo peso) o puré de papa sin cáscara (×1,6 el peso)",
 ("Almuerzo (12:30)",4): "o 250 g de pasta blanca cocida + puré de papa · sazona SOLO con sal: nada de ajo, cebolla ni comino",
 ("Almuerzo (12:30)",5): "o 250 g de puré de papa + 1 gelatina · pollo desmechado al vapor, solo sal",
 ("Media tarde (16:00)",3): "o 500 ml de isotónica + 4 galletas María · o 80 g de cereal de arroz con miel",
 ("Media tarde (16:00)",4): "o batido de 80 g de cereal de arroz con miel + 500 ml de bebida deportiva",
 ("Media tarde (16:00)",5): "o 500 ml con electrolitos + 4 galletas de agua con miel",
 ("Cena (19:00)",3): "el arroz vale igual como 250 g de pasta blanca cocida o 400 g de puré de papa",
 ("Cena (19:00)",4): "o 250 g de pasta blanca con un chorrito de aceite de oliva + tilapia",
 ("Cena (19:00)",5): "o 250 g de puré de papa sin piel + tilapia al vapor + agua de panela colada",
 ("Antes de dormir",3): "o 250 ml de agua de panela + 2 tajadas de pan",
 ("Antes de dormir",4): "o 250 ml de bebida deportiva + 2 tajadas de pan con miel",
 ("Pre-entreno (5:40 AM)",3): "o 1 banano grande + café · o 2 tostadas con miel",
}
for (_f,_d),_t in OPC.items():
    _c = R[_f][_d]
    if isinstance(_c, tuple): R[_f][_d] = (_c[0], _c[1], _t)

ORDEN = ["Entrenamiento","Pre-entreno (5:40 AM)","Jugo verde (7:30 AM)","Desayuno (8:00 AM)",
         "Media mañana (10:30)","Almuerzo (12:30)","Media tarde (16:00)","Cena (19:00)",
         "Antes de dormir","Hidratación","Suplementos","QUÉ EVITAR"]
COMIDAS = ["Pre-entreno (5:40 AM)","Desayuno (8:00 AM)","Media mañana (10:30)",
           "Almuerzo (12:30)","Media tarde (16:00)","Cena (19:00)","Antes de dormir"]

def nivel(cel, i):   # 0 = piso, 1 = meta  (el 3er elemento, si existe, son opciones)
    return cel[i] if isinstance(cel, tuple) else cel

# ---------- comprobacion de totales ----------
print("Carbohidratos por día (calculados, no estimados):\n")
print(f"{'':<16} {'PISO':>7} {'META':>9}   |  proteína (meta 100-115 g)")
for d in range(7):
    tot = []
    for k in (0,1):
        t = 0
        for c in COMIDAS:
            m = re.search(r"· (\d+) g CHO", nivel(R[c][d], k))
            if m: t += int(m.group(1))
        tot.append(t)
    pro = []
    for k in (0,1):
        t = 0
        for c in COMIDAS:
            m = re.search(r"(\d+) g prot", nivel(R[c][d], k))
            if m: t += int(m.group(1))
        pro.append(t)
    print(f"{DIAS[d]:<16} {tot[0]:>5} g {tot[1]:>7} g   |  prot {pro[0]:>3}-{pro[1]:>3} g")

# ---------- CSV ----------
path = os.path.join(BASE,"data","semana-carrera-nutricion.csv")
with open(path,"w",newline="",encoding="utf-8-sig") as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    w.writerow(["Momento del día"]+DIAS)
    w.writerow(["FASE"]+FASE)
    w.writerow(["OBJETIVO DE CARBOHIDRATOS"]+[f"PISO: {o[0]} || OBJETIVO: {o[1]}" if isinstance(o,tuple) else o for o in OBJ])
    for k in ORDEN:
        fila = []
        for c in R[k]:
            if isinstance(c, tuple):
                t = f"PISO: {c[0]} || META: {c[1]}"
                if len(c) > 2: t += f" || O BIEN: {c[2]}"
            else: t = c
            fila.append(t)
        w.writerow([k]+fila)
print("\nescrito", path)

# ==========================  SVG de la semana  ==========================
COL_W, LAB_W, PAD = 296, 152, 9
FS, LH = 10.8, 13.2
HEAD_H, SUB_H = 66, 28
MARGIN_T, MARGIN_L = 106, 22
CPL = 50

PAL = {0:("#F4F6F3","#5C6764"),1:("#F4F6F3","#5C6764"),2:("#F4F6F3","#5C6764"),
       3:("#FBF3EA","#A6521E"),4:("#F8EADC","#A6521E"),5:("#F5E2CE","#8A4318"),
       6:("#E4EFEE","#0E4F52")}
DESTACAR = {"Entrenamiento","QUÉ EVITAR"}

def wrap(t, w=CPL):
    out=[]
    for ch in t.split(" · "):
        out += textwrap.wrap(ch, w) or [""]
    return out

def lineas(cel):
    """Lineas que ocupa una celda: cada nivel mas su separador, y las opciones si las hay."""
    if isinstance(cel, tuple):
        n = sum(len(wrap(x, CPL-5)) for x in cel[:2]) + 1
        if len(cel) > 2: n += len(wrap(cel[2], CPL-5)) + 0.6
        return n
    return len(wrap(cel))

alturas = [max(max(lineas(c) for c in R[k])*LH + 2*PAD, 30) for k in ORDEN]
W = MARGIN_L*2 + LAB_W + COL_W*7
FOOT = 250
H = MARGIN_T + HEAD_H + SUB_H + sum(alturas) + FOOT

s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}" font-family="Helvetica Neue, Helvetica, Arial, sans-serif">',
 f'<rect width="{W:.0f}" height="{H:.0f}" fill="#FBFCFA"/>',
 f'<text x="{MARGIN_L}" y="36" font-size="25" font-weight="700" fill="#131A17">Semana de carrera · Maratón Medellín</text>',
 f'<text x="{MARGIN_L}" y="58" font-size="12.5" fill="#5C6764">Domingo 6 de septiembre de 2026 · 5:00 AM · Parque de las Luces · 83 kg · sin leche, sin proteína en polvo, sin frutos secos · todo en gramos</text>',
 # leyenda de los dos niveles
 f'<rect x="{MARGIN_L}" y="70" width="60" height="17" fill="#5C6764"/>',
 f'<text x="{MARGIN_L+30}" y="82" font-size="10" font-weight="700" fill="#FBFCFA" text-anchor="middle" letter-spacing="0.7">PISO</text>',
 f'<text x="{MARGIN_L+68}" y="82" font-size="11.5" fill="#131A17">lo mínimo que debes cumplir — te da ~90 % del glucógeno</text>',
 f'<rect x="{MARGIN_L+400}" y="70" width="60" height="17" fill="#A6521E"/>',
 f'<text x="{MARGIN_L+430}" y="82" font-size="10" font-weight="700" fill="#FBFCFA" text-anchor="middle" letter-spacing="0.7">META</text>',
 f'<text x="{MARGIN_L+468}" y="82" font-size="11.5" fill="#131A17">el óptimo teórico — si el estómago te lo permite, sin forzar</text>']

x0 = MARGIN_L + LAB_W
yh = MARGIN_T
for i in range(7):
    s.append(f'<rect x="{x0+i*COL_W:.0f}" y="{yh:.0f}" width="{COL_W}" height="{HEAD_H+SUB_H+sum(alturas):.0f}" fill="{PAL[i][0]}"/>')
for i,d in enumerate(DIAS):
    col = PAL[i][1]; cx = x0+i*COL_W+PAD
    s.append(f'<text x="{cx:.0f}" y="{yh+22:.0f}" font-size="13.5" font-weight="700" fill="{col}">{html.escape(d)}</text>')
    for j,l in enumerate(wrap(FASE[i],36)):
        s.append(f'<text x="{cx:.0f}" y="{yh+40+j*13:.0f}" font-size="10" font-weight="600" fill="{col}" letter-spacing="0.4">{html.escape(l.upper())}</text>')
y = yh+HEAD_H
s.append(f'<rect x="{MARGIN_L}" y="{y:.0f}" width="{W-2*MARGIN_L:.0f}" height="{SUB_H}" fill="#131A17"/>')
s.append(f'<text x="{MARGIN_L+PAD}" y="{y+18:.0f}" font-size="10" font-weight="700" fill="#FBFCFA" letter-spacing="0.6">CARBOHIDRATOS/DÍA</text>')
for i,o in enumerate(OBJ):
    cx = x0+i*COL_W+PAD
    if isinstance(o,tuple):
        s.append(f'<text x="{cx:.0f}" y="{y+12:.0f}" font-size="10.5" font-weight="700" fill="#C8D2CE">{html.escape(o[0])}</text>')
        s.append(f'<text x="{cx:.0f}" y="{y+24:.0f}" font-size="10.5" font-weight="700" fill="#E8A87C">{html.escape(o[1])}</text>')
    else:
        s.append(f'<text x="{cx:.0f}" y="{y+18:.0f}" font-size="11" font-weight="700" fill="#FBFCFA">{html.escape(o)}</text>')
y += SUB_H

for k,alto in zip(ORDEN, alturas):
    fuerte = k in DESTACAR
    if fuerte: s.append(f'<rect x="{MARGIN_L}" y="{y:.0f}" width="{W-2*MARGIN_L:.0f}" height="{alto:.0f}" fill="#EDF0EC" opacity="0.7"/>')
    s.append(f'<line x1="{MARGIN_L}" y1="{y:.1f}" x2="{W-MARGIN_L}" y2="{y:.1f}" stroke="#D3D9D2"/>')
    s.append(f'<text x="{MARGIN_L+PAD}" y="{y+PAD+10:.1f}" font-size="10.8" font-weight="700" fill="#131A17">{html.escape(k)}</text>')
    for i,cel in enumerate(R[k]):
        cx = x0+i*COL_W+PAD; ty = y+PAD+10
        if isinstance(cel, tuple):
            filas = [("PISO",cel[0],"#5C6764","#3A4644"),("META",cel[1],"#A6521E","#8A4318")]
            if len(cel) > 2: filas.append(("O BIEN",cel[2],"#0E4F52","#12615F"))
            for lab,txt_,bg,fg in filas:
                w_ = 30 if lab != "O BIEN" else 40
                s.append(f'<rect x="{cx:.0f}" y="{ty-8:.1f}" width="{w_}" height="11" fill="{bg}"/>')
                s.append(f'<text x="{cx+w_/2:.0f}" y="{ty:.1f}" font-size="7.6" font-weight="700" fill="#FBFCFA" text-anchor="middle" letter-spacing="0.4">{lab}</text>')
                pesos = {"PISO":"400","META":"600","O BIEN":"400"}
                for j,l in enumerate(wrap(txt_, CPL-5)):
                    s.append(f'<text x="{cx+w_+5:.0f}" y="{ty+j*LH:.1f}" font-size="{FS if lab!="O BIEN" else FS-0.6}" fill="{fg}" font-weight="{pesos[lab]}" font-style="{"italic" if lab=="O BIEN" else "normal"}">{html.escape(l)}</text>')
                ty += len(wrap(txt_, CPL-5))*LH + LH*0.5
        else:
            for j,l in enumerate(wrap(cel)):
                s.append(f'<text x="{cx:.0f}" y="{ty+j*LH:.1f}" font-size="{FS}" fill="{"#131A17" if fuerte else "#2C3835"}" font-weight="{"600" if fuerte else "400"}">{html.escape(l)}</text>')
    y += alto

for i in range(8):
    s.append(f'<line x1="{x0+i*COL_W:.0f}" y1="{yh:.0f}" x2="{x0+i*COL_W:.0f}" y2="{y:.0f}" stroke="#D3D9D2"/>')
s.append(f'<line x1="{MARGIN_L}" y1="{y:.1f}" x2="{W-MARGIN_L}" y2="{y:.1f}" stroke="#131A17" stroke-width="1.5"/>')
s.append(f'<rect x="{MARGIN_L}" y="{yh:.0f}" width="{W-2*MARGIN_L:.0f}" height="{y-yh:.0f}" fill="none" stroke="#D3D9D2"/>')

# panel 1: banco de intercambios · cada modulo = 25 g de carbohidrato
y += 28
s.append(f'<text x="{MARGIN_L}" y="{y:.0f}" font-size="14" font-weight="700" fill="#131A17">Banco de intercambios · cada uno de estos = <tspan fill="#A6521E">25 g de carbohidrato</tspan></text>')
s.append(f'<text x="{MARGIN_L+560}" y="{y:.0f}" font-size="12" fill="#5C6764">Suma módulos hasta llegar al número de cada casilla. Da igual de dónde vengan.</text>')
y += 18
MOD = [("90 g","arroz blanco cocido"),("100 g","pasta blanca cocida"),("150 g","puré de papa"),
       ("85 g","plátano maduro cocido"),("50 g","pan blanco · 1,7 tajadas"),("31 g","crema de arroz en seco"),
       ("32 g","cereal de arroz · Nestum"),("35 g","bocadillo · 1 unidad"),
       ("42 g","arequipe · 2 cdas"),("31 g","miel · 1,5 cdas"),("130 g","banano · 1 grande"),("180 g","gelatina"),
       ("280 ml","agua de panela"),("420 ml","bebida deportiva"),("170 ml","jugo de uva colado"),("6","galletas María")]
cols, mw = 8, (W-2*MARGIN_L-7*6)/8
for i,(gr,nom) in enumerate(MOD):
    bx = MARGIN_L + (i%cols)*(mw+6); by = y + (i//cols)*46
    s.append(f'<rect x="{bx:.0f}" y="{by:.0f}" width="{mw:.0f}" height="40" fill="#F4F6F3" stroke="#D3D9D2"/>')
    s.append(f'<text x="{bx+9:.0f}" y="{by+18:.0f}" font-size="15" font-weight="700" fill="#0E4F52">{gr}</text>')
    s.append(f'<text x="{bx+9:.0f}" y="{by+32:.0f}" font-size="9.5" fill="#5C6764">{nom}</text>')
y += 2*46 + 16

# panel 2: por que el arroz es el peor vehiculo
s.append(f'<text x="{MARGIN_L}" y="{y:.0f}" font-size="14" font-weight="700" fill="#131A17">¿Mucho arroz? Los mismos 126 g de carbohidratos, en distintos formatos:</text>')
y += 18
EQUIV = [("arroz blanco cocido","450 g","#8A4318"),("plátano maduro cocido","420 g","#5C6764"),
         ("pan blanco tajado","250 g","#5C6764"),("arequipe","210 g","#0E4F52"),
         ("bocadillo veleño","175 g","#0E4F52"),("panela disuelta en agua","140 g","#0E4F52")]
bw = (W-2*MARGIN_L-5*8)/6
for i,(nom,gr,col) in enumerate(EQUIV):
    bx = MARGIN_L + i*(bw+8)
    s.append(f'<rect x="{bx:.0f}" y="{y:.0f}" width="{bw:.0f}" height="44" fill="#F4F6F3" stroke="#D3D9D2"/>')
    s.append(f'<text x="{bx+10:.0f}" y="{y+21:.0f}" font-size="17" font-weight="700" fill="{col}">{gr}</text>')
    s.append(f'<text x="{bx+10:.0f}" y="{y+36:.0f}" font-size="10" fill="#5C6764">{nom}</text>')
y += 62
s.append(f'<text x="{MARGIN_L}" y="{y:.0f}" font-size="11.5" fill="#5C6764">El arroz cocido es 72 % agua: te llena el estómago con puro volumen. Si no te cabe, cámbialo por líquido (agua de panela, jugo de uva colado, isotónica) o por dulces densos (bocadillo, arequipe, miel).</text>')
s.append(f'<text x="{MARGIN_L}" y="{y+18:.0f}" font-size="11.5" fill="#5C6764">Proteína en los días de carga: 1,2-1,4 g/kg (100-115 g), no más. La proteína y la grasa le quitan sitio a los carbohidratos. Sazona solo con sal: nada de ajo, cebolla ni comino.</text>')
s.append('</svg>')
open(os.path.join(BASE,"data","semana-carrera.svg"),"w",encoding="utf-8").write("\n".join(s))
print("escrito data/semana-carrera.svg", f"({W:.0f}x{H:.0f})")

# ====================  SVG: tarjeta de carrera  ====================
PLAN = [("5:00","salida","SALIDA · Parque de las Luces",0,0),
 ("5:30","boca","Bocadillo veleño 30 g",22,0),   ("6:00","gel","UP GEL nº1",18,60),
 ("6:30","boca","Bocadillo veleño 30 g",22,60),  ("7:00","gel","UP GEL nº2",18,120),
 ("7:30","boca","Bocadillo veleño 30 g",22,120), ("8:00","gel","UP GEL nº3",18,180),
 ("8:30","boca","Bocadillo 30 g + 2 dátiles",52,180),("9:00","gel","UP GEL nº4",18,240),
 ("9:30","boca","Bocadillo veleño 30 g",22,240), ("10:00","gel","UP GEL nº5",18,300),
 ("10:30","gel","UP GEL nº6 · EL ÚLTIMO",18,360),("~10:45","meta","META",0,360)]
RW, RH0, fh = 760, 192, 46
RH = RH0 + len(PLAN)*fh + 236
CC = {"gel":"#A6521E","boca":"#0E4F52","salida":"#131A17","meta":"#131A17"}
g = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {RW} {RH}" width="{RW}" height="{RH}" font-family="Helvetica Neue, Helvetica, Arial, sans-serif">',
 f'<rect width="{RW}" height="{RH}" fill="#FBFCFA"/><rect width="{RW}" height="104" fill="#131A17"/>',
 '<text x="28" y="42" font-size="24" font-weight="700" fill="#FBFCFA">Plan de carrera · domingo 6 sep</text>',
 '<text x="28" y="66" font-size="13" fill="#9FB0AC">Maratón Medellín · salida 5:00 AM · Parque de las Luces</text>',
 '<text x="28" y="88" font-size="13" font-weight="700" fill="#E0855A">REGLA DEL RELOJ: en punto = GEL · y media = BOCADILLO</text>',
 '<text x="28" y="132" font-size="12" font-weight="700" fill="#5C6764" letter-spacing="0.8">HORA</text>',
 '<text x="120" y="132" font-size="12" font-weight="700" fill="#5C6764" letter-spacing="0.8">QUÉ TOMAS</text>',
 f'<text x="{RW-150}" y="132" font-size="12" font-weight="700" fill="#5C6764" letter-spacing="0.8">CHO ACUM.</text>',
 f'<text x="{RW-42}" y="132" font-size="12" font-weight="700" fill="#5C6764" letter-spacing="0.8" text-anchor="end">CAF.</text>']
yy, ac = RH0-22, 0
for hora,tipo,que,cho,caf in PLAN:
    ac += cho; col = CC[tipo]
    if tipo in ("salida","meta"):
        g += [f'<rect x="20" y="{yy-24:.0f}" width="{RW-40}" height="{fh-8}" fill="#131A17"/>',
              f'<text x="34" y="{yy+2:.0f}" font-size="15" font-weight="700" fill="#FBFCFA">{hora}</text>',
              f'<text x="126" y="{yy+2:.0f}" font-size="15" font-weight="700" fill="#FBFCFA">{que}</text>']
    else:
        if tipo=="gel": g.append(f'<rect x="20" y="{yy-24:.0f}" width="{RW-40}" height="{fh-8}" fill="#FAF0E7"/>')
        g += [f'<line x1="20" y1="{yy-24:.0f}" x2="{RW-20}" y2="{yy-24:.0f}" stroke="#D3D9D2"/>',
              f'<rect x="20" y="{yy-24:.0f}" width="4" height="{fh-8}" fill="{col}"/>',
              f'<text x="36" y="{yy+2:.0f}" font-size="16" font-weight="700" fill="#131A17">{hora}</text>',
              f'<text x="126" y="{yy+2:.0f}" font-size="14" font-weight="600" fill="{col}">{que}</text>',
              f'<text x="{RW-150}" y="{yy+2:.0f}" font-size="13" fill="#5C6764">{ac} g</text>']
        if caf:
            g.append(f'<text x="{RW-42}" y="{yy+2:.0f}" font-size="13" font-weight="{"700" if caf>=300 else "400"}" fill="{"#A6521E" if caf>=300 else "#5C6764"}" text-anchor="end">{caf} mg</text>')
    yy += fh
yy += 6
for col,t in [("#A6521E","NUNCA un séptimo gel. 6 geles = 360 mg de cafeína = 4,3 mg/kg."),
  ("#A6521E","Es ya 50 % más de lo máximo que has probado (4 geles = 240 mg)."),
  ("#131A17","Termo con TU suero hidratante. Sorbos constantes, ~500 ml por hora."),
  ("#131A17","500 ml no cubren 6 h: lleva 2-3 sobres y rearma en los puestos."),
  ("#131A17","Los 248 g de sólidos van solos: el suero hidrata, no alimenta."),
  ("#131A17","Si te empalaga el dulce: enjuaga con agua sola y sigue. NO dejes de comer."),
  ("#0E4F52","km 0-10: 15-20 s/km MÁS LENTO de lo que te pida el cuerpo.")]:
    g.append(f'<text x="28" y="{yy:.0f}" font-size="13" font-weight="600" fill="{col}">{t}</text>'); yy += 23
g.append(f'<text x="28" y="{yy+14:.0f}" font-size="12" fill="#5C6764">Desayuno 3:00 AM · 120 g de pan + 60 g de arequipe + café + 400 ml de agua con sal, limón y 40 g de panela = 132 g CHO</text>')
g.append('</svg>')
open(os.path.join(BASE,"data","plan-de-carrera.svg"),"w",encoding="utf-8").write("\n".join(g))
print(f"escrito data/plan-de-carrera.svg · {ac} g de sólidos · 360 mg de cafeína")
