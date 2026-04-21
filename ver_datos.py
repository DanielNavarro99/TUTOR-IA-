import sqlite3

conexion = sqlite3.connect("tutor.db")
cursor = conexion.cursor()

cursor.execute("SELECT * FROM interacciones")

datos = cursor.fetchall()

for fila in datos:
    print(fila)

conexion.close()