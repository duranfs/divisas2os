#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para integrar el logo real de R4 Banco Microfinanciero
"""

def actualizar_componente_logo_real():
    """Actualizar el componente para usar el logo real"""
    
    html_logo_real = """
<!-- Logo Real R4 Banco Microfinanciero -->
<a href="{{=URL('default','index')}}" class="navbar-brand d-flex align-items-center">
    <img src="{{=URL('static','images/logo-r4-real.png')}}" 
         alt="R4 Banco Microfinanciero" 
         class="logo-r4-real me-2"
         style="height: 40px; width: auto;">
    <div class="logo-text d-none d-md-block">
        <div class="logo-title">Sistema de Divisas</div>
        <div class="logo-subtitle">R4 Banco Microfinanciero</div>
    </div>
</a>
"""
    
    # Escribir componente actualizado
    with open("views/_logo_r4_real.html", 'w', encoding='utf-8') as f:
        f.write(html_logo_real)
    
    print("✅ Componente del logo real creado: views/_logo_r4_real.html")

def crear_css_logo_real():
    """Crear CSS para el logo real"""
    
    css_logo_real = """
/* Estilos para el logo real de R4 Banco Microfinanciero */
.navbar-brand {
    text-decoration: none !important;
    transition: all 0.3s ease;
}

.navbar-brand:hover {
    transform: translateY(-1px);
    text-decoration: none !important;
}

.logo-r4-real {
    max-height: 40px;
    width: auto;
    transition: all 0.3s ease;
    filter: brightness(1);
}

.logo-r4-real:hover {
    filter: brightness(1.1);
}

.logo-text {
    display: flex;
    flex-direction: column;
    line-height: 1.2;
}

.logo-title {
    font-size: 14px;
    font-weight: 600;
    color: #ffffff;
    margin: 0;
}

.logo-subtitle {
    font-size: 11px;
    font-weight: 400;
    color: #ffa366;
    margin: 0;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .logo-r4-real {
        max-height: 35px;
    }
    
    .logo-text {
        display: none !important;
    }
}

@media (max-width: 576px) {
    .logo-r4-real {
        max-height: 30px;
    }
}

/* Para el footer */
.footer-logo {
    height: 25px;
    width: auto;
    vertical-align: middle;
    margin-right: 8px;
}

/* Variante para sidebar si se necesita */
.sidebar .logo-r4-real {
    max-height: 35px;
    display: block;
    margin: 0 auto 15px auto;
}
"""
    
    # Escribir CSS
    with open("static/css/logo-r4-real.css", 'w', encoding='utf-8') as f:
        f.write(css_logo_real)
    
    print("✅ CSS del logo real creado: static/css/logo-r4-real.css")

def crear_instrucciones_logo():
    """Crear instrucciones para subir el logo"""
    
    instrucciones = """
# INSTRUCCIONES PARA INTEGRAR EL LOGO REAL DE R4

## 📋 PASOS PARA COMPLETAR LA INTEGRACIÓN

### 1. Subir el Logo
1. Guarda tu imagen del logo como: `static/images/logo-r4-real.png`
2. Formatos recomendados: PNG (preferido) o JPG
3. Tamaño recomendado: 200x60 píxeles aproximadamente
4. Fondo transparente (si es PNG)

### 2. Actualizar Layout
El script ya preparó los archivos necesarios:
- ✅ `views/_logo_r4_real.html` - Componente del logo
- ✅ `static/css/logo-r4-real.css` - Estilos del logo

### 3. Aplicar Cambios
Ejecuta: `python aplicar_logo_real.py`

## 🎨 CARACTERÍSTICAS DEL LOGO INTEGRADO

- **Responsive**: Se adapta a diferentes tamaños de pantalla
- **Hover Effects**: Efectos suaves al pasar el mouse
- **Texto Complementario**: "Sistema de Divisas" junto al logo
- **Footer**: Logo también en el pie de página
- **Optimizado**: Carga rápida y buena calidad

## 📱 COMPORTAMIENTO RESPONSIVE

- **Desktop**: Logo + texto completo
- **Tablet**: Logo + texto reducido  
- **Móvil**: Solo logo, sin texto

## 🔧 PERSONALIZACIÓN

Si necesitas ajustar el tamaño del logo, edita en `logo-r4-real.css`:

```css
.logo-r4-real {
    max-height: 40px; /* Cambia este valor */
}
```

## ✅ VERIFICACIÓN

Después de subir el logo:
1. Inicia web2py
2. Ve a tu aplicación
3. Verifica que el logo aparece en:
   - Barra de navegación superior
   - Footer (versión pequeña)
   - Todas las páginas del sistema

¡Tu logo de R4 Banco Microfinanciero estará perfectamente integrado!
"""
    
    with open("INSTRUCCIONES_LOGO_R4.md", 'w', encoding='utf-8') as f:
        f.write(instrucciones)
    
    print("✅ Instrucciones creadas: INSTRUCCIONES_LOGO_R4.md")

def crear_script_aplicacion():
    """Crear script para aplicar los cambios del logo real"""
    
    script_aplicacion = """#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def aplicar_logo_real():
    print("🎨 Aplicando logo real de R4 Banco Microfinanciero...")
    
    # Verificar que el logo existe
    if not os.path.exists("static/images/logo-r4-real.png"):
        print("❌ ERROR: No se encontró static/images/logo-r4-real.png")
        print("📋 Por favor:")
        print("1. Guarda tu logo como: static/images/logo-r4-real.png")
        print("2. Ejecuta este script nuevamente")
        return False
    
    # Leer layout actual
    try:
        with open("views/layout.html", 'r', encoding='utf-8') as f:
            layout_content = f.read()
    except Exception as e:
        print(f"❌ Error leyendo layout.html: {e}")
        return False
    
    # Actualizar CSS en layout
    if "logo-r4-real.css" not in layout_content:
        layout_content = layout_content.replace(
            'logo-r4.css',
            'logo-r4-real.css'
        )
        print("✅ CSS actualizado en layout.html")
    
    # Actualizar componente del logo
    if "_logo_r4.html" in layout_content:
        layout_content = layout_content.replace(
            "_logo_r4.html",
            "_logo_r4_real.html"
        )
        print("✅ Componente del logo actualizado")
    
    # Escribir layout actualizado
    try:
        with open("views/layout.html", 'w', encoding='utf-8') as f:
            f.write(layout_content)
        print("✅ Layout.html actualizado exitosamente")
    except Exception as e:
        print(f"❌ Error escribiendo layout.html: {e}")
        return False
    
    return True

def verificar_integracion():
    archivos_necesarios = [
        "static/images/logo-r4-real.png",
        "static/css/logo-r4-real.css", 
        "views/_logo_r4_real.html"
    ]
    
    print("\\n🔍 Verificando integración...")
    
    todos_ok = True
    for archivo in archivos_necesarios:
        if os.path.exists(archivo):
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo} - FALTANTE")
            todos_ok = False
    
    if todos_ok:
        print("\\n🟢 INTEGRACIÓN COMPLETA")
        print("🚀 Inicia web2py para ver tu logo de R4!")
    else:
        print("\\n🟡 INTEGRACIÓN INCOMPLETA")
        print("Revisa los archivos faltantes.")
    
    return todos_ok

if __name__ == "__main__":
    print("="*60)
    print("🎨 APLICANDO LOGO REAL R4 BANCO MICROFINANCIERO")
    print("="*60)
    
    if aplicar_logo_real():
        verificar_integracion()
    else:
        print("\\n❌ No se pudo completar la aplicación del logo")
"""
    
    with open("aplicar_logo_real.py", 'w', encoding='utf-8') as f:
        f.write(script_aplicacion)
    
    print("✅ Script de aplicación creado: aplicar_logo_real.py")

if __name__ == "__main__":
    print("🎨 PREPARANDO INTEGRACIÓN DEL LOGO REAL R4")
    print("="*50)
    
    actualizar_componente_logo_real()
    crear_css_logo_real()
    crear_instrucciones_logo()
    crear_script_aplicacion()
    
    print("\\n✅ PREPARACIÓN COMPLETA")
    print("\\n📋 PRÓXIMOS PASOS:")
    print("1. Guarda tu logo como: static/images/logo-r4-real.png")
    print("2. Ejecuta: python aplicar_logo_real.py")
    print("3. Inicia web2py para ver el resultado")
    print("\\n📖 Lee: INSTRUCCIONES_LOGO_R4.md para más detalles")