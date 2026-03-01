"""
Streamlit Cloud entrypoint for SolarModeling app.
Adjusts sys.path to locate utils and models directories correctly.
"""

import sys
import os
from pathlib import Path

# Ensure imports from Attached-Assets work
repo_root = Path(__file__).parent
attached_assets_dir = repo_root / "Attached-Assets"

# Add Attached-Assets to path so relative imports work
attached_assets_str = str(attached_assets_dir)
if attached_assets_str not in sys.path:
    sys.path.insert(0, attached_assets_str)

# Change to Attached-Assets directory for file operations (data/, uploads/, etc.)
os.chdir(attached_assets_dir)

# Now import and run the main app
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils.data_loader import load_data, generate_synthetic_data
from utils.plotting import plot_results
from utils.pdf_generator import generate_pdf
from models.linear_two_points import LinearTwoPoints
from models.polynomial_regression import PolynomialRegression
from models.knn import KNNRegressor
from models.random_forest import RandomForest
from models.decision_tree import DecisionTree

# Intentar importar modelos de Deep Learning (pueden no estar disponibles)
try:
    from models.pytorch_nn import PyTorchNN
    pytorch_available = True
except ImportError:
    pytorch_available = False
    PyTorchNN = None

try:
    from models.tensorflow_nn import TensorFlowNN
    tensorflow_available = True
except ImportError:
    tensorflow_available = False
    TensorFlowNN = None

# Configuración de la página
st.set_page_config(
    layout="wide",
    page_title="Modeling & Analysis Dashboard",
    page_icon="📈"
)

# Agregar encabezados necesarios para que el sitio funcione como PWA
st.markdown(
    """
    <link rel="manifest" href="/manifest.json">
    <script>
      if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/service-worker.js');
      }
    </script>
    """,
    unsafe_allow_html=True
)

# Estilos CSS personalizados para un look profesional "Dark Scientific"
st.markdown("""
    <style>
    .main {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    .stMetric {
        background-color: #1c2128;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #30363d;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }
    .stButton>button {
        width: 100%;
        background-color: #238636 !important;
        color: white !important;
        border: none;
        padding: 12px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #2ea043 !important;
        box-shadow: 0 0 10px rgba(46, 160, 67, 0.5);
    }
    .section-container {
        background-color: #1c2128;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #30363d;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.sidebar.image("https://img.icons8.com/fluency/96/data-analytics.png", width=70)
    st.sidebar.title("Configuración")
    
    st.title("📈 Modeling & Analysis Dashboard")
    st.markdown("Regresión lineal, mínimos cuadrados, modelos de machine learning y redes neuronales.")
    st.markdown("---")

    # --- Sidebar: Carga de Datos ---
    st.sidebar.header("📂 Entrada de Datos")
    uploaded_file = st.sidebar.file_uploader("Subir dataset CSV", type=["csv"])
    use_synthetic = st.sidebar.checkbox("Generar datos sintéticos de ejemplo", value=not uploaded_file)

    synthetic_params = {}
    if use_synthetic:
        with st.sidebar.expander("Parámetros de Ejemplo", expanded=True):
            synthetic_params['amplitude'] = st.slider("Amplitud", 1, 500, 100)
            synthetic_params['frequency'] = st.slider("Frecuencia", 0.01, 5.0, 0.5)
            synthetic_params['phase'] = st.slider("Fase", -3.14, 3.14, 0.0)
            synthetic_params['noise'] = st.slider("Ruido (std)", 0, 100, 10)

    st.sidebar.markdown("---")
    st.sidebar.header("⚙️ Hiperparámetros")
    
    with st.sidebar.expander("Modelos Clásicos y ML", expanded=False):
        poly_degree = st.number_input("Grado Polinomial", 1, 10, 3)
        knn_neighbors = st.number_input("K-Vecinos", 1, 20, 5)
        rf_trees = st.number_input("Árboles (RF)", 10, 500, 100)
        rf_depth = st.number_input("Profundidad (RF)", 1, 50, 10)
        dt_depth = st.number_input("Profundidad (DT)", 1, 50, 10)

    st.sidebar.subheader("🧠 Modelos Avanzados")
    with st.sidebar.expander("Redes Neuronales", expanded=True):
        nn_layers = st.selectbox("Capas Ocultas", [1, 2, 3, 5], index=1)
        nn_neurons = st.select_slider("Neuronas/Capa", options=[16, 32, 64, 128, 256], value=64)
        nn_activation = st.radio("Activación", ["relu", "sigmoid"], horizontal=True)
        nn_epochs = st.number_input("Épocas Entrenamiento", 50, 5000, 200)

    # determinar variables y, si se subió archivo
    if uploaded_file:
        file_key = uploaded_file.name
        if file_key not in st.session_state:
            try:
                df_loaded = load_data(uploaded_file)
                st.session_state[file_key] = df_loaded
                st.session_state['current_file'] = file_key
                cols = df_loaded.columns.tolist()
                st.session_state["x_var_label"] = cols[0]
                st.session_state["y_var_label"] = cols[1] if len(cols) > 1 else cols[0]
            except ValueError as e:
                st.sidebar.error(f"❌ Error en CSV: {str(e)}")
                st.sidebar.info("Asegúrate de que el archivo sea un CSV válido con al menos dos columnas.")
                st.stop()
            except Exception as e:
                st.sidebar.error(f"❌ Error inesperado: {str(e)}")
                st.stop()
        
        df = st.session_state[file_key]
        cols = df.columns.tolist()
        
        st.sidebar.info(f"📊 Columnas del archivo: {', '.join(cols)}")
        
        x_var = st.sidebar.selectbox("Columna independiente (eje X)", options=cols, index=0)
        y_var = st.sidebar.selectbox("Columna dependiente (eje Y)", options=cols, index=1 if len(cols) > 1 else 0)

        x_var_label = st.sidebar.text_input(
            "Etiqueta para variable independiente (eje X)",
            value=st.session_state.get('x_var_label', x_var),
            help="Escribe el nombre que quieres que aparezca en gráficos y PDF"
        )
        
        y_var_label = st.sidebar.text_input(
            "Etiqueta para variable dependiente (eje Y)", 
            value=st.session_state.get('y_var_label', y_var),
            help="Escribe el nombre que quieres que aparezca en gráficos y PDF"
        )
        
        st.session_state['x_var'] = x_var
        st.session_state['y_var'] = y_var
        st.session_state['x_var_label'] = x_var_label if x_var_label else x_var
        st.session_state['y_var_label'] = y_var_label if y_var_label else y_var

        x_var = st.session_state['x_var']
        y_var = st.session_state['y_var']
        x_var_label = st.session_state['x_var_label']
        y_var_label = st.session_state['y_var_label']
    else:
        x_var = "feature_1"
        y_var = "target"
        x_var_label = "Feature 1"
        y_var_label = "Target"
        df = None

    # --- Lógica de Ejecución ---
    if st.sidebar.button("🚀 INICIAR ANÁLISIS"):
        with st.spinner("Ejecutando algoritmos de regresión..."):
            try:
                if use_synthetic:
                    df = generate_synthetic_data(
                        synthetic_params.get('amplitude', 100),
                        synthetic_params.get('frequency', 0.5),
                        synthetic_params.get('phase', 0.0),
                        synthetic_params.get('noise', 10),
                    )
                    x_var, y_var = "feature_1", "target"
                    x_var_label, y_var_label = "Feature 1", "Target"
                elif uploaded_file:
                    file_key = uploaded_file.name
                    if file_key not in st.session_state or st.session_state.get('current_file') != file_key:
                        st.error("Error: archivo no cargado correctamente. Recarga la página.")
                        return
                    df = st.session_state[file_key]
                    cols = df.columns.tolist()
                    x_var = st.session_state.get('x_var', cols[0])
                    y_var = st.session_state.get('y_var', cols[1] if len(cols) > 1 else cols[0])
                    x_var_label = st.session_state.get("x_var_label", x_var)
                    y_var_label = st.session_state.get("y_var_label", y_var)
                else:
                    st.warning("Se requiere una fuente de datos para continuar.")
                    return

                df[x_var] = pd.to_numeric(df[x_var], errors='coerce')
                df[y_var] = pd.to_numeric(df[y_var], errors='coerce')
                df = df.dropna(subset=[x_var, y_var])

                if df.empty:
                    st.error("No quedan filas válidas tras convertir los datos a numéricos.")
                    return

                X = df[x_var].astype(float).values.reshape(-1, 1)
                y = df[y_var].astype(float).values

                # 2. Inicialización de Modelos
                models = [
                    LinearTwoPoints(),
                    PolynomialRegression(degree=poly_degree),
                    KNNRegressor(n_neighbors=knn_neighbors),
                    RandomForest(n_estimators=rf_trees, max_depth=rf_depth),
                    DecisionTree(max_depth=dt_depth),
                ]
                
                if pytorch_available and PyTorchNN is not None:
                    models.append(PyTorchNN(epochs=nn_epochs))
                if tensorflow_available and TensorFlowNN is not None:
                    models.append(TensorFlowNN(hidden_layers=nn_layers, neurons=nn_neurons, activation=nn_activation, epochs=nn_epochs//2))

                results = []
                best_r2 = -float('inf')
                best_name = ""

                # 3. Entrenamiento y Evaluación
                for model in models:
                    model.train(X, y)
                    y_pred = model.predict(X)
                    metrics = model.evaluate(y, y_pred)
                    
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.scatter(X, y, color='#4a90e2', alpha=0.5, label='Experimental', s=20)
                    sort_idx = np.argsort(X[:, 0])
                    ax.plot(X[sort_idx, 0], y_pred[sort_idx], color='#e74c3c', linewidth=2, label='Modelo')
                    ax.set_title(f"Modelado: {model.name}", color='white', fontsize=12)
                    ax.set_facecolor('#1c2128')
                    fig.patch.set_facecolor('#0d1117')
                    ax.tick_params(colors='white')
                    ax.legend()
                    ax.grid(True, alpha=0.1)
                    ax.set_xlabel(x_var_label)
                    ax.set_ylabel(y_var_label)
                    
                    train_fig = None
                    if hasattr(model, 'losses') or (hasattr(model, 'history') and model.history):
                        train_fig, tax = plt.subplots(figsize=(5, 3))
                        loss_data = model.losses if hasattr(model, 'losses') else model.history.history['loss']
                        tax.plot(loss_data, color='#f1c40f')
                        tax.set_title("Evolución del Error (Loss)", color='white')
                        tax.set_facecolor('#1c2128')
                        train_fig.patch.set_facecolor('#0d1117')
                        tax.tick_params(colors='white')
                        tax.grid(True, alpha=0.1)

                    results.append({
                        "obj": model,
                        "name": model.name,
                        "metrics": metrics,
                        "fig": fig,
                        "train_fig": train_fig,
                        "summary": getattr(model, 'summary', ''),
                        "equation": getattr(model, 'equation', '')
                    })

                    if metrics['r2'] > best_r2:
                        best_r2 = metrics['r2']
                        best_name = model.name

                # --- 4. Renderizado de Dashboard ---
                st.header("🏆 Resultado del Análisis")
                res_col1, res_col2 = st.columns([1, 2])
                with res_col1:
                    st.metric("Mejor Modelo (R²)", best_name, delta=f"{best_r2:.4f}")
                with res_col2:
                    st.success(f"El sistema ha identificado que **{best_name}** proporciona el ajuste más preciso para los datos actuales.")

                # Tabla Comparativa
                st.subheader("📊 Comparativa de Métricas")
                df_metrics = pd.DataFrame([
                    {
                        "Algoritmo": r["name"],
                        "MSE": f"{r['metrics']['mse']:.2f}",
                        "RMSE": f"{r['metrics']['rmse']:.2f}",
                        "MAE": f"{r['metrics']['mae']:.2f}",
                        "R²": f"{r['metrics']['r2']:.4f}"
                    } for r in results
                ])
                st.table(df_metrics)

                # Galería de Modelos
                st.header("🔍 Análisis Detallado por Modelo")
                for i in range(0, len(results), 2):
                    cols = st.columns(2)
                    for j in range(2):
                        if i + j < len(results):
                            r = results[i + j]
                            with cols[j]:
                                with st.container():
                                    st.markdown(f"#### {r['name']}")
                                    st.pyplot(r['fig'])
                                    if r['train_fig']:
                                        st.pyplot(r['train_fig'])
                                    with st.expander("Ver Detalles Técnicos"):
                                        st.code(f"Ecuación/Estructura: {r['equation']}")
                                        st.write(f"Descripción: {r['summary']}")

                st.session_state.analysis_results = {
                    "results": results,
                    "best_name": best_name,
                    "explanation": (
                        f"El modelo {best_name} ofreció el mejor ajuste para "
                        f"predecir {y_var_label} a partir de {x_var_label}."
                    ),
                    "x_var": x_var,
                    "y_var": y_var,
                    "x_var_label": x_var_label,
                    "y_var_label": y_var_label,
                }

            except Exception as e:
                st.error(f"Error crítico en el motor de análisis: {str(e)}")
                st.exception(e)

if __name__ == "__main__":
    main()

# --- UI para generación/descarga de PDF (fuera del bloque de análisis) ---
def export_pdf_section():
    st.markdown("---")
    st.subheader("📂 Generación de Entregables")
    pdf_path = "Reporte_Analisis_Final.pdf"

    if "analysis_results" not in st.session_state:
        st.info("Ejecuta '🚀 INICIAR ANÁLISIS' primero para habilitar la exportación de resultados.")
        return

    data = st.session_state.analysis_results

    if st.button("📄 GENERAR REPORTE CIENTÍFICO PDF"):
        try:
            # Pasar objetos completos con gráficas
            pdf_data = [{"name": r['name'], "metrics": r['metrics'], "fig": r.get('fig'), "train_fig": r.get('train_fig')} for r in data["results"]]
            abs_path = os.path.abspath(pdf_path)
            with st.spinner("Generando PDF..."):
                generate_pdf(
                    abs_path,
                    pdf_data,
                    data["best_name"],
                    data["explanation"],
                    x_label=data.get("x_var_label", "X"),
                    y_label=data.get("y_var_label", "Y"),
                )
            st.success("PDF generado correctamente.")
            try:
                with open(abs_path, "rb") as f:
                    st.session_state['pdf_bytes'] = f.read()
            except Exception as e:
                st.error(f"Error leyendo PDF generado: {e}")
        except Exception as e:
            st.error(f"Error generando PDF: {e}")

    if st.session_state.get('pdf_bytes'):
        st.success("PDF listo para descargar")
        st.download_button(
            "Descargar PDF",
            data=st.session_state['pdf_bytes'],
            file_name=os.path.basename(pdf_path),
            mime="application/pdf",
        )

export_pdf_section()
