import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey ,Boolean
from datetime import datetime
from typing import Union

from model import Base

class Instrutor(Base):
    __tablename__ = 'instrutor'
    
    
    id = Column(Integer,primary_key=True, unique=True)
    cpf = Column(String(20),unique = True)
    nome = Column(String(100))
    aula = Column(String(20))
    status = Column(Boolean)
    ultima_atualizacao = Column(DateTime,default=datetime.now())
    #relacionamento com a tabela cfc 
    cfc = Column(String , ForeignKey("cfc.codigo") , nullable=False)
    
    #construtor
    def __init__(self , cpf:str , nome:str, aula:str , status:Boolean , ultima_atualizacao:Union[DateTime,None] = None):
        """
        Cria novo Instrutor

        Arguments:
            cpf: cpf do instrutor
            nome: nome do instrutor
            aula: aula que o instrutor leciona , para qual tipo de carteira
            status: se está ativo
            ultima_atualizacao: data de quando o instrutor teve a ultima atualização
        """
        self.cpf = cpf
        self.nome = nome        
        self.aula = aula        
        self.status = status        
        if ultima_atualizacao:
          self.ultima_atualizacao = ultima_atualizacao
         
