# ✅ Checklist de Migración en Producción

## Sistema de Divisas Bancario - Task 11

**Fecha:** _________________  
**Ejecutado por:** _________________

---

## 📋 PRE-MIGRACIÓN

### Preparación del Entorno

- [ ] Leer `GUIA_EJECUCION_MIGRACION_PRODUCCION.md` completa
- [ ] Leer `REPORTE_MIGRACION_PRODUCCION.md`
- [ ] Verificar que todos los scripts están disponibles:
  - [ ] `migrar_cuentas.py`
  - [ ] `backup_bd_antes_migracion.py`
  - [ ] `ejecutar_migracion_produccion.py`
  - [ ] `validar_migracion_completa.py`
  - [ ] `verificar_estado_pre_migracion.py`
  - [ ] `EJECUTAR_MIGRACION_FINAL.bat`

### Verificación del Sistema

- [ ] Ejecutar verificación pre-migración:
  ```bash
  python web2py.py -S sistema_divisas -M -R verificar_estado_pre_migracion.py
  ```
- [ ] Revisar estadísticas mostradas
- [ ] Anotar totales actuales:
  - Total de cuentas: _________________
  - Total de clientes: _________________
  - Total de transacciones: _________________
  - Saldo total VES: _________________
  - Saldo total USD: _________________
  - Saldo total EUR: _________________
  - Saldo total USDT: _________________

### Backups

- [ ] Verificar backups existentes en `backups/`
- [ ] Crear backup manual adicional (RECOMENDADO):
  ```bash
  copy databases\storage.sqlite backups\storage_manual_YYYYMMDD.sqlite
  ```
- [ ] Verificar espacio en disco disponible
- [ ] Anotar ubicación del backup: _________________

### Preparación del Servidor

- [ ] Notificar a usuarios sobre mantenimiento (si aplica)
- [ ] Detener el servidor web2py (RECOMENDADO):
  - [ ] Presionar Ctrl+C en terminal de desarrollo, O
  - [ ] Detener servicio de producción (Apache/Nginx)
- [ ] Verificar que no hay usuarios conectados
- [ ] Anotar hora de inicio: _________________

---

## 🚀 EJECUCIÓN DE LA MIGRACIÓN

### Opción A: Ejecución Automatizada (RECOMENDADO)

- [ ] Ejecutar script batch:
  ```bash
  EJECUTAR_MIGRACION_FINAL.bat
  ```
- [ ] Revisar mensajes en consola
- [ ] Proporcionar confirmación cuando se solicite (escribir 'SI')
- [ ] Esperar a que termine completamente
- [ ] Anotar hora de finalización: _________________

### Opción B: Ejecución Manual

- [ ] Paso 1: Backup
  ```bash
  python backup_bd_antes_migracion.py
  ```
  - [ ] Verificar que el backup se creó correctamente
  - [ ] Anotar ubicación: _________________

- [ ] Paso 2: Migración
  ```bash
  python web2py.py -S sistema_divisas -M -R ejecutar_migracion_produccion.py
  ```
  - [ ] Revisar simulación
  - [ ] Proporcionar confirmación (escribir 'SI')
  - [ ] Esperar a que termine
  - [ ] Verificar mensaje de éxito

- [ ] Paso 3: Validación
  ```bash
  python web2py.py -S sistema_divisas -M -R validar_migracion_completa.py
  ```
  - [ ] Revisar resultados de validación
  - [ ] Verificar que no hay errores críticos

---

## 📊 POST-MIGRACIÓN

### Revisión de Reportes

- [ ] Localizar reporte de migración: `reporte_migracion_produccion_*.txt`
- [ ] Localizar reporte de validación: `validacion_migracion_*.txt`
- [ ] Revisar estadísticas en reportes:
  - [ ] Cuentas procesadas: _________________
  - [ ] Cuentas creadas: _________________
  - [ ] Cuentas VES: _________________
  - [ ] Cuentas USD: _________________
  - [ ] Cuentas EUR: _________________
  - [ ] Cuentas USDT: _________________
  - [ ] Errores encontrados: _________________

### Validación de Saldos

- [ ] Verificar que saldos totales coinciden:
  - [ ] VES: Antes _________ = Después _________
  - [ ] USD: Antes _________ = Después _________
  - [ ] EUR: Antes _________ = Después _________
  - [ ] USDT: Antes _________ = Después _________
- [ ] Diferencia aceptable (< 0.01): [ ] Sí [ ] No

### Validación de Cuentas

- [ ] Verificar que no hay números duplicados
- [ ] Verificar que todos los prefijos son correctos:
  - [ ] VES: Prefijo 01
  - [ ] USD: Prefijo 02
  - [ ] EUR: Prefijo 03
  - [ ] USDT: Prefijo 04
- [ ] Verificar que todos los clientes tienen cuenta VES
- [ ] Verificar que no hay cuentas sin cliente

### Validación de Transacciones

- [ ] Verificar que las transacciones tienen referencias correctas
- [ ] Verificar que no hay referencias inválidas

---

## 🔄 REINICIO DEL SISTEMA

### Reiniciar Servidor

- [ ] Iniciar servidor web2py:
  ```bash
  python web2py.py -a <password> -i 127.0.0.1 -p 8000
  ```
  O iniciar servicio de producción
- [ ] Verificar que el servidor inició correctamente
- [ ] Anotar hora de reinicio: _________________

### Verificación de Acceso

- [ ] Acceder a la aplicación:
  ```
  http://127.0.0.1:8000/sistema_divisas
  ```
- [ ] Verificar que la página carga correctamente
- [ ] Verificar que no hay errores en consola

---

## 🧪 PRUEBAS FUNCIONALES

### Pruebas de Autenticación

- [ ] Login con usuario administrador
  - Usuario: _________________
  - [ ] Login exitoso
  - [ ] Dashboard carga correctamente

- [ ] Login con usuario cliente
  - Usuario: _________________
  - [ ] Login exitoso
  - [ ] Dashboard carga correctamente

### Pruebas de Visualización de Cuentas

- [ ] Acceder a "Mis Cuentas"
- [ ] Verificar que se muestran cuentas por moneda
- [ ] Verificar que cada cuenta muestra:
  - [ ] Número de cuenta con prefijo correcto
  - [ ] Moneda claramente indicada
  - [ ] Saldo correcto
  - [ ] Estado de la cuenta

### Pruebas de Consulta de Saldo

- [ ] Consultar saldo de cuenta VES
  - Número de cuenta: _________________
  - Saldo mostrado: _________________
  - [ ] Saldo correcto

- [ ] Consultar saldo de cuenta USD (si existe)
  - Número de cuenta: _________________
  - Saldo mostrado: _________________
  - [ ] Saldo correcto

### Pruebas de Historial

- [ ] Acceder a historial de transacciones
- [ ] Verificar que se muestran transacciones
- [ ] Verificar que se muestran cuentas origen y destino
- [ ] Verificar que las monedas son correctas

### Pruebas de Operaciones (OPCIONAL)

- [ ] Crear nueva cuenta (si se desea probar)
  - Moneda: _________________
  - [ ] Cuenta creada exitosamente
  - [ ] Número de cuenta con prefijo correcto

- [ ] Realizar compra de divisa (si se desea probar)
  - [ ] Operación exitosa
  - [ ] Saldos actualizados correctamente

---

## 📝 DOCUMENTACIÓN

### Registro de Ejecución

- [ ] Completar sección de "Registro de Ejecución" en `REPORTE_MIGRACION_PRODUCCION.md`
- [ ] Guardar reportes generados en ubicación segura
- [ ] Documentar cualquier problema encontrado
- [ ] Documentar soluciones aplicadas

### Comunicación

- [ ] Notificar a usuarios que el sistema está disponible
- [ ] Informar sobre cambios en la estructura de cuentas
- [ ] Proporcionar soporte si es necesario

---

## ⚠️ EN CASO DE PROBLEMAS

### Si la migración falla:

- [ ] Detener el servidor
- [ ] Restaurar backup:
  ```bash
  copy backups\storage_antes_migracion_produccion_*.sqlite databases\storage.sqlite
  ```
- [ ] Reiniciar servidor
- [ ] Verificar funcionamiento
- [ ] Documentar el problema
- [ ] Revisar logs y reportes
- [ ] Contactar soporte técnico si es necesario

### Si hay errores menores:

- [ ] Documentar el error
- [ ] Verificar si es crítico o aceptable
- [ ] Revisar reporte de validación
- [ ] Decidir si continuar o revertir
- [ ] Aplicar correcciones si es posible

---

## ✅ CONFIRMACIÓN FINAL

### Validación Completa

- [ ] Migración ejecutada exitosamente
- [ ] Reportes revisados y aprobados
- [ ] Saldos validados y correctos
- [ ] Cuentas creadas correctamente
- [ ] Sistema funcional y operativo
- [ ] Pruebas funcionales exitosas
- [ ] Backups guardados de forma segura
- [ ] Documentación completada

### Aprobación

- [ ] Sistema listo para producción
- [ ] Usuarios pueden acceder
- [ ] Operaciones funcionan correctamente

**Firma de aprobación:** _________________

**Fecha:** _________________

**Hora:** _________________

---

## 📞 CONTACTOS DE SOPORTE

**Desarrollador:** Sistema de Divisas Bancario  
**Documentación:** 
- `GUIA_EJECUCION_MIGRACION_PRODUCCION.md`
- `REPORTE_MIGRACION_PRODUCCION.md`
- `RESUMEN_TASK_11_COMPLETADA.md`

**Archivos de log:**
- `reporte_migracion_produccion_*.txt`
- `validacion_migracion_*.txt`
- `databases/sql.log`

---

## 📋 NOTAS ADICIONALES

_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

---

**FIN DEL CHECKLIST**

---

## 🎯 RESUMEN DE ESTADO

**Estado de la migración:** [ ] Exitosa [ ] Con advertencias [ ] Fallida

**Tiempo total:** _________ minutos

**Problemas encontrados:** _________________

**Acciones correctivas:** _________________

**Sistema operativo:** [ ] Sí [ ] No

**Recomendaciones:** _________________________________________________________________

---

**Completado por:** _________________

**Fecha:** _________________

**Firma:** _________________
