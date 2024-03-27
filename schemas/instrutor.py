from pydantic import BaseModel
from datetime import datetime
from typing import List
from model.instrutor import Instrutor

class InstrutorSchema(BaseModel):
    """ Define como um novo instrutor deve ser representado para ser inserido"""    
    cpf: str = "00000000000"
    nome: str = "Joao"
    aula: str = "94127426063"
    status: bool = True
    cfc: str = "ab1234"
    
#estrutura get apenas por codigo    
class InstrutorBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será feita apenas com base no cpf instrutor. """
    cpf: str = "00000000000" 
    
#estrutura getAll  
class ListaInstrutoresSchema(BaseModel):
    """ Define como a lista de instrutores será retornada """
    instrutores:List[InstrutorSchema]
    
def apresenta_instrutores(instrutores: List[Instrutor]):
    """ Retorna uma representação do instrutor seguindo o schema definido em InstrutorViewSchema."""
    result = []
    for instrutor in instrutores:
        result.append({
            "id" : instrutor.id,
            "cpf": instrutor.cpf,
            "aula": instrutor.aula,
            "status": instrutor.status,
            "ultima_atualizacao": instrutor.ultima_atualizacao,
            "cfc": instrutor.cfc 
        })  
                   
    return{"instrutores": result}

class InstrutorViewSchema(BaseModel):
    """ Define como um instrutor será retornada"""
    id:int = 1
    cpf:str = "00000000000"
    nome:str = "Jose Ipson"
    aula: str = "AB"
    status:bool = True
    ultima_atualizacao = datetime.now()
    #relacionamento com a tabela cfc 
    cfc:str = "ab1234" 

#esquema delete        
class InstrutorDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição de remoção."""
    mesage: str
    codigo: str
    
#esquema apenas 1 instrutor    
def apresenta_instrutor(instrutor: Instrutor):
    """ Retorna uma representação do instrutor seguindo o schema definido em InstrutorViewSchema. """
    return{
        "id" : instrutor.id,
        "cpf": instrutor.cpf,
        "nome": instrutor.nome,
        "aula": instrutor.aula,
        "status": instrutor.status,
        "ultima_atualizacao": instrutor.ultima_atualizacao,
        "cfc": instrutor.cfc 
        }

class InstrutorListagemSchema(BaseModel):
    """ Define como um novo instrutor deve ser representado para ser inserido"""  
    id : int = 1 
    cpf: str = "00000000000"
    nome: str = "Joao"
    aula: str = "94127426063"
    status: bool = True
    cfc: str = "ab1234"    
    
class InstrutorPutSchema(BaseModel):
    """ Define como um novo instrutor deve ser representado para ser inserido"""   
    id : int = 1