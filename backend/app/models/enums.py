"""Valores permitidos de los campos ENUM (T18). Los nombres coinciden con la migración inicial."""

ENUM_frecuencia = ('unico', 'semanal', 'quincenal', 'mensual', 'anual')
ENUM_gasto_tipo = ('fijo', 'variable')
ENUM_estado_cuenta_estatus = ('procesando', 'extraido', 'revisado', 'error')
ENUM_origen_dato = ('extraido', 'manual')
ENUM_estado_revision = ('pendiente', 'confirmado', 'corregido', 'descartado')
ENUM_movimiento_tipo = ('cargo', 'pago', 'interes', 'comision', 'mensualidad_msi')
ENUM_plan_msi_estatus = ('activo', 'liquidado', 'cancelado')
ENUM_deuda_tipo = ('prestamo_personal', 'credito_auto', 'credito_hipotecario', 'familiar_amigo', 'otro')
ENUM_deuda_estatus = ('activa', 'liquidada')
