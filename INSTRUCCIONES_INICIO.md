# 🚀 Instrucciones de Inicio - Sistema de Divisas

## Archivos de Inicio Disponibles

### ✅ **iniciar_sistema_divisas_auto.bat** (RECOMENDADO)
**Uso:** Doble clic para iniciar
- Detecta automáticamente Python del sistema
- Verifica que todo esté configurado correctamente
- Muestra mensajes de error claros si algo falla
- **Mejor opción para la mayoría de usuarios**

### 🌐 **iniciar_sistema_divisas_navegador.bat**
**Uso:** Doble clic para iniciar con navegador
- Inicia el servidor automáticamente
- Abre el navegador en la aplicación
- Ideal para uso diario rápido

### 📝 **iniciar_sistema_divisas.bat**
**Uso:** Inicio básico
- Versión simple sin extras
- Solo inicia el servidor

### 🏢 **iniciar_sistema_divisas_produccion.bat**
**Uso:** Para entorno de producción
- Permite acceso desde otras computadoras en la red
- **IMPORTANTE:** Cambiar contraseña antes de usar
- Solo para uso en red local segura

## 🔧 Configuración

### Cambiar Puerto
Edita el archivo .bat y modifica:
```batch
-p 8000
```
Por ejemplo, para puerto 9000:
```batch
-p 9000
```

### Cambiar Contraseña de Admin
Edita el archivo .bat y modifica:
```batch
-a admin123
```
Por una contraseña segura:
```batch
-a MiPasswordSeguro2025!
```

### Permitir Acceso desde Otras Computadoras
Cambia:
```batch
-i 127.0.0.1
```
Por:
```batch
-i 0.0.0.0
```

## 🌐 URLs de Acceso

Después de iniciar el servidor:

- **Aplicación Principal:** http://127.0.0.1:8000/divisas2os
- **Panel Admin:** http://127.0.0.1:8000/admin
- **Documentación API:** http://127.0.0.1:8000/divisas2os/api

## ❌ Solución de Problemas

### Error: "Python no está instalado"
1. Instala Python desde: https://www.python.org/downloads/
2. Durante la instalación, marca "Add Python to PATH"
3. Reinicia la computadora

### Error: "No se encuentra web2py.py"
1. Verifica que web2py esté en `C:\web2py`
2. Si está en otra ubicación, edita la ruta en el archivo .bat

### Error: "ModuleNotFoundError: No module named 'encodings'"
- Este error se soluciona con los nuevos archivos .bat
- Usan el Python del sistema en lugar del embebido

### Puerto ya en uso
1. Cierra cualquier instancia anterior de web2py
2. O cambia el puerto en el archivo .bat

## 🛑 Detener el Servidor

- Presiona `Ctrl+C` en la ventana del servidor
- O simplemente cierra la ventana

## 📞 Soporte

Para más ayuda, consulta la documentación completa en:
`documentacion_tesis/README.md`
