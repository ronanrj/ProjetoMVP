from flask import redirect
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Tag

#from model import Cfc, Instrutor, Carro

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')