from typing import List

from fastapi import (APIRouter, 
                     status, 
                     Depends, 
                     HTTPException, 
                     Response)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.curso_model import CursoModel
from schemas.curso_schema import CursoSchema
from core.deps import get_session

router = APIRouter()

# POST curso
@router.post('/', 
             status_code=status.HTTP_201_CREATED, 
             response_model=CursoSchema)
async def post_curso(curso: CursoSchema, db: AsyncSession = Depends(get_session)):
    novo_curso: CursoModel = CursoModel(titulo=curso.titulo, 
                                        aulas= curso.aulas,
                                        horas= curso.horas)
    
    db.add(novo_curso)
    await db.commit()
    await db.refresh(novo_curso)

    return novo_curso


# GET cursos
@router.get('/', response_model=List[CursoSchema])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(CursoModel))
    cursos = result.scalars().all()

    return cursos
