
# ANEXO C: PRUEBAS Y VALIDACIONES

## C.1 Plan de Pruebas Unitarias

### C.1.1 Pruebas del Modelo de Datos

```python
# test_models.py
import unittest
from gluon import *

class TestModels(unittest.TestCase):
    
    def setUp(self):
        self.db = DAL('sqlite:memory:')
        # Definir tablas de prueba
        
    def test_cliente_creation(self):
        """Probar creación de cliente"""
        cliente_id = self.db.clientes.insert(
            cedula='12345678',
            nombre='Juan',
            apellido='Pérez',
            email='juan@email.com'
        )
        self.assertIsNotNone(cliente_id)
        
    def test_cuenta_creation(self):
        """Probar creación de cuenta"""
        # Crear cliente primero
        cliente_id = self.db.clientes.insert(
            cedula='12345678',
            nombre='Juan',
            apellido='Pérez'
        )
        
        # Crear cuenta
        cuenta_id = self.db.cuentas.insert(
            cliente_id=cliente_id,
            numero_cuenta='1234567890',
            saldo_ves=1000.00
        )
        self.assertIsNotNone(cuenta_id)
        
    def test_transaccion_compra(self):
        """Probar transacción de compra"""
        # Setup inicial
        cliente_id = self.db.clientes.insert(
            cedula='12345678',
            nombre='Juan',
            apellido='Pérez'
        )
        
        cuenta_id = self.db.cuentas.insert(
            cliente_id=cliente_id,
            numero_cuenta='1234567890',
            saldo_ves=3650.00  # Para comprar 100 USD a tasa 36.50
        )
        
        # Procesar compra
        transaccion_id = self.db.transacciones.insert(
            cuenta_id=cuenta_id,
            tipo_operacion='compra',
            moneda_origen='VES',
            moneda_destino='USD',
            monto_origen=3650.00,
            monto_destino=100.00,
            tasa_cambio=36.50
        )
        
        self.assertIsNotNone(transaccion_id)
```

### C.1.2 Pruebas de Controladores

```python
# test_controllers.py
import unittest
from gluon.globals import Request, Response, Session
from gluon.storage import Storage

class TestControllers(unittest.TestCase):
    
    def setUp(self):
        # Configurar entorno de prueba
        self.request = Request({})
        self.response = Response()
        self.session = Session()
        
    def test_login_success(self):
        """Probar login exitoso"""
        # Simular datos de login
        self.request.vars = Storage({
            'email': 'test@email.com',
            'password': 'password123'
        })
        
        # Ejecutar función de login
        result = login()
        
        # Verificar resultado
        self.assertIsNotNone(result)
        
    def test_compra_divisas_fondos_suficientes(self):
        """Probar compra con fondos suficientes"""
        # Setup de datos de prueba
        self.request.vars = Storage({
            'cuenta_id': 1,
            'moneda_destino': 'USD',
            'monto_ves': 1000.00
        })
        
        # Ejecutar función
        result = comprar_divisas()
        
        # Verificar que no hay errores
        self.assertNotIn('error', result)
        
    def test_compra_divisas_fondos_insuficientes(self):
        """Probar compra con fondos insuficientes"""
        # Setup de datos de prueba
        self.request.vars = Storage({
            'cuenta_id': 1,
            'moneda_destino': 'USD',
            'monto_ves': 100000.00  # Monto muy alto
        })
        
        # Ejecutar función
        result = comprar_divisas()
        
        # Verificar que hay error de fondos
        self.assertIn('fondos insuficientes', str(result).lower())
```

## C.2 Pruebas de Integración

### C.2.1 Prueba de Integración con API BCV

```python
# test_integration_bcv.py
import unittest
import requests_mock
from controllers.api import obtener_tasa_bcv

class TestBCVIntegration(unittest.TestCase):
    
    @requests_mock.Mocker()
    def test_obtener_tasa_usd_success(self, m):
        """Probar obtención exitosa de tasa USD"""
        
        # Mock de respuesta del BCV
        html_response = '''
        <div id="dolar">
            <strong>36,50</strong>
        </div>
        '''
        
        m.get('https://www.bcv.org.ve/', text=html_response)
        
        # Ejecutar función
        tasa = obtener_tasa_bcv('USD')
        
        # Verificar resultado
        self.assertEqual(tasa, 36.50)
        
    @requests_mock.Mocker()
    def test_obtener_tasa_eur_success(self, m):
        """Probar obtención exitosa de tasa EUR"""
        
        # Mock de respuesta del BCV
        html_response = '''
        <div id="euro">
            <strong>39,80</strong>
        </div>
        '''
        
        m.get('https://www.bcv.org.ve/', text=html_response)
        
        # Ejecutar función
        tasa = obtener_tasa_bcv('EUR')
        
        # Verificar resultado
        self.assertEqual(tasa, 39.80)
        
    @requests_mock.Mocker()
    def test_obtener_tasa_error_fallback(self, m):
        """Probar fallback cuando falla la API"""
        
        # Simular error de conexión
        m.get('https://www.bcv.org.ve/', exc=requests.ConnectionError)
        
        # Ejecutar función
        tasa = obtener_tasa_bcv('USD')
        
        # Verificar que usa tasa de respaldo
        self.assertEqual(tasa, 36.50)  # Tasa de respaldo
```

## C.3 Pruebas de Rendimiento

### C.3.1 Prueba de Carga de Transacciones

```python
# test_performance.py
import unittest
import time
from concurrent.futures import ThreadPoolExecutor

class TestPerformance(unittest.TestCase):
    
    def test_concurrent_transactions(self):
        """Probar múltiples transacciones concurrentes"""
        
        def procesar_transaccion(i):
            # Simular procesamiento de transacción
            start_time = time.time()
            
            # Ejecutar operación de compra
            result = comprar_divisas_test(
                cuenta_id=1,
                monto_ves=100.00,
                moneda_destino='USD'
            )
            
            end_time = time.time()
            return end_time - start_time
        
        # Ejecutar 50 transacciones concurrentes
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(procesar_transaccion, i) 
                      for i in range(50)]
            
            tiempos = [future.result() for future in futures]
        
        # Verificar que todas las transacciones se completaron en tiempo razonable
        tiempo_promedio = sum(tiempos) / len(tiempos)
        self.assertLess(tiempo_promedio, 2.0)  # Menos de 2 segundos promedio
        
    def test_database_query_performance(self):
        """Probar rendimiento de consultas a la base de datos"""
        
        start_time = time.time()
        
        # Ejecutar consulta compleja
        result = db().select(
            db.clientes.ALL,
            db.cuentas.ALL,
            db.transacciones.ALL,
            left=[
                db.cuentas.on(db.cuentas.cliente_id == db.clientes.id),
                db.transacciones.on(db.transacciones.cuenta_id == db.cuentas.id)
            ],
            limitby=(0, 1000)
        )
        
        end_time = time.time()
        tiempo_consulta = end_time - start_time
        
        # Verificar que la consulta se ejecuta en tiempo razonable
        self.assertLess(tiempo_consulta, 1.0)  # Menos de 1 segundo
```

## C.4 Casos de Prueba de Usuario

### C.4.1 Escenarios de Prueba Manual

| ID | Escenario | Pasos | Resultado Esperado |
|----|-----------|-------|-------------------|
| TC001 | Registro de nuevo cliente | 1. Ir a registro<br>2. Llenar formulario<br>3. Enviar | Cliente creado exitosamente |
| TC002 | Login con credenciales válidas | 1. Ir a login<br>2. Ingresar email/password<br>3. Enviar | Acceso al dashboard |
| TC003 | Compra de USD con fondos suficientes | 1. Ir a comprar divisas<br>2. Seleccionar cuenta<br>3. Ingresar monto<br>4. Confirmar | Transacción procesada |
| TC004 | Compra de USD con fondos insuficientes | 1. Ir a comprar divisas<br>2. Ingresar monto alto<br>3. Confirmar | Error de fondos insuficientes |
| TC005 | Consulta de historial | 1. Ir a historial<br>2. Seleccionar rango de fechas | Lista de transacciones |

### C.4.2 Criterios de Aceptación

- **Funcionalidad**: Todas las funciones principales deben operar correctamente
- **Rendimiento**: Tiempo de respuesta < 3 segundos para operaciones normales
- **Seguridad**: Validación de entrada en todos los formularios
- **Usabilidad**: Interfaz intuitiva y mensajes de error claros
- **Compatibilidad**: Funciona en Chrome, Firefox, Safari, Edge
- **Responsividad**: Adaptable a dispositivos móviles y tablets
