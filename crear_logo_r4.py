#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para crear el logo de R4 Banco Microfinanciero
"""

def crear_logo_css():
    """Crear estilos CSS para el logo"""
    
    css_logo = """
/* Estilos para el logo de R4 Banco Microfinanciero */
.logo-r4 {
    display: inline-flex;
    align-items: center;
    padding: 8px 16px;
    background: linear-gradient(135deg, #1a365d 0%, #2d5a87 100%);
    border-radius: 8px;
    border: 1px solid #2d5a87;
    box-shadow: 0 2px 8px rgba(26, 54, 93, 0.3);
    transition: all 0.3s ease;
    text-decoration: none !important;
}

.logo-r4:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(26, 54, 93, 0.4);
    text-decoration: none !important;
}

.logo-r4-icon {
    display: flex;
    align-items: center;
    margin-right: 12px;
}

.logo-r4-bars {
    display: flex;
    align-items: end;
    gap: 2px;
    margin-right: 8px;
}

.logo-r4-bar {
    border-radius: 1px;
}

.logo-r4-bar-1 {
    width: 3px;
    height: 20px;
    background: #ffa366;
}

.logo-r4-bar-2 {
    width: 3px;
    height: 16px;
    background: #ffd700;
}

.logo-r4-bar-3 {
    width: 3px;
    height: 12px;
    background: #ffa366;
}

.logo-r4-text {
    display: flex;
    flex-direction: column;
    line-height: 1;
}

.logo-r4-main {
    font-size: 18px;
    font-weight: bold;
    color: #ffffff;
    margin: 0;
}

.logo-r4-sub {
    font-size: 10px;
    font-weight: 600;
    color: #ffa366;
    margin: 0;
    margin-top: 2px;
}

.logo-r4-desc {
    font-size: 8px;
    color: #ffd700;
    margin: 0;
    margin-top: 1px;
}

/* Versión compacta para navbar */
.navbar-brand .logo-r4 {
    padding: 4px 12px;
    font-size: 0.9em;
}

.navbar-brand .logo-r4-main {
    font-size: 16px;
}

.navbar-brand .logo-r4-sub {
    font-size: 9px;
}

.navbar-brand .logo-r4-desc {
    font-size: 7px;
}

/* Versión para sidebar */
.sidebar .logo-r4 {
    width: 100%;
    justify-content: center;
    margin-bottom: 20px;
    padding: 12px 8px;
}

/* Responsive */
@media (max-width: 768px) {
    .logo-r4-desc {
        display: none;
    }
    
    .navbar-brand .logo-r4 {
        padding: 4px 8px;
    }
    
    .navbar-brand .logo-r4-main {
        font-size: 14px;
    }
    
    .navbar-brand .logo-r4-sub {
        font-size: 8px;
    }
}

@media (max-width: 576px) {
    .logo-r4-sub {
        display: none;
    }
    
    .logo-r4-bars {
        margin-right: 6px;
    }
}
"""
    
    # Escribir CSS
    with open("static/css/logo-r4.css", 'w', encoding='utf-8') as f:
        f.write(css_logo)
    
    print("✅ CSS del logo creado: static/css/logo-r4.css")

def crear_componente_logo():
    """Crear componente HTML del logo"""
    
    html_logo = """
<!-- Componente del Logo R4 Banco Microfinanciero -->
<a href="{{=URL('default','index')}}" class="logo-r4">
    <div class="logo-r4-icon">
        <div class="logo-r4-bars">
            <div class="logo-r4-bar logo-r4-bar-1"></div>
            <div class="logo-r4-bar logo-r4-bar-2"></div>
            <div class="logo-r4-bar logo-r4-bar-3"></div>
        </div>
    </div>
    <div class="logo-r4-text">
        <div class="logo-r4-main">R4</div>
        <div class="logo-r4-sub">BANCO</div>
        <div class="logo-r4-desc">MICROFINANCIERO</div>
    </div>
</a>
"""
    
    # Escribir componente
    with open("views/_logo_r4.html", 'w', encoding='utf-8') as f:
        f.write(html_logo)
    
    print("✅ Componente del logo creado: views/_logo_r4.html")

if __name__ == "__main__":
    crear_logo_css()
    crear_componente_logo()
    print("\n🎨 Logo de R4 Banco Microfinanciero creado exitosamente!")
    print("📋 Archivos generados:")
    print("- static/images/logo-r4-banco.svg")
    print("- static/css/logo-r4.css") 
    print("- views/_logo_r4.html")
    print("\n🔄 Próximo paso: Actualizar layout.html para incluir el logo")