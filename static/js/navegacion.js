/**
 * Sistema de Divisas Bancario - JavaScript para Navegación
 */

document.addEventListener('DOMContentLoaded', function() {
    // Función para resaltar el elemento de navegación activo
    function highlightActiveNavigation() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.nav-link, .dropdown-item');
        
        navLinks.forEach(function(link) {
            const href = link.getAttribute('href');
            if (href && currentPath.includes(href.split('?')[0])) {
                link.classList.add('active');
                
                // Si es un dropdown item, también activar el dropdown padre
                const dropdown = link.closest('.dropdown');
                if (dropdown) {
                    const dropdownToggle = dropdown.querySelector('.dropdown-toggle');
                    if (dropdownToggle) {
                        dropdownToggle.classList.add('active');
                    }
                }
            }
        });
    }
    
    // Función para manejar el colapso del sidebar en móviles
    function handleSidebarToggle() {
        const sidebarToggle = document.getElementById('sidebarToggle');
        const sidebar = document.querySelector('.sidebar');
        
        if (sidebarToggle && sidebar) {
            sidebarToggle.addEventListener('click', function() {
                sidebar.classList.toggle('show');
            });
        }
    }
    
    // Función para smooth scroll en enlaces internos
    function enableSmoothScroll() {
        const internalLinks = document.querySelectorAll('a[href^="#"]');
        
        internalLinks.forEach(function(link) {
            link.addEventListener('click', function(e) {
                const targetId = this.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                
                if (targetElement) {
                    e.preventDefault();
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
    
    // Función para mostrar tooltips en elementos con título
    function initializeTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Función para confirmar acciones destructivas
    function confirmDestructiveActions() {
        const destructiveLinks = document.querySelectorAll('[data-confirm]');
        
        destructiveLinks.forEach(function(link) {
            link.addEventListener('click', function(e) {
                const message = this.getAttribute('data-confirm');
                if (!confirm(message)) {
                    e.preventDefault();
                }
            });
        });
    }
    
    // Función para auto-actualizar tasas cada 5 minutos
    function autoUpdateRates() {
        const rateWidgets = document.querySelectorAll('.widget-tasas');
        
        if (rateWidgets.length > 0) {
            setInterval(function() {
                fetch('/default/api_dashboard_data')
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success') {
                            updateRateDisplay(data.data);
                        }
                    })
                    .catch(error => {
                        console.log('Error actualizando tasas:', error);
                    });
            }, 300000); // 5 minutos
        }
    }
    
    // Función para actualizar la visualización de tasas
    function updateRateDisplay(data) {
        const usdRate = document.querySelector('.tasa-usd .tasa-valor');
        const eurRate = document.querySelector('.tasa-eur .tasa-valor');
        const lastUpdate = document.querySelector('.tasa-actualizacion');
        
        if (usdRate && data.tasa_usd) {
            usdRate.textContent = parseFloat(data.tasa_usd).toLocaleString('es-VE', {
                minimumFractionDigits: 4,
                maximumFractionDigits: 4
            });
        }
        
        if (eurRate && data.tasa_eur) {
            eurRate.textContent = parseFloat(data.tasa_eur).toLocaleString('es-VE', {
                minimumFractionDigits: 4,
                maximumFractionDigits: 4
            });
        }
        
        if (lastUpdate && data.ultima_actualizacion) {
            lastUpdate.innerHTML = '<i class="fas fa-clock me-1"></i>Actualizado: ' + 
                new Date(data.ultima_actualizacion).toLocaleString('es-VE');
        }
    }
    
    // Función para manejar formularios con validación
    function handleFormValidation() {
        const forms = document.querySelectorAll('.needs-validation');
        
        forms.forEach(function(form) {
            form.addEventListener('submit', function(event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            });
        });
    }
    
    // Función para manejar la búsqueda en tablas
    function enableTableSearch() {
        const searchInputs = document.querySelectorAll('[data-table-search]');
        
        searchInputs.forEach(function(input) {
            const targetTable = document.querySelector(input.getAttribute('data-table-search'));
            
            if (targetTable) {
                input.addEventListener('keyup', function() {
                    const searchTerm = this.value.toLowerCase();
                    const rows = targetTable.querySelectorAll('tbody tr');
                    
                    rows.forEach(function(row) {
                        const text = row.textContent.toLowerCase();
                        row.style.display = text.includes(searchTerm) ? '' : 'none';
                    });
                });
            }
        });
    }
    
    // Función para inicializar dropdowns de Bootstrap
    function initializeDropdowns() {
        const dropdownElementList = [].slice.call(document.querySelectorAll('[data-bs-toggle="dropdown"]'));
        dropdownElementList.map(function (dropdownToggleEl) {
            return new bootstrap.Dropdown(dropdownToggleEl);
        });
    }
    
    // Inicializar todas las funciones
    initializeDropdowns();
    highlightActiveNavigation();
    handleSidebarToggle();
    enableSmoothScroll();
    initializeTooltips();
    confirmDestructiveActions();
    autoUpdateRates();
    handleFormValidation();
    enableTableSearch();
    
    // Agregar clase de carga completada
    document.body.classList.add('loaded');
});

// Función global para formatear números como moneda
function formatCurrency(amount, currency = 'VES') {
    const formatter = new Intl.NumberFormat('es-VE', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
    
    return formatter.format(amount);
}

// Función global para formatear números
function formatNumber(number, decimals = 2) {
    return parseFloat(number).toLocaleString('es-VE', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    });
}

// Función para mostrar notificaciones toast
function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remover el toast después de que se oculte
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

// Función para crear el contenedor de toasts si no existe
function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '1055';
    document.body.appendChild(container);
    return container;
}