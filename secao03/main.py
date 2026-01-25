from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi import Response
from fastapi import Path, Query, Header
from typing import Optional

from models import Curso


app = FastAPI()


cursos = {
    1: {
        "titulo": "Programação para leigos",
        "aulas": 112,
        "horas": 58
    },
    2:{
        "titulo": "Algoritmos e Lógica de Programação",
        "aulas": 87,
        "horas": 67
    }
}


@app.get('/cursos')
async def get_cursos():
    return cursos


@app.get('/cursos/{curso_id}')
async def get_curso(curso_id:int = Path(...,title='ID do curso',
                                        description='Deve ser entre 1 e 2',
                                        gt=0,
                                        lt=3)):
    try:
        curso = cursos[curso_id]
        return curso
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Curso não encontrado.')


@app.post('/cursos', status_code=status.HTTP_201_CREATED)
async def post_curso(curso: Curso):
    next_id: int = len(cursos)+1    
    cursos[next_id] = curso # pyright: ignore[reportArgumentType]
    del curso.id
    return curso


@app.put('/cursos/{curso_id}')
async def put_curso(curso_id:int, curso: Curso):
    if curso_id in cursos:
        cursos[curso_id] = curso # type: ignore
        del curso.id
        return curso
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Não existe um curso com o id {curso_id}')


@app.delete('/cursos/{curso_id}')
async def delete_curso(curso_id:int):
    if curso_id in cursos:
        del cursos[curso_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Não existe um curso com o id {curso_id}')


@app.get('/calculadora')
async def calcular(a:int,b:int,c: Optional[int] = None):
    soma = a+b
    if c:
        soma += c

    return {"Resultado": soma}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', 
                host='127.0.0.1', 
                port=8000,
                reload=True 
            )