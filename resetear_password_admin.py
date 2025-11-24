# -*- coding: utf-8 -*-
"""
Script para resetear la contraseña de un usuario
Útil cuando olvidas tu contraseña de administrador
"""

import sqlite3
import hashlib
import uuid

def resetear_password():
    print("=" * 70)
    print("RESETEAR CONTRASEÑA DE USUARIO")
    print("=" * 70)
    
    conn = sqlite3.connect('databases/storage.sqlite')
    cursor = conn.cursor()
    
    # 1. Listar usuarios disponibles
    print("\n1️⃣ USUARIOS DISPONIBLES:")
    print("-" * 70)
    
    cursor.execute("""
        SELECT id, email, first_name, last_name
        FROM auth_user
        ORDER BY id
    """)
    
    usuarios = cursor.fetchall()
    
    if not usuarios:
        print("❌ No hay usuarios en la base de datos")
        conn.close()
        return
    
    for usuario in usuarios:
        id_user, email, nombre, apellido = usuario
        print(f"{id_user}. {nombre} {apellido} ({email})")
    
    # 2. Seleccionar usuario
    print("\n" + "=" * 70)
    user_id = input("\n¿ID del usuario para resetear contraseña? ")
    
    try:
        user_id = int(user_id)
    except:
        print("❌ ID inválido")
        conn.close()
        return
    
    # Verificar que el usuario existe
    cursor.execute("SELECT email, first_name, last_name FROM auth_user WHERE id = ?", (user_id,))
    usuario = cursor.fetchone()
    
    if not usuario:
        print(f"❌ Usuario con ID {user_id} no encontrado")
        conn.close()
        return
    
    email, nombre, apellido = usuario
    
    # 3. Solicitar nueva contraseña
    print("\n" + "=" * 70)
    print(f"\n📧 Usuario: {nombre} {apellido} ({email})")
    nueva_password = input("\n¿Nueva contraseña? (mínimo 6 caracteres): ")
    
    if len(nueva_password) < 6:
        print("❌ La contraseña debe tener al menos 6 caracteres")
        conn.close()
        return
    
    confirmar = input("Confirmar contraseña: ")
    
    if nueva_password != confirmar:
        print("❌ Las contraseñas no coinciden")
        conn.close()
        return
    
    # 4. Generar hash de la contraseña usando el método de web2py
    # Formato: pbkdf2(1000,20,sha512)$salt$hash
    salt = str(uuid.uuid4()).replace('-', '')[:16]
    
    # Usar PBKDF2 con SHA512
    import hashlib
    key = hashlib.pbkdf2_hmac('sha512', nueva_password.encode('utf-8'), salt.encode('utf-8'), 1000, dklen=20)
    hash_hex = key.hex()
    
    password_hash = f"pbkdf2(1000,20,sha512)${salt}${hash_hex}"
    
    # 5. Actualizar en la base de datos
    print("\n" + "=" * 70)
    print("\n🔄 Actualizando contraseña...")
    
    cursor.execute("""
        UPDATE auth_user
        SET password = ?
        WHERE id = ?
    """, (password_hash, user_id))
    
    conn.commit()
    
    print(f"\n✅ Contraseña actualizada exitosamente para {nombre} {apellido}")
    print(f"\n📋 INFORMACIÓN DE LOGIN:")
    print(f"   Email: {email}")
    print(f"   Nueva contraseña: {nueva_password}")
    print(f"\n💡 Ahora puedes hacer login con estas credenciales")
    
    print("\n" + "=" * 70)
    
    conn.close()

if __name__ == '__main__':
    try:
        resetear_password()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
