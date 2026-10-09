"""Importar aquí cada modelo nuevo: Alembic y SQLAlchemy solo conocen las tablas que se importan."""

from app.models.usuario import Usuario
from app.models.categoria import Categoria
from app.models.ingreso import Ingreso
from app.models.gasto import Gasto
from app.models.tarjeta import Tarjeta
from app.models.estado_cuenta import EstadoCuenta
from app.models.plan_msi import PlanMsi
from app.models.movimiento import Movimiento
from app.models.deuda import Deuda
from app.models.score_historial import ScoreHistorial
from app.models.resumen_mensual import ResumenMensual

__all__ = ['Usuario', 'Categoria', 'Ingreso', 'Gasto', 'Tarjeta', 'EstadoCuenta', 'PlanMsi', 'Movimiento', 'Deuda', 'ScoreHistorial', 'ResumenMensual']
