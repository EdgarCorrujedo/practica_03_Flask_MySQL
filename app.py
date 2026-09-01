import os
import pymysql
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        database=os.environ.get('DB_NAME'),
        port=int(os.environ.get('DB_PORT', 18781)),
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    nombre = request.form.get('nombre')
    fecha_nacimiento = request.form.get('fecha_nacimiento')
    pasatiempos = request.form.getlist('pasatiempos')
    gustos = request.form.get('gustos')
    
    pasatiempos_str = ", ".join(pasatiempos)

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO alumnos (nombre, fecha_nacimiento, pasatiempos, gustos) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nombre, fecha_nacimiento, pasatiempos_str, gustos))
        connection.commit()
    finally:
        connection.close()

    return redirect(url_for('ver_alumnos'))

# RUTA CORREGIDA PARA EL ENLACE /alumnos
@app.route('/alumnos')
def ver_alumnos():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM alumnos")
            alumnos = cursor.fetchall()
        return render_template('alumnos.html', alumnos=alumnos)
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
