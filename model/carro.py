from sqlalchemy import Column, String, Integer, DateTime, ForeignKey , Boolean
from datetime import datetime
from typing import Union

from model import Base

class Carro(Base):
    __tablename__ = 'carro'  
    
    id = Column(Integer ,primary_key=True,unique=True)
    renavan = Column(Integer,unique = True)
    placa = Column(String(10))
    marca = Column(String(20))
    modelo = Column(String(20))
    status = Column(Boolean)
    ultima_atualizacao = Column(DateTime,default=datetime.now())
    #relacionamento com a tabela cfc    
    cfc = Column(String , ForeignKey("cfc.codigo") , nullable=False)
    
    #construtor
    def __init__(self , renavan:int , placa:str, marca:str, modelo:str , status:Boolean , ultima_atualizacao:Union[DateTime,None] = None):
        """
        Cria o cadastro de um novo carro da cfc

        Arguments:
            renavan: renavan do carro
            placa: placa do carro
            marca: marca do carro
            modelo: modelo do carro
            status: se está ativo
            ultima_atualizacao: data de quando o instrutor teve a ultima atualização
        """
        
        self.renavan = renavan
        self.placa = placa        
        self.marca = marca
        self.modelo = modelo          
        self.status = status        
        if ultima_atualizacao:
          self.ultima_atualizacao = ultima_atualizacao
