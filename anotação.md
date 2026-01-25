# FastAPI

## CRUD

- GET -> precisa do id até na rota, senão encontrar 404
- POST -> Rota limpa, passar o BaseModel no def, retorna 201
- PUT -> Precisa do id que será mudado e do BaseModel com os atributos que serão passados na atualização, senão encontrar 404
- DELETE -> Precisa do id até na rota, retorna 204(No content) se não encontrar id 404

## Path parameters

- No caso de rotas com id podemos definir um valor padrão, gt e lt para valores minimos e máximos e descrições e labels para documentação

## Query parameters

- Parecido ao Path, mas na rota precisa passar os parametros da função com ?a=2&b=3...

## Headers

- Header passado no http no request
