# 🎓 TARJETAS DE MEMORIZACIÓN - Preguntas Clave

## TARJETA 1: ¿Cuál es el objetivo del proyecto?
**Pregunta:** ¿Cuál es el objetivo principal del projeto?

**Respuesta (30 seg):**
"Modelar la radiación solar usando 7 algoritmos de Machine Learning. El objetivo es demostrar que con ingeniería de características apropiada (60% del impact) y arquitectura neural correcta (30% del impacto), podemos capturar la variabilidad real. Pasamos de R²=0.40 a R²=0.80 (+100%)."

**Clave memorística:** 7 modelos, 60-30-10 (features-neural-rf), +100% R²

---

## TARJETA 2: ¿Cuál es el problema que resuelves?
**Pregunta:** ¿Qué problema identificaste en los modelos originales?

**Respuesta (40 seg):**
"Los modelos originales generaban predicciones TAN SUAVES que no capturaban la variabilidad real de los datos. Veían la tendencia general pero perdían los picos y valles diarios.

Las causas fueron:
- **60%:** Falta de ingeniería de features → solo recibían tiempo lineal [1,2,3...]
- **30%:** Arquitectura neural insuficiente → 1 capa, 10 neuronas
- **10%:** Random Forest muy restringido → max_depth=10

Resultado: Explicaban solo 30% de la variabilidad (R²=0.40)"

**Analogía:** Es como un pronóstico que solo dice 'habrá sol' sin especificar cuándo hay nubes.

---

## TARJETA 3: ¿Cuáles fueron tus 3 mejoras principales?
**Pregunta:** ¿Cuáles fueron las principales mejoras implementadas?

**Respuesta (45 seg):**
"Tres mejoras coordinas:

1. **Feature Engineering (60% impacto):**
   - De 1 → 8 features
   - Agregué: sin(ciclo_diario), cos(ciclo_diario), sin(ciclo_anual), cos(ciclo_anual), t², t³
   - Captura NOW los patrones naturales de radiación solar

2. **Arquitectura Neural (30% impacto):**
   - PyTorch: 1 capa → 4 capas (64→128→64→32 neuronas) + ReLU + BatchNorm + Dropout
   - TensorFlow: 50 épocas → 1000 épocas + Early Stopping + Learning Rate Decay

3. **Random Forest (10% impacto):**
   - max_depth: 10 → 25 (permitir árboles más complejos)"

**Números clave:** 1→8, 1→4 capas, 50→1000 épocas

---

## TARJETA 4: ¿Por qué 1→8 features?
**Pregunta:** ¿Por qué aumentar de 1 a 8 features fue tan importante?

**Respuesta (35 seg):**
"Porque los datos del mundo real tienen PATRONES CÍCLICOS:
- Ciclo diario: El sol sale/se pone cada 24 horas
- Ciclo anual: Variación estacional cada 365 días

Con solo tiempo lineal [1, 2, 3, 4...] NO PUEDO capturar ciclos. Es ALGEBRAICAMENTE IMPOSIBLE.

Features cíclicas:
- sin(2π×t/24): Captura ciclo de 24 horas
- cos(2π×t/24): Desfase de 90 grados (complemjenta sin)
- Similar para ciclo anual

Con estas 8 features + no-lineales, el modelo ENTIENDE la periodicidad."

**Analogía:** Es como enseñarle a alguien a predecir mareas (cíclicas). No puedes si solo le das números lineales; necesitas explicar el ciclo lunar.

---

## TARJETA 5: ¿Cuáles fueron los resultados?
**Pregunta:** ¿Cuáles fueron los resultados cuantitativos?

**Respuesta (30 seg):**
"Antes de mejoras:
- R² = 0.40 (explica 40% de variabilidad)
- RMSE alto
- Predicciones suaves, sin detalles

Después de mejoras:
- R² = 0.80 ← **+100% mejora**
- RMSE reducido 60%
- MAE reducido 50%
- **Captura correctamente picos y valles diarios**

Visualización:
```
Antes:    ════════════ (línea plana)
Después:  ▄▃▀▂▄▃▀▂▄▃ (seguye datos reales)
```"

**Clave:** R²: 0.40→0.80, +100%, captura variabilidad

---

## TARJETA 6: ¿Cuáles son los 7 modelos?
**Pregunta:** ¿Cuáles son los 7 modelos que comparas?

**Respuesta (40 seg):**
"1. **Regresión Lineal** → Baseline simple
2. **Regresión Polinómica** → Captura curvatura
3. **Decision Tree** → Interpretable, segmentación
4. **K-Nearest Neighbors** → Basado en proximidad local
5. **Random Forest** → Ensemble robusto (principal competidor)
6. **PyTorch NN** → Deep Learning flexible, personalizable
7. **TensorFlow NN** → Deep Learning profesional con callbacks

Los últimos 2 fueron mejorados significativamente para capturar más variabilidad."

**Mnemotecnia:** Lin-Poly-DTree-KNN-RF-PyT-TF

---

## TARJETA 7: ¿Cuándo usarías cada modelo?
**Pregunta:** ¿Cuándo usarías Regresión Lineal vs Random Forest vs Deep Learning?

**Respuesta (50 seg):**
"Depende del contexto:

**Regresión Lineal:**
- Datos pequeños, relación lineal obvia
- Necesitas interpretabilidad extrema
- Prototipado rápido

**Random Forest:**
- Datos medianos/grandes
- Relaciones no-lineales complejas
- Balance entre fuerza y velocidad
- Muy robusto, pocas hiperparámetros

**Deep Learning (PyTorch/TensorFlow):**
- Datos MUCHOS (>10k registros)
- Patrones MUY complejos
- Tienes GPU disponible
- Aceptas poco interpretabilidad

Para nuestro caso específico (radiación solar cíclica):
- Linear falla (datos cíclicos)
- Regresión Polinómica funciona bien con 8 features
- Random Forest excelente
- Deep Learning el mejor si tienes datos + GPU"

**Decisión:** Random Forest = mejor balance costo-beneficio

---

## TARJETA 8: ¿Por qué feature engineering es 60%?
**Pregunta:** ¿Por qué dices que feature engineering es el 60% del impacto?

**Respuesta (35 seg):**
"Porque:

Sin ingeniería:
- Modelos reciben datos crudos débiles
- No pueden aprender lo que no ven
- Aunque tengas Deep Learning gigante, hay límite

Con ingeniería:
- Features bien diseñadas hacen trabajo fácil
- Hasta Linear Regression mejora 10x
- El modelo solo necesita conectar puntos

Analógía: 
Es como buscar a alguien. Si dices 'hombre, pelo negro' tienes millones de candidatos. Si dices 'hombre, pelo negro, cicatriz en frente, altura 1.80m' encuentras el correcto rápidamente.

FEATURES = DESCRIPCIÓN
MODELOS = BÚSQUEDA

Una descripción pobre requiere búsqueda perfecta (imposible).
Una descripción excelente permite búsqueda simple."

**Conclusión:** No puedes compensar mala ingeniería con mucha complejidad.

---

## TARJETA 9: Tecnologías usadas
**Pregunta:** ¿Cuáles tecnologías/librerías principales usaste?

**Respuesta (30 seg):**
"**Frontend:**
- Streamlit: Interface web interactiva

**Procesamiento:**
- Python 3.10
- Pandas: Manipular datos
- NumPy: Cálculos numéricos

**Modelos:**
- Scikit-learn: Regresión, tree, RF, KNN
- PyTorch: Red neuronal personalizada
- TensorFlow/Keras: Red neuronal profesional

**Visualización:**
- Matplotlib: Gráficos
- ReportLab: PDF generation

**Testing:**
- Validación 5-fold
- Cross-validation"

**Stack:** Python + Streamlit + Sklearn + PyTorch + TensorFlow + Matplotlib

---

## TARJETA 10: Instalación y ejecución
**Pregunta:** ¿Cómo instala y ejecuta alguien el proyecto?

**Respuesta (30 seg):**
"3 pasos simples:

```bash
# 1. Entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Dependencias
pip install -r requirements.txt

# 3. Ejecutar
streamlit run main.py
```

Luego:
1. Sube tu CSV
2. Selecciona X (independiente) e Y (dependiente)
3. Verás comparación de 7 modelos
4. Exporta PDF con resultados"

**Proceso:** venv → pip → streamlit run main.py

---

## TARJETA 11: ¿Cuál es el impacto práctico?
**Pregunta:** ¿Cuál es el impacto real de este proyecto en el mundo?

**Respuesta (40 seg):**
"Predecir radiación solar es CRÍTICO para:

1. **Energía Solar:** Plantas fotovoltaicas producen electricidad basada en radiación. Mejor predicción = mejor planificación de energía
2. **Sistema eléctrico:** Redes inteligentes necesitan predecir cuánto solar inyectan
3. **Investigación climática:** Entender patrones de radiación
4. **Optimización:** Ajustar sistemas HVAC, luminosidad artificial en casas

Con mejora +100% en precisión:
- Menos desperdicio de energía
- Mejor estabilidad en red eléctrica
- Más confiable para plantas de energía

En España: Reducir error en 100% puede significar millones en ahorro de energía anual."

**Aplicación:** Energías renovables, planificación de red eléctrica, Smart Cities

---

## TARJETA 12: ¿Qué aprendiste?
**Pregunta:** ¿Cuáles son los 3 aprendizajes académicos principales?

**Respuesta (40 seg):**
"1. **Feature Engineering es Fundamental**
   - 60% del impacto viene de aquí
   - Comprender el dominio (periodicidad solar) es esencial
   - No puedes compensar features malas con arquitectura

2. **Arquitectura Neuronal Importa, Pero No es Todo**
   - Aumentar capas/neuronas ayuda (30%)
   - Pero necesilas DATOS BUENOS para justificar complejidad
   - Trade-off: Complejidad vs Interpretabilidad

3. **Validación y Regularización Previenen Overfitting**
   - Batch Norm, Dropout, Early Stopping no son 'lujos'
   - Son NECESARIOS para Deep Learning confiable
   - Cross-validation evita sorpresas

Lección general: El 80/20 es real. 20% de esfuerzo (features) = 80% del resultado."

**Key Learnings:** Features > Arquitectura, Validación es crítica, Trade-offs son reales

---

## TARJETA 13: Extensiones futuras
**Pregunta:** ¿Qué mejoras o extensiones futuras has pensado?

**Respuesta (40 seg):**
"Corto plazo (próximos 3 meses):
- LSTM/GRU para capturar dependencias temporales largas
- Predicción multi-paso: 24h, 7 días, 30 días
- Agregación de variables exógenas (temperatura, humedad, nubosidad)

Mediano plazo (6 meses):
- Ensemble de los 7 modelos con voting
- Validar en datos reales de estaciones meteorológicas
- Dashboard interactivo con predicciones en vivo

Largo plazo (1+ año):
- Transferencia learning desde modelos pre-entrenados
- API REST para terceros
- Escalado a múltiples locaciones geográficas
- Integración con sistemas IoT real

Investigación:
- ¿Cómo impacta presencia de nubes?
- ¿Anomalías (eclipses)?
- ¿Previsibilidad a diferente escala temporal?"

**Roadmap:** LSTM → Exógenas → Ensemble → API → IoT

---

## TARJETA 14: Preguntas Capciosas
**Pregunta:** Si alguien pregunta '¿Por qué no usas solo Deep Learning?'

**Respuesta:**
"Porque el análisis mostró que 60% del problema es ingeniería de características, no arquitectura. Deep Learning solo resuelve 30%. Si tengo features débiles, ni Deep Learning gigante lo soluciona. Es mejor tener features excelentes + modelo simple que features débiles + modelo complejo."

---

**Pregunta:** Si alguien pregunta '¿Y si tengo otros datos que no son solares?'

**Respuesta:**
"La metodología es generalizable a CUALQUIER dato temporal/cíclico:
- Demanda eléctrica: ciclos diarios + semanales
- Tráfico: ciclos diarios + semanales
- Temperatura: ciclos diarios + anuales
- Compras online: ciclos semanales + anuales

Lo que cambiaría sería los PERIODOS específicos y features derivadas, pero el conceptg es el mismo."

---

**Pregunta:** Si alguien pregunta '¿Por qué Random Forest y no solo TensorFlow?'

**Respuesta:**
"Random Forest tiene VENTAJA:
- Más interpretable
- Menos datos necesarios (nuestro caso)
- Menos tiempo de entrenamiento
- Sin GPU required
- Hyperparámetros más intuitivos

Deep Learning GANA cuando:
- Tienes MUCHOS datos (100k+)
- Relaciones ULTRA complejas
- Necesitas exactitud máxima
- Tienes GPU

Para radiación solar con dataset mediano, Random Forest es mejor balance pragmático."

---

## 📚 TIPS DE MEMORIZACIÓN

### Técnica 1: Repetición Espaciada
- Leer completo 1 vez (energía fresca)
- Revisar tarjeta 1-3 después 30 min
- Revisar tarjeta 4-7 después 2 horas
- Revisar tarjeta 8-14 antes de dormir
- Día siguiente: Repaso rápido de todas

### Técnica 2: Enseñar a Otros
- Explica cada tarjeta a un amigo/compañero
- Te obligará a internalizarlo
- Detectarás fortalezas/debilidades

### Técnica 3: Flashcards Físicas
- Corta cada tarjeta y llévala
- Lee en momentos muertos (transporte)
- Quita la respuesta, solo lee pregunta

### Técnica 4: Construcción Mental
- Para cada tarjeta, crea una IMAGEN mental
- Asocia con un LUGAR específico (memory palace)
- Ejemplo: Tarjeta 1 = entrada proyecto
- Tarjeta 2 = problemas en hall
- Tarjeta 3 = soluciones en sala principal

### Técnica 5: Grabación de Audio
```bash
# En Windows: Recorder app y grábate diciendo cada respuesta
# Escucha nuevamente en el auto/transporte
```

---

## ⚡ ÚLTIMA REVISIÓN (30 minutos antes)

1. ✅ Leo TARJETA 1 (objetivo)
2. ✅ Leo TARJETA 2 (problema)
3. ✅ Leo TARJETA 3 (mejoras 3 principales)
4. ✅ Leo TARJETA 5 (resultados)
5. ✅ Leo TARJETA 12 (aprendizajes)

**Si tengo tiempo:**
- Leo TARJETA 4 (features especiales)
- Leo TARJETA 7 (cuándo cada modelo)
- Leo TARJETA 14 (preguntas capciosas)

---

**Impreso: Lleva este documento a la presentación (imprime TARJETAS 1, 2, 3, 5 si es permitido)**
