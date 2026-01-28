from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from core.base import Base

class CursoModel(Base):
    __tablename__ = "cursos"

    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    titulo: Mapped[str] = mapped_column(String(100))
    aulas: Mapped[int] = mapped_column(Integer)
    horas: Mapped[int] = mapped_column(Integer)
