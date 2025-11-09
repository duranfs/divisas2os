#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Diagnóstico simple del formulario de registro de clientes
"""

def diagnosticar_registro():
    """
    Diagnóstica el estado del formulario de registro
    """
    print("=== DIAGNÓSTICO DEL FORMULARIO DE REGISTRO ===")
    
    try:
        print("\n1. Verificando vista registrar.html...")
        
        # Leer el archivo de vista
        with open('views/clientes/registrar.html', 'r', encoding='utf-8') as f:
            vista_content = f.read()
        
        # Verificar elementos clave del formulario
        elementos_requeridos = [
            ('Formulario POST', 'form method="post"'),
            ('Campo Nombres', 'name="first_name"'),
            ('Campo Apellidos', 'name="last_name"'),
            ('Campo Cédula', 'name="cedula"'),
            ('Campo Email', 'name="email"'),
            ('Campo Teléfono', 'name="telefono"'),
            ('Campo Dirección', 'name="direccion"'),
            ('Campo Fecha Nacimiento', 'name="fecha_nacimiento"'),
            ('Campo Contraseña', 'name="password"'),
            ('Campo Confirmar Contraseña', 'name="password_confirm"'),
            ('Botón Submit', 'type="submit"'),
            ('Validación Bootstrap', 'class="form-control"'),
            ('Manejo de Errores', 'form.errors'),
            ('Mensaje de Éxito', 'registro_exitoso')
        ]
        
        elementos_encontrados = 0
        elementos_faltantes = []
        
        for nombre, elemento in elementos_requeridos:
            if elemento in vista_content:
                elementos_encontrados += 1
                print(f"   ✅ {nombre}")
            else:
                elementos_faltantes.append(nombre)
                print(f"   ❌ {nombre}")
        
        print(f"\n   📊 Elementos encontrados: {elementos_encontrados}/{len(elementos_requeridos)}")
        
        print("\n2. Verificando controlador clientes.py...")
        
        # Verificar que existe la función registrar
        with open('controllers/clientes.py', 'r', encoding='utf-8') as f:
            controller_content = f.read()
        
        controller_checks = [
            ('Función registrar', 'def registrar():'),
            ('Decorador login', '@auth.requires_login()'),
            ('Verificación permisos', 'auth.has_membership'),
            ('Validación email', 'request.vars.email'),
            ('Validación cédula', 'request.vars.cedula'),
            ('Validación contraseña', 'request.vars.password'),
            ('Inserción usuario', 'db.auth_user.insert'),
            ('Inserción cliente', 'db.clientes.insert'),
            ('Generación cuenta', 'generar_numero_cuenta'),
            ('Inserción cuenta', 'db.cuentas.insert'),
            ('Manejo errores', 'except Exception'),
            ('Return dict', 'return dict(form=form')
        ]
        
        controller_ok = 0
        for nombre, check in controller_checks:
            if check in controller_content:
                controller_ok += 1
                print(f"   ✅ {nombre}")
            else:
                print(f"   ❌ {nombre}")
        
        print(f"\n   📊 Elementos del controlador: {controller_ok}/{len(controller_checks)}")
        
        print("\n3. Verificando función generar_numero_cuenta()...")
        
        if 'def generar_numero_cuenta():' in controller_content:
            print("   ✅ Función generar_numero_cuenta() encontrada")
            
            # Verificar elementos de la función
            if 'random' in controller_content and '2001' in controller_content:
                print("   ✅ Lógica de generación parece correcta")
            else:
                print("   ⚠️  Lógica de generación puede tener problemas")
        else:
            print("   ❌ Función generar_numero_cuenta() NO encontrada")
        
        print("\n4. Verificando validaciones...")
        
        validaciones = [
            ('Validación email único', 'usuario_existente = db(db.auth_user.email'),
            ('Validación cédula única', 'cedula_existente = db(db.clientes.cedula'),
            ('Validación longitud contraseña', 'len(request.vars.password)'),
            ('Validación confirmación contraseña', 'password != request.vars.password_confirm'),
            ('Validación fecha nacimiento', 'fecha_nacimiento'),
            ('Manejo errores form', 'form.errors')
        ]
        
        validaciones_ok = 0
        for nombre, validacion in validaciones:
            if validacion in controller_content:
                validaciones_ok += 1
                print(f"   ✅ {nombre}")
            else:
                print(f"   ❌ {nombre}")
        
        print(f"\n   📊 Validaciones implementadas: {validaciones_ok}/{len(validaciones)}")
        
        print("\n5. Análisis de posibles problemas...")
        
        # Buscar posibles problemas
        problemas_potenciales = []
        
        if elementos_encontrados < len(elementos_requeridos):
            problemas_potenciales.append("Vista incompleta - faltan elementos del formulario")
        
        if controller_ok < len(controller_checks):
            problemas_potenciales.append("Controlador incompleto - faltan funcionalidades")
        
        if 'def generar_numero_cuenta():' not in controller_content:
            problemas_potenciales.append("Función generar_numero_cuenta() faltante")
        
        # Verificar si hay placeholder text
        if 'Formulario de registro de cliente...' in vista_content:
            problemas_potenciales.append("Vista contiene texto placeholder - no está completamente implementada")
        
        if problemas_potenciales:
            print("   ⚠️  Problemas detectados:")
            for i, problema in enumerate(problemas_potenciales, 1):
                print(f"      {i}. {problema}")
        else:
            print("   ✅ No se detectaron problemas obvios")
        
        print("\n6. Recomendaciones...")
        
        if elementos_encontrados == len(elementos_requeridos) and controller_ok == len(controller_checks):
            print("   ✅ El formulario parece estar completo")
            print("   💡 Si no funciona, verificar:")
            print("      - Permisos de usuario (debe ser admin/operador)")
            print("      - Logs de error en web2py")
            print("      - Consola del navegador para errores JS")
        else:
            print("   🔧 Requiere correcciones:")
            if elementos_encontrados < len(elementos_requeridos):
                print("      - Completar elementos faltantes en la vista")
            if controller_ok < len(controller_checks):
                print("      - Completar funcionalidades faltantes en el controlador")
        
        return elementos_encontrados == len(elementos_requeridos) and controller_ok == len(controller_checks)
        
    except FileNotFoundError as e:
        print(f"❌ Archivo no encontrado: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error durante el diagnóstico: {str(e)}")
        return False

if __name__ == "__main__":
    resultado = diagnosticar_registro()
    print(f"\n{'='*50}")
    if resultado:
        print("🎉 DIAGNÓSTICO: Formulario parece estar completo")
    else:
        print("🔧 DIAGNÓSTICO: Formulario requiere correcciones")
    print(f"{'='*50}")