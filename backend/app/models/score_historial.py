"""Modelo T18: score_historial"""

from datetime import date, datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, JSON, String
from sqlalchemy.dialects.mysql import BIGINT, SMALLINT
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import TimestampMixin


class ScoreHistorial(TimestampMixin, Base):
    """Historial del score. Solo se agregan filas; nunca se actualizan."""

    __tablename__ = 'score_historial'

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), ForeignKey('usuario.id', name='fk_score_historial_usuario_id_usuario', ondelete='CASCADE'), nullable=False)
    calculado_en: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    puntaje: Mapped[int] = mapped_column(SMALLINT(unsigned=True), nullable=False)
    version_modelo: Mapped[str] = mapped_column(String(20), nullable=False)
    componentes: Mapped[dict] = mapped_column(JSON(), nullable=False)

    __table_args__ = (
        Index('ix_score_historial_usuario_calculado', 'usuario_id', 'calculado_en'),
        CheckConstraint('puntaje BETWEEN 0 AND 100', name='ck_score_historial_puntaje_rango'),
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )
