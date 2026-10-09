"""Modelo T18: movimiento"""

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, Date, Enum, ForeignKey, Numeric, String, TIMESTAMP
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.enums import ENUM_estado_revision, ENUM_movimiento_tipo, ENUM_origen_dato
from app.models.mixins import TimestampMixin


class Movimiento(TimestampMixin, Base):
    """Línea de un estado de cuenta. Columnas *_extraida/o = lo que leyó el PDF (inmutable); el resto es lo que usa la app."""

    __tablename__ = 'movimiento'

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    estado_cuenta_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), ForeignKey('estado_cuenta.id', name='fk_movimiento_estado_cuenta_id_estado_cuenta', ondelete='CASCADE'), nullable=False, index=True)
    origen: Mapped[str] = mapped_column(Enum(*ENUM_origen_dato, name='origen_dato'), nullable=False)
    estado_revision: Mapped[str] = mapped_column(Enum(*ENUM_estado_revision, name='estado_revision'), nullable=False, server_default='pendiente')
    fecha: Mapped[date] = mapped_column(Date(), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(255), nullable=False)
    monto: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    tipo: Mapped[str] = mapped_column(Enum(*ENUM_movimiento_tipo, name='movimiento_tipo'), nullable=False)
    categoria_id: Mapped[int | None] = mapped_column(BIGINT(unsigned=True), ForeignKey('categoria.id', name='fk_movimiento_categoria_id_categoria', ondelete='SET NULL'), nullable=True, index=True)
    plan_msi_id: Mapped[int | None] = mapped_column(BIGINT(unsigned=True), ForeignKey('plan_msi.id', name='fk_movimiento_plan_msi_id_plan_msi', ondelete='SET NULL'), nullable=True, index=True)
    fecha_extraida: Mapped[date | None] = mapped_column(Date(), nullable=True)
    descripcion_extraida: Mapped[str | None] = mapped_column(String(255), nullable=True)
    monto_extraido: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    tipo_extraido: Mapped[str | None] = mapped_column(Enum(*ENUM_movimiento_tipo, name='movimiento_tipo'), nullable=True)
    confianza: Mapped[Decimal | None] = mapped_column(Numeric(3, 2), nullable=True)
    corregido_en: Mapped[datetime | None] = mapped_column(TIMESTAMP(), nullable=True)

    __table_args__ = (
        CheckConstraint('monto >= 0', name='ck_movimiento_monto_no_negativo'),
        CheckConstraint("origen <> 'manual' OR (fecha_extraida IS NULL AND descripcion_extraida IS NULL AND monto_extraido IS NULL AND tipo_extraido IS NULL)", name='ck_movimiento_manual_sin_extraidos'),
        CheckConstraint('confianza IS NULL OR (confianza >= 0 AND confianza <= 1)', name='ck_movimiento_confianza_rango'),
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )
