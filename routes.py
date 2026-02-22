import requests

url = "http://192.168.0.14:5000"



 # get
def get_id_usuario_by_token(token_):
    response = requests.get(f"{url}/teste", headers={'Authorization': f'Bearer {token_}'})
    if response.status_code == 200:
        return response.json().get("sucesso")
    else:
        print(response.status_code)
        print({'erro':response.json()})
        return {'erro':response.status_code}

def get_usuarios(token_): # Feito
    base_url = f"{url}/usuario"
    response = requests.get(base_url, headers={'Authorization': f'Bearer {token_}'})
    print(response.json())
    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code)
        print(response.json())
        return {'erro':response.status_code}


def get_usuario_por_id(id_usuario):
    response = requests.get(f"{url}/get_usuario/{id_usuario}")

    if response.status_code == 200:
        return response.json()  # dict
    return None

def get_livro_por_id(id_livro):
    response = requests.get(f"{url}/get_livro/{id_livro}")

    if response.status_code == 200:
        return response.json()
    return None


def get_historico_de_emprestimos_por_usuario(id_usuario):
    response = requests.get(f"{url}/historico_emprestimos/{id_usuario}")

    if response.status_code == 200:
        return response.json()
    return None


def get_livros(token_):
    base_url = f"{url}/livro"
    response = requests.get(base_url, headers={'Authorization': f'Bearer {token_}'})
    print(response.json())
    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code)
        print(response.json())
        return {'erro': response.status_code}

def get_emprestimos(token_):
    base_url = f"{url}/emprestimo"
    response = requests.get(base_url, headers={'Authorization': f'Bearer {token_}'})
    print(response.json())
    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code)
        print(response.json())
        return {'erro': response.status_code}



def get_livros_disponiveis():
    base_url = f"{url}/livros_disponiveis"
    response = requests.get(base_url)
    print(response.json())
    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code)
        print(response.json())
        return {'erro': response.status_code}


def get_livros_emprestados():
    base_url = f"{url}/livros_emprestados"
    response = requests.get(base_url)
    print(response.json())
    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code)
        print(response.json())
        return {'erro': response.status_code}

# post
def post_login(email, password):
    response = requests.post(f"{url}/login", json={"email": email, "senha": password})
    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code)
        print(response)
        return {'erro':response.status_code}



def post_livro(token_, titulo, autor, ISBN, resumo, leitura):
    response = requests.post(f"{url}/novo_livro",
    json={
        "titulo": titulo,
        "autor": autor,
        "ISBN": ISBN,
        "resumo": resumo,
        "leitura": leitura,
    },
    headers={'Authorization': f'Bearer {token_}'})
    if response.status_code == 201:
        return response.json()
    else:
        print(response.status_code)
        print(response.json())
        return {'erro': response.status_code}

# put

def put_editar_usuario(id_usuario, nome, papel, status_user, email, endereco, cpf):
    response = requests.put(f"{url}/editar_usuario/{id_usuario}",
    json={
        "nome":nome,
        "papel":papel,
        "status_user":status_user,
        "email":email,
        "endereco":endereco,
        "cpf":cpf,

    },

    )
    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code)
        print(response.json())
        return {'erro':response.status_code}


def put_editar_livro(id_livro, titulo, autor, ISBN, resumo, leitura):
    response = requests.put(
        f"{url}/editar_livro/{id_livro}",
        json={
            "titulo": titulo,
            "autor": autor,
            "ISBN": ISBN,
            "resumo": resumo,
            "leitura": leitura,
        }
    )

    return response.status_code



# delete

def delete_livro(id_livro):
    response = requests.delete(
        f"{url}/deletar_livro/{id_livro}")

    if response.status_code == 200:
        return response.json()
    return None


# Gráficos
def get_livros_mais_emp():
    base_url = f"{url}/grafico_livros_mais_emprestados"

    response = requests.get(
        base_url,

    )

    print("Status code:", response.status_code)
    print("Response text:", response.text)

    if response.status_code == 200:
        try:
            return response.json()
        except Exception:
            return {"erro": "Resposta inválida da API"}
    else:
        return {
            "erro": response.status_code,
            "mensagem": response.text
        }



def get_usuarios_que_mais_realizaram_emp():
    base_url = f"{url}/usuarios_que_mais_realizaram_emp"

    response = requests.get(
        base_url,

    )

    print("Status code:", response.status_code)
    print("Response text:", response.text)

    if response.status_code == 200:
        try:
            return response.json()
        except Exception:
            return {"erro": "Resposta inválida da API"}
    else:
        return {
            "erro": response.status_code,
            "mensagem": response.text
        }