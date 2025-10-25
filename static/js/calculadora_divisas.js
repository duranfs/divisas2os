/**
 * Calculadora de Divisas en Tiempo Real
 * Sistema de Divisas Bancario - Nueva Versión
 * El usuario ingresa cantidad de divisa, el sistema calcula bolívares
 */

class CalculadoraDivisas {
    constructor() {
        this.tasas = {
            USD: { compra: 36.50, venta: 36.80 },
            EUR: { compra: 40.25, venta: 40.60 },
            USDT: { compra: 36.45, venta: 36.75 }
        };
        this.tipoOperacion = this.detectarTipoOperacion();
        this.init();
    }

    async init() {
        console.log('Inicializando calculadora - Tipo:', this.tipoOperacion);
        await this.cargarTasas(); // Esperar a que se carguen las tasas
        this.configurarEventListeners();
        this.actualizarSimbolosDivisa();
        this.calcularBolivares(); // Calcular después de cargar tasas
    }

    detectarTipoOperacion() {
        const url = window.location.pathname;
        if (url.includes('comprar')) {
            return 'compra';
        } else if (url.includes('vender')) {
            return 'venta';
        }
        return 'compra'; // por defecto
    }

    configurarEventListeners() {
        // Evento principal: cuando cambia la cantidad de divisa
        $(document).on('input', '#cantidad_divisa', () => {
            this.calcularBolivares();
        });

        // Cuando cambia la divisa seleccionada
        $(document).on('change', '#moneda_destino, #moneda_origen', () => {
            this.actualizarSimbolosDivisa();
            this.calcularBolivares();
        });

        // El cálculo inicial se hace en init() después de cargar las tasas
    }

    actualizarSimbolosDivisa() {
        let monedaSeleccionada = '';
        
        if (this.tipoOperacion === 'compra') {
            const selectDivisa = document.getElementById('moneda_destino');
            monedaSeleccionada = selectDivisa ? selectDivisa.value : 'USD';
        } else {
            const selectDivisa = document.getElementById('moneda_origen');
            monedaSeleccionada = selectDivisa ? selectDivisa.value : 'USD';
        }

        // Actualizar símbolo en el input
        const simboloDivisa = document.getElementById('simbolo-divisa');
        if (simboloDivisa && monedaSeleccionada) {
            simboloDivisa.textContent = monedaSeleccionada;
        }
    }

    calcularBolivares() {
        const cantidadDivisa = document.getElementById('cantidad_divisa');
        const montoBolivaresCalculado = document.getElementById('monto_bolivares_calculado');
        const montoOrigenHidden = document.getElementById('monto_origen');

        if (!cantidadDivisa || !montoBolivaresCalculado) {
            console.log('Elementos no encontrados');
            return;
        }

        const cantidad = parseFloat(cantidadDivisa.value) || 0;
        let monedaSeleccionada = '';

        // Obtener la moneda según el tipo de operación
        if (this.tipoOperacion === 'compra') {
            const selectDivisa = document.getElementById('moneda_destino');
            monedaSeleccionada = selectDivisa ? selectDivisa.value : '';
        } else {
            const selectDivisa = document.getElementById('moneda_origen');
            monedaSeleccionada = selectDivisa ? selectDivisa.value : '';
        }

        if (cantidad > 0 && monedaSeleccionada && this.tasas[monedaSeleccionada]) {
            const tasa = this.tasas[monedaSeleccionada][this.tipoOperacion];
            const montoBolivares = cantidad * tasa;

            // Mostrar el resultado formateado
            montoBolivaresCalculado.value = this.formatearMonto(montoBolivares);
            
            // Actualizar campo oculto para enviar al servidor
            if (montoOrigenHidden) {
                montoOrigenHidden.value = montoBolivares.toFixed(2);
            }

            console.log(`Cálculo: ${cantidad} ${monedaSeleccionada} × ${tasa} = ${montoBolivares.toFixed(2)} VES`);
        } else {
            montoBolivaresCalculado.value = '0.00';
            if (montoOrigenHidden) {
                montoOrigenHidden.value = '0';
            }
        }
    }

    formatearMonto(monto) {
        return new Intl.NumberFormat('es-VE', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(monto);
    }

    async cargarTasas() {
        try {
            console.log('Cargando tasas desde el servidor...');
            const response = await fetch('/sistema_divisas/api/tasas_actuales');
            
            if (response.ok) {
                const data = await response.json();
                if (data.success && data.tasas) {
                    // Actualizar tasas manteniendo la estructura
                    Object.keys(data.tasas).forEach(moneda => {
                        if (this.tasas[moneda]) {
                            this.tasas[moneda] = data.tasas[moneda];
                        }
                    });
                    console.log('Tasas actualizadas:', this.tasas);
                } else {
                    console.warn('Respuesta del servidor sin tasas válidas, usando valores por defecto');
                }
            } else {
                console.warn('Error en respuesta del servidor, usando valores por defecto');
            }
        } catch (error) {
            console.warn('Error cargando tasas desde servidor, usando valores por defecto:', error);
        }
    }
}

// Auto-inicializar cuando el DOM esté listo
$(document).ready(async function() {
    // Solo inicializar si estamos en páginas de divisas
    if (window.location.pathname.includes('/divisas/')) {
        window.calculadoraDivisas = new CalculadoraDivisas();
    }
});