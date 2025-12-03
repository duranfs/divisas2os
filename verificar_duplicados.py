import sqlite3

conn = sqlite3.connect(r'applications\divisas2os\databases\storage.sqlite')
cursor = conn.cursor()

cursor.execute('''
    SELECT cliente_id, moneda, COUNT(*) as cnt 
    FROM cuentas 
    WHERE estado='activa' 
    GROUP BY cliente_id, moneda 
    HAVING COUNT(*) > 1
''')

duplicados = cursor.fetchall()
print(f'Cuentas duplicadas: {len(duplicados)}')
for row in duplicados:
    print(f'Cliente {row[0]}, Moneda {row[1]}: {row[2]} cuentas')

conn.close()
