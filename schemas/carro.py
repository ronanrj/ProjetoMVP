from datetime import datetime
from pydantic import BaseModel
from typing import List
from model.carro import Carro

class CarroSchema(BaseModel):
    """ Define como um novo carro deve ser representado para ser inserido"""
    id: int = 1 
    renavan: int = 2658568543
    placa: str = "Lag7598"
    marca: str = "Fiat"
    modelo: str = "147"
    status: bool = True    
    #relacionamento com a tabela cfc    
    cfc: str = "ab1222" 
    
    
    #estrutura get apenas por codigo    
class CarroBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será feita apenas com base no renavan. """
    renavan: int = 2658568543
    
#estrutura getAll  
class ListaCarrosSchema(BaseModel):
    """ Define como a lista de carro será retornada """
    carros:List[CarroSchema]

def apresenta_carros(carros:List[Carro]):
    """ Retorna uma representação de carro seguindo o schema definido em CarroViewSchema."""
    result = []
    for carro in carros:
        result.append({
            "id":carro.id,
            "renavan": carro.renavan,
            "placa": carro.placa,
            "marca": carro.marca,
            "modelo": carro.modelo,
            "status": carro.status,
            "ultima_atualizacao":carro.ultima_atualizacao,
            "cfc": carro.cfc
        })  
                                   
    return{"carros": result}

class CarroViewSchema(BaseModel):
    """ Define como um carro será retornado"""
    id: int = 1
    renavan: int = 1
    placa:str = "ab0000"
    marca:str = "Auto Escola Sem Nome"
    modelo:str = "43515658000149"
    status = True
    ultima_atualizacao = datetime.now()
    cfc = "ab132"

#esquema delete        
class CarroDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    renavan: str

#esquema apenas 1 cfc    
def apresenta_carro(carro: Carro):
    """ Retorna uma representação da cfc seguindo o schema definido em CfcViewSchema. """
    return{
            "id":carro.id,
            "renavan": carro.renavan,
            "placa": carro.placa,
            "marca": carro.marca,
            "modelo": carro.modelo,
            "status": carro.status,
            "ultima_atualizacao":carro.ultima_atualizacao,
            "cfc": carro.cfc
        }