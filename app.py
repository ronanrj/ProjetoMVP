from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError

from flask_cors import CORS

from model import Session,Cfc, Instrutor, Carro
from schemas import *

info = Info(title="MVP - API - Auto Escola", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
cfc_tag = Tag(name="Cfc", description="Adição, visualização e remoção de cfc à base")
instrutor_tag = Tag(name="Instrutor", description="Adição, visualização e remoção de instrutor à base")
# carro_tag = Tag(name="Carro", description="Adição, visualização e remoção de carro à base")

# @app.get('/', tags=[home_tag])
# def home():
#     """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
#     """
#     return redirect('/openapi')

@app.post('/cfc', tags=[cfc_tag],
          responses={"200": CfcViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_cfc(form: CfcSchema):
    """Adiciona uma nova cfc à base de dados

    Retorna uma representação dos produtos e comentários associados.
    """
    cfc = Cfc(
        codigo=form.codigo,
        nome=form.nome,
        cnpj=form.cnpj,
        status=form.status,
        regiao = form.regiao)        
    #logger.debug(f"Adicionando cfc de nome: '{cfc.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(cfc)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        #logger.debug(f"Adicionado cfc de nome: '{cfc.nome}'")
        return apresenta_cfc(cfc), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "cfc de mesmo nome já salvo na base :/"
        #logger.warning(f"Erro ao adicionar cfc '{cfc.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        #logger.warning(f"Erro ao adicionar cfc '{cfc.nome}', {error_msg}")
        return {"mesage": error_msg}, 400
    
@app.post('/instrutor', tags=[instrutor_tag],
          responses={"200": InstrutorViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_intrutor(form: InstrutorSchema):
    """Adiciona uma nova cfc à base de dados

    Retorna uma representação dos produtos e comentários associados.
    """
    cfc = Cfc(
        codigo=form.codigo,
        nome=form.nome,
        cnpj=form.cnpj,
        status=form.status,
        regiao = form.regiao)        
    #logger.debug(f"Adicionando cfc de nome: '{cfc.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(cfc)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        #logger.debug(f"Adicionado cfc de nome: '{cfc.nome}'")
        return apresenta_cfc(cfc), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "cfc de mesmo nome já salvo na base :/"
        #logger.warning(f"Erro ao adicionar cfc '{cfc.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        #logger.warning(f"Erro ao adicionar cfc '{cfc.nome}', {error_msg}")
        return {"mesage": error_msg}, 400    