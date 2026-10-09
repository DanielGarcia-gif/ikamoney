"""Modelo T18: tarjeta"""

from decimal import Decimal

from sqlalchemy import Boolean, CHAR, CheckConstraint, ForeignKey, Numeric, String, text
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import TimestampMixin


class Tarjeta(TimestampMixin, Base):
    """Tarjeta de crédito. Nunca se guarda el número completo ni el CVV."""

    __tablename__ = 'tarjeta'

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), ForeignKey('usuario.id', name='fk_tarjeta_usuario_id_usuario', ondelete='CASCADE'), nullable=False, index=True)
    nombre: Mapped[str] = mapped_column(String(60), nullable=False)
    banco: Mapped[str] = mapped_column(String(60), nullable=False)
    ultimos_4: Mapped[str | None] = mapped_column(CHAR(4), nullable=True)
    limite_credito: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    saldo_actual: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, server_default=text('0'))
    dia_corte: Mapped[int] = mapped_column(TINYINT(unsigned=True), nullable=False)
    dia_pago: Mapped[int] = mapped_column(TINYINT(unsigned=True), nullable=False)
    tasa_anual: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    activa: Mapped[bool] = mapped_column(Boolean(), nullable=False, server_default=text('1'))

    __table_args__ = (
        CheckConstraint('limite_credito >= 0', name='ck_tarjeta_limite_no_negativo'),
        CheckConstraint('dia_corte BETWEEN 1 AND 31', name='ck_tarjeta_dia_corte_rango'),
        CheckConstraint('dia_pago BETWEEN 1 AND 31', name='ck_tarjeta_dia_pago_rango'),
        CheckConstraint("ultimos_4 IS NULL OR ultimos_4 REGEXP '^[0-9]{4}$'", name='ck_tarjeta_ultimos_4_digitos'),
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )
