# Script para cargar y transformar datos de Ecobici en PostgreSQL

# Dependencias del proyecto:
#   pip install -r requirements.txt
#
# Versión de Python: 3.8+

# Importar librerías necesarias
import os
import glob
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# --- 1. CONFIGURACIÓN DE LA BASE DE DATOS ---
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# --- 2. FUNCIÓN PARA CONECTAR A POSTGRESQL ---
def get_db_connection():
    """Establece y devuelve una conexión a la base de datos."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("✅ Conexión a la base de datos exitosa.")
        return conn
    except psycopg2.OperationalError as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        return None

# --- 3. PROCESAMIENTO Y CARGA DE DATOS ---
def process_and_load_data(conn):
    """Procesa los archivos CSV y los carga en la base de datos."""
    cur = conn.cursor()

    # Ejecutar el script SQL para crear el esquema (esto limpia las tablas cada vez)
    with open('sql/schema.sql', 'r') as f:
        cur.execute(f.read())
    print("🚀 Esquema de base de datos creado/limpiado.")

    # Cargar todos los archivos de recorridos desde la carpeta /data
    path = 'data'
    all_files = glob.glob(os.path.join(path, "badata_ecobici_recorridos_realizados_*.csv"))
    
    all_trips = []
    for f in all_files:
        print(f"Procesando archivo: {f}...")
        df_temp = pd.read_csv(f)
        all_trips.append(df_temp)

    df_trips = pd.concat(all_trips, ignore_index=True)

    # Limpieza y renombrado de columnas, incluyendo las nuevas de lat/lon
    df_trips.rename(columns={
        'id_estacion_origen': 'start_station_id',
        'nombre_estacion_origen': 'start_station_name',
        'lat_estacion_origen': 'start_station_lat',
        'long_estacion_origen': 'start_station_lon',
        'id_estacion_destino': 'end_station_id',
        'nombre_estacion_destino': 'end_station_name',
        'lat_estacion_destino': 'end_station_lat',
        'long_estacion_destino': 'end_station_lon',
        'fecha_origen_recorrido': 'start_time',
        'fecha_destino_recorrido': 'end_time',
        'duracion_recorrido': 'duration_seconds' # Renombramos a segundos para luego convertir a minutos
    }, inplace=True)

    # Convertir a formato de fecha y hora
    df_trips['start_time'] = pd.to_datetime(df_trips['start_time'])
    df_trips['end_time'] = pd.to_datetime(df_trips['end_time'])

    # NUEVO: Convertir duración de segundos a minutos y a tipo entero
    df_trips['duration_minutes'] = (df_trips['duration_seconds'] / 60).astype(int)

    # NUEVO: Extraer estaciones únicas incluyendo sus coordenadas
    # Se extraen las de origen y destino por separado para capturar todas las estaciones
    stations_start = df_trips[['start_station_id', 'start_station_name', 'start_station_lat', 'start_station_lon']].rename(columns={
        'start_station_id': 'id',
        'start_station_name': 'name',
        'start_station_lat': 'latitude',
        'start_station_lon': 'longitude'
    })
    
    stations_end = df_trips[['end_station_id', 'end_station_name', 'end_station_lat', 'end_station_lon']].rename(columns={
        'end_station_id': 'id',
        'end_station_name': 'name',
        'end_station_lat': 'latitude',
        'end_station_lon': 'longitude'
    })
    
    # Se combinan ambas listas y se eliminan duplicados para tener un maestro de estaciones único
    df_stations = pd.concat([stations_start, stations_end]).drop_duplicates(subset=['id']).dropna()
    
    # Cargar estaciones (dim_stations) en la base de datos
    # El bucle ahora insertará latitud y longitud reales
    for index, row in df_stations.iterrows():
        cur.execute(
            "INSERT INTO dim_stations (station_id, station_name, latitude, longitude) VALUES (%s, %s, %s, %s) ON CONFLICT (station_id) DO NOTHING",
            (row['id'], row['name'], row['latitude'], row['longitude'])
        )
    print(f"Cargadas {len(df_stations)} estaciones únicas en la tabla dim_stations.")
    
    # Cargar viajes (fact_trips) en la base de datos
    # Seleccionamos las columnas finales y limpiamos filas con datos nulos
    trips_to_load = df_trips[['start_time', 'end_time', 'duration_minutes', 'start_station_id', 'end_station_id']].dropna()
    for index, row in trips_to_load.iterrows():
        cur.execute(
            "INSERT INTO fact_trips (start_time, end_time, duration_minutes, start_station_id, end_station_id) VALUES (%s, %s, %s, %s, %s)",
            (row['start_time'], row['end_time'], row['duration_minutes'], row['start_station_id'], row['end_station_id'])
        ) 
    print(f"Cargados {len(trips_to_load)} viajes en la tabla fact_trips.")

    # Confirmar los cambios en la base de datos
    conn.commit() # Guardar los cambios
    cur.close() 

# --- 4. EJECUCIÓN PRINCIPAL DEL SCRIPT ---
if __name__ == '__main__':
    conn = get_db_connection()
    if conn:
        process_and_load_data(conn)
        conn.close()
        print("✅ Proceso de carga de datos finalizado con éxito.")