from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.database import get_db

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    """El backend está vivo (no toca la base de datos)."""
    return {"status": "ok"}


@router.get("/ping-db")
def ping_db(db: Session = Depends(get_db)):
    """Prueba de la tubería: lee de MySQL en qué migración está el esquema.

    Si responde bien, la base conecta Y las migraciones ya se aplicaron.
    """
    try:
        row = db.execute(text("SELECT version_num FROM alembic_version")).first()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="No se pudo leer la base de datos. ¿Corriste las migraciones? (alembic upgrade head)",
        )
    if row is None:
        raise HTTPException(
            status_code=503,
            detail="La base no tiene migraciones aplicadas. Corre: alembic upgrade head",
        )
    return {"message": f"Base de datos conectada. Esquema en la migración {row[0]}."}
