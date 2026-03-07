import pandas as pd
import numpy as np
from math import sin, cos, asin, atan2, pi, degrees, radians

def calculate_solar_position(hour, doy, latitude, longitude):
    """
    Calcular posición solar aproximada.
    hour: hora del día (0-23)
    doy: día del año (1-365)
    latitude, longitude: en grados
    """
    # Declinación solar (grados)
    delta = 23.45 * sin(2 * pi * (doy - 81) / 365)

    # Ángulo horario (grados)
    omega = 15 * (hour - 12)

    # Elevación (grados)
    lat_rad = radians(latitude)
    delta_rad = radians(delta)
    omega_rad = radians(omega)

    sin_elev = sin(lat_rad) * sin(delta_rad) + cos(lat_rad) * cos(delta_rad) * cos(omega_rad)
    elevation = degrees(asin(max(min(sin_elev, 1), -1)))  # Clamp to [-1,1]

    # Azimut (grados, 0 = Norte, 90 = Este)
    cos_azim = (sin(delta_rad) * cos(lat_rad) - cos(delta_rad) * sin(lat_rad) * cos(omega_rad)) / cos(radians(elevation))
    sin_azim = cos(delta_rad) * sin(omega_rad) / cos(radians(elevation))

    azimuth = degrees(atan2(sin_azim, cos_azim))
    if azimuth < 0:
        azimuth += 360

    return elevation, azimuth

# Parámetros
latitude = 40.0
longitude = -3.0
doy = 172  # Junio

# Leer datos manualmente
with open('Attached-Assets/data/ejemplo.csv', 'r') as f:
    content = f.read()

# Reemplazar \\n por \n
content = content.replace('\\n', '\n')
lines = content.split('\n')
print("lines after replace:", lines)
data = []
for line in lines[1:]:  # Skip header
    if line.strip():
        parts = line.split(',')
        if len(parts) == 2:
            tiempo = float(parts[0])
            intensidad = float(parts[1])
            data.append({'tiempo': tiempo, 'intensidad_luz': intensidad})

print("data:", data)
df = pd.DataFrame(data)
print("DataFrame creado:")
print(df)
print("Columnas:", df.columns)

# Calcular posición para cada tiempo
positions = []
for t in df['tiempo']:
    elev, azim = calculate_solar_position(t, doy, latitude, longitude)
    positions.append((elev, azim))

df['elevation'] = [p[0] for p in positions]
df['azimuth'] = [p[1] for p in positions]

# Guardar
df.to_csv('Attached-Assets/data/ejemplo_con_posicion.csv', index=False)

print("Datos generados:")
print(df)