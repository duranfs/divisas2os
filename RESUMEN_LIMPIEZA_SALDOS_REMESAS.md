# Limpieza de Saldos, Movimientos, Remesas y Límites

## Script Creado

Se ha creado el script `limpiar_saldos_movimientos_remesas_limites.py` que limpia específicamente:

### ❌ Elimina:
- Movimientos de cuenta (`movimientos_cuenta`)
- Remesas diarias (`remesas_diarias`)
- Movimientos de remesas (`movimientos_remesas`)
- Límites de venta (`limites_venta`)
- Alertas de límites (`alertas_limites`)
- Resetea todos los saldos de cuentas a 0.00

### ✅ Mantiene:
- Clientes
- Cuentas (estructura)
- Usuarios
- Transacciones (historial completo)
- Tasas de cambio
- Configuración del sistema

## Uso Rápido

### Opción 1: Usando el archivo .bat (Windows)
```bash
limpiar_saldos_remesas.bat
```

### Opción 2: Comando directo
```bash
python web2py.py -S divisas2os_multiple -M -R limpiar_saldos_movimientos_remesas_limites.py
```

## Proceso Completo

1. **Detener el servidor web2py** (si está corriendo)

2. **Hacer backup de la base de datos**
   ```bash
   copy databases\storage.sqlite databases\backup_storage.sqlite
   ```

3. **Ejecutar el script**
   - Doble clic en `limpiar_saldos_remesas.bat`, o
   - Ejecutar el comando directo en la terminal

4. **Confirmar la operación**
   - Escribir `SI` cuando se solicite

5. **Verificar el resultado**
   - El script mostrará un resumen de las operaciones realizadas

6. **Reiniciar el servidor**
   ```bash
   iniciar_sistema_divisas.bat
   ```

## Verificación Post-Limpieza

El script automáticamente verifica:
- Cantidad de registros eliminados de cada tabla
- Saldos de cuentas (deben estar en 0.00)
- Estado de las tablas limpiadas

## Cuándo Usar Este Script

✅ **Usar cuando:**
- Necesitas resetear operaciones diarias (remesas, límites)
- Quieres limpiar saldos pero mantener el historial de transacciones
- Estás probando el sistema de remesas y límites
- Necesitas empezar con saldos en cero

❌ **NO usar cuando:**
- Estás en producción sin backup
- Necesitas mantener los saldos actuales
- Quieres conservar el historial de movimientos

## Seguridad

⚠️ **IMPORTANTE:**
- Siempre hacer backup antes de ejecutar
- Solo usar en desarrollo o con backup completo
- Los datos eliminados NO se pueden recuperar
- Confirmar que el nombre de la aplicación es correcto (`divisas2os_multiple`)

## Restaurar desde Backup

Si algo sale mal:
```bash
copy databases\backup_storage.sqlite databases\storage.sqlite
```

## Archivos Relacionados

- `limpiar_saldos_movimientos_remesas_limites.py` - Script principal
- `limpiar_saldos_remesas.bat` - Ejecutor para Windows
- `INSTRUCCIONES_LIMPIEZA.md` - Documentación completa
- `limpiar_datos_transaccionales.py` - Limpieza más amplia (incluye transacciones)
- `limpiar_todo_excepto_usuarios.py` - Limpieza completa

---

**Creado:** 29 de Noviembre de 2025  
**Sistema:** Sistema de Divisas Bancario  
**Framework:** web2py
