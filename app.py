from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError

from flask_cors import CORS

from model import Session,Cfc, Instrutor, Carro
from schemas import *

info = Info(title="MVP - API - Auto Escola", version="1.0.0")
app = OpenAPI(__name__, info=info)
app.config['SWAGGER_BASEPATH'] = '/swagger'
CORS(app)

# definindo tags
cfc_tag = Tag(name="Cfc - auto escola", description="Adição, visualização e remoção de uma auto escola à base")
carro_tag = Tag(name="Carro", description="Adição, visualização e remoção de carro à base")
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
instrutor_tag = Tag(name="Instrutor", description="Adição, visualização e remoção de instrutor à base")

@app.post('/cfc', tags=[cfc_tag],
          responses={"200": CfcViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_cfc(form: CfcSchema):
    """Adiciona uma nova auto escola à base de dados

    Retorna uma representação das auto escolas e instrutor e carros associados.
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
        error_msg = "auto escola de mesmo nome já salvo na base :/"
        #logger.warning(f"Erro ao adicionar cfc '{cfc.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        #logger.warning(f"Erro ao adicionar cfc '{cfc.nome}', {error_msg}")
        return {"mesage": error_msg}, 400

#get all cfc
@app.get('/cfc', tags=[cfc_tag],
         responses={"200": ListaCfcsSchema, "404": ErrorSchema})
def get_cfcs():
    """Faz a busca por todas as auto escolas cadastrados

    Retorna uma representação da lista de todas as auto escolas.
    """
    #logger.debug(f"Coletando produtos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    cfcs = session.query(Cfc).all()

    if not cfcs:
        # se não há produtos cadastrados
        return {"cfcs": []}, 200
    else:
        #logger.debug(f"%d rodutos econtrados" % len(produtos))
        # retorna a representação de produto
        print(cfcs)
        return apresenta_cfcs(cfcs), 200

#getbycod
@app.get('/cfc/<codigo>', tags=[cfc_tag],
         responses={"200": CfcViewSchema, "404": ErrorSchema})
def get_cfc(query: CfcBuscaSchema):
    """Faz a busca por uma auto escola a partir do codigo da auto escola

    Retorna uma representação das auto escolas e carros e instrutores.
    """
    cfc_codigo = query.codigo
    #logger.debug(f"Coletando dados sobre produto #{produto_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    cfc = session.query(Cfc).filter(Cfc.codigo == cfc_codigo).first()

    if not cfc:
        # se o cfc não foi encontrado
        error_msg = "auto escola não encontrado na base :/"
        #logger.warning(f"Erro ao buscar produto '{cfc_codigo}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        #logger.debug(f"CFC econtrado: '{produto.nome}'")
        # retorna a representação de cfc
        return apresenta_cfc(cfc), 200
    
# delete cfc
@app.delete('/cfc/<codigo>', tags=[cfc_tag],
            responses={"200": CfcDelSchema, "404": ErrorSchema})
def del_cfc(query: CfcBuscaSchema):
    """Deleta uma auto escola a partir do codigo informado

    Retorna uma mensagem de confirmação da remoção.
    """
    cfc_codigo = unquote(unquote(query.codigo))
    print(cfc_codigo)
    #logger.debug(f"Deletando dados sobre cfc #{cfc_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Cfc).filter(Cfc.codigo == cfc_codigo).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        #logger.debug(f"Deletado produto #{cfc_nome}")
        return {"mesage": "Auto escola removida", "codigo": cfc_codigo}
    else:
        # se o cfc não foi encontrado
        error_msg = "Cfc não encontrado na base :/"
        #logger.warning(f"Erro ao deletar produto #'{cfc_codigo}', {error_msg}")
        return {"mesage": error_msg}, 404    

#falta a put (alterar)
# update cfc
@app.put('/cfc/<id>', tags=[cfc_tag],
         responses={"200": CfcSchema, "404": ErrorSchema})
def update_cfc(query:CfcPutSchema,form: CfcSchema ):
    """Atualiza uma auto escola existente na base de dados

    Retorna uma representação atualizada da auto escola.
    """
    # obtendo o código da cfc a ser atualizada
    #cfc_id = unquote(unquote(query.id))
    cfc_id = query.id

    # criando conexão com a base
    session = Session()

    # buscando a cfc a ser atualizada
    cfc = session.query(Cfc).filter(Cfc.id == cfc_id).first()

    if not cfc:
        # se a cfc não foi encontrada
        error_msg = "Cfc não encontrada na base :/"
        return {"message": error_msg}, 404

    # atualizando os atributos da cfc com os valores fornecidos
    cfc.codigo = form.codigo
    cfc.nome = form.nome
    cfc.cnpj = form.cnpj
    cfc.status = form.status
    cfc.regiao = form.regiao

    try:
        # efetuando a atualização no banco de dados
        session.commit()
        # retornando a representação atualizada da cfc
        return apresenta_cfc(cfc), 200

    except Exception as e:
        # caso ocorra algum erro durante a atualização
        error_msg = "Não foi possível atualizar a cfc :/"
        return {"message": error_msg}, 400

@app.post('/carro', tags=[carro_tag],
          responses={"200": CarroViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_carro(form: CarroSchema):
    """Adiciona um carro à base de dados
    Retorna uma representação do carro cadastrado.
    """
    carro = Carro(
        renavan=form.renavan,
        placa=form.placa,
        marca=form.marca,
        modelo=form.modelo,
        status = form.status,
        cfc = form.cfc)        
    #logger.debug(f"Adicionando cfc de nome: '{cfc.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        session.add(carro)
        session.commit()
        #logger.debug(f"Adicionado cfc de nome: '{cfc.nome}'")
        return apresenta_carro(carro), 200

    except IntegrityError as e:
        # como a duplicidade do renavan é a provável razão do IntegrityError
        error_msg = "Carro com o mesmo renavan já salvo na base :/"
        #logger.warning(f"Erro ao adicionar cfc '{cfc.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        #logger.warning(f"Erro ao adicionar cfc '{cfc.nome}', {error_msg}")
        return {"mesage": error_msg}, 400
    
@app.get('/carro', tags=[carro_tag],
         responses={"200": ListaCarrosSchema, "404": ErrorSchema})
def get_carros():
    """Faz a busca por todas os carros cadastrados
    Retorna uma representação da lista de todas os carros.
    """
    #logger.debug(f"Coletando produtos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    carros = session.query(Carro).all()

    if not carros:
        # se não há produtos cadastrados
        return {"carros": []}, 200
    else:
        #logger.debug(f"%d rodutos econtrados" % len(produtos))
        # retorna a representação de produto
        print(carros)
        return apresenta_carros(carros), 200 
    
@app.get('/carro/<renavan>', tags=[carro_tag],
         responses={"200": CarroViewSchema, "404": ErrorSchema})
def get_carro(query: CarroBuscaSchema):
    """Faz a busca por um carro a partir do renavan
    Retorna uma representação dos carros
    """
    carro_renavan = query.renavan
    #logger.debug(f"Coletando dados sobre produto #{produto_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    carro = session.query(Carro).filter(Carro.renavan == carro_renavan).first()

    if not carro:
        # se o cfc não foi encontrado
        error_msg = "Carro não encontrado na base :/"
        #logger.warning(f"Erro ao buscar produto '{cfc_codigo}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        #logger.debug(f"CFC econtrado: '{produto.nome}'")
        # retorna a representação de cfc
        return apresenta_carro(carro), 200

@app.delete('/carro/<renavan>', tags=[carro_tag],
            responses={"200": CarroDelSchema, "404": ErrorSchema})
def del_carro(query: CarroBuscaSchema):
    """Deleta um carro a partir do renavan informado
    Retorna uma mensagem de confirmação da remoção.
    """
    carro_renavan = unquote(unquote(str(query.renavan)))
    print(carro_renavan)
    #logger.debug(f"Deletando dados sobre cfc #{cfc_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Carro).filter(Carro.renavan == carro_renavan).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        #logger.debug(f"Deletado produto #{cfc_nome}")
        return {"mesage": "Carro removido", "renavan": carro_renavan}
    else:
        # se o cfc não foi encontrado
        error_msg = "Carro não encontrado na base :/"
        #logger.warning(f"Erro ao deletar produto #'{cfc_codigo}', {error_msg}")
        return {"mesage": error_msg}, 404        

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

    
@app.post('/instrutor', tags=[instrutor_tag],
          responses={"200": InstrutorViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_intrutor(form: InstrutorSchema):
    """Adiciona um novo instrutor à base de dados
    Retorna uma representação dos instrutores .
    """
    instrutor = Instrutor(
        cpf = form.cpf,
        nome = form.nome,
        aula = form.aula,
        status=form.status,
        cfc = form.cfc)          

    #logger.debug(f"Adicionando cfc de nome: '{cfc.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(instrutor)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        #logger.debug(f"Adicionado cfc de nome: '{cfc.nome}'")
        return apresenta_instrutor(instrutor), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "instrutor de mesmo cpf já salvo na base :/"
        #logger.warning(f"Erro ao adicionar cfc '{cfc.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        #logger.warning(f"Erro ao adicionar cfc '{cfc.nome}', {error_msg}")
        return {"mesage": error_msg}, 400    
    
#get all cfc
@app.get('/instrutor', tags=[instrutor_tag],
         responses={"200": ListaInstrutoresSchema, "404": ErrorSchema})
def get_instrutores():
    """Faz a busca por todos os instrutores cadastrados

    Retorna uma representação de lista de todos os instrutores das auto escolas.
    """
    #logger.debug(f"Coletando produtos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    instrutores = session.query(Instrutor).all()

    if not instrutores:
        # se não há produtos cadastrados
        return {"instrutores": []}, 200
    else:
        #logger.debug(f"%d rodutos econtrados" % len(produtos))
        # retorna a representação de produto
        print(instrutores)
        return apresenta_instrutores(instrutores), 200

@app.get('/instrutor/<cpf>', tags=[instrutor_tag],
         responses={"200": InstrutorViewSchema, "404": ErrorSchema})
def get_instrutor(query: InstrutorBuscaSchema):
    """Faz a busca por um instrutor a partir do cpf

    Retorna uma representação de  instrutores
    """
    instrutor_cpf = query.cpf
    #logger.debug(f"Coletando dados sobre produto #{produto_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    instrutor = session.query(Instrutor).filter(Instrutor.cpf == instrutor_cpf).first()

    if not instrutor:
        # se o cfc não foi encontrado
        error_msg = "instrutor não encontrado na base :/"
        #logger.warning(f"Erro ao buscar produto '{cfc_codigo}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        #logger.debug(f"CFC econtrado: '{produto.nome}'")
        # retorna a representação de cfc
        return apresenta_instrutor(instrutor), 200
    
    
@app.delete('/instrutor/<cpf>', tags=[instrutor_tag],
            responses={"200": InstrutorDelSchema, "404": ErrorSchema})
def del_instrutor(query: InstrutorBuscaSchema):
    """Deleta um instrutor a partir do cpf informado

    Retorna uma mensagem de confirmação da remoção.
    """
    instrutor_cpf = unquote(unquote(query.cpf))
    print(instrutor_cpf)
    #logger.debug(f"Deletando dados sobre cfc #{cfc_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Instrutor).filter(Instrutor.cpf == instrutor_cpf).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        #logger.debug(f"Deletado produto #{cfc_nome}")
        return {"mesage": "Instrutor removido", "cpf": instrutor_cpf}
    else:
        # se o cfc não foi encontrado
        error_msg = "Instrutor não encontrado na base :/"
        #logger.warning(f"Erro ao deletar produto #'{cfc_codigo}', {error_msg}")
        return {"mesage": error_msg}, 404    
    
@app.put('/instrutor/<id>', tags=[instrutor_tag],
         responses={"200": InstrutorSchema, "404": ErrorSchema})
def update_instrutor(query:InstrutorPutSchema,form: InstrutorSchema ):
    """Atualiza um instrutor existente na base de dados

    Retorna uma representação atualizada do instrutor.
    """
    # obtendo o código da cfc a ser atualizada
    #cfc_id = unquote(unquote(query.id))
    instrutor_id = query.id

    # criando conexão com a base
    session = Session()

    # buscando a cfc a ser atualizada
    instrutor = session.query(Instrutor).filter(Instrutor.id == instrutor_id).first()

    if not instrutor:
        # se a cfc não foi encontrada
        error_msg = "Instrutor não encontrada na base :/"
        return {"message": error_msg}, 404

    # atualizando os atributos da cfc com os valores fornecidos
    instrutor.cpf = form.cpf
    instrutor.nome = form.nome
    instrutor.aula = form.aula
    instrutor.status = form.status
    instrutor.cfc = form.cfc
    
    try:
        # efetuando a atualização no banco de dados
        session.commit()
        # retornando a representação atualizada da cfc
        return apresenta_instrutor(instrutor), 200

    except Exception as e:
        # caso ocorra algum erro durante a atualização
        error_msg = "Não foi possível atualizar o instrutor :/"
        return {"message": error_msg}, 400