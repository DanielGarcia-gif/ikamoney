"""Modelo T18: usuario"""

from sqlalchemy import CHAR, String, UniqueConstraint
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import TimestampMixin


class Usuario(TimestampMixin, Base):
    """Persona que usa IKAMONEY."""

    __tablename__ = 'usuario'

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    correo: Mapped[str] = mapped_column(String(255), nullable=False)
    contrasena_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    moneda: Mapped[str] = mapped_column(CHAR(3), nullable=False, server_default='MXN')

    __table_args__ = (
        UniqueConstraint('correo', name='uq_usuario_correo'),
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )
