from passlib.context import CryptContext


CRIPTO = CryptContext(schemes=['bcrypt'])


def verificar_senha(senha:str, hash_senha: str) ->bool:
    """
    Docstring para verificar_senha se está correta, comparando
    a senha em texto puro, informada pelo usuário, e o
    hash da senha que estará salvo no banco de dados durante
    a criação de conta.
    
    :param senha: Description
    :type senha: str
    :param hash: Description
    :type hash: str
    :return: Description
    :rtype: bool
    """

    return CRIPTO.verify(senha, hash_senha)


def gerar_hash_senha(senha:str) -> str:
    """
    Docstring para gerar_hash_senha para retornar
    o hash da senha
    
    :param senha: Description
    :type senha: str
    :return: Description
    :rtype: str
    """
    return CRIPTO.hash(senha)
