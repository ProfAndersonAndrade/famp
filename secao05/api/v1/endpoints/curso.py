from typing import List

from fastapi import (APIRouter, 
                     status, 
                     Depends, 
                     HTTPException, 
                     Response)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.cuso_model import CursoModel
from core.deps import get_session


router = APIRouter()

# POST curso
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CursoModel)
async def post_curso(curso: CursoModel, db: AsyncSession = Depends(get_session)):
    novo_curso = CursoModel(titulo=curso.titulo,
                            aulas=curso.aulas,
                            horas=curso.horas)
    db.add(novo_curso)
    await db.commit()

    return novo_curso


# GET cursos
@router.get('/', status_code=status.HTTP_200_OK, response_model=List[CursoModel])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(CursoModel))
    cursos: List[CursoModel] = result.scalars().all()

    return cursos


# GET curso
@router.get('/{curso_id}', status_code=status.HTTP_200_OK, response_model=CursoModel)
async def get_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(CursoModel).where(CursoModel.id == curso_id))
    curso = result.scalar_one_or_none()

    if curso:
        return curso
    else:
        raise HTTPException(detail='Curso não encontrado!',
                            status_code=status.HTTP_404_NOT_FOUND)


# PUT curso
@router.put('/{curso_id}', status_code=status.HTTP_200_OK, response_model=CursoModel)
async def put_curso(curso_id: int, curso: CursoModel, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(CursoModel).where(CursoModel.id == curso_id))
    curso_up: CursoModel = result.scalar_one_or_none()

    if curso:
        curso_up.titulo = curso.titulo
        curso_up.aulas = curso.aulas
        curso_up.horas = curso.horas

        await db.commit()

        return curso
    else:
        raise HTTPException(detail='Curso não encontrado!',
                            status_code=status.HTTP_404_NOT_FOUND)
    

# DELETE curso
@router.delete('/{curso_id}', status_code=status.HTTP_200_OK, response_model=CursoModel)
async def delete_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(CursoModel).where(CursoModel.id == curso_id))
    curso_del: CursoModel = result.scalar_one_or_none()

    if curso_del:        

        await db.delete(curso_del)
        await db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(detail='Curso não encontrado!',
                            status_code=status.HTTP_404_NOT_FOUND)