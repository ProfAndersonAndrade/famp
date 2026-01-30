# FastAPI

## Seção 03

### CRUD

- GET -> precisa do id até na rota, senão encontrar 404
- POST -> Rota limpa, passar o BaseModel no def, retorna 201
- PUT -> Precisa do id que será mudado e do BaseModel com os atributos que serão passados na atualização, senão encontrar 404
- DELETE -> Precisa do id até na rota, retorna 204(No content) se não encontrar id 404

### Path parameters

- No caso de rotas com id podemos definir um valor padrão, gt e lt para valores minimos e máximos e descrições e labels para documentação

### Query parameters

- Parecido ao Path, mas na rota precisa passar os parametros da função com ?a=2&b=3...

### Headers

- Header passado no http no request

### Injeção de dependências

- Injeção de dependências funciona quando precisamos do resultado de uma função antes de percorrer outra.
Na aula 20 fizemos um exemplo de uma função com sleep(1) que rodava antes do get, bom para banco de dados onde inserimos sessões

### Definindo Rotas - aula 22

- Vamos oraganizar as rotas

├── main.py
├── requirements.txt
└── routes
' ' ' ' '├── curso_router.py
' ' ' ' '└── usuario_router.py

- No main.py organizo as rotas:

```python
app = FastAPI()

app.include_router(curso_router.router, tags=['cursos'])
app.include_router(usuario_router.router, tags=['usuarios'])
```

- Nos routers configuramos os @router:

```python
from fastapi import APIRouter

router = APIRouter()

@router.get('/api/v1/cursos')
async def get_cursos():
    return {'info':"Todos os cursos"}
```

### Validação pydantic

- No models.py podemos fazer validações dos atributos,
indicando limites:

```python
@field_validator('titulo', check_fields=False)
    def validar_titulo(cls, value:str):
        palavras = value.split(' ')
        if len(palavras) < 3:
            raise ValueError('O título deve ter pelo menos 3 palavras')
        if value.islower():
            raise ValueError('O título deve ser capitalizado.') 
```

## Seção 04

### Módulo Core

- A estrutura de pastas será essa:

seção04
├── api/
├── core/
├── models/
├── schemas/
├── criar_tabelas.py
├── main.py
└── requirements.txt

- Na pasta core criamos os arquivos deps.py, configs.py, base.py e database.py. A ideia deles é configurar o banco e criar as tabelas, para isso vamos importar estes arquivos no criar_tabelas.py.

- No configs.py:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "postgresql+asyncpg://user:password@localhost:5432/faculdade"

    class Config:
        case_sensitive = True

settings = Settings()
```

-No base.py:

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

- No database.py:

```python
from sqlalchemy.ext.asyncio import (create_async_engine, 
                                    AsyncEngine, 
                                    AsyncSession, 
                                    async_sessionmaker)

from core.configs import settings

engine: AsyncEngine = create_async_engine(settings.DB_URL)

Session = async_sessionmaker(
    bind= engine,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)
```

- No deps.py (curso desatualizado, precisei pesquisar a nova forma do SQLAlchemy)

```python
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import Session

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        yield session
```

- Na pasta models criamos o __all_models.py e p curso_model.py
- No curso_model.py:

```python
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from core.base import Base

class CursoModel(Base):
    __tablename__ = "cursos"

    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    titulo: Mapped[str] = mapped_column(String(100))
    aulas: Mapped[int] = mapped_column(Integer)
    horas: Mapped[int] = mapped_column(Integer)
```

- Na pasta schemas criamos o arquivo curso_schema.py (abaixo o código). Ela parece o curso_model.py, mas em models lidamos na comunicação dos dados no banco de dados e no schema a comunicação de json com os dados, a validação deles. Resumindo validamos a entrada dos dados com schemas e armazenamos com o models:

``` python
from typing import Optional
from pydantic import BaseModel as SCBaseModel
from pydantic import ConfigDict

class CursoSchema(SCBaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int
    model_config = ConfigDict(from_attributes=True)
```

### Módulo models - aula 39

- Na pasta models criaremosos arquivos __all_models.py e o curso_model.py. No "all" puxaremos todos os models, só puxaremos o curso_model aqui:

```python
from models.curso_model import CursoModel
```

- No curso_model.py modelamos o que entra no BD:

```python
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from core.base import Base

class CursoModel(Base):
    __tablename__ = "cursos"

    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    titulo: Mapped[str] = mapped_column(String(100))
    aulas: Mapped[int] = mapped_column(Integer)
    horas: Mapped[int] = mapped_column(Integer)
```

### Criando tabelas

- No arquivo por fora das pastas criar_tabelas.py:

```python
from core.database import engine
from core.base import Base

async def create_tables() -> None:
    import models.__all_models
    print('Criando tabelas no banco de dados')

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print('Tabelas criadas com sucesso!')

if __name__ == '__main__':
    import asyncio

    asyncio.run(create_tables())
```

### Módulo api - aula 41 e 42

- Na pasta api criaremos a pasta v1.
- Dentro da pasta v1 criaremos a pasta endpoints e o arquivo api.py.
- A ideia é configurar as rotas dentro de endpoints com um arquivo com o nome da rota, no caso será curso.py, e no api.py incluímos as rotas importando dos arquivos de endpoints:

```python
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
@router.get('/', response_model=List[CursoSchema], status_code=status.HTTP_200_OK)
async def get_cursos(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(CursoModel))
    cursos = result.scalars().all()

    return cursos


# GET curso
@router.get('/{curso_id}', status_code=status.HTTP_200_OK, response_model=CursoSchema)
async def get_curso(curso_id:int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(CursoModel).where(CursoModel.id == curso_id))
    curso = result.scalar_one_or_none()

    if curso:
        return curso
    else:
        raise HTTPException(detail='Curso não encontrado!',
                            status_code=status.HTTP_404_NOT_FOUND)


# PUT curso
@router.put('/{curso_id}', status_code=status.HTTP_200_OK, response_model=CursoSchema)
async def put_curso(curso_id:int, curso:CursoSchema ,db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(CursoModel).where(CursoModel.id == curso_id))
    curso_up = result.scalar_one_or_none()

    if curso_up:
        curso_up.titulo = curso.titulo
        curso_up.aulas = curso.aulas
        curso_up.horas = curso.horas

        await db.commit()
        return curso_up
    else:
        raise HTTPException(detail='Curso não encontrado!',
                            status_code=status.HTTP_404_NOT_FOUND)
    

# DELETE curso
@router.delete('/{curso_id}', status_code=status.HTTP_200_OK, response_model=CursoSchema)
async def delete_curso(curso_id:int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(CursoModel).where(CursoModel.id == curso_id))
    curso_del = result.scalar_one_or_none()

    if curso_del:
        await db.delete(curso_del)
        await db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(detail='Curso não encontrado!',
                            status_code=status.HTTP_404_NOT_FOUND)
```

- Incluímos as rotas:

```python
from fastapi import APIRouter
from api.v1.endpoints import curso


api_router = APIRouter()
api_router.include_router(curso.router, prefix='/cursos', tags=['cursos'])
# /api/v1/cursos
```

### O  main

- Vamos configurar por fim o main centralizando tudo. Se api.py da pasta api/v1 centraliza as rotas, o main importa o api.py e incluir os recursos na URL e roda o projeto no terminal com o comando "python main.py" :

```python
from fastapi import FastAPI

from core.configs import settings
from api.v1.api import api_router

app = FastAPI(title='Cursos API - FastAPI SQL Alchemy')
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', 
                host='127.0.0.1', 
                port=8000,
                reload=True, 
                log_level='info'
            )
```

## Seção 05

- Essa seção é voltado ao ORM SQLModel, dos mesmo criadores do FastAPI. Logo uma diferença clara é que no SQLAlchemy separamos o models dos schemas, no SQLModel só tem o models.

- Estrutura:

secao05
├── api/
├── core/
├── models/
├── criar_tabelas.py
├── main.py
└── requirements.txt

### Módulo core

- O config.py serve para criar os settings e URL tanto de BD como da rota (api/v1/...).

- A estrutura de pastas será essa:

seção04
├── api/
├── core/
├── models/
├── schemas/
├── criar_tabelas.py
├── main.py
└── requirements.txt

- Na pasta core criamos os arquivos deps.py, configs.py, base.py e database.py. A ideia deles é configurar o banco e criar as tabelas, para isso vamos importar estes arquivos no criar_tabelas.py.

- No configs.py:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "postgresql+asyncpg://user:password@localhost:5432/faculdade"

    class Config:
        case_sensitive = True

settings = Settings()
```

- No database.py:

```python
from sqlalchemy.ext.asyncio import (create_async_engine, 
                                    AsyncEngine, 
                                    AsyncSession, 
                                    async_sessionmaker)

from core.configs import settings

engine: AsyncEngine = create_async_engine(settings.DB_URL)

Session = async_sessionmaker(
    bind= engine,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)
```

- No deps.py (curso desatualizado, precisei pesquisar a nova forma do SQLAlchemy)

```python
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import Session

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        yield session
```

- Não muda muito do SQLAlchemy

### Módulo models aula 39

- Na pasta models criamos o __all_models.py e p curso_model.py
- No curso_model.py:

```python
from typing import Optional

from sqlmodel import Field, SQLModel

class CursoModel(SQLModel, table=True):
    __tablename__: str = 'cursos'

    id:Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    aulas: int
    horas: int
```

- O table=True interno é para diferenciar um schema (que nao vira tabela) para um model (o True é para criar tabela). Por isso aqui teremos models e schemas, diferenciando pelo table.
- No "all" puxaremos todos os models, só puxaremos o curso_model aqui:

```python
from models.curso_model import CursoModel
```

### Criando tabelas SQLModel

- Não muda muito do SQLAlchemy

```python
from sqlmodel import SQLModel

from core.database import engine


async def create_tables() -> None:
    import models.__all_models
    print('Criando as tabelas no BD...')
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    print('Tabelas criadas com sucesso!')


if __name__ == '__main__':
    import asyncio

    asyncio.run(create_tables())
```

### Módulo Api

- Criamos a pasta v1.
- Dentro de v1 criamos o arquivo api.py e a pasta endpoints.
- Dentro de endpoints criamos o curso.py
- No curso.py:

