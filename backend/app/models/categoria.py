"""Modelo T18: categoria"""

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import TimestampMixin


class Categoria(TimestampMixin, Base):
    """Categoría de gasto. usuario_id NULL = categoría base del sistema."""

    __tablename__ = 'categoria'

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    usuario_id: Mapped[int | None] = mapped_column(BIGINT(unsigned=True), ForeignKey('usuario.id', name='fk_categoria_usuario_id_usuario', ondelete='CASCADE'), nullable=True)
    nombre: Mapped[str] = mapped_column(String(60), nullable=False)

    __table_args__ = (
        UniqueConstraint('usuario_id', 'nombre', name='uq_categoria_usuario_nombre'),
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )
