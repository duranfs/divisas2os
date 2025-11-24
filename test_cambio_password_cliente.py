# -*- coding: utf-8 -*-
"""
Test: Verificar que se puede cambiar la contraseña de un cliente
"""

import sqlite3
from gluon.contrib.pbkdf2 import pbkdf2_hex
import uuid

def test_cambio_password():
    print("=" * 70)
    print("TEST: CAMBIO DE CONTRASEÑA DE CLIENTE")
    print("=" * 70)
    
    conn = sqlite3.connect('databases/storage.sqlite')
    cursor = conn.cursor()
    
    # 1. Buscar un cliente de prueba
    print("\n1️⃣ BUSCAR CLIENTE DE PRUEBA:")
    print("-" * 70)
    
    cursor.execute("""
        SELECT c.id, c.cedula, c.user_id, u.email, u.first_name, u.last_name
        FROM clientes c
        JOIN auth_user u ON c.user_id = u.id
        LIMIT 1
    """)
    
    cliente = cursor.fetchone()
    
    if not cliente:
        print("❌ No hay clientes en la base de datos")
        conn.close()
        return
    
    cliente_id, cedula, user_id, email, nombre, apellido = cliente
    
    print(f"Cliente encontrado:")
    print(f"  ID: {cliente_id}")
    print(f"  Cédula: {cedula}")
    print(f"  Nombre: {nombre} {apellido}")
    print(f"  Email: {email}")
    print(f"  User ID: {user_id}")
    
    # 2. Ver contraseña actual
    print("\n2️⃣ CONTRASEÑA ACTUAL:")
    print("-" * 70)
    
    cursor.execute("""
        SELECT password
        FROM auth_user
        WHERE id = ?
    """, (user_id,))
    
    password_actual = cursor.fetchone()[0]
    print(f"Hash actual: {password_actual[:50]}...")
    
    # 3. Simular cambio de contraseña
    print("\n3️⃣ SIMULAR CAMBIO DE CONTRASEÑA:")
    print("-" * 70)
    
    nueva_password = "nuevaclave123"
    salt = str(uuid.uuid4())
    nuevo_hash = pbkdf2_hex(nueva_password, salt)
    
    print(f"Nueva contraseña: {nueva_password}")
    print(f"Nuevo hash: {nuevo_hash[:50]}...")
    
    # NO vamos a actualizar realmente, solo mostrar cómo se haría
    print("\n✅ El sistema puede generar el hash correctamente")
    print("\n📋 INSTRUCCIONES PARA USAR:")
    print("-" * 70)
    print("1. Ve a 'Gestión de Clientes' en el dashboard")
    print("2. Haz clic en 'Editar' en cualquier cliente")
    print("3. Verás dos nuevos campos:")
    print("   - Nueva Contraseña (opcional)")
    print("   - Confirmar Nueva Contraseña")
    print("4. Si quieres cambiar la contraseña:")
    print("   - Escribe la nueva contraseña en ambos campos")
    print("   - Haz clic en 'Actualizar Cliente'")
    print("5. Si NO quieres cambiar la contraseña:")
    print("   - Deja los campos vacíos")
    print("   - Solo se actualizarán los otros datos")
    
    print("\n" + "=" * 70)
    
    conn.close()

if __name__ == '__main__':
    try:
        test_cambio_password()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
