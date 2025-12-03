# -*- coding: utf-8 -*-
"""
Verificar configuración de acceso administrativo
"""

print("=" * 80)
print("VERIFICACIÓN DE ACCESO ADMINISTRATIVO")
print("=" * 80)

# Verificar configuración de appconfig
import os

appconfig_path = "private/appconfig.ini"

if os.path.exists(appconfig_path):
    print(f"\n✓ Archivo de configuración encontrado: {appconfig_path}")
    
    with open(appconfig_path, 'r') as f:
        content = f.read()
        
    # Buscar configuraciones relevantes
    if 'security' in content.lower():
        print("\n📋 Configuración de seguridad:")
        for line in content.split('\n'):
            if 'security' in line.lower() or 'admin' in line.lower():
                print(f"  {line}")
else:
    print(f"\n⚠️  No se encontró {appconfig_path}")

# Verificar si hay password de admin configurado
admin_password_file = "../../parameters_8000.py"
if os.path.exists(admin_password_file):
    print(f"\n✓ Archivo de password admin encontrado")
else:
    print(f"\n⚠️  No se encontró archivo de password admin")

print("\n" + "=" * 80)
print("ACCESO A LA INTERFAZ ADMINISTRATIVA")
print("=" * 80)
print("\nPara acceder a los tickets de error:")
print("1. Ir a: http://127.0.0.1:8000/admin")
print("2. Password: admin123")
print("3. Click en 'divisas2os_multiple'")
print("4. Click en 'errors' en el menú lateral")
print("\nSi aparece '403 FORBIDDEN', es porque:")
print("- El servidor no está en modo desarrollo")
print("- O necesitas acceder desde localhost")
print("\nAlternativamente, usa el script:")
print("  python leer_tickets_error.py")
print("=" * 80)
