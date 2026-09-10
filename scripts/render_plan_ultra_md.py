#!/usr/bin/env python3
"""Renderiza docs/11-plan-ultra-50k.md desde data/plan_ultra.json."""
import json, os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(BASE,"data","plan_ultra.json")))

FASES = {
 "F0": ("Fase 0 · Recuperación activa", "Semanas 1-4",
   "Cerrar la maratón antes de abrir el ultra. Análisis de pisada, decisión de calzado, confirmación de que el tibial posterior está en cero. Nada de estructura todavía."),
 "F1": ("Fase 1 · Base aeróbica y umbral", "Semanas 5-12",
   "Idéntica en espíritu a la Fase 1 del plan de maratón — es exactamente lo que faltó en el debut. Aparece el primer back-to-back (sábado largo + domingo corto), todavía sin intención específica de ultra, solo para que el cuerpo se acostumbre a la idea de correr con piernas cansadas."),
 "F2": ("Fase 2 · Específico de ultra", "Semanas 13-24",
   "El bloque que de verdad construye la resistencia de ultra: fondos consecutivos cada vez más largos, power-hiking en subida, nutrición con comida real, y el fin de semana más largo de todo el plan en la semana 21."),
 "F3": ("Fase 3 · Taper", "Semanas 25-27",
   "Tres semanas, un poco más largo que el taper de maratón porque hay más fatiga acumulada de los fondos dobles. Baja el volumen, no la intensidad."),
 "RACE": ("Semana de carrera", "Semana 28", "50 km. Nada nuevo, ya lo ensayaste todo en la semana 18 y 21."),
}
ORDEN = ["F0","F1","F2","F3","RACE"]

L=[]; w=L.append
w("# 11 · Plan hacia el primer 50 K\n")
w(f"**Inicio:** lunes 14 de septiembre de 2026 · **Carrera:** domingo 28 de marzo de 2027 · **28 semanas**\n")
w(f"**Volumen total:** {sum(s['km'] for s in d['semanas'])} km · **Fin de semana más largo:** semana 21, sábado 5h + domingo 2h30\n")
w("""
Este es el bloque 1 de la [ruta a 100 km](10-ruta-a-100km.md). No es un plan nuevo desde cero: las semanas 1-12 son la misma base y umbral que le faltó al debut de maratón (ver [retro](09-retro-maraton-1.md)); lo que cambia frente a un ciclo de maratón es la Fase 2, donde aparece lo específico de ultra.

## Qué hay de nuevo frente al plan de maratón

- **Fin de semana doble (back-to-back).** El domingo ya no es un trote regenerativo: es un fondo con las piernas todavía cansadas del sábado. Es la adaptación más específica de ultra que existe — el cuerpo aprende a seguir produciendo energía cuando el glucógeno ya está bajo, que es exactamente la situación de las últimas horas de un ultra.
- **Los largos van en tiempo, no en kilómetros**, igual que en el plan de maratón, pero mucho más largos: hasta 5 horas en el pico. El terreno (plano vs con desnivel) hace que un mismo tiempo produzca distancias muy distintas, así que el tiempo es la única unidad que tiene sentido aquí.
- **Caminar las subidas es la técnica, no el fracaso.** Desde la semana 14 hay sesiones dedicadas a practicar el *power-hiking*: subir caminando fuerte, con las manos en los muslos si hace falta, más rápido de lo que se siente natural caminar. En terreno empinado, caminar rápido gasta menos energía que correr despacio.
- **Nutrición con comida real.** Los geles y bocadillos siguen para las sesiones de calidad, pero los fondos largos de la Fase 2 son el momento de practicar arroz, papa cocida, caldo — lo que de verdad vas a encontrar en los avituallamientos de un ultra a partir de la tercera hora.
- **Menos intensidad todavía que en maratón.** El umbral sigue siendo el estímulo central (por lo mismo que en el debut: es lo que nunca se había entrenado), pero la velocidad pura importa aún menos en 50 km que en 42. No hay sesiones de VO2máx en este plan.

## Las 28 semanas
""")

fase_actual=None
for s in d["semanas"]:
    if s["fase"] != fase_actual:
        fase_actual = s["fase"]
        t,r,desc = FASES[fase_actual]
        w(f"\n### {t}\n\n*{r}*\n\n{desc}\n")
        w("\n| Sem | Fechas | km | Sábado | Domingo (back-to-back) | Calidad · miércoles | Foco |")
        w("|---|---|---|---|---|---|---|")
    sab = f"**{s['sab_min']//60}h{s['sab_min']%60:02d}**<br><small>{s['sab_desc']}</small>" if s["sab_min"] else "descanso"
    dom = f"**{s['dom_min']//60}h{s['dom_min']%60:02d}**<br><small>{s['dom_desc']}</small>" if s["dom_min"] else "descanso"
    w(f"| {s['semana']} | {s['etiqueta']} | {s['km']} | {sab} | {dom} | {s['calidad']} | {s['foco']} |")

w("""

---

## Fuerza: qué cambia frente al plan de maratón

El de maratón (documento 03) sigue siendo la base — sóleo, tibial posterior, fuerza pesada de piernas — con dos añadidos propios de ultra:

- **Excéntrico de cuádriceps** (sentadilla búlgara con bajada lenta de 4 segundos, step-down controlado) desde la Fase 0. Las bajadas largas de un ultra producen un daño muscular distinto al de correr en plano, y el cuádriceps es quien más lo sufre. Se entrena con anticipación, no se descubre en la carrera.
- **Se corta el excéntrico en el taper** (semana 26 en adelante), igual que la pliometría se corta en el plan de maratón: todo el riesgo, ningún beneficio que llegue a tiempo.

## Equipo y logística que no existían en el plan de maratón

- **Mochila o chaleco de hidratación** — a partir de fondos de 2h+, empieza a llevar lo que planeas usar en carrera, para acostumbrar el cuerpo (y la espalda) a correr con peso.
- **Linterna frontal** — no es indispensable para un 50 K con salida diurna, pero si el bloque 3 (100 K) va a exigirla, no cuesta nada empezar a probarla en algún fondo nocturno de la Fase 2.
- **Bastones (opcional)** — solo si el 50 K elegido tiene desnivel serio. Se aprenden a usar entrenando, no el día de la carrera.
- **Kit de pies para horas** — cambio de medias, talco o vaselina de repaso, tirita de repuesto. Con tu historial de ajuste de zapatilla (documento 09), esto no es opcional para ti.

## Cómo se sacrifica algo si hace falta

Mismo orden de prioridad que en el plan de maratón: **1)** el fondo del sábado · **2)** el domingo de piernas cargadas (es el segundo más importante, no el primero en caer — es la adaptación específica de ultra) · **3)** la sesión de calidad del miércoles · **4)** los rodajes fáciles entre semana · **5)** el gimnasio.
""")
open(os.path.join(BASE,"docs","11-plan-ultra-50k.md"),"w").write("\n".join(L)+"\n")
print("escrito docs/11-plan-ultra-50k.md")
