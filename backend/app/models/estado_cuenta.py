"""Modelo T18: estado_cuenta"""

from datetime import date
from decimal import Decimal

from sqlalchemy import CheckConstraint, Date, Enum, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.enums import ENUM_estado_cuenta_estatus
from app.models.mixins import TimestampMixin


class EstadoCuenta(TimestampMixin, Base):
    """Estado de cuenta (PDF) de una tarjeta: uno por fecha de corte."""

    __tablename__ = 'estado_cuenta'

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    tarjeta_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), ForeignKey('tarjeta.id', name='fk_estado_cuenta_tarjeta_id_tarjeta', ondelete='CASCADE'), nullable=False)
    periodo_inicio: Mapped[date] = mapped_column(Date(), nullable=False)
    fecha_corte: Mapped[date] = mapped_column(Date(), nullable=False)
    fecha_limite_pago: Mapped[date] = mapped_column(Date(), nullable=False)
    saldo_al_corte: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    pago_minimo: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    pago_no_intereses: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    archivo_ref: Mapped[str | None] = mapped_column(String(255), nullable=True)
    estatus: Mapped[str] = mapped_column(Enum(*ENUM_estado_cuenta_estatus, name='estado_cuenta_estatus'), nullable=False, server_default='procesando')

    __table_args__ = (
        UniqueConstraint('tarjeta_id', 'fecha_corte', name='uq_estado_cuenta_tarjeta_corte'),
        CheckConstraint('fecha_corte >= periodo_inicio', name='ck_estado_cuenta_corte_desde_inicio'),
        CheckConstraint('fecha_limite_pago > fecha_corte', name='ck_estado_cuenta_pago_despues_corte'),
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )
