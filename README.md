# Social API

Uma API de rede social simples e eficiente construída com **FastAPI** e **Python**, projetada para aprendizado e demonstração de boas práticas. O projeto suporta funcionalidades essenciais como cadastro de usuários, autenticação via JWT, criação de postagens e comentários.

## 🚀 Funcionalidades

- **Autenticação**: Registro de usuários e login seguro (OAuth2 com JWT).
- **Posts**: Criação e listagem de postagens.
- **Comentários**: Adição e visualização de comentários vinculados a posts.
- **Banco de Dados**: Persistência de dados utilizando SQLAlchemy (modo assíncrono) e SQLite.
- **Monitoramento**: Configuração de logs estruturados e correlação de requisições.

## 🛠️ Tecnologias Utilizadas

- [Python 3.12+](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderno e rápido.
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM para interação com banco de dados.
- [Pydantic](https://docs.pydantic.dev/) - Validação de dados.
- [Pytest](https://docs.pytest.org/) - Testes automatizados.

## 📦 Instalação

Siga os passos abaixo para configurar o ambiente de desenvolvimento:

1. **Clone o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd python
   ```

2. **Crie um ambiente virtual**
   ```bash
   python -m venv .venv
   ```

3. **Ative o ambiente virtual**
   - Windows:
     ```bash
     .\.venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```

4. **Instale as dependências**
   Principais:
   ```bash
   pip install -r requirements.txt
   ```
   Desenvolvimento (testes e linting):
   ```bash
   pip install -r requirements-dev.txt
   ```

## ⚙️ Configuração

Copie o arquivo de exemplo de variáveis de ambiente e ajuste conforme necessário:

```bash
cp .env.exemple .env
# Ou no Windows: copy .env.exemple .env
```

## ▶️ Executando a Aplicação

Para iniciar o servidor de desenvolvimento:

```bash
uvicorn socialapi.main:app --reload
```

A API estará rodando em: `http://127.0.0.1:8000`

### Documentação Interativa
O FastAPI gera documentação automaticamente. Acesse:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 🧪 Testes

Para executar a suíte de testes automatizados:

```bash
pytest
```

Para executar os testes com visualização de cobertura (coverage):

```bash
pytest --cov=socialapi --cov-report=html
```

## 📂 Estrutura do Projeto

- `socialapi/`: Pacote principal da aplicação.
  - `routers/`: Definição de endpoints (User, Post, Comment).
  - `models/`: Modelos de dados e schemas Pydantic.
  - `service/`: Lógica de negócio e acesso a dados.
  - `core/`: Configurações globais (Database, Logging, Security).
- `tests/`: Testes unitários e de integração.
