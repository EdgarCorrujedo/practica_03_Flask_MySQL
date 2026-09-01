import pymysql
import os

def borrar():
    connection = pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=int(os.getenv('DB_PORT', 3306)),
        ssl={'ssl': {'reject_unauthorized': False}}
    )
    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE alumnos")
    connection.commit()
    connection.close()
    print("TABLA BORRADA CORRECTAMENTE")

if __name__ == "__main__":
    borrar()
