
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
