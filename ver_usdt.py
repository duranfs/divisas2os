import sqlite3

db_path = r'C:\web2py\applications\divisas2os\databases\storage.sqlite'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT id, usd_ves, usdt_ves, eur_ves, activa FROM tasas_cambio WHERE activa = 1")
activa = cursor.fetchone()

if activa:
    print("Tasa activa:")
    print("ID:", activa[0])
    print("USD/VES:", activa[1])
    print("USDT/VES:", activa[2])
    print("EUR/VES:", activa[3])
    
    if activa[2] is None or activa[2] == 0:
        print("\nActualizando USDT a 241.76...")
        cursor.execute("UPDATE tasas_cambio SET usdt_ves = 241.76 WHERE id = ?", (activa[0],))
        conn.commit()
        print("Actualizado!")

conn.close()
