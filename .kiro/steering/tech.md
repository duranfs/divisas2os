# Stack Tecnológico - Sistema de Divisas Bancario

## Framework Principal

**web2py** - Framework web Python con arquitectura MVC
- Versión requerida: 3.0.10 o superior
- Base de datos: SQLite (desarrollo) / PostgreSQL (producción)
- ORM integrado (DAL - Database Abstraction Layer)

## Tecnologías Frontend

- **HTML5** con templates web2py
- **Bootstrap 3** para diseño responsive
- **CSS personalizado** con paleta de colores específica:
  - Fondo: Negro (#000000)
  - Menú: Naranja suave (#FFA366)  
  - Acento: Dorado (#FFD700)
- **JavaScript/jQuery** para interactividad

## Base de Datos

- **SQLite** para desarrollo (storage.sqlite)
- **DAL de web2py** para abstracción de base de datos
- **Migraciones automáticas** habilitadas en desarrollo
- **Índices optimizados** para consultas frecuentes

## Integraciones Externas

- **API del BCV** para obtener tasas oficiales de cambio
- **BeautifulSoup** para parsing de HTML del BCV
- **Requests** para llamadas HTTP

## Autenticación y Seguridad

- **Sistema Auth de web2py** integrado
- **Roles y permisos** granulares (administrador, operador, cliente)
- **Validación de entrada** en todos los formularios
- **Logging de auditoría** completo

## Comandos Comunes

### Desarrollo
```bash
# Iniciar servidor de desarrollo
python web2py.py -a <password> -i 127.0.0.1 -p 8000

# Acceder a la aplicación
http://127.0.0.1:8000/sistema_divisas

# Panel administrativo
http://127.0.0.1:8000/sistema_divisas/appadmin
```

### Testing
```bash
# Ejecutar pruebas unitarias
python web2py.py -S sistema_divisas -M -R tests/run_tests.py

# Pruebas específicas de clientes
python web2py.py -S sistema_divisas -M -R tests/test_clientes.py
```

### Base de Datos
```bash
# Resetear base de datos (desarrollo)
rm databases/*.table
rm databases/storage.sqlite

# Backup de base de datos
cp databases/storage.sqlite backups/storage_$(date +%Y%m%d).sqlite
```

## Estructura de Archivos Clave

- `models/db.py` - Definición de modelos y configuración de BD
- `controllers/` - Lógica de negocio por módulo
- `views/` - Templates HTML organizados por controlador
- `static/` - Archivos CSS, JS e imágenes
- `private/appconfig.ini` - Configuración de la aplicación

## Dependencias Python

- **web2py** (framework principal)
- **requests** (llamadas HTTP)
- **beautifulsoup4** (parsing HTML)
- **decimal** (cálculos precisos de divisas)

## Configuración de Producción

- Deshabilitar `reload=True` en configuración
- Configurar servidor web (Apache/Nginx)
- Usar base de datos PostgreSQL
- Habilitar compresión CSS/JS
- Configurar HTTPS obligatorio