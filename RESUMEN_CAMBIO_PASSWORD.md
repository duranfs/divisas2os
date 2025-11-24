# Funcionalidad: Cambio de Contraseña de Cliente

## Implementación Completada

Se agregó la funcionalidad para que los administradores puedan cambiar la contraseña de los clientes desde la página de edición.

## Cambios Realizados

### 1. Controlador (`controllers/clientes.py`)

#### Imports agregados:
```python
import uuid
```

#### Campos agregados al formulario de edición:
```python
Field('nueva_password', 'password', label='Nueva Contraseña (opcional)', 
      comment='Dejar en blanco para mantener la contraseña actual'),
Field('confirmar_password', 'password', label='Confirmar Nueva Contraseña')
```

#### Validación de contraseña:
- Verifica que ambas contraseñas coincidan
- Requiere mínimo 6 caracteres
- Es opcional (si se deja en blanco, no se cambia la contraseña)

#### Actualización de contraseña:
```python
if form.vars.nueva_password:
    from gluon.contrib.pbkdf2 import pbkdf2_hex
    salt = str(uuid.uuid4())
    datos_actualizar['password'] = pbkdf2_hex(form.vars.nueva_password, salt)
    log_security_event('PASSWORD_CHANGE', usuario.id, 
                     f'Contraseña cambiada por administrador para cliente {cliente.cedula}',
                     request.client)
```

## Cómo Usar

### Para Administradores:

1. **Ir a Gestión de Clientes**
   - Dashboard → Gestión de Clientes → Listar Clientes

2. **Seleccionar un cliente**
   - Hacer clic en el botón "Editar" del cliente

3. **Cambiar la contraseña (opcional)**
   - Si quieres cambiar la contraseña:
     - Escribe la nueva contraseña en "Nueva Contraseña"
     - Repite la misma contraseña en "Confirmar Nueva Contraseña"
   - Si NO quieres cambiar la contraseña:
     - Deja ambos campos vacíos

4. **Guardar cambios**
   - Haz clic en "Actualizar Cliente"
   - El sistema validará y guardará los cambios

## Validaciones Implementadas

### Contraseña:
- ✅ Ambas contraseñas deben coincidir
- ✅ Mínimo 6 caracteres
- ✅ Opcional (puede dejarse en blanco)
- ✅ Se registra en el log de seguridad cuando se cambia

### Otros campos:
- ✅ Email único (no puede estar usado por otro usuario)
- ✅ Cédula única (no puede estar usada por otro cliente)
- ✅ Todos los campos requeridos deben estar completos

## Seguridad

### Encriptación:
- La contraseña se encripta usando **PBKDF2** con salt único
- No se almacena en texto plano
- Usa el mismo método que el registro de usuarios

### Auditoría:
- Se registra en el log de seguridad cuando un administrador cambia la contraseña
- Incluye: ID de usuario, cédula del cliente, IP del administrador, fecha/hora

### Permisos:
- Solo usuarios con rol "administrador" u "operador" pueden editar clientes
- Requiere autenticación (`@auth.requires_login()`)

## Mensajes de Error

| Error | Mensaje |
|-------|---------|
| Contraseñas no coinciden | "Las contraseñas no coinciden" |
| Contraseña muy corta | "La contraseña debe tener al menos 6 caracteres" |
| Email duplicado | "Este email ya está registrado por otro usuario" |
| Cédula duplicada | "Esta cédula ya está registrada por otro cliente" |

## Ejemplo de Uso

### Escenario 1: Cambiar solo la contraseña
```
Cliente: Juan Pérez (V-12345678)
Acción: Cambiar contraseña a "nuevaclave123"

Resultado:
✅ Contraseña actualizada
✅ Otros datos sin cambios
✅ Evento registrado en log de seguridad
```

### Escenario 2: Actualizar datos sin cambiar contraseña
```
Cliente: María González (V-87654321)
Acción: Cambiar teléfono y dirección
Campos de contraseña: Vacíos

Resultado:
✅ Teléfono y dirección actualizados
✅ Contraseña sin cambios
✅ No se registra evento de cambio de contraseña
```

### Escenario 3: Cambiar todo
```
Cliente: Pedro Rodríguez (V-11223344)
Acción: Actualizar email, teléfono y contraseña

Resultado:
✅ Todos los datos actualizados
✅ Nueva contraseña encriptada
✅ Evento registrado en log de seguridad
```

## Notas Técnicas

### Hash de Contraseña:
- Algoritmo: PBKDF2-SHA512
- Salt: UUID único por contraseña
- Formato: `pbkdf2(1000,20,sha512)$salt$hash`

### Compatibilidad:
- Compatible con el sistema de autenticación de web2py
- Usa las mismas funciones que `auth.register()`
- El cliente puede hacer login inmediatamente con la nueva contraseña

## Testing

Para probar la funcionalidad:

1. Crear un cliente de prueba
2. Ir a editar el cliente
3. Cambiar la contraseña
4. Cerrar sesión
5. Intentar login con la nueva contraseña
6. Verificar que funciona correctamente

## Archivos Modificados

- `controllers/clientes.py` - Lógica de cambio de contraseña
- Ningún archivo de vista fue modificado (usa el formulario generado automáticamente)
