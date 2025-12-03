# Instrucciones para Scripts de Limpieza

## Scripts Disponibles

Se han creado tres scripts para limpiar datos del sistema:

### 1. `limpiar_saldos_movimientos_remesas_limites.py` (Limpieza Específica) ⭐ RECOMENDADO

**Elimina:**
- ✗ Todos los movimientos de cuenta
- ✗ Todas las remesas diarias
- ✗ Todos los movimientos de remesas
- ✗ Todos los límites de venta
- ✗ Todas las alertas de límites
- ✗ Resetea todos los saldos de cuentas a 0.00

**Mantiene:**
- ✓ Clientes
- ✓ Cuentas (estructura)
- ✓ Usuarios
- ✓ Transacciones (historial)
- ✓ Tasas de cambio
- ✓ Configuración del sistema

**Uso:**
```bash
python web2py.py -S divisas2os_multiple -M -R limpiar_saldos_movimientos_remesas_limites.py
```

**Confirmación requerida:** Escribir `SI`

---

### 2. `limpiar_datos_transaccionales.py` (Limpieza Parcial)

**Elimina:**
- ✗ Todas las transacciones
- ✗ Todos los movimientos
- ✗ Todas las remesas
- ✗ Todos los límites de transacciones
- ✗ Resetea todos los saldos de cuentas a 0.00

**Mantiene:**
- ✓ Clientes
- ✓ Cuentas (estructura)
- ✓ Usuarios
- ✓ Tasas de cambio
- ✓ Configuración del sistema

**Uso:**
```bash
python web2py.py -S divisas2os_multiple -M -R limpiar_datos_transaccionales.py
```

**Confirmación requerida:** Escribir `SI`

---

### 3. `limpiar_todo_excepto_usuarios.py` (Limpieza Completa)

**Elimina:**
- ✗ Todos los clientes
- ✗ Todas las cuentas
- ✗ Todas las transacciones
- ✗ Todos los movimientos
- ✗ Todas las remesas
- ✗ Todos los límites

**Mantiene:**
- ✓ Usuarios (auth_user)
- ✓ Tasas de cambio
- ✓ Configuración del sistema
- ✓ Logs de auditoría

**Uso:**
```bash
python web2py.py -S divisas2os_multiple -M -R limpiar_todo_excepto_usuarios.py
```

**Confirmación requerida:** Escribir `ELIMINAR TODO`

---

## Recomendaciones de Uso

### Cuándo usar `limpiar_saldos_movimientos_remesas_limites.py`: ⭐ RECOMENDADO
- Quieres limpiar saldos, movimientos, remesas y límites específicamente
- Necesitas resetear las operaciones diarias pero mantener el historial de transacciones
- Estás probando el sistema de remesas y límites
- Quieres empezar con saldos en cero pero mantener clientes, cuentas y transacciones

### Cuándo usar `limpiar_datos_transaccionales.py`:
- Quieres resetear las transacciones pero mantener la estructura de clientes y cuentas
- Estás probando el flujo de transacciones
- Quieres empezar con saldos en cero pero mantener los clientes

### Cuándo usar `limpiar_todo_excepto_usuarios.py`:
- Quieres empezar completamente desde cero
- Estás en fase de desarrollo y quieres limpiar todo
- Quieres mantener solo los usuarios del sistema

---

## Precauciones Importantes

⚠️ **ADVERTENCIAS:**

1. **Hacer backup antes de ejecutar cualquier script**
   ```bash
   # Backup de la base de datos
   copy databases\storage.sqlite databases\backup_storage_%date%.sqlite
   ```

2. **Usar solo en desarrollo**
   - Estos scripts NO deben ejecutarse en producción sin un backup completo
   - Los datos eliminados NO se pueden recuperar

3. **Verificar el nombre de la aplicación**
   - Los scripts usan `divisas2os_multiple` como nombre de aplicación
   - Si tu aplicación tiene otro nombre, modifica el comando:
   ```bash
   python web2py.py -S TU_NOMBRE_APP -M -R limpiar_datos_transaccionales.py
   ```

4. **Reiniciar el servidor después de la limpieza**
   - Después de ejecutar cualquier script, reinicia web2py
   - Esto asegura que los cambios se reflejen correctamente

---

## Proceso Recomendado

### Para Limpieza Específica (saldos, movimientos, remesas y límites): ⭐ RECOMENDADO

1. **Detener el servidor web2py** (si está corriendo)

2. **Hacer backup**
   ```bash
   copy databases\storage.sqlite databases\backup_storage.sqlite
   ```

3. **Ejecutar el script**
   ```bash
   python web2py.py -S divisas2os_multiple -M -R limpiar_saldos_movimientos_remesas_limites.py
   ```

4. **Confirmar** escribiendo `SI`

5. **Verificar** que el script completó exitosamente

6. **Reiniciar el servidor**
   ```bash
   python web2py.py -a <password> -i 127.0.0.1 -p 8000
   ```

### Para Limpieza Parcial (solo transacciones):

1. **Detener el servidor web2py** (si está corriendo)

2. **Hacer backup**
   ```bash
   copy databases\storage.sqlite databases\backup_storage.sqlite
   ```

3. **Ejecutar el script**
   ```bash
   python web2py.py -S divisas2os_multiple -M -R limpiar_datos_transaccionales.py
   ```

4. **Confirmar** escribiendo `SI`

5. **Verificar** que el script completó exitosamente

6. **Reiniciar el servidor**
   ```bash
   python web2py.py -a <password> -i 127.0.0.1 -p 8000
   ```

### Para Limpieza Completa:

1. **Detener el servidor web2py** (si está corriendo)

2. **Hacer backup**
   ```bash
   copy databases\storage.sqlite databases\backup_storage.sqlite
   ```

3. **Ejecutar el script**
   ```bash
   python web2py.py -S divisas2os_multiple -M -R limpiar_todo_excepto_usuarios.py
   ```

4. **Confirmar** escribiendo `ELIMINAR TODO`

5. **Verificar** que el script completó exitosamente

6. **Reiniciar el servidor**
   ```bash
   python web2py.py -a <password> -i 127.0.0.1 -p 8000
   ```

---

## Verificación Post-Limpieza

Después de ejecutar cualquier script, verifica:

1. **Accede al sistema** con tu usuario administrador

2. **Verifica el dashboard**
   - Debe mostrar 0 transacciones (ambos scripts)
   - Debe mostrar 0 clientes (solo script completo)
   - Debe mostrar 0 cuentas (solo script completo)

3. **Verifica las cuentas** (si usaste limpieza parcial)
   - Todas las cuentas deben tener saldo 0.00
   - Las cuentas deben seguir existiendo

4. **Prueba crear un nuevo cliente**
   - Debe funcionar correctamente
   - Debe poder crear cuentas
   - Debe poder realizar transacciones

---

## Solución de Problemas

### Error: "No module named 'gluon'"
- Asegúrate de ejecutar el script con `python web2py.py -S ...`
- No ejecutes el script directamente con `python limpiar_...py`

### Error: "Application not found"
- Verifica el nombre de tu aplicación
- Usa el nombre correcto en el comando `-S nombre_app`

### Error: "Permission denied"
- Cierra el servidor web2py antes de ejecutar el script
- Verifica que no haya procesos usando la base de datos

### Los cambios no se reflejan
- Reinicia el servidor web2py
- Limpia el cache del navegador (Ctrl + F5)
- Verifica que el script completó sin errores

---

## Restaurar desde Backup

Si algo sale mal, puedes restaurar desde el backup:

1. **Detener el servidor web2py**

2. **Restaurar el archivo de base de datos**
   ```bash
   copy databases\backup_storage.sqlite databases\storage.sqlite
   ```

3. **Reiniciar el servidor**

---

## Contacto y Soporte

Si tienes problemas con los scripts:
1. Revisa los mensajes de error en la consola
2. Verifica que hiciste backup antes de ejecutar
3. Consulta la documentación de web2py sobre manejo de base de datos

---

**Última actualización:** 29 de Noviembre de 2025
