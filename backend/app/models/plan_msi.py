"""Modelo T18: plan_msi"""

from datetime import date
from decimal import Decimal

from sqlalchemy import CheckConstraint, Date, Enum, ForeignKey, Numeric, String, text
from sqlalchemy.dialects.mysql import BIGINT, SMALLINT
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.enums import ENUM_origen_dato, ENUM_plan_msi_estatus
from app.models.mixins import TimestampMixin


class PlanMsi(TimestampMixin, Base):
    """Plan de meses sin intereses de una tarjeta. Entidad central: nunca es un gasto."""

    __tablename__ = 'plan_msi'

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    tarjeta_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), ForeignKey('tarjeta.id', name='fk_plan_msi_tarjeta_id_tarjeta', ondelete='CASCADE'), nullable=False, index=True)
    categoria_id: Mapped[int | None] = mapped_column(BIGINT(unsigned=True), ForeignKey('categoria.id', name='fk_plan_msi_categoria_id_categoria', ondelete='SET NULL'), nullable=True, index=True)
    descripcion: Mapped[str] = mapped_column(String(120), nullable=False)
    monto_original: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    num_mensualidades: Mapped[int] = mapped_column(SMALLINT(unsigned=True), nullable=False)
    mensualidades_pagadas: Mapped[int] = mapped_column(SMALLINT(unsigned=True), nullable=False, server_default=text('0'))
    monto_mensualidad: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    fecha_compra: Mapped[date] = mapped_column(Date(), nullable=False)
    estatus: Mapped[str] = mapped_column(Enum(*ENUM_plan_msi_estatus, name='plan_msi_estatus'), nullable=False, server_default='activo')
    origen: Mapped[str] = mapped_column(Enum(*ENUM_origen_dato, name='origen_dato'), nullable=False)

    __table_args__ = (
        CheckConstraint('monto_original > 0', name='ck_plan_msi_monto_original_positivo'),
        CheckConstraint('num_mensualidades >= 2', name='ck_plan_msi_mensualidades_minimo'),
        CheckConstraint('mensualidades_pagadas <= num_mensualidades', name='ck_plan_msi_pagadas_en_rango'),
        CheckConstraint('monto_mensualidad > 0', name='ck_plan_msi_monto_mensualidad_positivo'),
        CheckConstraint('ABS(monto_original - monto_mensualidad * num_mensualidades) <= num_mensualidades * 0.01', name='ck_plan_msi_monto_coherente'),
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )
