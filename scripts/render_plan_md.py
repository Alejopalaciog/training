#!/usr/bin/env python3
"""Renderiza docs/01-plan-26-semanas.md a partir de data/plan.json."""
import json, os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(BASE, "data", "plan.json")))

FASES = {
 "F0": ("Fase 0 · Reconstrucción y calibración", "Semanas 1-4",
   "Arreglar el tejido antes de pedirle velocidad. Cero series duras. Aquí se define tu línea base real y se instala la disciplina del ritmo fácil. Si sales de esta fase sin molestias, el resto del plan funciona."),
 "F1": ("Fase 1 · Base aeróbica y umbral", "Semanas 5-12",
   "El bloque que más marca te va a bajar. Entra el trabajo de umbral, que es exactamente lo que te falta. El volumen sube de 38 a 54 km. Aquí también se completa la bajada a ~78 kg."),
 "F2": ("Fase 2 · Específico de maratón", "Semanas 13-22",
   "Todo se vuelve específico: rodajes largos con bloques a ritmo de maratón, nutrición en carrera ensayada, aclimatación al calor de Medellín. El 21K de control de la semana 15 fija tu ritmo objetivo definitivo. **Se acaba el déficit calórico.**"),
 "F3": ("Fase 3 · Afinamiento (taper)", "Semanas 23-25",
   "Se recorta el volumen 30-60% pero **se mantiene la intensidad**. Es el error clásico: la gente deja de correr rápido y llega plana. Vas a correr menos, no más suave."),
 "RACE": ("Semana de carrera", "Semana 26", "Carga de carbohidratos, logística, y correr."),
}
ORDEN = ["F0","F1","F2","F3","RACE"]

L = []
w = L.append
w("# 01 · El plan, semana a semana\n")
w(f"**Inicio:** lunes 7 de septiembre de 2026 · **Maratón:** domingo 7 de marzo de 2027 · **26 semanas**\n")
w(f"**Volumen total:** {sum(s['km'] for s in d['semanas'])} km · **Pico semanal:** {max(s['km'] for s in d['semanas'])} km (semana 21)\n")
w("""
## Cómo leer este plan

- **Cada fila te dice exactamente qué corres cada día.** Los kilómetros de lunes, jueves y domingo son rodajes fáciles: sales, corres esa distancia en zona 2 y ya. El miércoles es la única sesión dura de la semana. El viernes no se corre.
- **¿No entiendes un término?** Umbral, RM, rectas, fartlek, cuestas, VO2max: todo está explicado en el [documento 07 · Glosario](07-glosario.md).
- **Los rodajes largos están en TIEMPO, no en distancia.** Es deliberado. Pasar de 3 h 15 min corriendo tiene un coste de recuperación y un riesgo de lesión que no compensa el beneficio adicional, y a 83 kg eso te aplica el doble. La distancia entre paréntesis es la estimación a tu ritmo previsto; si vas más lento, corres menos km — y está bien.
- **Los km semanales son un objetivo, no un contrato.** ±10% es cumplimiento perfecto.
- **RM = ritmo maratón.** Sale de la tabla de ritmos (documento 02), y se reindexa después de cada test.
- **Semanas de descarga** (4, 8, 12, 16, 20): bajan ~25-30%. No son opcionales. Son donde ocurre la adaptación.

## Estructura semanal fija

| Día | 6:00 AM | Mediodía o noche |
|---|---|---|
| **Lunes** | Gym A — Fuerza tren inferior (pesado) | Carrera fácil 35-45 min |
| **Martes** | — (movilidad 10 min opcional) | **Jiujitsu** |
| **Miércoles** | Gym B — Torso | **Sesión de calidad** |
| **Jueves** | — | Carrera fácil 40-50 min + técnica/cadencia |
| **Viernes** | **Descanso total** | — |
| **Sábado** | **Rodaje largo** | Gym C — core + tendón (ligero, opcional) |
| **Domingo** | Regenerativo 30-40 min muy suave *o* descanso | — |

**Por qué está así ordenado:**
- El **viernes descansa completo** para llegar entero al rodaje largo del sábado. Es el día más importante de la semana; no se negocia.
- El **Gym C va el sábado por la tarde**, después del largo, no el viernes. Principio de consolidación: apilar el estrés en los días duros y dejar los fáciles verdaderamente fáciles, en vez de repartirlo y no recuperar nunca.
- La **calidad va el miércoles**, con el martes de jiujitsu antes y el jueves fácil después. Nunca corres duro al día siguiente de pierna pesada.
- El **domingo es flexible**: si el sábado saliste con tu novia, mueve el largo al domingo y el regenerativo al sábado. Lo único que no se puede es hacer el largo el mismo fin de semana dos veces.

### Si tienes que saltarte algo
Orden de prioridad, de mayor a menor: **1)** rodaje largo · **2)** sesión de calidad · **3)** Gym A (pierna) · **4)** carrera fácil del lunes/jueves · **5)** Gym B (torso) · **6)** regenerativo del domingo. Sacrifica desde abajo.

---
""")

fase_actual = None
for s in d["semanas"]:
    if s["fase"] != fase_actual:
        fase_actual = s["fase"]
        titulo, rango, desc = FASES[fase_actual]
        w(f"\n## {titulo}\n\n*{rango}*\n\n{desc}\n")
        w("\n| Sem | Fechas | Total | Lun · fácil | **Mié · sesión de calidad** | Jue · fácil | **Sáb · rodaje largo** | Dom · regenerativo |")
        w("|---|---|---|---|---|---|---|---|")
    d = s["dias"]
    if s["largo_min"]:
        h, m = divmod(s["largo_min"], 60)
        t = f"**{h}h{m:02d}**" if m else f"**{h}h**"
        largo = f'{t} · ~{d["sab"]:g} km<br><small>{s["largo_desc"]}</small>'
    else:
        largo = f'**42,195 km**<br><small>{s["largo_desc"]}</small>'
    dom = f'{d["dom"]:g} km' if d["dom"] else "descanso"
    w(f"| **{s['semana']}** | {s['etiqueta']} | {s['km']} | {d['lun']:g} km | {s['calidad']}<br><small>total con calentamiento: ~{d['mie']:g} km</small> | {d['jue']:g} km | {largo} | {dom} |")

w("""

---

## Los 5 hitos que miden si vas bien

| Cuándo | Qué | Para qué sirve |
|---|---|---|
| **Semana 1** | Contrarreloj de 30 min | Define tu FC de umbral y tus zonas. Todo el plan se calibra con esto. |
| **Semana 8** | 10 km a tope | Primer control objetivo. Reindexas ritmos. Deberías haber ganado 2-4 min. |
| **Semana 15** (dom 20 dic) | **Media maratón a tope** | El predictor más fiable. **Tu ritmo de maratón sale de aquí**, no de la ilusión. |
| **Semana 21** | Largo de 3h15 con 8 km finales a RM | Prueba de que el ritmo objetivo es sostenible con fatiga. |
| **Semana 22** | Simulación: 16 km a RM con nutrición completa | Ensayo general. Si algo va a fallar, que falle aquí. |

### La regla de la semana 15
Tu media maratón de control × **2,1** = tu tiempo de maratón realista. No 2,0. Si haces 2:08, tu maratón es 4:29, no 4:16. **Salir a un ritmo que tu 21K no respalda es la causa número uno de reventar en el km 32.**

## Reglas de progresión (las que evitan que te lesiones)

1. **Nunca subas volumen y calidad la misma semana.** Sube uno, mantén el otro.
2. **Máximo +10% de volumen semanal**, y solo si la semana anterior se completó sin dolor.
3. **Un solo estímulo nuevo por semana.** Exactamente lo que no hiciste antes del 30K.
4. **Dolor que cambia tu forma de correr = para.** Molestia sorda que se calienta y desaparece: sigue con cautela. Dolor punzante, que empeora al avanzar, o que te hace cojear: para ese día y aplica el protocolo del documento 03.
5. **Regla de las 48 h:** si una molestia sigue igual o peor a las 48 h, sáltate la calidad de esa semana y haz solo rodaje fácil. Perder una sesión cuesta nada; perder seis semanas cuesta la maratón.
""")
open(os.path.join(BASE,"docs","01-plan-26-semanas.md"),"w").write("\n".join(L)+"\n")
print("escrito docs/01-plan-26-semanas.md")
