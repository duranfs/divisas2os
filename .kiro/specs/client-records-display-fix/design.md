# Documento de Diseño

## Resumen

Este diseño aborda la corrección del problema de visualización de registros de clientes en el sistema de divisas bancario. El problema principal es que las vistas HTML no están renderizando correctamente los datos de clientes que se pasan desde los controladores, mostrando texto estático en lugar de los registros reales.

## Arquitectura

### Componentes Afectados

1. **Controlador de Clientes** (`controllers/clientes.py`)
   - Función `listar()` - Necesita verificación de datos pasados a la vista
   - Función `detalle()` - Requiere validación de renderizado de datos

2. **Vista de Listado** (`views/clientes/listar.html`)
   - Template HTML estático que necesita integración dinámica de datos
   - Implementación de loops para mostrar registros de clientes

3. **Controlador de Cuentas** (`controllers/cuentas.py`)
   - Función `listar_todas()` - Para administradores
   - Función `index()` - Para clientes individuales

4. **Vistas de Cuentas** (`views/cuentas/`)
   - Templates que necesitan mostrar datos de cuentas dinámicamente

## Componentes e Interfaces

### 1. Controlador de Clientes - Función `listar()`

**Problema Identificado:**
- El controlador está pasando datos correctamente pero la vista no los está utilizando
- Falta validación de que los datos se estén recuperando correctamente

**Solución:**
```python
def listar():
    # Verificar permisos
    if not (auth.has_membership('administrador') or auth.has_membership('operador')):
        session.flash = "No tiene permisos para ver la lista de clientes"
        redirect(URL('default', 'index'))
    
    # Parámetros de búsqueda y filtrado
    buscar = request.vars.buscar or ''
    estado_filtro = request.vars.estado or 'todos'
    
    # Construir query base con JOIN explícito
    query = (db.clientes.user_id == db.auth_user.id)
    
    # Aplicar filtros
    if buscar:
        query &= ((db.auth_user.first_name.contains(buscar)) |
                 (db.auth_user.last_name.contains(buscar)) |
                 (db.auth_user.email.contains(buscar)) |
                 (db.clientes.cedula.contains(buscar)))
    
    if estado_filtro != 'todos':
        query &= (db.auth_user.estado == estado_filtro)
    
    # Obtener clientes con paginación
    page = int(request.vars.page or 1)
    items_per_page = 20
    
    total_clientes = db(query).count()
    clientes = db(query).select(
        db.clientes.ALL,
        db.auth_user.ALL,
        limitby=((page-1)*items_per_page, page*items_per_page),
        orderby=db.clientes.fecha_registro
    )
    
    # Calcular información de paginación
    total_pages = (total_clientes + items_per_page - 1) // items_per_page
    
    # Obtener estadísticas
    stats = {
        'total': db(db.clientes.id > 0).count(),
        'activos': db((db.clientes.user_id == db.auth_user.id) & 
                     (db.auth_user.estado == 'activo')).count(),
        'inactivos': db((db.clientes.user_id == db.auth_user.id) & 
                       (db.auth_user.estado == 'inactivo')).count()
    }
    
    return dict(
        clientes=clientes,
        buscar=buscar,
        estado_filtro=estado_filtro,
        page=page,
        total_pages=total_pages,
        total_clientes=total_clientes,
        stats=stats
    )
```

### 2. Vista de Listado de Clientes

**Problema Identificado:**
- La tabla tiene contenido estático en lugar de iterar sobre los datos de clientes
- Faltan los filtros funcionales conectados al controlador

**Solución:**
```html
<!-- Filtros de búsqueda funcionales -->
<form method="GET" action="{{=URL('clientes', 'listar')}}">
    <div class="row">
        <div class="col-md-4">
            <div class="mb-3">
                <label class="form-label">Buscar por nombre</label>
                <input type="text" name="buscar" class="form-control" 
                       placeholder="Nombre del cliente" value="{{=buscar}}">
            </div>
        </div>
        <div class="col-md-4">
            <div class="mb-3">
                <label class="form-label">Estado</label>
                <select name="estado" class="form-control">
                    <option value="todos" {{='selected' if estado_filtro == 'todos' else ''}}>Todos los estados</option>
                    <option value="activo" {{='selected' if estado_filtro == 'activo' else ''}}>Activo</option>
                    <option value="inactivo" {{='selected' if estado_filtro == 'inactivo' else ''}}>Inactivo</option>
                </select>
            </div>
        </div>
        <div class="col-md-4">
            <div class="mb-3">
                <label class="form-label">&nbsp;</label>
                <div>
                    <button type="submit" class="btn btn-primary me-2">
                        <i class="fas fa-search me-1"></i>Buscar
                    </button>
                    <a href="{{=URL('clientes', 'listar')}}" class="btn btn-secondary">
                        <i class="fas fa-times me-1"></i>Limpiar
                    </a>
                </div>
            </div>
        </div>
    </div>
</form>

<!-- Tabla de clientes con datos dinámicos -->
<div class="table-responsive">
    <table class="table table-striped">
        <thead>
            <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Cédula</th>
                <th>Email</th>
                <th>Estado</th>
                <th>Fecha Registro</th>
                <th>Acciones</th>
            </tr>
        </thead>
        <tbody>
            {{if clientes:}}
                {{for cliente in clientes:}}
                <tr>
                    <td>{{=cliente.clientes.id}}</td>
                    <td>{{=cliente.auth_user.first_name}} {{=cliente.auth_user.last_name}}</td>
                    <td>{{=cliente.clientes.cedula}}</td>
                    <td>{{=cliente.auth_user.email}}</td>
                    <td>
                        {{if cliente.auth_user.estado == 'activo':}}
                            <span class="badge bg-success">Activo</span>
                        {{else:}}
                            <span class="badge bg-danger">Inactivo</span>
                        {{pass}}
                    </td>
                    <td>{{=cliente.clientes.fecha_registro.strftime('%d/%m/%Y') if cliente.clientes.fecha_registro else 'N/A'}}</td>
                    <td>
                        <a href="{{=URL('clientes', 'detalle', args=[cliente.clientes.id])}}" 
                           class="btn btn-sm btn-info me-1" title="Ver detalles">
                            <i class="fas fa-eye"></i>
                        </a>
                        <a href="{{=URL('clientes', 'editar', args=[cliente.clientes.id])}}" 
                           class="btn btn-sm btn-warning me-1" title="Editar">
                            <i class="fas fa-edit"></i>
                        </a>
                    </td>
                </tr>
                {{pass}}
            {{else:}}
                <tr>
                    <td colspan="7" class="text-center text-muted py-4">
                        <i class="fas fa-info-circle me-2"></i>
                        {{if buscar or estado_filtro != 'todos':}}
                            No se encontraron clientes que coincidan con los filtros aplicados.
                        {{else:}}
                            No hay clientes registrados en el sistema.
                        {{pass}}
                        <br>
                        <a href="{{=URL('clientes', 'registrar')}}" class="btn btn-success mt-2">
                            <i class="fas fa-plus me-1"></i>Registrar Primer Cliente
                        </a>
                    </td>
                </tr>
            {{pass}}
        </tbody>
    </table>
</div>

<!-- Paginación -->
{{if total_pages > 1:}}
<nav aria-label="Paginación de clientes">
    <ul class="pagination justify-content-center">
        {{if page > 1:}}
            <li class="page-item">
                <a class="page-link" href="{{=URL('clientes', 'listar', vars={'page': page-1, 'buscar': buscar, 'estado': estado_filtro})}}">
                    Anterior
                </a>
            </li>
        {{pass}}
        
        {{for p in range(max(1, page-2), min(total_pages+1, page+3)):}}
            <li class="page-item {{='active' if p == page else ''}}">
                <a class="page-link" href="{{=URL('clientes', 'listar', vars={'page': p, 'buscar': buscar, 'estado': estado_filtro})}}">
                    {{=p}}
                </a>
            </li>
        {{pass}}
        
        {{if page < total_pages:}}
            <li class="page-item">
                <a class="page-link" href="{{=URL('clientes', 'listar', vars={'page': page+1, 'buscar': buscar, 'estado': estado_filtro})}}">
                    Siguiente
                </a>
            </li>
        {{pass}}
    </ul>
</nav>
{{pass}}

<!-- Estadísticas -->
{{if stats:}}
<div class="row mt-4">
    <div class="col-md-4">
        <div class="card text-center">
            <div class="card-body">
                <h5 class="card-title">{{=stats.total}}</h5>
                <p class="card-text">Total Clientes</p>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card text-center">
            <div class="card-body">
                <h5 class="card-title text-success">{{=stats.activos}}</h5>
                <p class="card-text">Clientes Activos</p>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card text-center">
            <div class="card-body">
                <h5 class="card-title text-danger">{{=stats.inactivos}}</h5>
                <p class="card-text">Clientes Inactivos</p>
            </div>
        </div>
    </div>
</div>
{{pass}}
```

### 3. Controlador de Cuentas - Función `listar_todas()`

**Problema Identificado:**
- Similar al controlador de clientes, necesita verificación de datos

**Solución:**
```python
@auth.requires_membership('administrador')
def listar_todas():
    # Parámetros de búsqueda
    buscar = request.vars.buscar or ''
    estado = request.vars.estado or 'todos'
    tipo = request.vars.tipo or 'todos'
    
    # Query base con JOIN para obtener datos del cliente
    query = (db.cuentas.cliente_id == db.clientes.id) & \
            (db.clientes.user_id == db.auth_user.id)
    
    # Aplicar filtros
    if buscar:
        query &= ((db.cuentas.numero_cuenta.contains(buscar)) |
                 (db.clientes.cedula.contains(buscar)) |
                 (db.auth_user.first_name.contains(buscar)) |
                 (db.auth_user.last_name.contains(buscar)))
    
    if estado != 'todos':
        query &= (db.cuentas.estado == estado)
    
    if tipo != 'todos':
        query &= (db.cuentas.tipo_cuenta == tipo)
    
    # Obtener cuentas con paginación
    page = int(request.vars.page or 1)
    items_per_page = 25
    
    cuentas = db(query).select(
        db.cuentas.ALL,
        db.clientes.cedula,
        db.auth_user.first_name,
        db.auth_user.last_name,
        db.auth_user.email,
        orderby=~db.cuentas.fecha_creacion,
        limitby=((page-1)*items_per_page, page*items_per_page)
    )
    
    # Contar total para paginación
    total_cuentas = db(query).count()
    total_pages = (total_cuentas + items_per_page - 1) // items_per_page
    
    return dict(
        cuentas=cuentas,
        buscar=buscar,
        estado=estado,
        tipo=tipo,
        page=page,
        total_pages=total_pages,
        total_cuentas=total_cuentas
    )
```

## Modelos de Datos

### Estructura de Datos para Clientes
```python
# Datos que se pasan a la vista de clientes
{
    'clientes': [
        {
            'clientes': {
                'id': 1,
                'user_id': 2,
                'cedula': 'V-12345678',
                'fecha_registro': datetime(2024, 1, 15)
            },
            'auth_user': {
                'id': 2,
                'first_name': 'Juan',
                'last_name': 'Pérez',
                'email': 'juan.perez@email.com',
                'estado': 'activo'
            }
        }
    ],
    'buscar': '',
    'estado_filtro': 'todos',
    'page': 1,
    'total_pages': 1,
    'total_clientes': 1,
    'stats': {
        'total': 1,
        'activos': 1,
        'inactivos': 0
    }
}
```

### Estructura de Datos para Cuentas
```python
# Datos que se pasan a la vista de cuentas
{
    'cuentas': [
        {
            'cuentas': {
                'id': 1,
                'cliente_id': 1,
                'numero_cuenta': '20011234567890123456',
                'tipo_cuenta': 'corriente',
                'saldo_ves': Decimal('1000.00'),
                'saldo_usd': Decimal('50.00'),
                'saldo_eur': Decimal('25.00'),
                'estado': 'activa'
            },
            'clientes': {
                'cedula': 'V-12345678'
            },
            'auth_user': {
                'first_name': 'Juan',
                'last_name': 'Pérez',
                'email': 'juan.perez@email.com'
            }
        }
    ]
}
```

## Manejo de Errores

### 1. Errores de Base de Datos
```python
def listar():
    try:
        # Lógica de consulta
        clientes = db(query).select(...)
        return dict(clientes=clientes, ...)
    except Exception as e:
        # Log del error
        import logging
        logger = logging.getLogger("web2py.app.clientes")
        logger.error(f"Error al obtener lista de clientes: {str(e)}")
        
        # Mostrar mensaje de error al usuario
        response.flash = "Error al cargar la lista de clientes. Intente nuevamente."
        return dict(
            clientes=[],
            error_message="No se pudieron cargar los datos de clientes.",
            buscar='',
            estado_filtro='todos',
            page=1,
            total_pages=0,
            total_clientes=0,
            stats={'total': 0, 'activos': 0, 'inactivos': 0}
        )
```

### 2. Manejo de Registros Corruptos
```python
def procesar_clientes_seguros(clientes_raw):
    """Procesa clientes y maneja registros corruptos"""
    clientes_validos = []
    
    for cliente in clientes_raw:
        try:
            # Validar campos requeridos
            if (hasattr(cliente, 'clientes') and hasattr(cliente, 'auth_user') and
                cliente.clientes and cliente.auth_user and
                cliente.clientes.id and cliente.auth_user.first_name):
                clientes_validos.append(cliente)
            else:
                # Log del registro problemático
                logger.warning(f"Registro de cliente incompleto omitido: ID {getattr(cliente.clientes, 'id', 'unknown') if hasattr(cliente, 'clientes') else 'unknown'}")
        except Exception as e:
            logger.error(f"Error procesando registro de cliente: {str(e)}")
            continue
    
    return clientes_validos
```

## Estrategia de Testing

### 1. Pruebas de Controlador
```python
def test_listar_clientes():
    """Prueba que el controlador devuelve datos correctos"""
    # Crear cliente de prueba
    user_id = db.auth_user.insert(
        first_name='Test',
        last_name='User',
        email='test@test.com',
        password='test123'
    )
    
    cliente_id = db.clientes.insert(
        user_id=user_id,
        cedula='V-12345678'
    )
    
    # Ejecutar función del controlador
    result = exec_controller('clientes', 'listar')
    
    # Verificar resultados
    assert 'clientes' in result
    assert len(result['clientes']) > 0
    assert result['total_clientes'] > 0
```

### 2. Pruebas de Vista
```python
def test_vista_clientes_renderiza():
    """Prueba que la vista renderiza correctamente con datos"""
    # Datos de prueba
    test_data = {
        'clientes': [mock_cliente],
        'buscar': '',
        'estado_filtro': 'todos',
        'page': 1,
        'total_pages': 1,
        'total_clientes': 1,
        'stats': {'total': 1, 'activos': 1, 'inactivos': 0}
    }
    
    # Renderizar vista
    html = render_template('clientes/listar.html', test_data)
    
    # Verificar contenido
    assert 'Test User' in html
    assert 'V-12345678' in html
    assert 'test@test.com' in html
```

### 3. Pruebas de Integración
```python
def test_flujo_completo_listado():
    """Prueba el flujo completo desde controlador hasta vista"""
    # Crear datos de prueba
    setup_test_clients()
    
    # Simular request
    request.vars = Storage({'buscar': 'Test', 'estado': 'activo'})
    
    # Ejecutar controlador
    result = clientes_listar()
    
    # Verificar filtros aplicados
    assert all('Test' in (c.auth_user.first_name + c.auth_user.last_name) 
              for c in result['clientes'])
    assert all(c.auth_user.estado == 'activo' for c in result['clientes'])
```

## Consideraciones de Rendimiento

### 1. Optimización de Consultas
- Usar JOINs explícitos en lugar de consultas separadas
- Implementar índices en campos de búsqueda frecuente
- Limitar resultados con paginación

### 2. Cache de Datos
- Implementar cache para estadísticas que no cambian frecuentemente
- Cache de resultados de búsqueda por períodos cortos

### 3. Lazy Loading
- Cargar datos adicionales solo cuando sea necesario
- Implementar carga asíncrona para tablas grandes

## Seguridad

### 1. Validación de Entrada
- Sanitizar todos los parámetros de búsqueda
- Validar permisos antes de mostrar datos
- Escapar contenido HTML para prevenir XSS

### 2. Control de Acceso
- Verificar roles antes de mostrar datos sensibles
- Implementar filtros de datos basados en permisos
- Auditar accesos a listados de clientes

Esta solución de diseño aborda sistemáticamente el problema de visualización de registros, proporcionando una base sólida para la implementación de las correcciones necesarias.