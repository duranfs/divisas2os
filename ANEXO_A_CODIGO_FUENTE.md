
# ANEXO A: CÓDIGO FUENTE PRINCIPAL

## A.1 Estructura del Proyecto

```
sistema_divisas/
├── controllers/
│   ├── default.py          # Dashboard y autenticación
│   ├── clientes.py         # Gestión de clientes
│   ├── cuentas.py          # Manejo de cuentas
│   ├── divisas.py          # Operaciones de divisas
│   └── reportes.py         # Reportes administrativos
├── models/
│   ├── db.py               # Modelos de base de datos
│   └── menu.py             # Configuración de menú
├── views/
│   ├── layout.html         # Template base
│   ├── clientes/           # Vistas de clientes
│   ├── cuentas/            # Vistas de cuentas
│   └── divisas/            # Vistas de divisas
└── static/
    ├── css/                # Hojas de estilo
    ├── js/                 # JavaScript
    └── images/             # Imágenes
```

## A.2 Modelo de Base de Datos Principal

```python
# Tabla de clientes
db.define_table('clientes',
    Field('cedula', 'string', length=12, unique=True, notnull=True),
    Field('nombre', 'string', length=100, notnull=True),
    Field('apellido', 'string', length=100, notnull=True),
    Field('email', 'string', length=150),
    Field('telefono', 'string', length=20),
    Field('direccion', 'text'),
    Field('fecha_registro', 'datetime', default=request.now),
    Field('activo', 'boolean', default=True),
    format='%(nombre)s %(apellido)s'
)

# Tabla de cuentas bancarias
db.define_table('cuentas',
    Field('cliente_id', 'reference clientes', notnull=True),
    Field('numero_cuenta', 'string', length=20, unique=True, notnull=True),
    Field('tipo_cuenta', 'string', length=20, default='ahorro'),
    Field('saldo_ves', 'decimal(15,2)', default=0),
    Field('saldo_usd', 'decimal(15,2)', default=0),
    Field('saldo_eur', 'decimal(15,2)', default=0),
    Field('fecha_apertura', 'datetime', default=request.now),
    Field('activa', 'boolean', default=True),
    format='%(numero_cuenta)s'
)

# Tabla de transacciones
db.define_table('transacciones',
    Field('cuenta_id', 'reference cuentas', notnull=True),
    Field('tipo_operacion', 'string', length=20, notnull=True),
    Field('moneda_origen', 'string', length=3, notnull=True),
    Field('moneda_destino', 'string', length=3, notnull=True),
    Field('monto_origen', 'decimal(15,2)', notnull=True),
    Field('monto_destino', 'decimal(15,2)', notnull=True),
    Field('tasa_cambio', 'decimal(10,4)', notnull=True),
    Field('comprobante', 'string', length=50, unique=True),
    Field('fecha_transaccion', 'datetime', default=request.now),
    Field('procesada', 'boolean', default=False)
)
```

## A.3 Controlador Principal de Divisas

```python
def comprar_divisas():
    """Función para comprar USD o EUR con VES"""
    
    if not auth.is_logged_in():
        redirect(URL('default', 'user/login'))
    
    form = FORM(
        DIV(
            LABEL('Cuenta:', _for='cuenta'),
            SELECT(_name='cuenta_id', _id='cuenta', requires=IS_IN_DB(
                db(db.cuentas.cliente_id == auth.user.id), 
                'cuentas.id', '%(numero_cuenta)s'
            )),
            _class='form-group'
        ),
        DIV(
            LABEL('Moneda a comprar:', _for='moneda'),
            SELECT('USD', 'EUR', _name='moneda_destino', _id='moneda'),
            _class='form-group'
        ),
        DIV(
            LABEL('Monto en VES:', _for='monto'),
            INPUT(_name='monto_ves', _type='number', _step='0.01', 
                  _min='0', _id='monto', _class='form-control'),
            _class='form-group'
        ),
        INPUT(_type='submit', _value='Comprar', _class='btn btn-primary')
    )
    
    if form.process().accepted:
        # Obtener tasa actual del BCV
        tasa = obtener_tasa_bcv(form.vars.moneda_destino)
        
        # Calcular monto en divisa
        monto_divisa = float(form.vars.monto_ves) / tasa
        
        # Validar fondos suficientes
        cuenta = db.cuentas[form.vars.cuenta_id]
        if cuenta.saldo_ves >= float(form.vars.monto_ves):
            
            # Procesar transacción
            db.transacciones.insert(
                cuenta_id=form.vars.cuenta_id,
                tipo_operacion='compra',
                moneda_origen='VES',
                moneda_destino=form.vars.moneda_destino,
                monto_origen=form.vars.monto_ves,
                monto_destino=monto_divisa,
                tasa_cambio=tasa,
                comprobante=generar_comprobante()
            )
            
            # Actualizar saldos
            if form.vars.moneda_destino == 'USD':
                cuenta.update_record(
                    saldo_ves=cuenta.saldo_ves - float(form.vars.monto_ves),
                    saldo_usd=cuenta.saldo_usd + monto_divisa
                )
            else:  # EUR
                cuenta.update_record(
                    saldo_ves=cuenta.saldo_ves - float(form.vars.monto_ves),
                    saldo_eur=cuenta.saldo_eur + monto_divisa
                )
            
            session.flash = 'Compra realizada exitosamente'
            redirect(URL('cuentas', 'mis_cuentas'))
        else:
            form.errors.monto_ves = 'Fondos insuficientes'
    
    return dict(form=form)
```

## A.4 Integración con API del BCV

```python
import requests
from bs4 import BeautifulSoup
import cache

def obtener_tasa_bcv(moneda='USD'):
    """Obtener tasa oficial del BCV con cache"""
    
    cache_key = f'tasa_{moneda}'
    tasa = cache.ram(cache_key, lambda: None, time_expire=300)  # 5 minutos
    
    if tasa is None:
        try:
            url = 'https://www.bcv.org.ve/'
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            if moneda == 'USD':
                elemento = soup.find('div', {'id': 'dolar'})
            elif moneda == 'EUR':
                elemento = soup.find('div', {'id': 'euro'})
            
            if elemento:
                tasa_texto = elemento.find('strong').text
                tasa = float(tasa_texto.replace(',', '.'))
                cache.ram(cache_key, lambda: tasa, time_expire=300)
            else:
                # Tasa de respaldo si falla el scraping
                tasa = 36.50 if moneda == 'USD' else 39.80
                
        except Exception as e:
            # Log del error y usar tasa de respaldo
            logger.error(f'Error obteniendo tasa BCV: {e}')
            tasa = 36.50 if moneda == 'USD' else 39.80
    
    return tasa
```
