#!/usr/bin/env python3
"""Fuente unica de verdad del plan de maraton.

Uso:
    python3 scripts/generar_plan.py                          # fecha por defecto (2027-03-07)
    python3 scripts/generar_plan.py --carrera 2027-05-16     # mueve la carrera; recalcula todo
    python3 scripts/generar_plan.py --carrera 2027-05-16 --extra base

--extra decide que hacer con las semanas sobrantes si hay mas de 26 disponibles:
    base   -> repite semanas de la Fase 1 (recomendado: mas base aerobica)
    espec  -> repite semanas de la Fase 2 (mas trabajo especifico)
Si hay menos de 26 semanas, avisa y recorta desde la Fase 1.

Emite data/plan.json, que consumen render_plan_md.py y build_artifact.py.
"""
import argparse, datetime as dt, json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIN_DEFECTO = dt.date(2027, 3, 7)

# (fase, km, largo_min, descripcion_largo, calidad, foco)
BLOQUE = [
 ("F0",28, 90,"Rodaje continuo suave, sin ritmo objetivo","TEST: 30 min contrarreloj (define tus zonas)","Calibracion. Cero intensidad fuera del test."),
 ("F0",32,105,"Continuo suave","6x20 s rectas (progresivas) al final de un rodaje","Cadencia: subir 5% respecto a tu media actual."),
 ("F0",36,120,"Continuo suave","Fartlek 6x2' comodo-fuerte / 2' suave","Primer estimulo. Nada de series en pista."),
 ("F0",27, 90,"Continuo suave","8x20 s rectas","DESCARGA. Reevaluar tibial posterior."),
 ("F1",38,120,"Continuo, ultimos 15' un poco mas firmes","Umbral 3x6' / 2' trote","Empieza practica de nutricion en carrera (30 g/h)."),
 ("F1",42,135,"Continuo","Umbral 4x6' / 2' trote","Nutricion 40 g/h. Medir tasa de sudoracion."),
 ("F1",46,150,"Continuo","Cuestas 10x45 s fuerte / bajada trote","Cuestas = fuerza sin impacto. Clave para tu tibial."),
 ("F1",35,105,"Continuo","TEST: 10 km contrarreloj o carrera","DESCARGA + control. Reindexar ritmos."),
 ("F1",46,135,"Ultimos 20' progresivos","Umbral 3x8' / 2' trote","Nutricion 50 g/h."),
 ("F1",50,150,"Continuo","Umbral 2x15' / 3' trote","Primer bloque largo de umbral."),
 ("F1",54,165,"Continuo","Cuestas 12x45 s + 2x10' umbral","Semana mas dura de la Fase 1."),
 ("F1",40,120,"Continuo","Umbral 3x6'","DESCARGA. Fin de la fase de perdida de grasa."),
 ("F2",52,150,"3x10' a ritmo maraton dentro del largo","Umbral 4x8' / 2' trote","Aparece el ritmo maraton (RM). Nutricion 60 g/h."),
 ("F2",60,165,"2x20' a RM (uno a mitad, otro al final)","VO2max 5x3' fuerte / 2' trote","Primer trabajo de VO2max del plan."),
 ("F2",45,127,"MEDIA MARATON DE CONTROL a tope","Solo activacion 3x1' el miercoles","Este resultado FIJA tu ritmo de maraton real."),
 ("F2",42,120,"Continuo suave, sin estructura","Fartlek libre 20' por sensacion","Semana amortiguadora: recuperacion del 21K."),
 ("F2",52,165,"3x12' a RM","Umbral 4x8'","Retomar estructura. Nutricion 70 g/h."),
 ("F2",58,180,"2x25' a RM","VO2max 6x3' / 2' trote","Empieza aclimatacion al calor (correr en Medellin)."),
 ("F2",62,195,"3x5 km a RM / 1 km trote","Umbral 2x20' / 3' trote","Sesion mas especifica del plan."),
 ("F2",48,120,"Continuo","Umbral 3x6'","DESCARGA antes del pico."),
 ("F2",64,195,"PICO: largo con ultimos 8 km a RM","Umbral 5x6'","Semana de mayor carga de todo el plan."),
 ("F2",56,165,"SIMULACION: 16 km a RM con nutricion completa","Umbral 3x8'","Ensayo general: ropa, zapatillas, geles, desayuno."),
 ("F3",46,135,"8 km finales a RM","Umbral 3x6'","TAPER 1: -28% volumen, intensidad intacta."),
 ("F3",36,105,"6 km a RM","VO2max 4x1000 m a ritmo 10 km","TAPER 2: -44%. Cortar pliometria."),
 ("F3",26, 75,"4 km a RM","3x1600 m a RM","TAPER 3: -60%. Empieza carga de carbos el jueves."),
 ("RACE",54,  0,"MARATON 42,195 km - domingo","2x2 km a RM el martes","Semana de carrera. 12 km faciles + la maraton."),
]
# indices repetibles si sobran semanas (semanas de construccion, nunca de descarga ni test)
REPETIBLES = {"base":[8,9,10], "espec":[16,17,18]}

# ---------- ritmos ----------
def mmss(s): s=int(round(s)); return f"{s//60}:{s%60:02d}"
def hms(s):
    s=int(round(s))
    return f"{s//3600}:{(s%3600)//60:02d}:{s%60:02d}" if s>=3600 else f"{s//60}:{s%60:02d}"
def riegel(t1,d1,d2): return t1*(d2/d1)**1.06
ALTITUD_GANANCIA = 0.030   # Rionegro 2.125 m -> Medellin 1.495 m

def zonas(t5k):
    p5 = t5k/5.0
    umbral = p5+17; rm = umbral+22
    return dict(regenerativo=rm+110, facil=rm+75, maraton=rm, umbral=umbral, intervalos=p5-6,
                pred_10k=riegel(t5k,5,10), pred_21k=riegel(t5k,5,21.0975), pred_42k=riegel(t5k,5,42.195))

TESTS = [("36:00",2160),("34:00",2040),("32:00",1920),("30:00",1800),("28:00",1680),("26:00",1560)]

# ---------- reparto diario ----------
# ritmo facil estimado: mejora de ~8:15/km (sem 1) a ~7:15/km (final)
def pace_facil(i, n): return 495 - (495-435)*(i/max(n-1,1))

def dias_de(km_tot, largo_min, i, n, fase, ldesc=""):
    pf = pace_facil(i,n)
    if "MEDIA MARATON" in ldesc: largo = 21.1          # la carrera de control ES la sesion larga
    elif largo_min:              largo = round(largo_min*60/pf*2)/2
    else:                        largo = 42.195
    resto = max(km_tot - largo, 0)
    if fase == "F0":  rep = dict(lun=.30, mie=.35, jue=.35, dom=0)
    elif fase=="RACE":rep = dict(lun=.40, mie=.35, jue=.25, dom=0)
    else:             rep = dict(lun=.26, mie=.30, jue=.27, dom=.17)
    d = {k: round(resto*v*2)/2 for k,v in rep.items()}
    d["sab"] = largo; d["pace_facil"] = mmss(pf)
    return d

def construir(fin, extra):
    ini_ideal = fin - dt.timedelta(days=6) - dt.timedelta(days=(len(BLOQUE)-1)*7)
    hoy = dt.date.today()
    disp = (fin - dt.timedelta(days=6) - hoy).days // 7 + 1
    plan = list(BLOQUE); aviso = None
    if disp > len(BLOQUE):
        sobran = disp - len(BLOQUE)
        idx = REPETIBLES[extra]
        for k in range(sobran):
            plan.insert(idx[-1]+1+k, BLOQUE[idx[k % len(idx)]])
        aviso = f"Hay {disp} semanas disponibles: se insertaron {sobran} semanas extra de {'base aerobica' if extra=='base' else 'trabajo especifico'}."
    elif disp < len(BLOQUE) and disp > 0:
        faltan = len(BLOQUE) - disp
        aviso = (f"AVISO: solo hay {disp} semanas hasta la carrera, el plan necesita {len(BLOQUE)}. "
                 f"Se recortaron {faltan} semanas de la Fase 1 (base). Con menos de 22 semanas el riesgo de lesion sube "
                 f"de forma significativa: considera mover la fecha.")
        for _ in range(faltan):
            for j,b in enumerate(plan):
                if b[0]=="F1" and j not in (7,):
                    plan.pop(j); break
    n = len(plan)
    ini = fin - dt.timedelta(days=6) - dt.timedelta(days=(n-1)*7)
    filas = []
    for i,(fase,km,largo,ldesc,cal,foco) in enumerate(plan):
        a = ini + dt.timedelta(days=i*7); b = a + dt.timedelta(days=6)
        filas.append(dict(semana=i+1, fase=fase, km=km, largo_min=largo, largo_desc=ldesc,
            calidad=cal, foco=foco, inicio=a.isoformat(), fin=b.isoformat(),
            etiqueta=f"{a.day} {a.strftime('%b').lower()} - {b.day} {b.strftime('%b').lower()}",
            dias=dias_de(km, largo, i, n, fase, ldesc)))
    return filas, aviso, ini

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--carrera", default=FIN_DEFECTO.isoformat(), help="fecha de la maraton, YYYY-MM-DD (debe ser domingo)")
    ap.add_argument("--extra", default="base", choices=["base","espec"])
    a = ap.parse_args()
    fin = dt.date.fromisoformat(a.carrera)
    if fin.weekday() != 6:
        print(f"AVISO: {fin} no es domingo ({fin.strftime('%A')}). El plan lo asume igual.")
    filas, aviso, ini = construir(fin, a.extra)

    ritmos = []
    for et,t in TESTS:
        z = zonas(t); m = z['pred_42k']*(1-ALTITUD_GANANCIA)
        ritmos.append(dict(test5k=et, regenerativo=mmss(z['regenerativo']), facil=mmss(z['facil']),
            maraton=mmss(z['maraton']), umbral=mmss(z['umbral']), intervalos=mmss(z['intervalos']),
            pred_10k=hms(z['pred_10k']), pred_21k=hms(z['pred_21k']),
            maraton_medellin=hms(m), maraton_medellin_pace=mmss(m/42.195)))

    json.dump(dict(inicio=ini.isoformat(), carrera=fin.isoformat(), semanas=filas,
                   ritmos=ritmos, altitud_ganancia=ALTITUD_GANANCIA, aviso=aviso),
              open(os.path.join(BASE,"data","plan.json"),"w"), ensure_ascii=False, indent=1)

    if aviso: print(aviso, "\n")
    print(f"{len(filas)} semanas · inicio {ini} · carrera {fin}")
    print(f"{'SEM':>3} {'FECHAS':<17} {'FA':<4} {'KM':>3} | {'LUN':>5} {'MIE':>5} {'JUE':>5} {'SAB':>6} {'DOM':>5} | CALIDAD")
    print("-"*112)
    for r in filas:
        d = r["dias"]
        print(f"{r['semana']:>3} {r['etiqueta']:<17} {r['fase']:<4} {r['km']:>3} | "
              f"{d['lun']:>5} {d['mie']:>5} {d['jue']:>5} {d['sab']:>6} {d['dom']:>5} | {r['calidad'][:44]}")
    print(f"\nTotal {sum(r['km'] for r in filas)} km · pico {max(r['km'] for r in filas)} km")
    print("\nTest 5k | Regen | Facil | R.MARATON | Umbral | Interv | 10K     | 21K     | MARATON MEDELLIN")
    print("-"*104)
    for r in ritmos:
        print(f"{r['test5k']:<7} | {r['regenerativo']:<5} | {r['facil']:<5} | {r['maraton']:<9} | {r['umbral']:<6} | "
              f"{r['intervalos']:<6} | {r['pred_10k']:<7} | {r['pred_21k']:<7} | {r['maraton_medellin']} ({r['maraton_medellin_pace']}/km)")
