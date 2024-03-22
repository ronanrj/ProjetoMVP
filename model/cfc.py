from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from model import Base , Instrutor , Carro


class Cfc(Base):
    __tablename__ = 'cfc'
    
    id = Column(Integer, unique=True)
    codigo = Column("pk_cfc",String(20),unique=True , primary_key=True)
    nome = Column(String(100))
    cnpj = Column(String(20))
    status = Column(Boolean)
    regiao = Column(String(50))
    ultima_atualizacao = Column(DateTime,default=datetime.now())
    
    #definição d erelacionamento faltando
    instrutores = relationship("Instrutor")
    carros = relationship("Carro")
    
    
    def __init__(self, codigo:str , nome:str , cnpj:str , status:Boolean , regiao:str , ultima_atualizacao:Union[DateTime,None] = None ):
        """
        Cria uma Cfc

        Arguments:
            codigo = codigo unico da auto escola
            nome: nome da auto escola.
            cnpj: cnpj da auto escola
            status: se a auto escola está ativa
            regiao: regiao onde se encontra a 
            ultima_atualizacao: data de quando o cfc teve a ultima atualização
        """        
        self.codigo =codigo
        self.nome = nome
        self.cnpj = cnpj
        self.status = status
        self.regiao = regiao        
        if ultima_atualizacao:
          self.ultima_atualizacao = ultima_atualizacao
          
    def adiciona_instrutor(self, instrutor:Instrutor):
       """ Adiciona um novo instrutor na cfc """
       self.instrutores.append(instrutor)
                 
    def adiciona_carro(self, carro:Carro):
       """ Adiciona um novo carro na cfc """
       self.carros.append(carro)                 
