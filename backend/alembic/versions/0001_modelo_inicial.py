"""Modelo inicial (T18): crea las 11 tablas de IKAMONEY.

Revision ID: 0001
Revises:
Create Date: 2026-10-09
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# Congelada a propósito: una migración nunca importa código de la app,
# para que siga funcionando igual aunque los modelos cambien después.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

ENUM_frecuencia = ('unico', 'semanal', 'quincenal', 'mensual', 'anual')
ENUM_gasto_tipo = ('fijo', 'variable')
ENUM_estado_cuenta_estatus = ('procesando', 'extraido', 'revisado', 'error')
ENUM_origen_dato = ('extraido', 'manual')
ENUM_estado_revision = ('pendiente', 'confirmado', 'corregido', 'descartado')
ENUM_movimiento_tipo = ('cargo', 'pago', 'interes', 'comision', 'mensualidad_msi')
ENUM_plan_msi_estatus = ('activo', 'liquidado', 'cancelado')
ENUM_deuda_tipo = ('prestamo_personal', 'credito_auto', 'credito_hipotecario', 'familiar_amigo', 'otro')
ENUM_deuda_estatus = ('activa', 'liquidada')

TABLE_OPTS = dict(mysql_engine="InnoDB", mysql_charset="utf8mb4")


def upgrade() -> None:
    op.create_table(
        'usuario',
        sa.Column('id', mysql.BIGINT(unsigned=True), autoincrement=True, nullable=False),
        sa.Column('nombre', sa.String(100), nullable=False),
        sa.Column('correo', sa.String(255), nullable=False),
        sa.Column('contrasena_hash', sa.String(255), nullable=False),
        sa.Column('moneda', sa.CHAR(3), nullable=False, server_default='MXN'),
        sa.Column('creado_en', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('actualizado_en', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('correo', name=op.f('uq_usuario_correo')),
        **TABLE_OPTS,
    )
    op.create_table(
        'categoria',
        sa.Column('id', mysql.BIGINT(unsigned=True), autoincrement=True, nullable=False),
        sa.Column('usuario_id', mysql.BIGINT(unsigned=True), nullable=True),
        sa.Column('nombre', sa.String(60), nullable=False),
        sa.Column('creado_en', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('actualizado_en', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], name=op.f('fk_categoria_usuario_id_usuario'), ondelete='CASCADE'),
        sa.UniqueConstraint('usuario_id', 'nombre', name=op.f('uq_categoria_usuario_nombre')),
        **TABLE_OPTS,
    )
    op.create_table(
        'ingreso',
        sa.Column('id', mysql.BIGINT(unsigned=True), autoincrement=True, nullable=False),
        sa.Column('usuario_id', mysql.BIGINT(unsigned=True), nullable=False),
        sa.Column('descripcion', sa.String(120), nullable=False),
        sa.Column('monto', sa.Numeric(12, 2), nullable=False),
        sa.Column('frecuencia', sa.Enum(*ENUM_frecuencia, name='frecuencia'), nullable=False),
        sa.Column('fecha_inicio', sa.Date(), nullable=False),
        sa.Column('fecha_fin', sa.Date(), nullable=True),
        sa.Column('activo', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('creado_en', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('actualizado_en', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], name=op.f('fk_ingreso_usuario_id_usuario'), ondelete='CASCADE'),
        sa.CheckConstraint('monto > 0', name=op.f('ck_ingreso_monto_positivo')),
        sa.CheckConstraint('fecha_fin IS NULL OR fecha_fin >= fecha_inicio', name=op.f('ck_ingreso_fechas_validas')),
        sa.Index(op.f('ix_ingreso_usuario_id'), 'usuario_id'),
        **TABLE_OPTS,
    )
    op.create_table(
        'gasto',
        sa.Column('id', mysql.BIGINT(unsigned=True), autoincrement=True, nullable=False),
        sa.Column('usuario_id', mysql.BIGINT(unsigned=True), nullable=False),
        sa.Column('categoria_id', mysql.BIGINT(unsigned=True), nullable=False),
        sa.Column('descripcion', sa.String(120), nullable=False),
        sa.Column('tipo', sa.Enum(*ENUM_gasto_tipo, name='gasto_tipo'), nullable=False),
        sa.Column('monto', sa.Numeric(12, 2), nullable=False),
        sa.Column('frecuencia', sa.Enum(*ENUM_frecuencia, name='frecuencia'), nullable=False),
        sa.Column('fecha_inicio', sa.Date(), nullable=False),
        sa.Column('fecha_fin', sa.Date(), nullable=True),
        sa.Column('activo', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('creado_en', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('actualizado_en', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], name=op.f('fk_gasto_usuario_id_usuario'), ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['categoria_id'], ['categoria.id'], name=op.f('fk_gasto_categoria_id_categoria'), ondelete='RESTRICT'),
        sa.CheckConstraint('monto > 0', name=op.f('ck_gasto_monto_positivo')),
        sa.CheckConstraint('fecha_fin IS NULL OR fecha_fin >= fecha_inicio', name=op.f('ck_gasto_fechas_validas')),
        sa.CheckConstraint("(tipo = 'variable' AND frecuencia = 'unico') OR (tipo = 'fijo' AND frecuencia <> 'unico')", name=op.f('ck_gasto_tipo_frecuencia')),
        sa.Index(op.f('ix_gasto_usuario_id'), 'usuario_id'),
        sa.Index(op.f('ix_gasto_categoria_id'), 'categoria_id'),
        **TABLE_OPTS,
    )
    op.create_table(
        'tarjeta',
        sa.Column('id', mysql.BIGINT(unsigned=True), autoincrement=True, nullable=False),
        sa.Column('usuario_id', mysql.BIGINT(unsigned=True), nullable=False),
        sa.Column('nombre', sa.String(60), nullable=False),
        sa.Column('banco', sa.String(60), nullable=False),
        sa.Column('ultimos_4', sa.CHAR(4), nullable=True),
        sa.Column('limite_credito', sa.Numeric(12, 2), nullable=False),
        sa.Column('saldo_actual', sa.Numeric(12, 2), nullable=False, server_default=sa.text('0')),
        sa.Column('dia_corte', mysql.TINYINT(unsigned=True), nullable=False),
        sa.Column('dia_pago', mysql.TINYINT(unsigned=True), nullable=False),
        sa.Column('tasa_anual', sa.Numeric(5, 2), nullable=True),
        sa.Column('activa', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('creado_en', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('actualizado_en', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], name=op.f('fk_tarjeta_usuario_id_usuario'), ondelete='CASCADE'),
        sa.CheckConstraint('limite_credito >= 0', name=op.f('ck_tarjeta_limite_no_negativo')),
        sa.CheckConstraint('dia_corte BETWEEN 1 AND 31', name=op.f('ck_tarjeta_dia_corte_rango')),
        sa.CheckConstraint('dia_pago BETWEEN 1 AND 31', name=op.f('ck_tarjeta_dia_pago_rango')),
        sa.CheckConstraint("ultimos_4 IS NULL OR ultimos_4 REGEXP '^[0-9]{4}$'", name=op.f('ck_tarjeta_ultimos_4_digitos')),
        sa.Index(op.f('ix_tarjeta_usuario_id'), 'usuario_id'),
        **TABLE_OPTS,
    )
    op.create_table(
        'estado_cuenta',
        sa.Column('id', mysql.BIGINT(unsigned=True), autoincrement=True, nullable=False),
        sa.Column('tarjeta_id', mysql.BIGINT(unsigned=True), nullable=False),
        sa.Column('periodo_inicio', sa.Date(), nullable=False),
        sa.Column('fecha_corte', sa.Date(), nullable=False),
        sa.Column('fecha_limite_pago', sa.Date(), nullable=False),
        sa.Column('saldo_al_corte', sa.Numeric(12, 2), nullable=False),
        sa.Column('pago_minimo', sa.Numeric(12, 2), nullable=True),
        sa.Column('pago_no_intereses', sa.Numeric(12, 2), nullable=True),
        sa.Column('archivo_ref', sa.String(255), nullable=True),
        sa.Column('estatus', sa.Enum(*ENUM_estado_cuenta_estatus, name='estado_cuenta_estatus'), nullable=False, server_default='procesando'),
        sa.Column('creado_en', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('actualizado_en', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['tarjeta_id'], ['tarjeta.id'], name=op.f('fk_estado_cuenta_tarjeta_id_tarjeta'), ondelete='CASCADE'),
        sa.UniqueConstraint('tarjeta_id', 'fecha_corte', name=op.f('uq_estado_cuenta_tarjeta_corte')),
        sa.CheckConstraint('fecha_corte >= periodo_inicio', name=op.f('ck_estado_cuenta_corte_desde_inicio')),
        sa.CheckConstraint('fecha_limite_pago > fecha_corte', name=op.f('ck_estado_cuenta_pago_despues_corte')),
        **TABLE_OPTS,
    )
    op.create_table(
        'plan_msi',
        sa.Column('id', mysql.BIGINT(unsigned=True), autoincrement=True, nullable=False),
        sa.Column('tarjeta_id', mysql.BIGINT(unsigned=True), nullable=False),
        sa.Column('categoria_id', mysql.BIGINT(unsigned=True), nullable=True),
        sa.Column('descripcion', sa.String(120), nullable=False),
        sa.Column('monto_original', sa.Numeric(12, 2), nullable=False),
        sa.Column('num_mensualidades', mysql.SMALLINT(unsigned=True), nullable=False),
        sa.Column('mensualidades_pagadas', mysql.SMALLINT(unsigned=True), nullable=False, server_default=sa.text('0')),
        sa.Column('monto_mensualidad', sa.Numeric(12, 2), nullable=False),
        sa.Column('fecha_compra', sa.Date(), nullable=False),
        sa.Column('estatus', sa.Enum(*ENUM_plan_msi_estatus, name='plan_msi_estatus'), nullable=False, server_default='activo'),
        sa.Column('origen', sa.Enum(*ENUM_origen_dato, name='origen_dato'), nullable=False),
        sa.Column('creado_en', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('actualizado_en', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['tarjeta_id'], ['tarjeta.id'], name=op.f('fk_plan_msi_tarjeta_id_tarjeta'), ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['categoria_id'], ['categoria.id'], name=op.f('fk_plan_msi_categoria_id_categoria'), ondelete='SET NULL'),
        sa.CheckConstraint('monto_original > 0', name=op.f('ck_plan_msi_monto_original_positivo')),
        sa.CheckConstraint('num_mensualidades >= 2', name=op.f('ck_plan_msi_mensualidades_minimo')),
        sa.CheckConstraint('mensualidades_pagadas <= num_mensualidades', name=op.f('ck_plan_msi_pagadas_en_rango')),
        sa.CheckConstraint('monto_mensualidad > 0', name=op.f('ck_plan_msi_monto_mensualidad_positivo')),
        sa.CheckConstraint('ABS(monto_original - monto_mensualidad * num_mensualidades) <= num_mensualidades * 0.01', name=op.f('ck_plan_msi_monto_coherente')),
        sa.Index(op.f('ix_plan_msi_tarjeta_id'), 'tarjeta_id'),
        sa.Index(op.f('ix_plan_msi_categoria_id'), 'categoria_id'),
        **TABLE_OPTS,
    )
    op.create_table(
        'movimiento',
        sa.Column('id', mysql.BIGINT(unsigned=True), autoincrement=True, nullable=False),
        sa.Column('estado_cuenta_id', mysql.BIGINT(unsigned=True), nullable=False),
        sa.Column('origen', sa.Enum(*ENUM_origen_dato, name='origen_dato'), nullable=False),
        sa.Column('estado_revision', sa.Enum(*ENUM_estado_revision, name='estado_revision'), nullable=False, server_default='pendiente'),
        sa.Column('fecha', sa.Date(), nullable=False),
        sa.Column('descripcion', sa.String(255), nullable=False),
        sa.Column('monto', sa.Numeric(12, 2), nullable=False),
        sa.Column('tipo', sa.Enum(*ENUM_movimiento_tipo, name='movimiento_tipo'), nullable=False),
        sa.Column('categoria_id', mysql.BIGINT(unsigned=True), nullable=True),
        sa.Column('plan_msi_id', mysql.BIGINT(unsigned=True), nullable=True),
        sa.Column('fecha_extraida', sa.Date(), nullable=True),
        sa.Column('descripcion_extraida', sa.String(255), nullable=True),
        sa.Column('monto_extraido', sa.Numeric(12, 2), nullable=True),
        sa.Column('tipo_extraido', sa.Enum(*ENUM_movimiento_tipo, name='movimiento_tipo'), nullable=True),
        sa.Column('confianza', sa.Numeric(3, 2), nullable=True),
        sa.Column('corregido_en', sa.TIMESTAMP(), nullable=True),
        sa.Column('creado_en', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('actualizado_en', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['estado_cuenta_id'], ['estado_cuenta.id'], name=op.f('fk_movimiento_estado_cuenta_id_estado_cuenta'), ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['categoria_id'], ['categoria.id'], name=op.f('fk_movimiento_categoria_id_categoria'), ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['plan_msi_id'], ['plan_msi.id'], name=op.f('fk_movimiento_plan_msi_id_plan_msi'), ondelete='SET NULL'),
        sa.CheckConstraint('monto >= 0', name=op.f('ck_movimiento_monto_no_negativo')),
        sa.CheckConstraint("origen <> 'manual' OR (fecha_extraida IS NULL AND descripcion_extraida IS NULL AND monto_extraido IS NULL AND tipo_extraido IS NULL)", name=op.f('ck_movimiento_manual_sin_extraidos')),
        sa.CheckConstraint('confianza IS NULL OR (confianza >= 0 AND confianza <= 1)', name=op.f('ck_movimiento_confianza_rango')),
        sa.Index(op.f('ix_movimiento_estado_cuenta_id'), 'estado_cuenta_id'),
        sa.Index(op.f('ix_movimiento_categoria_id'), 'categoria_id'),
        sa.Index(op.f('ix_movimiento_plan_msi_id'), 'plan_msi_id'),
        **TABLE_OPTS,
    )
    op.create_table(
        'deuda',
        sa.Column('id', mysql.BIGINT(unsigned=True), autoincrement=True, nullable=False),
        sa.Column('usuario_id', mysql.BIGINT(unsigned=True), nullable=False),
        sa.Column('nombre', sa.String(100), nullable=False),
        sa.Column('acreedor', sa.String(100), nullable=True),
        sa.Column('tipo', sa.Enum(*ENUM_deuda_tipo, name='deuda_tipo'), nullable=False),
        sa.Column('monto_original', sa.Numeric(12, 2), nullable=False),
        sa.Column('saldo_actual', sa.Numeric(12, 2), nullable=False),
        sa.Column('tasa_anual', sa.Numeric(5, 2), nullable=True),
        sa.Column('pago_mensual', sa.Numeric(12, 2), nullable=True),
        sa.Column('dia_pago', mysql.TINYINT(unsigned=True), nullable=True),
        sa.Column('fecha_inicio', sa.Date(), nullable=True),
        sa.Column('estatus', sa.Enum(*ENUM_deuda_estatus, name='deuda_estatus'), nullable=False, server_default='activa'),
        sa.Column('creado_en', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('actualizado_en', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], name=op.f('fk_deuda_usuario_id_usuario'), ondelete='CASCADE'),
        sa.CheckConstraint('monto_original > 0', name=op.f('ck_deuda_monto_original_positivo')),
        sa.CheckConstraint('saldo_actual >= 0', name=op.f('ck_deuda_saldo_no_negativo')),
        sa.CheckConstraint('dia_pago IS NULL OR dia_pago BETWEEN 1 AND 31', name=op.f('ck_deuda_dia_pago_rango')),
        sa.Index(op.f('ix_deuda_usuario_id'), 'usuario_id'),
        **TABLE_OPTS,
    )
    op.create_table(
        'score_historial',
        sa.Column('id', mysql.BIGINT(unsigned=True), autoincrement=True, nullable=False),
        sa.Column('usuario_id', mysql.BIGINT(unsigned=True), nullable=False),
        sa.Column('calculado_en', sa.DateTime(), nullable=False),
        sa.Column('puntaje', mysql.SMALLINT(unsigned=True), nullable=False),
        sa.Column('version_modelo', sa.String(20), nullable=False),
        sa.Column('componentes', sa.JSON(), nullable=False),
        sa.Column('creado_en', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('actualizado_en', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], name=op.f('fk_score_historial_usuario_id_usuario'), ondelete='CASCADE'),
        sa.CheckConstraint('puntaje BETWEEN 0 AND 100', name=op.f('ck_score_historial_puntaje_rango')),
        sa.Index(op.f('ix_score_historial_usuario_calculado'), 'usuario_id', 'calculado_en'),
        **TABLE_OPTS,
    )
    op.create_table(
        'resumen_mensual',
        sa.Column('id', mysql.BIGINT(unsigned=True), autoincrement=True, nullable=False),
        sa.Column('usuario_id', mysql.BIGINT(unsigned=True), nullable=False),
        sa.Column('periodo', sa.Date(), nullable=False),
        sa.Column('total_ingresos', sa.Numeric(12, 2), nullable=False),
        sa.Column('total_gastos', sa.Numeric(12, 2), nullable=False),
        sa.Column('total_mensualidades_msi', sa.Numeric(12, 2), nullable=False),
        sa.Column('total_deuda', sa.Numeric(12, 2), nullable=False),
        sa.Column('utilizacion_credito', sa.Numeric(5, 2), nullable=False),
        sa.Column('creado_en', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('actualizado_en', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], name=op.f('fk_resumen_mensual_usuario_id_usuario'), ondelete='CASCADE'),
        sa.UniqueConstraint('usuario_id', 'periodo', name=op.f('uq_resumen_mensual_usuario_periodo')),
        sa.CheckConstraint('DAYOFMONTH(periodo) = 1', name=op.f('ck_resumen_mensual_periodo_primer_dia')),
        **TABLE_OPTS,
    )


def downgrade() -> None:
    op.drop_table('resumen_mensual')
    op.drop_table('score_historial')
    op.drop_table('deuda')
    op.drop_table('movimiento')
    op.drop_table('plan_msi')
    op.drop_table('estado_cuenta')
    op.drop_table('tarjeta')
    op.drop_table('gasto')
    op.drop_table('ingreso')
    op.drop_table('categoria')
    op.drop_table('usuario')
