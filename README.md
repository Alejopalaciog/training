# Plan de maratón · 26 semanas

**Debut en maratón · Rionegro/Guarne (~2.125 m) → Medellín (~1.495 m)**
**Inicio:** lunes 7 de septiembre de 2026 · **Carrera:** domingo 7 de marzo de 2027

| | |
|---|---|
| Punto de partida | 83 kg · 20-30 km/semana · largo máximo 30 km @ 8:00/km |
| Objetivo principal | **Terminar sano entre 4:30 y 4:40** (6:24-6:38/km) |
| Objetivo ambicioso | 4:20 (6:10/km) si todo sale bien |
| Peso objetivo | 77 kg en la línea de salida (también categoría de jiujitsu) |
| Volumen total | 1.175 km · pico de 64 km en la semana 21 |
| Se mantiene | 3 días de gimnasio + jiujitsu semanal |

## Los documentos

| # | Documento | Qué contiene |
|---|---|---|
| 00 | [Diagnóstico y objetivos](docs/00-diagnostico.md) | Por qué tu pace no baja, qué pasó en tu 30K, los tres niveles de objetivo |
| 01 | [**El plan, semana a semana**](docs/01-plan-26-semanas.md) | Las 26 semanas, la estructura semanal fija, las reglas de progresión |
| 02 | [Ritmos y sesiones](docs/02-sesiones-y-ritmos.md) | El test que calibra todo, tu tabla de ritmos, cómo se ejecuta cada sesión, cadencia, zapatillas |
| 03 | [Fuerza y prevención](docs/03-fuerza-y-prevencion.md) | Los 3 días de gimnasio por fase, sóleo y tibial posterior, jiujitsu, protocolo de molestias |
| 04 | [Nutrición](docs/04-nutricion.md) | Macros por tipo de día, los 6 kg y cuándo, comida real colombiana, nutrición en carrera, carga de carbos, contraste con el plan de tu amigo |
| 05 | [Otros factores](docs/05-otros-factores.md) | Sueño, calor, estrategia de carrera, logística, elegir la carrera |
| 06 | [Registro y alertas](docs/06-registro-y-alertas.md) | Qué medir, semáforo semanal, cómo retomar tras parar, fechas clave |

## Empieza por aquí

1. Lee el **documento 00** completo. Son 5 minutos y explica el porqué de todo lo demás.
2. **Semana 1, miércoles: haz el test de 30 minutos** (documento 02). Sin ese número, el resto del plan es genérico.
3. Pide la **analítica de sangre** (ferritina, hemograma, vitamina D, TSH) esta misma semana.
4. Pésate en ayunas todos los días durante 2 semanas para calibrar tus calorías reales.
5. Pon las **fechas clave** (documento 06) en el calendario hoy.

## Las tres reglas que sostienen el plan

1. **El 80% de tu volumen tiene que ser verdaderamente fácil.** Si dudas, ve más lento.
2. **Un solo estímulo nuevo por semana.** Nunca subas volumen y calidad a la vez.
3. **El déficit calórico termina en la semana 12.** A partir de ahí se come para entrenar, no para adelgazar.

## Regenerar el plan

El calendario y las tablas de ritmos se generan desde un script, no están escritos a mano:

```bash
python3 scripts/generar_plan.py      # recalcula calendario y ritmos -> data/plan.json
python3 scripts/render_plan_md.py    # regenera docs/01-plan-26-semanas.md
```

Si cambia la fecha de la carrera o quieres ajustar volúmenes, edita `SEMANAS` en `scripts/generar_plan.py` y vuelve a ejecutar ambos.
