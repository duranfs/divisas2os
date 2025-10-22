/**
 * Calculadora de Divisas en Tiempo Real
 * Sistema de Divisas Bancario
 * Requisitos: 4.1, 5.1
 */

class CalculadoraDivisas {
    constructor() {
        this.tasasActuales = null;
        this.ultimaActualizacion = null;
        this.intervalId = null;
        this.init();
    }

    init() {
        // Obtener tasas iniciales
        this.obtenerTasas();
        
        // Configurar actualización automática cada 5 minutos
        this.intervalId = setInterval(() => {
            this.obtenerTasas();
        }, 300000); // 5 minutos
        
        // Configurar event listeners
        this.configurarEventListeners();
    }

    configurarEventListeners() {
        // Listeners para campos de monto
        $(document).on('input', '.monto-origen', (e) => {
            this.calcularCambio(e.target);
        });

        // Listeners para selección de moneda
        $(document).on('change', '.moneda-origen, .moneda-destino', (e) => {
            const container = $(e.target).closest('.calculadora-container');
            this.calcularCambioContainer(container);
        });

        // Listener para tipo de operación
        $(document).on('change', '.tipo-operacion', (e) => {
            const container = $(e.target).closest('.calculadora-container');
            this.actualizarTipoOperacion(container);
        });

        // Listener para validación de fondos
        $(document).on('change', '.cuenta-selector', (e) => {
            const container = $(e.target).closest('.calculadora-container');
            this.validarFondos(container);
        });
    }

    async obtenerTasas() {
        try {
            const response = await fetch('/divisas/tasas_actuales');
            const data = await response.json();
            
            if (data.success) {
                this.tasasActuales = data.tasas;
                this.ultimaActualizacion = new Date();
                this.actualizarWidgetTasas();
                console.log('Tasas actualizadas:', this.tasasActuales);
            } else {
                console.error('Error obteniendo tasas:', data.error);
                this.mostrarError('Error obteniendo tasas de cambio');
            }
        } catch (error) {
            console.error('Error en petición de tasas:', error);
            this.mostrarError('Error de conexión al obtener tasas');
        }
    }

    actualizarWidgetTasas() {
        if (!this.tasasActuales) return;

        // Actualizar widget de tasas en el dashboard
        $('.tasa-usd-ves').text(this.formatearTasa(this.tasasActuales.usd_ves));
        $('.tasa-eur-ves').text(this.formatearTasa(this.tasasActuales.eur_ves));
        $('.fecha-actualizacion').text(this.formatearFechaHora(this.tasasActuales.fecha, this.tasasActuales.hora));
        $('.fuente-tasa').text(this.tasasActuales.fuente);
        
        // Actualizar indicador de estado
        $('.estado-tasas').removeClass('text-danger').addClass('text-success').text('Actualizado');
    }

    async calcularCambio(inputElement) {
        const container = $(inputElement).closest('.calculadora-container');
        await this.calcularCambioContainer(container);
    }

    async calcularCambioContainer(container) {
        try {
            const monto = parseFloat(container.find('.monto-origen').val()) || 0;
            const monedaOrigen = container.find('.moneda-origen').val();
            const monedaDestino = container.find('.moneda-destino').val();
            const tipoOperacion = container.find('.tipo-operacion').val();

            if (monto <= 0) {
                this.limpiarResultados(container);
                return;
            }

            if (!monedaOrigen || !monedaDestino || !tipoOperacion) {
                this.limpiarResultados(container);
                return;
            }

            // Mostrar indicador de carga
            container.find('.calculando-indicator').show();

            const response = await fetch('/divisas/calcular_cambio', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    monto: monto,
                    moneda_origen: monedaOrigen,
                    moneda_destino: monedaDestino,
                    tipo_operacion: tipoOperacion
                })
            });

            const data = await response.json();
            
            if (data.success) {
                this.mostrarResultados(container, data);
                await this.validarFondos(container);
            } else {
                this.mostrarErrorCalculadora(container, data.error);
            }

        } catch (error) {
            console.error('Error calculando cambio:', error);
            this.mostrarErrorCalculadora(container, 'Error de conexión');
        } finally {
            container.find('.calculando-indicator').hide();
        }
    }

    mostrarResultados(container, data) {
        // Actualizar campos de resultado
        container.find('.monto-destino').val(this.formatearMonto(data.monto_convertido));
        container.find('.comision-calculada').text(this.formatearMonto(data.comision));
        container.find('.total-debitado').text(this.formatearMonto(data.total_debitado));
        container.find('.tasa-aplicada').text(this.formatearTasa(data.tasa_aplicada));
        
        // Mostrar información de la tasa
        container.find('.info-tasa').show();
        container.find('.fecha-tasa').text(`${data.fecha_tasa} ${data.hora_tasa}`);
        
        // Mostrar resumen de la operación
        container.find('.resumen-operacion').show();
        
        // Limpiar errores previos
        container.find('.error-calculadora').hide();
    }

    mostrarErrorCalculadora(container, mensaje) {
        container.find('.error-calculadora').text(mensaje).show();
        this.limpiarResultados(container);
    }

    limpiarResultados(container) {
        container.find('.monto-destino').val('');
        container.find('.comision-calculada').text('0.00');
        container.find('.total-debitado').text('0.00');
        container.find('.tasa-aplicada').text('0.0000');
        container.find('.info-tasa').hide();
        container.find('.resumen-operacion').hide();
        container.find('.validacion-fondos').hide();
    }

    async validarFondos(container) {
        try {
            const cuentaId = container.find('.cuenta-selector').val();
            const monto = parseFloat(container.find('.total-debitado').text()) || 0;
            const tipoOperacion = container.find('.tipo-operacion').val();
            
            if (!cuentaId || monto <= 0) {
                container.find('.validacion-fondos').hide();
                return;
            }

            // Determinar la moneda a validar según el tipo de operación
            let moneda;
            if (tipoOperacion === 'compra') {
                moneda = 'VES'; // Para compra se debita VES
            } else {
                moneda = container.find('.moneda-origen').val(); // Para venta se debita la divisa extranjera
            }

            const response = await fetch('/divisas/validar_fondos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    cuenta_id: cuentaId,
                    monto: monto,
                    moneda: moneda
                })
            });

            const data = await response.json();
            
            if (data.success) {
                this.mostrarValidacionFondos(container, data, moneda);
            } else {
                this.mostrarErrorValidacion(container, data.error);
            }

        } catch (error) {
            console.error('Error validando fondos:', error);
            this.mostrarErrorValidacion(container, 'Error validando fondos');
        }
    }

    mostrarValidacionFondos(container, data, moneda) {
        const validacionDiv = container.find('.validacion-fondos');
        validacionDiv.show();

        if (data.fondos_suficientes) {
            validacionDiv.removeClass('alert-danger').addClass('alert-success');
            validacionDiv.find('.icono-validacion').removeClass('fa-times-circle').addClass('fa-check-circle');
            validacionDiv.find('.mensaje-validacion').text('Fondos suficientes');
            validacionDiv.find('.detalle-fondos').text(
                `Saldo disponible: ${this.formatearMonto(data.saldo_disponible)} ${moneda}`
            );
            
            // Habilitar botón de confirmación
            container.find('.btn-confirmar-transaccion').prop('disabled', false);
        } else {
            validacionDiv.removeClass('alert-success').addClass('alert-danger');
            validacionDiv.find('.icono-validacion').removeClass('fa-check-circle').addClass('fa-times-circle');
            validacionDiv.find('.mensaje-validacion').text('Fondos insuficientes');
            validacionDiv.find('.detalle-fondos').text(
                `Saldo disponible: ${this.formatearMonto(data.saldo_disponible)} ${moneda} | ` +
                `Faltante: ${this.formatearMonto(Math.abs(data.diferencia))} ${moneda}`
            );
            
            // Deshabilitar botón de confirmación
            container.find('.btn-confirmar-transaccion').prop('disabled', true);
        }
    }

    mostrarErrorValidacion(container, mensaje) {
        const validacionDiv = container.find('.validacion-fondos');
        validacionDiv.show().removeClass('alert-success').addClass('alert-warning');
        validacionDiv.find('.icono-validacion').removeClass('fa-check-circle fa-times-circle').addClass('fa-exclamation-triangle');
        validacionDiv.find('.mensaje-validacion').text('Error en validación');
        validacionDiv.find('.detalle-fondos').text(mensaje);
        
        // Deshabilitar botón de confirmación por seguridad
        container.find('.btn-confirmar-transaccion').prop('disabled', true);
    }

    actualizarTipoOperacion(container) {
        const tipoOperacion = container.find('.tipo-operacion').val();
        
        if (tipoOperacion === 'compra') {
            // Compra: VES -> USD/EUR
            container.find('.moneda-origen').val('VES').prop('disabled', true);
            container.find('.moneda-destino').prop('disabled', false);
            container.find('.label-monto-origen').text('Monto en VES a cambiar:');
            container.find('.label-monto-destino').text('Recibirá:');
        } else if (tipoOperacion === 'venta') {
            // Venta: USD/EUR -> VES
            container.find('.moneda-origen').prop('disabled', false);
            container.find('.moneda-destino').val('VES').prop('disabled', true);
            container.find('.label-monto-origen').text('Monto en divisa a vender:');
            container.find('.label-monto-destino').text('Recibirá en VES:');
        }
        
        // Recalcular si hay valores
        this.calcularCambioContainer(container);
    }

    formatearMonto(monto) {
        return parseFloat(monto).toLocaleString('es-VE', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }

    formatearTasa(tasa) {
        return parseFloat(tasa).toLocaleString('es-VE', {
            minimumFractionDigits: 4,
            maximumFractionDigits: 4
        });
    }

    formatearFechaHora(fecha, hora) {
        try {
            const fechaObj = new Date(`${fecha}T${hora}`);
            return fechaObj.toLocaleString('es-VE', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit'
            });
        } catch (error) {
            return `${fecha} ${hora}`;
        }
    }

    mostrarError(mensaje) {
        // Mostrar error en el widget de tasas
        $('.estado-tasas').removeClass('text-success').addClass('text-danger').text('Error');
        
        // Mostrar notificación si existe el sistema
        if (typeof toastr !== 'undefined') {
            toastr.error(mensaje);
        } else {
            console.error(mensaje);
        }
    }

    destruir() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
        }
    }
}

// Funciones de utilidad globales
window.CalculadoraDivisas = CalculadoraDivisas;

// Función para inicializar calculadora en una página específica
function inicializarCalculadora() {
    if (window.calculadoraDivisas) {
        window.calculadoraDivisas.destruir();
    }
    window.calculadoraDivisas = new CalculadoraDivisas();
}

// Función para crear widget de tasas
function crearWidgetTasas(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = `
        <div class="card border-warning">
            <div class="card-header bg-warning text-dark">
                <h5 class="card-title mb-0">
                    <i class="fas fa-exchange-alt"></i> Tasas de Cambio
                </h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <div class="text-center">
                            <h6>USD/VES</h6>
                            <h4 class="text-primary tasa-usd-ves">---.----</h4>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="text-center">
                            <h6>EUR/VES</h6>
                            <h4 class="text-info tasa-eur-ves">---.----</h4>
                        </div>
                    </div>
                </div>
                <hr>
                <div class="row">
                    <div class="col-12">
                        <small class="text-muted">
                            <i class="fas fa-clock"></i> 
                            Actualizado: <span class="fecha-actualizacion">--</span>
                        </small>
                        <br>
                        <small class="text-muted">
                            <i class="fas fa-source"></i> 
                            Fuente: <span class="fuente-tasa">--</span>
                        </small>
                        <br>
                        <small class="estado-tasas text-muted">Cargando...</small>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Función para crear calculadora completa
function crearCalculadoraCompleta(containerId, tipoOperacion = 'compra') {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = `
        <div class="calculadora-container">
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title">
                        <i class="fas fa-calculator"></i> 
                        Calculadora de ${tipoOperacion === 'compra' ? 'Compra' : 'Venta'} de Divisas
                    </h5>
                </div>
                <div class="card-body">
                    <!-- Selector de tipo de operación -->
                    <div class="form-group">
                        <label for="tipo-operacion">Tipo de Operación:</label>
                        <select class="form-control tipo-operacion" id="tipo-operacion">
                            <option value="compra" ${tipoOperacion === 'compra' ? 'selected' : ''}>Compra de Divisas</option>
                            <option value="venta" ${tipoOperacion === 'venta' ? 'selected' : ''}>Venta de Divisas</option>
                        </select>
                    </div>

                    <!-- Selector de cuenta -->
                    <div class="form-group">
                        <label for="cuenta-selector">Cuenta:</label>
                        <select class="form-control cuenta-selector" id="cuenta-selector" required>
                            <option value="">Seleccione una cuenta</option>
                        </select>
                    </div>

                    <div class="row">
                        <div class="col-md-6">
                            <!-- Monto origen -->
                            <div class="form-group">
                                <label class="label-monto-origen">Monto a cambiar:</label>
                                <div class="input-group">
                                    <input type="number" class="form-control monto-origen" 
                                           placeholder="0.00" step="0.01" min="0.01">
                                    <div class="input-group-append">
                                        <select class="form-control moneda-origen">
                                            <option value="VES">VES</option>
                                            <option value="USD">USD</option>
                                            <option value="EUR">EUR</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <!-- Monto destino -->
                            <div class="form-group">
                                <label class="label-monto-destino">Recibirá:</label>
                                <div class="input-group">
                                    <input type="text" class="form-control monto-destino" 
                                           placeholder="0.00" readonly>
                                    <div class="input-group-append">
                                        <select class="form-control moneda-destino">
                                            <option value="VES">VES</option>
                                            <option value="USD">USD</option>
                                            <option value="EUR">EUR</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Indicador de cálculo -->
                    <div class="calculando-indicator text-center" style="display: none;">
                        <i class="fas fa-spinner fa-spin"></i> Calculando...
                    </div>

                    <!-- Error de calculadora -->
                    <div class="alert alert-danger error-calculadora" style="display: none;"></div>

                    <!-- Información de la tasa -->
                    <div class="info-tasa" style="display: none;">
                        <div class="card bg-light">
                            <div class="card-body">
                                <h6>Información de la Operación</h6>
                                <div class="row">
                                    <div class="col-md-3">
                                        <strong>Tasa Aplicada:</strong><br>
                                        <span class="tasa-aplicada">0.0000</span>
                                    </div>
                                    <div class="col-md-3">
                                        <strong>Comisión:</strong><br>
                                        <span class="comision-calculada">0.00</span>
                                    </div>
                                    <div class="col-md-3">
                                        <strong>Total a Debitar:</strong><br>
                                        <span class="total-debitado">0.00</span>
                                    </div>
                                    <div class="col-md-3">
                                        <strong>Fecha/Hora Tasa:</strong><br>
                                        <small class="fecha-tasa">--</small>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Validación de fondos -->
                    <div class="validacion-fondos alert" style="display: none;">
                        <i class="fas icono-validacion"></i>
                        <strong class="mensaje-validacion"></strong><br>
                        <small class="detalle-fondos"></small>
                    </div>

                    <!-- Resumen de operación -->
                    <div class="resumen-operacion" style="display: none;">
                        <hr>
                        <button type="button" class="btn btn-primary btn-confirmar-transaccion" disabled>
                            <i class="fas fa-check"></i> Confirmar Transacción
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Auto-inicializar cuando el DOM esté listo
$(document).ready(function() {
    // Solo inicializar si estamos en páginas de divisas
    if (window.location.pathname.includes('/divisas/')) {
        inicializarCalculadora();
    }
});