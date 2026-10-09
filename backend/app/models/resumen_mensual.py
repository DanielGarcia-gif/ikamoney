"""Modelo T18: resumen_mensual"""

from datetime import date
from decimal import Decimal

from sqlalchemy import CheckConstraint, Date, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import TimestampMixin


class ResumenMensual(TimestampMixin, Base):
    """Foto de las cifras del usuario al cierre de cada mes."""

    __tablename__ = 'resumen_mensual'

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), ForeignKey('usuario.id', name='fk_resumen_mensual_usuario_id_usuario', ondelete='CASCADE'), nullable=False)
    periodo: Mapped[date] = mapped_column(Date(), nullable=False)
    total_ingresos: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    total_gastos: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    total_mensualidades_msi: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    total_deuda: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    utilizacion_credito: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)

    __table_args__ = (
        UniqueConstraint('usuario_id', 'periodo', name='uq_resumen_mensual_usuario_periodo'),
        CheckConstraint('DAYOFMONTH(periodo) = 1', name='ck_resumen_mensual_periodo_primer_dia'),
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )
