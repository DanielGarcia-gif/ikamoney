from datetime import datetime

from sqlalchemy import TIMESTAMP, text
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    """creado_en y actualizado_en: los llena MySQL, la app no los escribe."""

    creado_en: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    actualizado_en: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )
