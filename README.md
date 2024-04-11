# ProjetoMVP backEnd API
ProjetoMVP backEnd API - Este projeto faz parte da entrega para conclusão do mvp da sprint Desevolvimento Full Stack Básico do curso de pós graduação da PUC RIO. O objetivo do projeto é um cadastro simples de auto escolas com relacionamento de carros e instrutores em uma base de dados sqlite

---
## Como executar 

Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

> Ambiente virtual Python

Cria o ambiente virtual com o comando python -m venv env

Após, ativar o ambiente com o comando .\env\Scripts\Activate.ps1

Após, será necessário ter todas as libs python listadas no `requirements.txt` instaladas.

```
(env)$ pip install -r requirements.txt
```

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
