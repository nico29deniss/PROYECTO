import mysql.connector
from mysql.connector import Error

# --- Configuración de la base de datos ---
config = {
    'host': 'localhost',
    'user': 'root',                
    'password': '',                
    'database': 'heladeriasdb', 
    'port': 3308                   
}

def get_db_connection():
    """
    Establece y retorna la conexión a la base de datos MySQL.
    Si falla, retorna None y muestra el error.
    """
    try:
        conn = mysql.connector.connect(**config)
        return conn
    except Error as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        return None

def cerrar_conexion(conn):
    """
    Cierra la conexión a la base de datos si está abierta.
    """
    if conn and conn.is_connected():
        conn.close()
        # print("Conexión a la base de datos cerrada.")

# Este bloque se usa para probar la conexión
if __name__ == "__main__":
    conn_test = get_db_connection()
    if conn_test:
        print("¡Prueba de conexión exitosa! 🎉")
        cerrar_conexion(conn_test)