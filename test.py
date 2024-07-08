import mysql.connector
import time
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# Configura la conexión a la base de datos
config = {
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'database': os.getenv("DB_NAME"),
}

# Conectar a la base de datos
conn = mysql.connector.connect(**config)
cursor = conn.cursor()


# Función para insertar la fecha y hora actual
def insertar_fecha_hora():
    while True:
        # Obtiene la fecha y hora actual
        fecha_hora_actual = datetime.now()
        cursor.execute("FLUSH HOSTS")
        
        # Inserta en la base de datos
        cursor.execute("INSERT INTO fechasyhoras (date) VALUES (%s)", (fecha_hora_actual,))
        conn.commit()
        
        print(f"Insertado: {fecha_hora_actual}")
        
        # Espera 5 segundos antes de la siguiente inserción
        time.sleep(5)

try:
    insertar_fecha_hora()
except KeyboardInterrupt:
    print("Programa interrumpido por el usuario")
finally:
    cursor.close()
    conn.close()
