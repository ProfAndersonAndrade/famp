from typing import Optional

from pydantic import BaseModel, field_validator


class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int # mais de 12 aulas
    horas: int # mais de 10h


    @field_validator('titulo', check_fields=False)
    def validar_titulo(cls, value:str):
        palavras = value.split(' ')
        if len(palavras) < 3:
            raise ValueError('O título deve ter pelo menos 3 palavras')
        
        if value.islower():
            raise ValueError('O título deve ser capitalizado.')
        

    @field_validator('aulas', check_fields=False)
    def validar_aulas(cls, value:int):
        
        if value > 12:
            raise ValueError('A quantidade de aulas deve ser maior que 12 aulas')
        return value
    
    @field_validator('horas', check_fields=False)
    def validar_aulas(cls, value:int):
        
        if value > 10:
            raise ValueError('O curso deve ter menos de 10 horas.')
        return value


cursos=[
    Curso(id = 1, titulo="Programação para leigos", aulas=11, horas=8),
    Curso(id = 2, titulo="Algoritmos e Lógica de Programação", aulas=10, horas=7),
]
