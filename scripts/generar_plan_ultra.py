#!/usr/bin/env python3
"""Ciclo base-ultra -> primer 50K. Fuente unica de verdad (como generar_plan.py
para la maraton). 28 semanas: recuperacion, base+umbral, especifico de ultra
con fondos consecutivos (sabado+domingo), taper de 3 semanas, semana de carrera.

Uso:
    python3 scripts/generar_plan_ultra.py
    python3 scripts/generar_plan_ultra.py --carrera 2027-04-11
"""
import argparse, datetime as dt, json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIN_DEFECTO = dt.date(2027, 3, 28)   # domingo, semana 28 desde el 14 sep 2026

# (fase, km, largo_sab_min, desc_sab, largo_dom_min, desc_dom, calidad, foco)
BLOQUE = [
 ("F0", 8,  30,"Caminata + movilidad", 0,"Descanso","Ninguna","Reposo total. Análisis de pisada esta semana."),
 ("F0",14,  30,"Trote muy suave",     20,"Trote muy suave","Ninguna","Retorno gradual. Confirmar cero dolor de tibial."),
 ("F0",22,  40,"Trote suave",         30,"Trote suave","4x20\" rectas","Cero dolor antes de subir carga."),
 ("F0",28,  50,"Trote suave",         35,"Trote suave","Fartlek 4x2'","Decisión de calzado del ciclo. Empieza excéntrico de cuádriceps."),
 ("F1",38,  90,"Continuo",            45,"Trote muy suave · primer back-to-back corto","Umbral 3x6' / 2' trote","Primeras semanas de umbral real."),
 ("F1",42, 105,"Continuo",            50,"Trote suave","Umbral 4x6' / 2' trote","—"),
 ("F1",46, 120,"Continuo, últimos 15' firmes",55,"Trote suave","Cuestas 10x45\" fuerte / bajada trote","Fuerza específica sin impacto."),
 ("F1",34,  80,"Continuo",            40,"Trote suave","TEST: 10K contrarreloj","DESCARGA. Reindexar ritmos tras la maratón."),
 ("F1",48, 135,"Continuo",            60,"Trote suave","Umbral 3x8' / 2' trote","—"),
 ("F1",52, 150,"Continuo",            70,"Trote suave","Umbral 2x15' / 3' trote","—"),
 ("F1",56, 165,"Continuo",            75,"Trote suave","Cuestas 12x45\" + 2x10' umbral","Semana más dura de la base."),
 ("F1",40, 105,"Continuo",            50,"Trote suave","Umbral 3x6'","DESCARGA. Analítica de control. Fin de la base."),
 ("F2",55, 180,"Bloques a ritmo de ultra + power-hike en subida",90,"Con piernas cargadas","Umbral 4x8' / 2' trote","Empieza el back-to-back real. Nutrición sólida (arroz, papa, caldo) en el largo."),
 ("F2",60, 195,"Continuo, terreno irregular si hay",90,"Con piernas cargadas","Fartlek en terreno irregular","Practicar CAMINAR las subidas a propósito, no correrlas."),
 ("F2",45, 120,"Libre, sin estructura",60,"Libre","Ninguna estructurada","Semana de fiestas. Recuperación amortiguadora."),
 ("F2",58, 210,"Continuo + desnivel si hay acceso",105,"Con piernas cargadas","Umbral 3x10'","Retomar estructura."),
 ("F2",64, 240,"Con desnivel: alternar trote/power-hike",120,"Con piernas cargadas","Cuestas largas 8x2'","Primer fin de semana de 4h+."),
 ("F2",68, 255,"Continuo",            120,"Con piernas cargadas","Umbral 4x8' / 2' trote","Probar calzado y nutrición COMPLETOS de carrera."),
 ("F2",48, 120,"Continuo",            60,"Trote suave","Umbral 3x6'","DESCARGA."),
 ("F2",66, 270,"Continuo + desnivel", 135,"Con piernas cargadas","Fartlek largo","—"),
 ("F2",70, 300,"PICO: el fondo más largo del plan",150,"Con piernas cargadas","Umbral 3x10'","Semana de mayor carga. Ensayar TODO el equipo de carrera."),
 ("F2",60, 240,"Últimos 90' a ritmo de ultra",120,"Con piernas cargadas","Umbral 2x20' / 3' trote","Simulación de ritmo objetivo."),
 ("F2",44, 120,"Continuo",            60,"Trote suave","Umbral 3x6'","DESCARGA."),
 ("F2",56, 210,"Empieza a bajar hacia el taper",90,"Con piernas cargadas","Cuestas cortas 10x30\"","Fin del bloque específico."),
 ("F3",42, 120,"Con 30' a ritmo de carrera",60,"Trote suave","Umbral 3x6'","TAPER 1: -25% de volumen."),
 ("F3",30,  75,"Continuo suave",      45,"Trote muy suave","4x1000 m a ritmo 10K","TAPER 2: -45%. Cortar excéntricos de bajada."),
 ("F3",20,  45,"Con progresiones suaves",0,"Descanso","Activación 4x3' a ritmo objetivo","TAPER 3: -65%. Carga de carbohidratos los últimos 2 días."),
 ("RACE",50,0,"🏁 CARRERA: 50 km",   0,"Descanso","Activación suave el martes","Semana de carrera."),
]

def mmss(s): s=int(round(s)); return f"{s//60}:{s%60:02d}"
def hms(s):
    s=int(round(s))
    return f"{s//3600}:{(s%3600)//60:02d}:{s%60:02d}" if s>=3600 else f"{s//60}:{s%60:02d}"

def construir(fin):
    n = len(BLOQUE)
    ini = fin - dt.timedelta(days=6) - dt.timedelta(days=(n-1)*7)
    filas = []
    for i,(fase,km,sab_min,sab_d,dom_min,dom_d,cal,foco) in enumerate(BLOQUE):
        a = ini + dt.timedelta(days=i*7); b = a + dt.timedelta(days=6)
        filas.append(dict(semana=i+1, fase=fase, km=km,
            sab_min=sab_min, sab_desc=sab_d, dom_min=dom_min, dom_desc=dom_d,
            calidad=cal, foco=foco, inicio=a.isoformat(), fin=b.isoformat(),
            etiqueta=f"{a.day} {a.strftime('%b').lower()} - {b.day} {b.strftime('%b').lower()}",
            back_to_back = dom_min > 0 and fase in ("F1","F2")))
    return filas, ini

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--carrera", default=FIN_DEFECTO.isoformat(), help="fecha del 50K, YYYY-MM-DD")
    a = ap.parse_args()
    fin = dt.date.fromisoformat(a.carrera)
    if fin.weekday() != 6:
        print(f"AVISO: {fin} no es domingo ({fin.strftime('%A')}).")
    filas, ini = construir(fin)

    json.dump(dict(inicio=ini.isoformat(), carrera=fin.isoformat(), semanas=filas),
               open(os.path.join(BASE,"data","plan_ultra.json"),"w"), ensure_ascii=False, indent=1)

    print(f"{len(filas)} semanas · inicio {ini} · carrera (50K) {fin}")
    print(f"{'SEM':>3} {'FECHAS':<17} {'FA':<5} {'KM':>3} | {'SÁBADO':<38} | {'DOMINGO (back-to-back)':<28}")
    print("-"*130)
    for r in filas:
        sab = f"{r['sab_min']//60}h{r['sab_min']%60:02d}" if r['sab_min'] else "—"
        dom = f"{r['dom_min']//60}h{r['dom_min']%60:02d}" if r['dom_min'] else "—"
        print(f"{r['semana']:>3} {r['etiqueta']:<17} {r['fase']:<5} {r['km']:>3} | "
              f"{sab:<5} {r['sab_desc'][:31]:<31} | {dom:<5} {r['dom_desc'][:22]:<22}")
    tot = sum(r['km'] for r in filas)
    pico = max(filas, key=lambda r:r['km'])
    print(f"\nTotal {tot} km en {len(filas)} semanas · pico {pico['km']} km (semana {pico['semana']})")
    pico_t = max(filas, key=lambda r: r['sab_min']+r['dom_min'])
    print(f"Fin de semana más largo: semana {pico_t['semana']} · sábado {pico_t['sab_min']//60}h{pico_t['sab_min']%60:02d} + domingo {pico_t['dom_min']//60}h{pico_t['dom_min']%60:02d}")
