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
```
app = FastAPI()

app.include_router(curso_router.router, tags=['cursos'])
app.include_router(usuario_router.router, tags=['usuarios'])
```

- Nos routers configuramos os @router:
```
from fastapi import APIRouter

router = APIRouter()

@router.get('/api/v1/cursos')
async def get_cursos():
    return {'info':"Todos os cursos"}
```

### Validação pydantic

- No models.py podemos fazer validações dos atributos,
indicando limites: 

```
@field_validator('titulo', check_fields=False)
    def validar_titulo(cls, value:str):
        palavras = value.split(' ')
        if len(palavras) < 3:
            raise ValueError('O título deve ter pelo menos 3 palavras')
        if value.islower():
            raise ValueError('O título deve ser capitalizado.') 
```




