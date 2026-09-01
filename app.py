import os
from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', ''),
        database=os.environ.get('DB_NAME', 'practica03_db'),
        port=int(os.environ.get('DB_PORT', 3306)),
        cursorclass=pymysql.cursors.DictCursor
    )

def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                fecha DATE NOT NULL,
                pasatiempos VARCHAR(255) NOT NULL,
                preferencia VARCHAR(50) NOT NULL
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error al inicializar BD: {e}")

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    nombre = request.form.get('nombre')
    fecha = request.form.get('fecha')
    pasatiempos = request.form.getlist('pasatiempos')
    pasatiempos_str = ", ".join(pasatiempos)
    preferencia = request.form.get('preferencia')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usuarios (nombre, fecha, pasatiempos, preferencia)
        VALUES (%s, %s, %s, %s)
    ''', (nombre, fecha, pasatiempos_str, preferencia))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('lista'))

@app.route('/lista')
def lista():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('lista.html', usuarios=usuarios)

if __name__ == '__main__':
    app.run(debug=True)
