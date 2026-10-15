# Biblioteca Web

Interface web de administração da biblioteca digital. Consome a [API Biblioteca](https://github.com/vinicincosta/API_biblioteca), a mesma usada pelo [app mobile](https://github.com/vinicincosta/app_biblioteca): gerenciamento de livros, usuários e empréstimos, com um dashboard de gráficos.

## Funcionalidades

- Login com e-mail e senha (autenticação feita pela API) e controle de sessão
- **Livros**: listagem, edição, exclusão com confirmação e filtros de livros disponíveis e emprestados
- **Usuários**: listagem e histórico de empréstimos por usuário
- **Empréstimos**: listagem com livro, usuário, datas e status
- **Dashboard**: gráficos de barras (Chart.js) com os livros mais emprestados e os usuários que mais emprestam
- Menu de navegação (Usuários, Livros, Empréstimos) exibido para o perfil `admin`

### Implementadas, em ajuste

- **Cadastrar livro**: o livro é gravado na API, mas a tela exibe mensagem de erro (o retorno da chamada é comparado ao código `200`, e a API responde `201`)
- **Editar usuário**: a chamada usa `/editar_usuario/<id>`, e a rota da API é `/editar_usuarios/<id>`
- **Livros emprestados**: os campos aparecem em branco (o template lê `titulo`, `autor`, etc.; a API devolve `livro_titulo`, `livro_autor`, etc.)

## Tecnologias

- Python 3 e Flask (templates Jinja2, sessão)
- Requests (comunicação com a API)
- Bootstrap 5.3 e Chart.js, carregados por CDN

## Estrutura

```
Biblioteca_Web/
├── app.py          # rotas Flask, login e controle de sessão
├── routes.py       # chamadas à API (requests) e URL base da API
├── templates/      # páginas Jinja2: login, livros, usuários, empréstimos, histórico, dashboard
└── static/         # style.css e ícone do dashboard
```

## Como rodar

1. Suba a [API Biblioteca](https://github.com/vinicincosta/API_biblioteca).

2. Instale as dependências do site:

```bash
git clone https://github.com/vinicincosta/Biblioteca_Web.git
cd Biblioteca_Web

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install flask requests
```

3. Aponte o site para a API editando `url` em `routes.py`:

```python
url = "http://localhost:5000"    # troque pelo endereço da sua API
```

4. Inicie o site. A API usa a porta 5000, então rode o site em outra:

```bash
flask --app app run --debug --port 5001
```

Acesse `http://localhost:5001` e entre com um usuário cadastrado na API. O primeiro usuário `admin` pode ser criado pela rota `POST /cadastro` da API (veja o README dela).

## Projetos relacionados

- [API_biblioteca](https://github.com/vinicincosta/API_biblioteca): backend REST em Flask
- [app_biblioteca](https://github.com/vinicincosta/app_biblioteca): app mobile em Flet
