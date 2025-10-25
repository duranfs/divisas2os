/**
 * Calculadora Simple de Divisas
 * Versión simplificada que funciona sin complicaciones
 */

// Variables globales
let tasasGlobales = {
    USD: { compra: 36.50, venta: 36.80 },
    EUR: { compra: 40.25, venta: 40.60 },
    USDT: { compra: 36.45, venta: 36.75 }
};

// Función para cargar tasas desde la API
async function cargarTasasSimples() {
    try {
        console.log('🔄 Cargando tasas desde API...');
        console.log('📍 URL de API:', '/sistema_divisas/api/tasas_simples');
        
        const response = await fetch('/sistema_divisas/api/tasas_simples');
        console.log('📡 Respuesta de API:', response.status, response.statusText);
        
        if (response.ok) {
            const data = await response.json();
            console.log('📊 Datos recibidos:', data);
            
            if (data.success && data.tasas) {
                tasasGlobales = data.tasas;
                console.log('✅ Tasas cargadas exitosamente:', tasasGlobales);
                console.log('💰 USD Compra:', tasasGlobales.USD.compra, 'Venta:', tasasGlobales.USD.venta);
                console.log('💰 EUR Compra:', tasasGlobales.EUR.compra, 'Venta:', tasasGlobales.EUR.venta);
                return true;
            } else {
                console.log('⚠️ Respuesta sin tasas válidas:', data);
            }
        } else {
            console.log('❌ Error en respuesta HTTP:', response.status);
        }
        
        console.log('⚠️ Usando tasas por defecto');
        return false;
    } catch (error) {
        console.log('❌ Error cargando tasas, usando por defecto:', error);
        console.log('🔍 Detalles del error:', error.message);
        return false;
    }
}

// Calculadora para COMPRAR (usuario ingresa divisa, calcula bolívares)
function inicializarCalculadoraCompra() {
    console.log('🧮 Inicializando calculadora de COMPRA...');
    
    const cantidadInput = document.getElementById('cantidad_divisa');
    const monedaSelect = document.getElementById('moneda_destino');
    const bolivaresOutput = document.getElementById('monto_bolivares_calculado');
    const montoHidden = document.getElementById('monto_origen');
    
    if (!cantidadInput || !monedaSelect || !bolivaresOutput) {
        console.log('❌ Elementos no encontrados para calculadora de compra');
        return;
    }
    
    function calcularCompra() {
        const cantidad = parseFloat(cantidadInput.value) || 0;
        const moneda = monedaSelect.value;
        
        console.log('🧮 Calculando compra:', {cantidad, moneda});
        
        if (cantidad > 0 && moneda && tasasGlobales[moneda]) {
            const tasa = tasasGlobales[moneda].compra;
            const bolivares = cantidad * tasa;
            
            console.log(`🧮 COMPRA: ${cantidad} ${moneda} × ${tasa} = ${bolivares.toFixed(2)} VES`);
            console.log('📊 Tasas disponibles:', tasasGlobales);
            
            bolivaresOutput.value = bolivares.toLocaleString('es-ES', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });
            
            if (montoHidden) {
                montoHidden.value = bolivares.toFixed(2);
            }
        } else {
            bolivaresOutput.value = '0.00';
            if (montoHidden) {
                montoHidden.value = '0';
            }
        }
    }
    
    // Event listeners
    cantidadInput.addEventListener('input', calcularCompra);
    monedaSelect.addEventListener('change', calcularCompra);
    
    console.log('✅ Calculadora de compra configurada');
}

// Calculadora para VENDER (usuario ingresa divisa, calcula bolívares)
function inicializarCalculadoraVenta() {
    console.log('🧮 Inicializando calculadora de VENTA...');
    
    const cantidadInput = document.getElementById('cantidad_divisa_venta');
    const monedaSelect = document.getElementById('moneda_origen');
    const bolivaresOutput = document.getElementById('monto_bolivares_recibir');
    const montoHidden = document.getElementById('monto_destino');
    
    if (!cantidadInput || !monedaSelect || !bolivaresOutput) {
        console.log('❌ Elementos no encontrados para calculadora de venta');
        return;
    }
    
    function calcularVenta() {
        const cantidad = parseFloat(cantidadInput.value) || 0;
        const moneda = monedaSelect.value;
        
        console.log('🧮 Calculando venta:', {cantidad, moneda});
        
        if (cantidad > 0 && moneda && tasasGlobales[moneda]) {
            const tasa = tasasGlobales[moneda].venta;
            const bolivares = cantidad * tasa;
            
            console.log(`🧮 VENTA: ${cantidad} ${moneda} × ${tasa} = ${bolivares.toFixed(2)} VES`);
            console.log('📊 Tasas disponibles:', tasasGlobales);
            
            bolivaresOutput.value = bolivares.toLocaleString('es-ES', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });
            
            if (montoHidden) {
                montoHidden.value = bolivares.toFixed(2);
            }
        } else {
            bolivaresOutput.value = '0.00';
            if (montoHidden) {
                montoHidden.value = '0';
            }
        }
    }
    
    // Event listeners
    cantidadInput.addEventListener('input', calcularVenta);
    monedaSelect.addEventListener('change', calcularVenta);
    
    console.log('✅ Calculadora de venta configurada');
}

// Auto-inicialización
document.addEventListener('DOMContentLoaded', async function() {
    console.log('🚀 Inicializando calculadoras simples...');
    
    // Cargar tasas primero
    await cargarTasasSimples();
    
    // Detectar qué página estamos y configurar la calculadora apropiada
    const url = window.location.pathname;
    
    if (url.includes('comprar')) {
        console.log('📄 Página de COMPRAR detectada');
        inicializarCalculadoraCompra();
    } else if (url.includes('vender')) {
        console.log('📄 Página de VENDER detectada');
        inicializarCalculadoraVenta();
    } else {
        console.log('📄 Página no reconocida para calculadora');
    }
    
    console.log('✅ Inicialización completada');
});