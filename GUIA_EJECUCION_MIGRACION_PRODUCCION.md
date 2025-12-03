# Guía de Ejecución de Migración en Producción

## Sistema de Divisas Bancario - Migración de Cuentas Multi-Moneda

**Fecha:** 2025-11-25  
**Versión:** 1.0  
**Estado:** Listo para Producción

---

## 📋 Resumen Ejecutivo

Esta guía describe el proceso completo para ejecutar la migración del sistema de cuentas multi-moneda (una cuenta con múltiples saldos) al nuevo modelo bancario tradicional (una cuenta por moneda).

### Cambios Principales

- **Antes:** Una cuenta con campos `saldo_ves`, `saldo_usd`, `saldo_eur`, `saldo_usdt`
- **Después:** Múltiples cuentas por cliente, cada una con un campo `moneda` y un campo `saldo`

---

## ⚠️ ADVERTENCIAS IMPORTANTES

1. **BACKUP OBLIGATORIO:** Se realizará backup automático, pero se recomienda tener un backup manual adicional
2. **DOWNTIME:** Se recomienda detener el servidor durante la migración (estimado: 5-10 minutos)
3. **USUARIOS:** Asegurarse de que no haya usuarios conectados durante la migración
4. **REVERSIÓN:** En caso de problemas, se puede restaurar el backup

---

## 📦 Pre-requisitos

### Verificar antes de comenzar:

- [ ] Servidor web2py funcionando correctamente
- [ ] Base de datos `storage.sqlite` accesible
- [ ] Espacio en disco suficiente (mínimo 2x tamaño de BD)
- [ ] Permisos de escritura en directorio `backups/`
- [ ] Python y web2py configurados correctamente

### Archivos necesarios:

- `migrar_cuentas.py` - Script principal de migración
- `backup_bd_antes_migracion.py` - Script de backup
- `ejecutar_migracion_produccion.py` - Script de ejecución completa
- `validar_migracion_completa.py` - Script de validación post-migración

---

## 🚀 Proceso de Migración

### PASO 1: Preparación (5 minutos)

#### 1.1 Detener el servidor (RECOMENDADO)

```bash
# Si está usando el servidor de desarrollo
# Presionar Ctrl+C en la terminal donde corre web2py

# Si está usando un servidor de producción (Apache/Nginx)
# Detener el servicio correspondiente
```

#### 1.2 Verificar estado actual

```bash
# Navegar al directorio de web2py
cd C:\web2py

# Verificar que la base de datos existe
dir applications\sistema_divisas\databases\storage.sqlite
```

#### 1.3 Backup manual (OPCIONAL pero RECOMENDADO)

```bash
# Crear backup manual adicional
copy applications\sistema_divisas\databases\storage.sqlite applications\sistema_divisas\backups\storage_manual_backup.sqlite
```

---

### PASO 2: Ejecución de Migración (5-10 minutos)

#### Opción A: Ejecución Completa Automatizada (RECOMENDADO)

```bash
python web2py.py -S sistema_divisas -M -R applications/sistema_divisas/ejecutar_migracion_produccion.py
```

Este script ejecuta automáticamente:
1. ✅ Backup completo de la base de datos
2. ✅ Migración de cuentas
3. ✅ Validación de integridad de datos
4. ✅ Verificación de cuentas creadas
5. ✅ Generación de reporte completo

**Confirmación requerida:** El script solicitará confirmación antes de realizar cambios permanentes.

#### Opción B: Ejecución Paso a Paso (Para mayor control)

**Paso 2.1: Backup**

```bash
python applications\sistema_divisas\backup_bd_antes_migracion.py
```

**Paso 2.2: Migración**

```bash
python web2py.py -S sistema_divisas -M -R applications/sistema_divisas/migrar_cuentas.py
```

El script mostrará:
- Simulación de la migración (dry-run)
- Solicitud de confirmación
- Ejecución real de la migración
- Validación automática
- Reporte detallado

**Paso 2.3: Validación**

```bash
python web2py.py -S sistema_divisas -M -R applications/sistema_divisas/validar_migracion_completa.py
```

---

### PASO 3: Verificación Post-Migración (2-3 minutos)

#### 3.1 Revisar reportes generados

Los scripts generan reportes automáticos:

- `reporte_migracion_produccion_YYYYMMDD_HHMMSS.txt` - Reporte completo de migración
- `validacion_migracion_YYYYMMDD_HHMMSS.txt` - Reporte de validación

**Ubicación:** Directorio raíz de la aplicación

#### 3.2 Verificar estadísticas clave

El reporte debe mostrar:

```
✅ Cuentas procesadas: [número]
✅ Cuentas creadas: [número]
✅ Saldos totales coinciden
✅ No hay números de cuenta duplicados
✅ Todos los clientes tienen cuenta VES
```

#### 3.3 Verificar en la base de datos (OPCIONAL)

```bash
# Abrir consola de web2py
python web2py.py -S sistema_divisas -M

# Ejecutar consultas de verificación
>>> db(db.cuentas.id > 0).count()  # Total de cuentas
>>> db(db.cuentas.moneda == 'VES').count()  # Cuentas VES
>>> db(db.cuentas.moneda == 'USD').count()  # Cuentas USD
```

---

### PASO 4: Reiniciar Sistema (1 minuto)

#### 4.1 Reiniciar servidor web2py

```bash
# Servidor de desarrollo
python web2py.py -a <password> -i 127.0.0.1 -p 8000

# O servidor de producción
# Iniciar el servicio correspondiente
```

#### 4.2 Verificar acceso

```
http://127.0.0.1:8000/sistema_divisas
```

#### 4.3 Pruebas funcionales básicas

- [ ] Login de usuario
- [ ] Visualización de dashboard de cuentas
- [ ] Consulta de saldo por cuenta
- [ ] Creación de nueva cuenta (opcional)

---

## 📊 Resultados Esperados

### Estructura de Cuentas

**Antes de la migración:**
```
Cliente 1 → Cuenta 12345678901234567890
            ├─ saldo_ves: 1000.00
            ├─ saldo_usd: 50.00
            ├─ saldo_eur: 0.00
            └─ saldo_usdt: 0.00
```

**Después de la migración:**
```
Cliente 1 → Cuenta VES 0112345678901234567890 (saldo: 1000.00)
         → Cuenta USD 0298765432109876543210 (saldo: 50.00)
```

### Números de Cuenta

- **VES:** Prefijo `01` + 18 dígitos (mantiene número original)
- **USD:** Prefijo `02` + 18 dígitos (nuevo número generado)
- **EUR:** Prefijo `03` + 18 dígitos (nuevo número generado)
- **USDT:** Prefijo `04` + 18 dígitos (nuevo número generado)

### Validaciones Automáticas

El sistema valida:

1. ✅ Saldos totales coinciden antes y después
2. ✅ No se pierden datos
3. ✅ Cada cliente tiene al menos una cuenta VES
4. ✅ No hay cuentas duplicadas por cliente y moneda
5. ✅ Todos los números de cuenta son únicos
6. ✅ Todos los prefijos son correctos

---

## 🔧 Solución de Problemas

### Problema: "Error al agregar columnas"

**Causa:** Las columnas `moneda` y `saldo` ya existen  
**Solución:** Esto es normal, el script continúa automáticamente

### Problema: "Diferencia en saldos"

**Causa:** Inconsistencia en los datos  
**Solución:** 
1. Revisar el reporte detallado
2. Verificar transacciones recientes
3. Si la diferencia es < 0.01, es aceptable (redondeo)

### Problema: "Números de cuenta duplicados"

**Causa:** Colisión en generación aleatoria (muy raro)  
**Solución:** 
1. El script reintenta automáticamente
2. Si persiste, revisar el código de generación

### Problema: "Cliente sin cuenta VES"

**Causa:** Error en la lógica de migración  
**Solución:**
1. Revisar el cliente específico en el reporte
2. Crear cuenta VES manualmente si es necesario

---

## 🔄 Plan de Reversión

### Si la migración falla o hay problemas críticos:

#### Opción 1: Restaurar desde backup automático

```bash
# Detener el servidor
# Ctrl+C o detener servicio

# Restaurar backup
copy applications\sistema_divisas\backups\storage_antes_migracion_produccion_YYYYMMDD_HHMMSS.sqlite applications\sistema_divisas\databases\storage.sqlite

# Reiniciar servidor
python web2py.py -a <password> -i 127.0.0.1 -p 8000
```

#### Opción 2: Restaurar desde backup manual

```bash
# Detener el servidor
# Restaurar backup manual
copy applications\sistema_divisas\backups\storage_manual_backup.sqlite applications\sistema_divisas\databases\storage.sqlite

# Reiniciar servidor
```

---

## 📝 Checklist de Ejecución

### Antes de la migración:
- [ ] Backup manual realizado
- [ ] Servidor detenido (recomendado)
- [ ] No hay usuarios conectados
- [ ] Espacio en disco verificado

### Durante la migración:
- [ ] Script de migración ejecutado
- [ ] Confirmación proporcionada
- [ ] Sin errores críticos
- [ ] Reporte generado

### Después de la migración:
- [ ] Validación ejecutada exitosamente
- [ ] Reportes revisados
- [ ] Estadísticas verificadas
- [ ] Servidor reiniciado
- [ ] Pruebas funcionales realizadas

---

## 📞 Contacto y Soporte

**Desarrollador:** Sistema de Divisas Bancario  
**Fecha de creación:** 2025-11-25  
**Versión del sistema:** 1.0

### Archivos de log:

- `reporte_migracion_produccion_*.txt` - Reporte completo
- `validacion_migracion_*.txt` - Validación post-migración
- `databases/sql.log` - Log de consultas SQL

---

## ✅ Conclusión

Esta migración es un cambio estructural importante pero seguro. Los scripts incluyen:

- ✅ Backups automáticos
- ✅ Validaciones exhaustivas
- ✅ Reportes detallados
- ✅ Capacidad de reversión
- ✅ Confirmación antes de cambios permanentes

**Tiempo estimado total:** 15-20 minutos  
**Downtime recomendado:** 10-15 minutos  
**Nivel de riesgo:** Bajo (con backups y validaciones)

---

**¡Buena suerte con la migración!** 🚀
