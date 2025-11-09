# Datos de Prueba - Sistema de Divisas Bancario

## Resumen

Este directorio contiene scripts para generar y verificar datos de prueba para el Sistema de Divisas Bancario, cumpliendo con los requisitos 1.1 y 2.1 del spec de corrección de visualización de registros de clientes.

## Archivos Creados

### Scripts Principales

1. **`create_test_data.py`** - Generador de datos de prueba
   - Crea usuarios con diferentes estados (activo/inactivo)
   - Genera clientes asociados a los usuarios
   - Crea cuentas con diferentes tipos (corriente/ahorro) y saldos
   - Limpia datos de prueba anteriores antes de crear nuevos

2. **`verify_display.py`** - Verificador de visualización
   - Verifica que las consultas JOIN funcionen correctamente
   - Prueba filtros de búsqueda (nombre, cédula, estado)
   - Valida estadísticas de clientes
   - Confirma que los saldos de cuentas se muestren correctamente

3. **`run_test_data_creation.py`** - Script principal
   - Ejecuta ambos scripts en secuencia
   - Proporciona resumen completo de resultados
   - Incluye instrucciones para próximos pasos

### Scripts de Prueba Existentes

4. **`test_clientes.py`** - Pruebas unitarias completas del módulo de clientes
5. **`test_clientes_simple.py`** - Pruebas de validación simplificadas
6. **`run_tests.py`** - Ejecutor de pruebas unitarias

## Datos de Prueba Generados

### Usuarios de Prueba (8 usuarios)

| Nombre | Email | Estado | Cédula |
|--------|-------|--------|--------|
| Franklin Rodríguez | franklin.rodriguez@test.com | activo | V-TEST001 |
| María González | maria.gonzalez@test.com | activo | V-TEST002 |
| Carlos Martínez | carlos.martinez@test.com | inactivo | E-TEST003 |
| Ana López | ana.lopez@test.com | activo | V-TEST004 |
| José Hernández | jose.hernandez@test.com | activo | V-TEST005 |
| Carmen Pérez | carmen.perez@test.com | inactivo | E-TEST006 |
| Roberto Silva | roberto.silva@test.com | activo | V-TEST007 |
| Luisa Morales | luisa.morales@test.com | activo | V-TEST008 |

### Distribución de Estados
- **Activos**: 6 usuarios (75%)
- **Inactivos**: 2 usuarios (25%)

### Cuentas de Prueba (12 cuentas)

- **Tipos de cuenta**:
  - Corriente: 8 cuentas
  - Ahorro: 4 cuentas

- **Estados de cuenta**:
  - Activas: 12 cuentas (100%)
  - Inactivas: 0 cuentas

- **Saldos totales aproximados**:
  - VES: 31,398,418.56
  - USD: 60,679.27
  - EUR: 36,175.41
  - USDT: 6,203.65

## Cómo Usar los Scripts

### Generar Datos de Prueba

```bash
# Ejecutar script completo (recomendado)
python tests/run_test_data_creation.py

# O ejecutar scripts individuales
python tests/create_test_data.py
python tests/verify_display.py
```

### Ejecutar Pruebas Unitarias

```bash
# Pruebas completas
python tests/run_tests.py

# Pruebas simplificadas
python tests/test_clientes_simple.py
```

## Verificación de Funcionalidad

Los scripts verifican que:

1. **Listado de Clientes** (`/clientes/listar`):
   - ✅ La consulta JOIN funciona correctamente
   - ✅ Se muestran todos los campos requeridos (ID, nombre, cédula, email, estado)
   - ✅ Los filtros de búsqueda funcionan (nombre, cédula, estado)
   - ✅ Las estadísticas son correctas (total, activos, inactivos)

2. **Listado de Cuentas** (`/cuentas/listar_todas`):
   - ✅ Se muestran cuentas con información del cliente
   - ✅ Los saldos se formatean correctamente
   - ✅ Se distinguen tipos de cuenta (corriente/ahorro)
   - ✅ No hay saldos negativos

3. **Paginación**:
   - ✅ Se calcula correctamente el número de páginas
   - ℹ️ Con 11 clientes totales, no se necesita paginación (< 20)

## Resultados de Verificación

### Estado Actual
- **Total de clientes**: 11 (3 existentes + 8 de prueba)
- **Clientes activos**: 9
- **Clientes inactivos**: 2
- **Total de cuentas**: 16
- **Todas las verificaciones**: ✅ PASARON

### Consultas Probadas

1. **Consulta principal de clientes**:
```sql
SELECT 
    c.id, c.cedula, c.fecha_registro,
    u.first_name, u.last_name, u.email, u.estado
FROM clientes c
JOIN auth_user u ON c.user_id = u.id
ORDER BY c.fecha_registro DESC
```

2. **Filtros de búsqueda**:
   - Por nombre: `WHERE u.first_name LIKE '%término%' OR u.last_name LIKE '%término%'`
   - Por cédula: `WHERE c.cedula LIKE '%término%'`
   - Por estado: `WHERE u.estado = 'activo/inactivo'`

3. **Estadísticas**:
   - Total: `SELECT COUNT(*) FROM clientes`
   - Activos: `SELECT COUNT(*) FROM clientes c JOIN auth_user u ON c.user_id = u.id WHERE u.estado = 'activo'`
   - Inactivos: `SELECT COUNT(*) FROM clientes c JOIN auth_user u ON c.user_id = u.id WHERE u.estado = 'inactivo'`

## Próximos Pasos para Pruebas

1. **Iniciar servidor web2py**:
   ```bash
   python web2py.py -a <password> -i 127.0.0.1 -p 8000
   ```

2. **Acceder a las vistas**:
   - Listado de clientes: `http://127.0.0.1:8000/divisas2os/clientes/listar`
   - Listado de cuentas: `http://127.0.0.1:8000/divisas2os/cuentas/listar_todas`

3. **Probar funcionalidades**:
   - Filtros de búsqueda por nombre, cédula y estado
   - Visualización de estadísticas en tarjetas
   - Navegación y ordenamiento
   - Formato correcto de montos y fechas

## Limpieza de Datos de Prueba

Los datos de prueba se identifican por:
- **Usuarios**: emails que terminan en `@test.com`
- **Clientes**: cédulas que contienen `TEST` (V-TEST001, E-TEST003, etc.)
- **Cuentas**: números que contienen `TEST` (2001TEST...)

Para limpiar manualmente:
```sql
DELETE FROM movimientos_cuenta WHERE cuenta_id IN (SELECT id FROM cuentas WHERE numero_cuenta LIKE '%TEST%');
DELETE FROM transacciones WHERE cuenta_id IN (SELECT id FROM cuentas WHERE numero_cuenta LIKE '%TEST%');
DELETE FROM cuentas WHERE numero_cuenta LIKE '%TEST%';
DELETE FROM clientes WHERE cedula LIKE '%TEST%';
DELETE FROM auth_user WHERE email LIKE '%@test.com';
```

## Requisitos Cumplidos

- ✅ **Requisito 1.1**: Generar clientes de prueba con diferentes estados
- ✅ **Requisito 2.1**: Crear cuentas de prueba con diferentes tipos y saldos
- ✅ **Verificación**: Confirmar que los datos se muestren correctamente en las vistas

Los datos de prueba permiten validar completamente la funcionalidad de visualización de registros de clientes y cuentas, asegurando que las correcciones implementadas en las vistas funcionen correctamente.