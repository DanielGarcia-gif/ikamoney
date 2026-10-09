"""Modelo T18: deuda"""

from datetime import date
from decimal import Decimal

from sqlalchemy import CheckConstraint, Date, Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.enums import ENUM_deuda_estatus, ENUM_deuda_tipo
from app.models.mixins import TimestampMixin


class Deuda(TimestampMixin, Base):
    """Préstamo o deuda que no es tarjeta ni MSI."""

    __tablename__ = 'deuda'

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), ForeignKey('usuario.id', name='fk_deuda_usuario_id_usuario', ondelete='CASCADE'), nullable=False, index=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    acreedor: Mapped[str | None] = mapped_column(String(100), nullable=True)
    tipo: Mapped[str] = mapped_column(Enum(*ENUM_deuda_tipo, name='deuda_tipo'), nullable=False)
    monto_original: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    saldo_actual: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    tasa_anual: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    pago_mensual: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    dia_pago: Mapped[int | None] = mapped_column(TINYINT(unsigned=True), nullable=True)
    fecha_inicio: Mapped[date | None] = mapped_column(Date(), nullable=True)
    estatus: Mapped[str] = mapped_column(Enum(*ENUM_deuda_estatus, name='deuda_estatus'), nullable=False, server_default='activa')

    __table_args__ = (
        CheckConstraint('monto_original > 0', name='ck_deuda_monto_original_positivo'),
        CheckConstraint('saldo_actual >= 0', name='ck_deuda_saldo_no_negativo'),
        CheckConstraint('dia_pago IS NULL OR dia_pago BETWEEN 1 AND 31', name='ck_deuda_dia_pago_rango'),
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )
