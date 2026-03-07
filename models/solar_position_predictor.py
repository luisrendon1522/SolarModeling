import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib

class SolarPositionPredictor:
    def __init__(self):
        self.scaler_X = StandardScaler()
        self.scaler_y = StandardScaler()
        self.model_elevation = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model_azimuth = RandomForestRegressor(n_estimators=100, random_state=42)

    def load_data(self, filepath):
        df = pd.read_csv(filepath)
        # Inputs: tiempo, intensidad_luz
        X = df[['tiempo', 'intensidad_luz']].values
        # Outputs: elevation, azimuth
        y = df[['elevation', 'azimuth']].values
        return X, y

    def train(self, X, y):
        # Escalar inputs
        X_scaled = self.scaler_X.fit_transform(X)

        # Escalar outputs
        y_scaled = self.scaler_y.fit_transform(y)

        # Dividir datos
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

        # Entrenar modelos
        self.model_elevation.fit(X_train, y_train[:, 0])
        self.model_azimuth.fit(X_train, y_train[:, 1])

        # Evaluar
        y_pred_elev = self.model_elevation.predict(X_test)
        y_pred_azim = self.model_azimuth.predict(X_test)

        y_pred = np.column_stack((y_pred_elev, y_pred_azim))
        y_test_descaled = self.scaler_y.inverse_transform(y_test)
        y_pred_descaled = self.scaler_y.inverse_transform(y_pred)

        mse = mean_squared_error(y_test_descaled, y_pred_descaled)
        r2 = r2_score(y_test_descaled, y_pred_descaled)

        print(f"MSE: {mse:.2f}")
        print(f"R²: {r2:.2f}")

        return mse, r2

    def predict(self, tiempo, irradiancia):
        X = np.array([[tiempo, irradiancia]])
        X_scaled = self.scaler_X.transform(X)

        elev_pred = self.model_elevation.predict(X_scaled)[0]
        azim_pred = self.model_azimuth.predict(X_scaled)[0]

        y_pred_scaled = np.array([[elev_pred, azim_pred]])
        y_pred = self.scaler_y.inverse_transform(y_pred_scaled)[0]

        return {'elevation': y_pred[0], 'azimuth': y_pred[1]}

    def save_model(self, filepath):
        joblib.dump({
            'scaler_X': self.scaler_X,
            'scaler_y': self.scaler_y,
            'model_elevation': self.model_elevation,
            'model_azimuth': self.model_azimuth
        }, filepath)

    def load_model(self, filepath):
        models = joblib.load(filepath)
        self.scaler_X = models['scaler_X']
        self.scaler_y = models['scaler_y']
        self.model_elevation = models['model_elevation']
        self.model_azimuth = models['model_azimuth']

if __name__ == "__main__":
    predictor = SolarPositionPredictor()
    X, y = predictor.load_data('Attached-Assets/data/ejemplo_con_posicion.csv')
    predictor.train(X, y)
    predictor.save_model('models/solar_position_predictor.pkl')

    # Ejemplo de predicción
    result = predictor.predict(12, 850)  # Mediodía, alta irradiancia
    print(f"Predicción para tiempo=12, irradiancia=850: {result}")