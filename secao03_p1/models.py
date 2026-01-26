from typing import Optional

from pydantic import BaseModel


class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int


cursos=[
    Curso(id = 1, titulo="Programação para leigos", aulas=112, horas=58),
    Curso(id = 2, titulo="Algoritmos e Lógica de Programação", aulas=87, horas=67),
]
