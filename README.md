# Plan de maratón · 26 semanas

**Debut en maratón · Rionegro/Guarne (~2.125 m) → Medellín (~1.495 m)**
**Inicio:** lunes 7 de septiembre de 2026 · **Carrera:** domingo 7 de marzo de 2027

| | |
|---|---|
| Punto de partida | 27 años · 1,72 m · 83 kg · FC reposo 52 · 20-30 km/semana · mejor 21K 2:44 |
| Objetivo principal | **Terminar sano entre 4:45 y 4:55** (6:45-7:00/km) |
| Objetivo ambicioso | 4:30 (6:24/km) si todo sale bien |
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
| 07 | [**Glosario**](docs/07-glosario.md) | Qué significa cada término: umbral, RM, rectas, fartlek, VO2max, RIR, negative split… |
| 08 | [Mensaje para tu entrenador](docs/08-mensaje-para-tu-entrenador.md) | Texto listo para copiar y pegar, con el porqué de cada ajuste |

## Otros archivos

| Archivo | Qué es |
|---|---|
| `Plan-Maraton-26-Semanas.pdf` | El plan completo en PDF, para el celular |
| `plan-maraton.html` | La página consultable (la misma que está publicada) |
| `data/plan.json` | El plan en datos: semanas, días, ritmos. Lo consumen los generadores |
| `data/semana-carrera-nutricion.csv` | La tabla de tu amigo, corregida y adaptada a la semana de carrera |

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
npm run plan     # calendario + ritmos + docs/01 + fragmentos de la página
npm run pdf      # regenera Plan-Maraton-26-Semanas.pdf desde plan-maraton.html
```

### Cambiar la fecha de la carrera

```bash
python3 scripts/generar_plan.py --carrera 2027-05-16          # mueve la maratón
python3 scripts/generar_plan.py --carrera 2027-05-16 --extra espec
```

El script recalcula **todo** hacia atrás desde la fecha que le des:

- **Si hay más de 26 semanas**, inserta semanas extra. `--extra base` (por defecto) añade base aeróbica; `--extra espec` añade trabajo específico.
- **Si hay menos de 26**, recorta semanas de la Fase 1 y **avisa**. Por debajo de 22 semanas el riesgo de lesión sube de forma significativa.

Después de cambiar la fecha, ejecuta `npm run plan` y luego `npm run pdf` para regenerar los documentos y el PDF.

La primera vez, para el PDF: `npm install` (necesita Chromium; en un equipo normal, `npx playwright install chromium`).
