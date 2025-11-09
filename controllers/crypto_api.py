# -*- coding: utf-8 -*-
"""
Controlador Crypto API - Sistema de Divisas Bancario
Maneja la obtención de tasas de criptomonedas desde fuentes externas
"""

import logging
import datetime
import json
from decimal import Decimal, InvalidOperation

# Importar urllib para hacer requests HTTP
try:
    from urllib.request import urlopen, Request
    from urllib.error import URLError, HTTPError
    from urllib.parse import urlencode
except ImportError:
    from urllib2 import urlopen, Request, URLError, HTTPError
    from urllib import urlencode

# Intentar importar requests si está disponible
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# Configurar logging
logger = logging.getLogger("web2py.app.divisas.crypto")

# Configuración de APIs de criptomonedas
CRYPTO_APIS = {
    'coingecko': {
        'url': 'https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=usd',
        'timeout': 10,
        'headers': {
            'User-Agent': 'Sistema-Divisas-Bancario/1.0'
        }
    },
    'coinapi': {
        'url': 'https://rest.coinapi.io/v1/exchangerate/USDT/USD',
        'timeout': 10,
        'headers': {
            'User-Agent': 'Sistema-Divisas-Bancario/1.0',
            # 'X-CoinAPI-Key': 'TU_API_KEY_AQUI'  # Opcional si tienes API key
        }
    },
    'binance': {
        'url': 'https://api.binance.com/api/v3/ticker/price?symbol=USDTUSD',
        'timeout': 10,
        'headers': {
            'User-Agent': 'Sistema-Divisas-Bancario/1.0'
        }
    }
}

def obtener_tasa_usdt():
    """
    Obtiene la tasa USDT/USD desde múltiples fuentes
    Retorna la tasa USDT en VES basada en USD
    """
    try:
        logger.info("Iniciando obtención de tasa USDT")
        
        # Obtener tasa USD/VES actual
        tasa_usd_ves = obtener_tasa_usd_actual()
        if not tasa_usd_ves:
            logger.error("No se pudo obtener tasa USD/VES")
            return None
        
        # Intentar obtener USDT/USD desde diferentes APIs
        usdt_usd_rate = None
        
        # Intentar CoinGecko primero
        usdt_usd_rate = obtener_usdt_coingecko()
        if usdt_usd_rate:
            logger.info(f"Tasa USDT/USD obtenida de CoinGecko: {usdt_usd_rate}")
        else:
            # Intentar Binance como respaldo
            usdt_usd_rate = obtener_usdt_binance()
            if usdt_usd_rate:
                logger.info(f"Tasa USDT/USD obtenida de Binance: {usdt_usd_rate}")
            else:
                # Usar valor por defecto (USDT ≈ 1 USD)
                usdt_usd_rate = 0.9999
                logger.warning("Usando tasa USDT/USD por defecto: 0.9999")
        
        # Calcular USDT/VES = USDT/USD * USD/VES
        usdt_ves_rate = float(usdt_usd_rate) * float(tasa_usd_ves)
        
        logger.info(f"Tasa USDT/VES calculada: {usdt_ves_rate}")
        return round(usdt_ves_rate, 4)
        
    except Exception as e:
        logger.error(f"Error obteniendo tasa USDT: {str(e)}")
        return None

def obtener_tasa_usd_actual():
    """Obtiene la tasa USD/VES actual de la base de datos"""
    try:
        tasa_actual = db(db.tasas_cambio.activa == True).select(
            orderby=~db.tasas_cambio.fecha | ~db.tasas_cambio.hora,
            limitby=(0, 1)
        ).first()
        
        if tasa_actual and tasa_actual.usd_ves:
            return float(tasa_actual.usd_ves)
        
        # Si no hay tasa activa, buscar la más reciente
        tasa_reciente = db().select(
            db.tasas_cambio.ALL,
            orderby=~db.tasas_cambio.fecha | ~db.tasas_cambio.hora,
            limitby=(0, 1)
        ).first()
        
        if tasa_reciente and tasa_reciente.usd_ves:
            return float(tasa_reciente.usd_ves)
        
        return None
        
    except Exception as e:
        logger.error(f"Error obteniendo tasa USD actual: {str(e)}")
        return None

def obtener_usdt_coingecko():
    """Obtiene tasa USDT/USD desde CoinGecko API"""
    try:
        config = CRYPTO_APIS['coingecko']
        
        if HAS_REQUESTS:
            response = requests.get(
                config['url'],
                timeout=config['timeout'],
                headers=config['headers']
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'tether' in data and 'usd' in data['tether']:
                    return float(data['tether']['usd'])
        else:
            # Usar urllib como alternativa
            req = Request(config['url'])
            for key, value in config['headers'].items():
                req.add_header(key, value)
            
            response = urlopen(req, timeout=config['timeout'])
            if response.getcode() == 200:
                content = response.read()
                data = json.loads(content.decode('utf-8'))
                if 'tether' in data and 'usd' in data['tether']:
                    return float(data['tether']['usd'])
        
        return None
        
    except Exception as e:
        logger.warning(f"Error obteniendo USDT desde CoinGecko: {str(e)}")
        return None

def obtener_usdt_binance():
    """Obtiene tasa USDT/USD desde Binance API"""
    try:
        config = CRYPTO_APIS['binance']
        
        if HAS_REQUESTS:
            response = requests.get(
                config['url'],
                timeout=config['timeout'],
                headers=config['headers']
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'price' in data:
                    # Binance devuelve el precio como string
                    return float(data['price'])
        else:
            # Usar urllib como alternativa
            req = Request(config['url'])
            for key, value in config['headers'].items():
                req.add_header(key, value)
            
            response = urlopen(req, timeout=config['timeout'])
            if response.getcode() == 200:
                content = response.read()
                data = json.loads(content.decode('utf-8'))
                if 'price' in data:
                    return float(data['price'])
        
        return None
        
    except Exception as e:
        logger.warning(f"Error obteniendo USDT desde Binance: {str(e)}")
        return None

def obtener_usdt_coinapi():
    """Obtiene tasa USDT/USD desde CoinAPI (requiere API key)"""
    try:
        config = CRYPTO_APIS['coinapi']
        
        # Solo intentar si hay API key configurada
        if 'X-CoinAPI-Key' not in config['headers']:
            logger.info("CoinAPI no configurada (falta API key)")
            return None
        
        if HAS_REQUESTS:
            response = requests.get(
                config['url'],
                timeout=config['timeout'],
                headers=config['headers']
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'rate' in data:
                    return float(data['rate'])
        else:
            # Usar urllib como alternativa
            req = Request(config['url'])
            for key, value in config['headers'].items():
                req.add_header(key, value)
            
            response = urlopen(req, timeout=config['timeout'])
            if response.getcode() == 200:
                content = response.read()
                data = json.loads(content.decode('utf-8'))
                if 'rate' in data:
                    return float(data['rate'])
        
        return None
        
    except Exception as e:
        logger.warning(f"Error obteniendo USDT desde CoinAPI: {str(e)}")
        return None

@auth.requires_membership('administrador')
def actualizar_tasa_usdt():
    """
    Función administrativa para actualizar solo la tasa USDT
    """
    try:
        logger.info("Actualizando tasa USDT manualmente")
        
        # Obtener nueva tasa USDT
        nueva_tasa_usdt = obtener_tasa_usdt()
        
        if nueva_tasa_usdt:
            # Actualizar la tasa activa actual
            tasa_activa = db(db.tasas_cambio.activa == True).select().first()
            
            if tasa_activa:
                # Actualizar la tasa existente
                db(db.tasas_cambio.id == tasa_activa.id).update(
                    usdt_ves=nueva_tasa_usdt,
                    fuente_usdt='CoinGecko/Binance'
                )
                db.commit()
                
                logger.info(f"Tasa USDT actualizada: {nueva_tasa_usdt}")
                
                return response.json({
                    'success': True,
                    'mensaje': f'Tasa USDT actualizada: {nueva_tasa_usdt}',
                    'tasa_usdt': nueva_tasa_usdt
                })
            else:
                return response.json({
                    'success': False,
                    'mensaje': 'No hay tasa activa para actualizar'
                })
        else:
            return response.json({
                'success': False,
                'mensaje': 'No se pudo obtener tasa USDT desde las APIs'
            })
            
    except Exception as e:
        logger.error(f"Error actualizando tasa USDT: {str(e)}")
        return response.json({
            'success': False,
            'mensaje': f'Error: {str(e)}'
        })

def test_apis_crypto():
    """
    Función de prueba para verificar conectividad con APIs de criptomonedas
    """
    resultados = {
        'coingecko': {'disponible': False, 'tasa': None, 'error': None},
        'binance': {'disponible': False, 'tasa': None, 'error': None},
        'coinapi': {'disponible': False, 'tasa': None, 'error': None}
    }
    
    # Probar CoinGecko
    try:
        tasa_cg = obtener_usdt_coingecko()
        if tasa_cg:
            resultados['coingecko']['disponible'] = True
            resultados['coingecko']['tasa'] = tasa_cg
        else:
            resultados['coingecko']['error'] = 'No se pudo obtener tasa'
    except Exception as e:
        resultados['coingecko']['error'] = str(e)
    
    # Probar Binance
    try:
        tasa_bn = obtener_usdt_binance()
        if tasa_bn:
            resultados['binance']['disponible'] = True
            resultados['binance']['tasa'] = tasa_bn
        else:
            resultados['binance']['error'] = 'No se pudo obtener tasa'
    except Exception as e:
        resultados['binance']['error'] = str(e)
    
    # Probar CoinAPI
    try:
        tasa_ca = obtener_usdt_coinapi()
        if tasa_ca:
            resultados['coinapi']['disponible'] = True
            resultados['coinapi']['tasa'] = tasa_ca
        else:
            resultados['coinapi']['error'] = 'API key no configurada o error'
    except Exception as e:
        resultados['coinapi']['error'] = str(e)
    
    return dict(
        resultados=resultados,
        has_requests=HAS_REQUESTS,
        timestamp=datetime.datetime.now().isoformat()
    )

# Función pública para obtener tasa USDT (sin autenticación)
def consultar_tasa_usdt():
    """
    Consulta pública de la tasa USDT actual
    """
    try:
        tasa_actual = db(db.tasas_cambio.activa == True).select().first()
        
        if tasa_actual and tasa_actual.usdt_ves:
            return response.json({
                'success': True,
                'tasa_usdt_ves': float(tasa_actual.usdt_ves),
                'fecha': str(tasa_actual.fecha),
                'hora': str(tasa_actual.hora),
                'fuente': getattr(tasa_actual, 'fuente_usdt', 'Sistema')
            })
        else:
            return response.json({
                'success': False,
                'mensaje': 'No hay tasa USDT disponible'
            })
            
    except Exception as e:
        logger.error(f"Error consultando tasa USDT: {str(e)}")
        return response.json({
            'success': False,
            'mensaje': 'Error interno del servidor'
        })