# Documento de Diseño - Sistema de Divisas Bancario

## Visión General

El Sistema de Divisas Bancario es una aplicación web desarrollada en web2py que permite a los clientes de un banco realizar operaciones de compra y venta de divisas (VES, USD, EUR) utilizando las tasas oficiales del Banco Central de Venezuela. La aplicación sigue el patrón MVC de web2py y utiliza una arquitectura modular para facilitar el mantenimiento y escalabilidad.

## Arquitectura

### Arquitectura General
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Presentación  │    │     Lógica      │    │     Datos       │
│   (Views/HTML)  │◄──►│  (Controllers)  │◄──►│   (Models/DB)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                       ▲                       ▲
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CSS/JS        │    │   API Externa   │    │   SQLite DB     │
│   (Bootstrap)   │    │   (BCV Tasas)   │    │   (Storage)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Componentes Principales

1. **Módulo de Autenticación**: Gestión de usuarios y sesiones
2. **Módulo de Clientes**: Registro y gestión de información personal
3. **Módulo de Cuentas**: Gestión de cuentas bancarias y saldos
4. **Módulo de Tasas**: Obtención y gestión de tasas de cambio
5. **Módulo de Transacciones**: Procesamiento de compra/venta
6. **Módulo de Reportes**: Generación de informes y consultas
7. **Módulo de API**: Integración con servicios externos

## Componentes e Interfaces

### Estructura de Controladores

```python
# controllers/default.py - Controlador principal
- index()           # Dashboard principal
- login()           # Autenticación
- logout()          # Cerrar sesión
- dashboard()       # Panel de control del cliente

# controllers/clientes.py - Gestión de clientes
- registrar()       # Registro de nuevos clientes
- perfil()          # Gestión de perfil
- listar()          # Lista de clientes (admin)

# controllers/cuentas.py - Gestión de cuentas
- crear()           # Crear nueva cuenta
- consultar()       # Consultar saldos
- movimientos()     # Historial de movimientos

# controllers/divisas.py - Operaciones de divisas
- comprar()         # Compra de divisas
- vender()          # Venta de divisas
- tasas()           # Consulta de tasas actuales

# controllers/reportes.py - Reportes y consultas
- transacciones()   # Reporte de transacciones
- clientes()        # Reporte de clientes
- exportar()        # Exportación de datos

# controllers/api.py - Servicios API
- obtener_tasas()   # Obtener tasas del BCV
- actualizar_tasas() # Actualizar tasas en BD
```

### Interfaces de Usuario

#### Dashboard Principal
- Tasas actuales prominentes (VES/USD, VES/EUR)
- Resumen de cuentas del cliente
- Accesos rápidos a operaciones
- Últimas transacciones

#### Módulo de Transacciones
- Calculadora de cambio en tiempo real
- Formularios de compra/venta
- Confirmación de operaciones
- Generación de comprobantes

#### Panel Administrativo
- Gestión de clientes
- Monitoreo de transacciones
- Reportes y estadísticas
- Configuración del sistema

## Modelos de Datos

### Esquema de Base de Datos

```python
# Tabla de Clientes (extiende auth_user)
db.define_table('clientes',
    Field('user_id', 'reference auth_user'),
    Field('cedula', 'string', length=20, unique=True),
    Field('telefono', 'string', length=20),
    Field('direccion', 'text'),
    Field('fecha_nacimiento', 'date'),
    Field('estado', 'string', default='activo'),
    Field('fecha_registro', 'datetime', default=request.now),
    format='%(cedula)s - %(user_id)s'
)

# Tabla de Cuentas
db.define_table('cuentas',
    Field('cliente_id', 'reference clientes'),
    Field('numero_cuenta', 'string', length=20, unique=True),
    Field('tipo_cuenta', 'string', default='corriente'),
    Field('saldo_ves', 'decimal(15,2)', default=0),
    Field('saldo_usd', 'decimal(15,2)', default=0),
    Field('saldo_eur', 'decimal(15,2)', default=0),
    Field('estado', 'string', default='activa'),
    Field('fecha_creacion', 'datetime', default=request.now),
    format='%(numero_cuenta)s'
)

# Tabla de Tasas de Cambio
db.define_table('tasas_cambio',
    Field('fecha', 'date', default=request.now.date()),
    Field('hora', 'time', default=request.now.time()),
    Field('usd_ves', 'decimal(10,4)'),
    Field('eur_ves', 'decimal(10,4)'),
    Field('fuente', 'string', default='BCV'),
    Field('activa', 'boolean', default=True),
    format='%(fecha)s - USD: %(usd_ves)s'
)

# Tabla de Transacciones
db.define_table('transacciones',
    Field('cuenta_id', 'reference cuentas'),
    Field('tipo_operacion', 'string'), # 'compra' o 'venta'
    Field('moneda_origen', 'string', length=3),
    Field('moneda_destino', 'string', length=3),
    Field('monto_origen', 'decimal(15,2)'),
    Field('monto_destino', 'decimal(15,2)'),
    Field('tasa_aplicada', 'decimal(10,4)'),
    Field('comision', 'decimal(15,2)', default=0),
    Field('numero_comprobante', 'string', length=50, unique=True),
    Field('estado', 'string', default='completada'),
    Field('fecha_transaccion', 'datetime', default=request.now),
    Field('observaciones', 'text'),
    format='%(numero_comprobante)s'
)

# Tabla de Configuración del Sistema
db.define_table('configuracion',
    Field('clave', 'string', length=50, unique=True),
    Field('valor', 'text'),
    Field('descripcion', 'text'),
    Field('fecha_actualizacion', 'datetime', default=request.now),
    format='%(clave)s'
)
```

### Validaciones y Restricciones

```python
# Validaciones para clientes
db.clientes.cedula.requires = [
    IS_NOT_EMPTY(),
    IS_MATCH(r'^[VE]-?\d{7,8}$', error_message='Formato de cédula inválido'),
    IS_NOT_IN_DB(db, 'clientes.cedula')
]

# Validaciones para cuentas
db.cuentas.numero_cuenta.requires = [
    IS_NOT_EMPTY(),
    IS_LENGTH(20, 20),
    IS_NOT_IN_DB(db, 'cuentas.numero_cuenta')
]

# Validaciones para transacciones
db.transacciones.tipo_operacion.requires = IS_IN_SET(['compra', 'venta'])
db.transacciones.moneda_origen.requires = IS_IN_SET(['VES', 'USD', 'EUR'])
db.transacciones.moneda_destino.requires = IS_IN_SET(['VES', 'USD', 'EUR'])
```

## Manejo de Errores

### Estrategia de Manejo de Errores

1. **Errores de Validación**: Mostrar mensajes claros en formularios
2. **Errores de Conexión API**: Usar tasas almacenadas como respaldo
3. **Errores de Transacción**: Rollback automático y notificación
4. **Errores del Sistema**: Logging detallado y páginas de error personalizadas

### Implementación

```python
# En controllers/api.py
def obtener_tasas_bcv():
    try:
        # Intentar obtener tasas del BCV
        response = requests.get(BCV_API_URL, timeout=10)
        if response.status_code == 200:
            return procesar_tasas(response.json())
        else:
            raise Exception("Error en respuesta del BCV")
    except Exception as e:
        # Log del error
        logger.error(f"Error obteniendo tasas BCV: {str(e)}")
        # Usar tasas almacenadas
        return obtener_ultimas_tasas_db()

# En controllers/divisas.py
def procesar_transaccion():
    try:
        db.begin()
        # Procesar transacción
        resultado = ejecutar_transaccion()
        db.commit()
        return resultado
    except Exception as e:
        db.rollback()
        session.flash = f"Error en transacción: {str(e)}"
        redirect(URL('divisas', 'index'))
```

## Estrategia de Pruebas

### Tipos de Pruebas

1. **Pruebas Unitarias**: Validación de funciones individuales
2. **Pruebas de Integración**: Verificación de módulos conectados
3. **Pruebas de API**: Validación de servicios externos
4. **Pruebas de UI**: Verificación de interfaz de usuario

### Herramientas y Framework

```python
# Usar unittest de Python para pruebas
import unittest
from gluon.globals import Request, Response, Session
from gluon.storage import Storage

class TestDivisas(unittest.TestCase):
    def setUp(self):
        # Configurar entorno de prueba
        self.db = DAL('sqlite:memory:')
        # Definir tablas de prueba
        
    def test_calculo_cambio(self):
        # Probar cálculos de cambio de moneda
        pass
        
    def test_validacion_fondos(self):
        # Probar validación de fondos suficientes
        pass
```

### Casos de Prueba Críticos

1. **Cálculo de Tasas**: Verificar precisión en conversiones
2. **Validación de Fondos**: Asegurar fondos suficientes antes de transacciones
3. **Integridad de Datos**: Verificar consistencia en saldos
4. **Seguridad**: Validar autenticación y autorización
5. **API Externa**: Manejar fallos de conexión correctamente

## Diseño Visual y UX

### Paleta de Colores

```css
:root {
    --color-fondo: #000000;        /* Negro - Fondo principal */
    --color-menu: #FFA366;         /* Naranja suave - Menú y navegación */
    --color-acento: #FFD700;       /* Dorado - Elementos destacados */
    --color-texto: #FFFFFF;        /* Blanco - Texto principal */
    --color-texto-secundario: #CCCCCC; /* Gris claro - Texto secundario */
}
```

### Estructura de Layout

```html
<!-- Layout principal -->
<div class="container-fluid">
    <nav class="navbar navbar-expand-lg" style="background-color: var(--color-menu);">
        <!-- Menú de navegación -->
    </nav>
    
    <div class="row">
        <div class="col-md-2 sidebar" style="background-color: var(--color-fondo);">
            <!-- Menú lateral -->
        </div>
        <div class="col-md-10 main-content">
            <!-- Contenido principal -->
        </div>
    </div>
</div>
```

### Componentes UI Principales

1. **Dashboard de Tasas**: Visualización prominente de tasas actuales
2. **Calculadora de Cambio**: Herramienta interactiva para cálculos
3. **Formularios de Transacción**: Interfaces claras para operaciones
4. **Tablas de Historial**: Presentación organizada de movimientos
5. **Gráficos de Tendencias**: Visualización de evolución de tasas

## Integración con API Externa

### Conexión con BCV

```python
# Configuración de API
BCV_API_CONFIG = {
    'url_base': 'https://www.bcv.org.ve/',
    'endpoint_tasas': 'estadisticas/dolar-euro',
    'timeout': 10,
    'retry_attempts': 3
}

# Función de obtención de tasas
def obtener_tasas_bcv():
    import requests
    from bs4 import BeautifulSoup
    
    try:
        response = requests.get(
            BCV_API_CONFIG['url_base'] + BCV_API_CONFIG['endpoint_tasas'],
            timeout=BCV_API_CONFIG['timeout']
        )
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extraer tasas del HTML
            usd_rate = extraer_tasa_usd(soup)
            eur_rate = extraer_tasa_eur(soup)
            
            return {
                'usd_ves': usd_rate,
                'eur_ves': eur_rate,
                'fecha': datetime.now(),
                'fuente': 'BCV'
            }
    except Exception as e:
        logger.error(f"Error obteniendo tasas BCV: {str(e)}")
        return None
```

### Programación de Actualizaciones

```python
# En models/scheduler.py (si está habilitado)
if configuration.get("scheduler.enabled"):
    scheduler.queue_task(
        'actualizar_tasas_bcv',
        period=3600,  # Cada hora
        timeout=300,  # 5 minutos timeout
        repeats=0,    # Repetir indefinidamente
        retry_failed=3
    )
```

## Seguridad

### Medidas de Seguridad Implementadas

1. **Autenticación**: Sistema auth de web2py con contraseñas seguras
2. **Autorización**: Control de acceso basado en roles
3. **Validación de Entrada**: Sanitización de todos los inputs
4. **Transacciones Seguras**: Uso de transacciones de BD
5. **Logging de Auditoría**: Registro de todas las operaciones críticas

### Configuración de Seguridad

```python
# En models/db.py
auth.settings.password_min_length = 8
auth.settings.password_field = 'password'
auth.settings.login_after_registration = False
auth.settings.registration_requires_verification = True

# Roles del sistema
auth.add_group('administrador', 'Administrador del sistema')
auth.add_group('cliente', 'Cliente bancario')
auth.add_group('operador', 'Operador bancario')
```

## Consideraciones de Rendimiento

### Optimizaciones Implementadas

1. **Índices de BD**: Índices en campos de búsqueda frecuente
2. **Cache de Tasas**: Cache de tasas para reducir llamadas API
3. **Paginación**: Paginación en listados largos
4. **Compresión**: Compresión de CSS/JS en producción

### Monitoreo

```python
# Logging de rendimiento
import time

def monitor_performance(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} ejecutado en {end_time - start_time:.2f}s")
        return result
    return wrapper
```