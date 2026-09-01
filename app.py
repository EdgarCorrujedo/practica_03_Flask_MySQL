import os
from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# Configuración de conexión a MySQL
# Utiliza variables de entorno para Render o valores por defecto para pruebas locales
MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
MYSQL_DB = os.environ.get('MYSQL_DB', 'practica03_db')
MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))

def get_db_connection():
    return pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        port=MYSQL_PORT,
        autocommit=True
    )

# Crear la tabla de alumnos si no existe
def init_db():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alumnos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    fecha_nacimiento DATE NOT NULL,
                    pasatiempos TEXT,
                    me_gusta VARCHAR(100) NOT NULL
                )
            ''')
        conn.close()
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")

# Inicializar tabla al arrancar la app
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/saludar', methods=['POST'])
def saludar():
    nombre = request.form.get('nombre')
    fecha_nacimiento = request.form.get('fecha_nacimiento')
    pasatiempos_lista = request.form.getlist('pasatiempos')
    pasatiempos = ", ".join(pasatiempos_lista)
    me_gusta = request.form.get('me_gusta')

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "INSERT INTO alumnos (nombre, fecha_nacimiento, pasatiempos, me_gusta) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nombre, fecha_nacimiento, pasatiempos, me_gusta))
        conn.close()
    except Exception as e:
        print(f"Error al guardar los datos: {e}")

    return redirect(url_for('alumnos'))

@app.route('/alumnos')
def alumnos():
    lista_alumnos = []
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, nombre, fecha_nacimiento, pasatiempos, me_gusta FROM alumnos")
            lista_alumnos = cursor.fetchall()
        conn.close()
    except Exception as e:
        print(f"Error al consultar los datos: {e}")

    return render_template('lista_alumnos.html', alumnos=lista_alumnos)

if __name__ == '__main__':
    app.run(debug=True)
