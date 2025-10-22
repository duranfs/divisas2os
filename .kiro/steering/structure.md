# Estructura del Proyecto - Sistema de Divisas Bancario

## Arquitectura web2py MVC

El proyecto sigue la estructura estándar de web2py con separación clara entre Modelo-Vista-Controlador.

## Organización de Directorios

### `/controllers/` - Lógica de Negocio
- `default.py` - Controlador principal (dashboard, autenticación)
- `clientes.py` - Gestión de clientes bancarios
- `cuentas.py` - Manejo de cuentas bancarias y saldos
- `divisas.py` - Operaciones de compra/venta de divisas
- `reportes.py` - Generación de reportes administrativos
- `api.py` - Integración con API del BCV y servicios externos
- `admin.py` - Funciones administrativas del sistema
- `appadmin.py` - Panel de administración de base de datos

### `/models/` - Definición de Datos
- `db.py` - **Archivo principal**: Configuración de BD, tablas, validaciones, auth, auditoría
- `menu.py` - Configuración del menú de navegación
- `scheduler_tasks.py` - Tareas programadas (actualización de tasas)
- `error_config.py` - Configuración de manejo de errores

### `/views/` - Presentación
Organizadas por controlador:
- `default/` - Vistas del dashboard principal
- `clientes/` - Formularios y listados de clientes
- `cuentas/` - Interfaces de gestión de cuentas
- `divisas/` - Formularios de transacciones y calculadora
- `reportes/` - Vistas de reportes y exportación
- `api/` - Widgets de tasas y gráficos
- `admin/` - Interfaces administrativas
- `layout.html` - Template base del sistema
- `error_*.html` - Páginas de error personalizadas

### `/static/` - Recursos Estáticos
- `css/` - Hojas de estilo personalizadas
  - `sistema-divisas.css` - Estilos principales
  - `error-pages.css` - Estilos para páginas de error
- `js/` - JavaScript personalizado
  - `calculadora_divisas.js` - Calculadora de cambio en tiempo real
  - `navegacion.js` - Funcionalidades de navegación
- `images/` - Imágenes y logos
- `temp/` - Archivos temporales

### `/modules/` - Módulos Personalizados
- `breadcrumbs.py` - Sistema de navegación breadcrumb
- `error_handler.py` - Manejo centralizado de errores
- `__init__.py` - Inicialización de módulos

### `/databases/` - Base de Datos
- `storage.sqlite` - Base de datos principal
- `*.table` - Archivos de definición de tablas
- `sql.log` - Log de consultas SQL

### `/private/` - Configuración Privada
- `appconfig.ini` - **Archivo crítico**: Configuración de la aplicación

### `/tests/` - Pruebas Unitarias
- `run_tests.py` - Ejecutor principal de pruebas
- `test_clientes.py` - Pruebas del módulo de clientes
- `test_clientes_simple.py` - Pruebas básicas

### `/languages/` - Internacionalización
- `es.py` - Traducciones en español (idioma principal)
- Otros idiomas disponibles para futuras expansiones

## Convenciones de Nomenclatura

### Controladores
- Nombres en minúsculas y plural: `clientes.py`, `cuentas.py`
- Funciones descriptivas: `registrar()`, `consultar()`, `listar()`

### Modelos de Base de Datos
- Nombres de tablas en minúsculas y plural: `clientes`, `cuentas`, `transacciones`
- Campos con prefijos descriptivos: `fecha_registro`, `numero_cuenta`
- Referencias con sufijo `_id`: `cliente_id`, `cuenta_id`

### Vistas
- Organizadas por controlador en subdirectorios
- Nombres coinciden con funciones del controlador
- Template base: `layout.html`

### CSS/JavaScript
- Archivos minificados para producción: `.min.css`, `.min.js`
- Nombres descriptivos del módulo: `calculadora_divisas.js`

## Flujo de Datos Principal

1. **Autenticación** → `default.py` → Dashboard personalizado por rol
2. **Operaciones de Cliente** → `divisas.py` → Validación → `cuentas.py` → BD
3. **Actualización de Tasas** → `api.py` → BCV → Cache → BD
4. **Reportes** → `reportes.py` → Consultas → Exportación

## Archivos de Configuración Críticos

- `models/db.py` - **MÁS IMPORTANTE**: Toda la lógica de BD y seguridad
- `private/appconfig.ini` - Configuración de conexiones y parámetros
- `views/layout.html` - Template base para toda la aplicación

## Patrones de Desarrollo

### Validaciones
- Validaciones en el modelo (`db.py`)
- Validaciones adicionales en controladores
- Mensajes de error en español

### Seguridad
- Decoradores `@auth.requires_login()` en funciones sensibles
- Control de roles con funciones personalizadas: `es_administrador()`, `es_cliente()`
- Logging de auditoría en todas las operaciones críticas

### Manejo de Errores
- Try/catch en operaciones críticas
- Rollback automático en transacciones fallidas
- Páginas de error personalizadas

### Cache y Rendimiento
- Cache de tasas de cambio (5 minutos)
- Índices de BD en campos de búsqueda frecuente
- Paginación en listados largos