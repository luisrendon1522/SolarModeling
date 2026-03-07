# 📄 CHEAT SHEET - Una Página (Referencia Rápida)

## PROYECTO: SOLAR MODELING DASHBOARD

---

## 🎯 EN UNA FRASE
"Sistema que modela radiación solar usando 7 modelos ML, demostrando cómo feature engineering (60%) + arquitectura neural (30%) mejoran predicciones +100% capturando variabilidad real."

---

## 🔢 NÚMEROS CLAVE
| Métrica | Valor |
|---------|-------|
| Modelos | 7 (Linear, Poly, Tree, KNN, RF, PyTorch, TensorFlow) |
| Features | 1 → 8 (ingeniería cíclica) |
| Mejora R² | 0.40 → 0.80 (+100%) |
| Variabilidad | 30% → 75% (+150%) |
| Impacto feature-eng | 60% del total |
| Impacto arquitectura | 30% del total |
| Impacto RF tuning | 10% del total |

---

## ⚠️ PROBLEMA
**Modelos generaban predicciones SUAVES (underfitting)**
- Veían tendencia pero no picos/valles
- Señal real: ▄▄▀▀▄▄▀▀▄▄ → Predicción: ═════════

**Por qué:**
1. **Features crudas:** Solo tiempo [1,2,3...] → No captan ciclos naturales
2. **Arquitectura débil:** 1 capa/10 neuronas → Insuficiente complejidad
3. **RF restringido:** max_depth=10 → Árboles muy pequeños

---

## ✅ SOLUCIÓN
**3 mejoras coordinadas:**

### 1️⃣ Feature Engineering → +40% precisión
```
[tiempo] → [tiempo, sin(24h), cos(24h), sin(anual), cos(anual), t², t³, ...]
```
Agregué features cíclicas porque radiación solar es periódica (día/año)

### 2️⃣ Arquitectura Neural → +30% precisión
**PyTorch:** 1→4 capas, 10→64-128 neuronas, Sigmoid→ReLU, +Dropout, +BatchNorm
**TensorFlow:** 50→1000 épocas, +Early Stopping, +Learning Rate Decay

### 3️⃣ Random Forest → +10% precisión
max_depth: 10→25 (permitir árboles más complejos)

---

## 📊 RESULTADOS

**Cuantitativos:**
- ✅ R²: 0.40 → 0.80 (+100%)
- ✅ RMSE: -60% (error reducido)
- ✅ Captura variabilidad: 30% → 75%

**Visualización Antes/Después:**
```
Real:     ▄▄▀▀▄▄▀▀▄▄▀▀▄▄▀▀▄▄  (cíclica, variable)
Antes:    ════════════════════  (suave, plana)
Después:  ▄▃▀▂▄▃▀▂▄▃▀▂▄▃▀▂▄▃  (captura picos/valles)
```

---

## 🛠️ STACK TÉCNICO
- **Python 3.10**
- **Streamlit** (interface)
- **Scikit-learn** (modelos clásicos)
- **PyTorch** (Deep Learning)
- **TensorFlow** (Deep Learning)
- **Pandas/NumPy** (procesamiento)
- **Matplotlib** (visuales)
- **ReportLab** (PDF)

---

## 🚀 INSTALACIÓN (3 PASOS)
```bash
python -m venv venv
source venv/bin/activate       # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
streamlit run main.py
```

---

## 🧠 APRENDIZAJES PRINCIPALES

| Concepto | Impacto |
|----------|--------|
| **Feature Engineering** | 60% - Forma más impactante de mejorar |
| **Arquitectura Neuronal** | 30% - Importa pero no es TODO |
| **Regularización** | Dropout, BatchNorm, L2 = Evitar overfitting |
| **Validación** | Early Stopping previene sorpresas |
| **Trade-offs** | Simplicidad vs Precisión = Pragmatismo |

**Lección:** Feature engineering ANTES que complejidad. El 80/20 es real.

---

## 💡 CUÁNDO USAR CADA MODELO

| Modelo | Cuándo | Ventaja |
|--------|--------|---------|
| **Linear** | Pocos datos, relación lineal obvia | Interpretable |
| **Polynomial** | Datos medianos, no-linealidad suave | Balance |
| **Tree** | Interpretabilidad crítica | Explicable |
| **RF** | Datos medianos, complejidad media | Robusto |
| **Deep Learning** | Datos grandes (100k+), ultra-complejo | Potente |

**Para nuestro caso:** Random Forest = mejor balance

---

## 🎓 RESPUESTAS RÁPIDAS A PREGUNTAS

**P: ¿Por qué no solo TensorFlow?**
R: 60% es ingenería features, 30% arquitectura. Features >Complejidad.

**P: ¿8 features? ¿De dónde salieron?**
R: Análisis del dominio. Radiación = cíclica (diaria/anual). Agregué sin/cos para esos ciclos.

**P: ¿Por qué Random Forest gana?**
R: Menos datos necesarios que Deep Learning. Mejor interpretabilidad. Menos overfitting.

**P: ¿Y si cambio los datos?**
R: La metodología generaliza a cualquier serie temporal cíclica (tráfico, demanda, temperatura).

**P: ¿Cuál es la próxima mejora?**
R: LSTM para tener en cuenta dependencias temporales largas. Agregar variables exógenas (nubes, temp).

---

## 📈 FLUJO DE LA PRESENTACIÓN (20 MIN)

1. **Intro (2 min):** Qué es, objetivo
2. **Problema (2 min):** Señala gráfico ANTES oscuro
3. **Solución (3 min):** 3 mejoras principales
4. **Técnica (2 min):** Arquitectura + technologies
5. **Resultados (2 min):** Muestra gráficos DESPUÉS brillantes
6. **Demo (5 min):** Carga CSV, ejecuta, genera PDF
7. **Cierre (1 min):** Preguntas
8. **Preguntas (3 min):** Q&A

---

## 🎬 DEMO EN VIVO (si es necesario)

```bash
# PASO 1: Activar venv
.\venv\Scripts\activate

# PASO 2: Ejecutar Streamlit
streamlit run main.py

# PASO 3: En browser que abre
- Subir CSV (usar datos_prueba.csv si existe)
- Seleccionar variables X, Y
- Ejecutar
- Mostrar gráficos y tabla de métricas
- Generar PDF
- Mostrar PDF generado
```

**Tiempo:** 3-5 minutos para demo completa

---

## ⚡ PREPARACIÓN (1 HORA ANTES)

**Checklist:**
- ✅ Venv activado
- ✅ Dependencias instaladas (`pip list` para verificar)
- ✅ Streamlit abierto (prueba 1 vez)
- ✅ Datos de ejemplo listos
- ✅ Gráficos comparativos impresos (backup visual)
- ✅ PDF de ejemplo generado
- ✅ Leer TARJETA 1, 2, 3, 5 (memorización rápida)
- ✅ Scripts de prueba listos (`test_model_improvements.py`)

**Material a llevar:**
- Laptop con proyecto
- PowerPoint o diapositivas (opcional)
- CHEAT SHEET impreso (este archivo)
- PDF de resultados ejemplo

---

## 🎯 PUNTOS CLAVE PARA RECORDAR

1. **"El problema es la ingeniería de características, no la arquitectura"**
2. **"De 1 a 8 features: Capturá ciclos naturales"**
3. **"R² subió de 0.40 a 0.80: Es el peso del antes/después"**
4. **"Random Forest gana por pragmatismo: datos medianos, sin GPU"**
5. **"Aplicable a cualquier serie temporal cíclica"**

---

## 📚 ARCHIVOS CLAVE A MOSTRAR

| Archivo | Por qué | Cuándo |
|---------|---------|--------|
| `GUION_PRESENTACION.md` | Guión completo | Memorización previa |
| `TARJETAS_MEMORIZACIÓN.md` | Preguntas esperadas | Antes de presentar |
| `main.py` | Código principal | Si pregunta arquitectura |
| `models/feature_engineering.py` | Implementación features | Si pregunta "¿Cómo?" |
| `test_model_improvements.py` | Prueba visual | Si quiere ver comparación |
| PDF de salida | Resultado real | Final de presentación |

---

## ⏰ TIMELINE (Durante presentación)

| Tiempo | Actividad |
|--------|-----------|
| 0:00-2:00 | Introducción + Contexto |
| 2:00-4:00 | Problemática (mostrar gráficos) |
| 4:00-7:00 | Solución (3 mejoras, detalles) |
| 7:00-9:00 | Arquitectura técnica |
| 9:00-11:00 | Resultados cuantitativos |
| 11:00-16:00 | **DEMO EN VIVO** (o mostrar video) |
| 16:00-17:00 | Aprendizajes + Futuro |
| 17:00-20:00 | Preguntas |

---

**Última línea antes de entrar:** *"El 20% del esfuerzo (features) genera 80% del resultado. TODO el resto es perfeccionamiento."*

---

🎤 **TÚ TIENES ESTO. ¡Éxito!** 🎤
