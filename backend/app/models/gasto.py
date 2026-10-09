"""Modelo T18: gasto"""

from datetime import date
from decimal import Decimal

from sqlalchemy import Boolean, CheckConstraint, Date, Enum, ForeignKey, Numeric, String, text
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.enums import ENUM_frecuencia, ENUM_gasto_tipo
from app.models.mixins import TimestampMixin


class Gasto(TimestampMixin, Base):
    """Gasto fijo o variable que NO viene de un estado de cuenta."""

    __tablename__ = 'gasto'

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), ForeignKey('usuario.id', name='fk_gasto_usuario_id_usuario', ondelete='CASCADE'), nullable=False, index=True)
    categoria_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), ForeignKey('categoria.id', name='fk_gasto_categoria_id_categoria', ondelete='RESTRICT'), nullable=False, index=True)
    descripcion: Mapped[str] = mapped_column(String(120), nullable=False)
    tipo: Mapped[str] = mapped_column(Enum(*ENUM_gasto_tipo, name='gasto_tipo'), nullable=False)
    monto: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    frecuencia: Mapped[str] = mapped_column(Enum(*ENUM_frecuencia, name='frecuencia'), nullable=False)
    fecha_inicio: Mapped[date] = mapped_column(Date(), nullable=False)
    fecha_fin: Mapped[date | None] = mapped_column(Date(), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean(), nullable=False, server_default=text('1'))

    __table_args__ = (
        CheckConstraint('monto > 0', name='ck_gasto_monto_positivo'),
        CheckConstraint('fecha_fin IS NULL OR fecha_fin >= fecha_inicio', name='ck_gasto_fechas_validas'),
        CheckConstraint("(tipo = 'variable' AND frecuencia = 'unico') OR (tipo = 'fijo' AND frecuencia <> 'unico')", name='ck_gasto_tipo_frecuencia'),
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )
