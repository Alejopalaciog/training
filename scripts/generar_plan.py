#!/usr/bin/env python3
"""Genera el calendario de 26 semanas y las tablas de ritmos del plan de maraton.

Fuente unica de verdad: si cambias algo aqui, re-ejecuta y se regeneran
docs/01-plan-26-semanas.md y data/plan.json.
"""
import datetime as dt, json, os

INICIO = dt.date(2026, 9, 7)          # lunes semana 1
CARRERA = dt.date(2027, 3, 7)         # domingo semana 26
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (n, fase, km, largo_min, descripcion_largo, calidad, foco)
SEMANAS = [
 (1,"F0",28, 90,"Rodaje continuo suave, sin ritmo objetivo","TEST: 30 min contrarreloj (define tus zonas)","Calibracion. Cero intensidad fuera del test."),
 (2,"F0",32,105,"Continuo suave","6x20 s rectas (progresivas) al final de un rodaje","Cadencia: subir 5% respecto a tu media actual."),
 (3,"F0",36,120,"Continuo suave","Fartlek 6x2' comodo-fuerte / 2' suave","Primer estimulo. Nada de series en pista."),
 (4,"F0",27, 90,"Continuo suave","8x20 s rectas","DESCARGA. Reevaluar tibial posterior."),
 (5,"F1",38,120,"Continuo, ultimos 15' un poco mas firmes","Umbral 3x6' / 2' trote","Empieza practica de nutricion en carrera (30 g/h)."),
 (6,"F1",42,135,"Continuo","Umbral 4x6' / 2' trote","Nutricion 40 g/h. Medir tasa de sudoracion."),
 (7,"F1",46,150,"Continuo","Cuestas 10x45 s fuerte / bajada trote","Cuestas = fuerza sin impacto. Clave para tu tibial."),
 (8,"F1",35,105,"Continuo","TEST: 10 km contrarreloj o carrera","DESCARGA + control. Reindexar ritmos."),
 (9,"F1",46,135,"Ultimos 20' progresivos","Umbral 3x8' / 2' trote","Nutricion 50 g/h."),
 (10,"F1",50,150,"Continuo","Umbral 2x15' / 3' trote","Primer bloque largo de umbral."),
 (11,"F1",54,165,"Continuo","Cuestas 12x45 s + 2x10' umbral","Semana mas dura de la Fase 1."),
 (12,"F1",40,120,"Continuo","Umbral 3x6'","DESCARGA. Fin de la fase de perdida de grasa."),
 (13,"F2",52,150,"3x10' a ritmo maraton dentro del largo","Umbral 4x8' / 2' trote","Aparece el ritmo maraton (RM). Nutricion 60 g/h."),
 (14,"F2",60,165,"2x20' a RM (uno a mitad, otro al final)","VO2 5x3' fuerte / 2' trote","Semana pico del bloque."),
 (15,"F2",45,127,"MEDIA MARATON DE CONTROL (dom 20 dic) a tope","Solo activacion 3x1' el miercoles","Este resultado FIJA tu ritmo de maraton real."),
 (16,"F2",42,120,"Continuo suave, sin estructura","Fartlek libre 20' por sensacion","Fiestas. Recuperacion del 21K. Volumen flexible."),
 (17,"F2",52,165,"3x12' a RM","Umbral 4x8'","Retomar estructura. Nutricion 70 g/h."),
 (18,"F2",58,180,"2x25' a RM","VO2 6x3' / 2' trote","Empieza aclimatacion al calor (correr en Medellin)."),
 (19,"F2",62,195,"3x5 km a RM / 1 km trote","Umbral 2x20' / 3' trote","Sesion mas especifica del plan."),
 (20,"F2",48,120,"Continuo","Umbral 3x6'","DESCARGA antes del pico."),
 (21,"F2",64,195,"PICO: largo con ultimos 8 km a RM","Umbral 5x6'","Semana de mayor carga de todo el plan."),
 (22,"F2",56,165,"SIMULACION: 16 km a RM con nutricion completa","Umbral 3x8'","Ensayo general: ropa, zapatillas, geles, desayuno."),
 (23,"F3",46,135,"8 km finales a RM","Umbral 3x6'","TAPER 1: -28% volumen, intensidad intacta."),
 (24,"F3",36,105,"6 km a RM","4x1000 m a ritmo 10 km","TAPER 2: -44%. Cortar pliometria."),
 (25,"F3",26, 75,"4 km a RM","3x1600 m a RM","TAPER 3: -60%. Empieza carga de carbohidratos jueves."),
 (26,"RACE",54, 0,"MARATON 42.195 km - domingo 7 de marzo","2x2 km a RM el martes","Semana de carrera. 12 km faciles + la maraton."),
]

def mmss(seg):
    seg = int(round(seg)); return f"{seg//60}:{seg%60:02d}"

def riegel(t1, d1, d2):
    return t1 * (d2 / d1) ** 1.06

def zonas(t5k_seg):
    """Deriva zonas de ritmo (s/km) desde un 5000 m a tope, en ALTITUD (Rionegro ~2.125 m)."""
    p5 = t5k_seg / 5.0
    umbral = p5 + 17
    rm     = umbral + 22          # ritmo maraton para un corredor de 4h+
    facil  = rm + 75
    regen  = rm + 110
    inter  = p5 - 6
    return dict(regenerativo=regen, facil=facil, maraton=rm, umbral=umbral, intervalos=inter,
                pred_10k=riegel(t5k_seg,5,10), pred_21k=riegel(t5k_seg,5,21.0975),
                pred_42k=riegel(t5k_seg,5,42.195))

# Conversion altitud: entrena a 2.125 m (Rionegro/Guarne), compite a 1.495 m (Medellin).
# ~1.5-2% de mejora aerobica por cada 300 m de descenso -> 630 m ~= 3%.
ALTITUD_GANANCIA = 0.030

filas = []
for n, fase, km, largo, desc_largo, calidad, foco in SEMANAS:
    ini = INICIO + dt.timedelta(days=(n-1)*7)
    fin = ini + dt.timedelta(days=6)
    filas.append(dict(semana=n, fase=fase, km=km, largo_min=largo, largo_desc=desc_largo,
                      calidad=calidad, foco=foco,
                      inicio=ini.isoformat(), fin=fin.isoformat(),
                      etiqueta=f"{ini.day} {ini.strftime('%b').lower()} - {fin.day} {fin.strftime('%b').lower()}"))

tests = [("32:00",1920),("30:00",1800),("28:00",1680),("26:00",1560),("24:00",1440)]
tabla_ritmos = []
for etiqueta, t in tests:
    z = zonas(t)
    tabla_ritmos.append(dict(test5k=etiqueta, **{k:(mmss(v) if k.startswith(('regen','facil','marat','umbral','inter')) else v) for k,v in z.items()}))

out = dict(inicio=INICIO.isoformat(), carrera=CARRERA.isoformat(),
           semanas=filas, ritmos=tabla_ritmos, altitud_ganancia=ALTITUD_GANANCIA)
with open(os.path.join(BASE,"data","plan.json"),"w") as f:
    json.dump(out,f,ensure_ascii=False,indent=1)

# ---- salida legible ----
print("SEM | FECHAS            | FASE | KM | LARGO      | SESION DE CALIDAD")
print("-"*110)
for r in filas:
    h = f"{r['largo_min']//60}h{r['largo_min']%60:02d}" if r['largo_min'] else "CARRERA"
    print(f"{r['semana']:>3} | {r['etiqueta']:<17} | {r['fase']:<4} | {r['km']:>2} | {h:<10} | {r['calidad']}")
print(f"\nVolumen total del plan: {sum(r['km'] for r in filas)} km en 26 semanas")
print(f"Pico semanal: {max(r['km'] for r in filas)} km (semana {max(filas,key=lambda r:r['km'])['semana']})")

print("\n\nTABLA DE RITMOS (s/km) SEGUN TU TEST DE 5 km EN ALTITUD")
print("Test 5k | Regen | Facil | R.MARATON | Umbral | Interv | Pred 10k | Pred 21k | Pred 42k(alt) | Pred 42k(Medellin)")
print("-"*125)
for etiqueta,t in tests:
    z = zonas(t)
    m_alt = z['pred_42k']; m_med = m_alt*(1-ALTITUD_GANANCIA)
    def hms(s):
        s=int(s)
        return f"{s//3600}:{(s%3600)//60:02d}:{s%60:02d}" if s>=3600 else f"{s//60}:{s%60:02d}"
    print(f"{etiqueta:<7} | {mmss(z['regenerativo']):<5} | {mmss(z['facil']):<5} | {mmss(z['maraton']):<9} | "
          f"{mmss(z['umbral']):<6} | {mmss(z['intervalos']):<6} | {hms(z['pred_10k']):<8} | {hms(z['pred_21k']):<8} | "
          f"{hms(m_alt):<13} | {hms(m_med)} ({mmss(m_med/42.195)}/km)")
