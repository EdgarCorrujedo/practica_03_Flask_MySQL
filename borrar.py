from app import get_db_connection

def borrar():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE alumnos")
    conn.commit()
    conn.close()
    print("TABLA BORRADA")

if __name__ == "__main__":
    borrar()
