import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ------------------------------
# FIXTURE: produto_factory
# ------------------------------
# Esta fixture cria produtos temporários para uso nos testes.
# Ela mantém o controle dos produtos criados e os deleta automaticamente após o término do teste.

@pytest.fixture
def produto_factory():
    produtos_criados = []

    def criar_produto(nome="Produto Teste", descricao="Descrição de teste", preco=10.0, categoria="Lanche"):
        response = client.post("/produtos/", json={
            "nome": nome,
            "descricao": descricao,
            "preco": preco,
            "categoria": categoria
        })
        assert response.status_code == 201, f"Falha ao criar produto. Status: {response.status_code} - {response.text}"
        produto = response.json()
        produtos_criados.append(produto["id"])
        return produto

    yield criar_produto

    for produto_id in produtos_criados:
        client.delete(f"/produtos/{produto_id}")

def test_criar_produto(produto_factory):
    produto = produto_factory(nome="Produto Teste", descricao="Descrição de teste", preco=12.50, categoria="Lanche")
    assert produto["nome"] == "Produto Teste"

def test_listar_produtos():
    response = client.get("/produtos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_buscar_produto_por_id(produto_factory):
    produto = produto_factory(nome="Item", descricao="desc", preco=5.5, categoria="Lanche")
    produto_id = produto["id"]
    response = client.get(f"/produtos/{produto_id}")
    assert response.status_code == 200
    assert response.json()["id"] == produto_id

def test_atualizar_produto(produto_factory):
    produto = produto_factory(nome="Item", descricao="desc", preco=5.5, categoria="Lanche")
    produto_id = produto["id"]
    response = client.put(
        f"/produtos/{produto_id}",
        json={"nome": "Item Atualizado", "descricao": "Nova", "preco": 7.5, "categoria": "Lanche"}
    )
    assert response.status_code == 200
    assert response.json()["nome"] == "Item Atualizado"

def test_deletar_produto(produto_factory):
    produto = produto_factory(nome="Item", descricao="desc", preco=5.5, categoria="Lanche")
    produto_id = produto["id"]
    delete = client.delete(f"/produtos/{produto_id}")
    assert delete.status_code == 204
    get = client.get(f"/produtos/{produto_id}")
    assert get.status_code == 404 or get.json() is None

def test_buscar_produto_inexistente(produto_factory):
    produto = produto_factory(nome="Produto Temporário", descricao="Será deletado", preco=10.0, categoria="Lanche")
    produto_id = produto["id"]
    client.delete(f"/produtos/{produto_id}")

    response = client.get(f"/produtos/{produto_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Produto não encontrado"

def test_atualizar_produto_inexistente(produto_factory):
    produto = produto_factory(nome="Produto Temporário", descricao="Será deletado", preco=10.0, categoria="Lanche")
    produto_id = produto["id"]
    client.delete(f"/produtos/{produto_id}")

    payload = {
        "nome": "Produto Inexistente",
        "descricao": "Esse produto não existe",
        "preco": 99.99,
        "categoria": "Lanche"
    }
    response = client.put(f"/produtos/{produto_id}", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Produto não encontrado"

def test_deletar_produto_inexistente(produto_factory):
    produto = produto_factory(nome="Produto Temporário", descricao="Será deletado", preco=10.0, categoria="Lanche")
    produto_id = produto["id"]
    client.delete(f"/produtos/{produto_id}")

    response = client.delete(f"/produtos/{produto_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Produto não encontrado"

def test_criar_produto_sem_nome():
    response = client.post("/produtos/", json={
        "descricao": "Produto sem nome",
        "preco": 10.0,
        "categoria": "Lanche"
    })
    assert response.status_code == 422
    assert "nome" in response.text

def test_criar_produto_sem_preco():
    response = client.post("/produtos/", json={
        "nome": "Produto sem preço",
        "descricao": "Faltando preço",
        "categoria": "Lanche"
    })
    assert response.status_code == 422
    assert "preco" in response.text

def test_criar_produto_com_preco_string():
    response = client.post("/produtos/", json={
        "nome": "Produto Inválido",
        "descricao": "Preço como string",
        "preco": "dez reais",
        "categoria": "Lanche"
    })
    assert response.status_code == 422
    assert "preco" in response.text

def test_criar_produto_com_preco_negativo():
    response = client.post("/produtos/", json={
        "nome": "Produto Inválido",
        "descricao": "Preço negativo",
        "preco": -5.0,
        "categoria": "Lanche"
    })
    assert response.status_code in (400, 422)

def test_criar_produto_com_nome_muito_longo():
    nome_excessivo = "A" * 300  # Simula um nome com 300 caracteres
    response = client.post("/produtos/", json={
        "nome": nome_excessivo,
        "descricao": "Nome muito longo",
        "preco": 10.0,
        "categoria": "Lanche"
    })
    assert response.status_code == 422 or response.status_code == 400

def test_atualizar_produto_com_preco_negativo(produto_factory):
    produto = produto_factory(nome="Produto válido", descricao="Para testar atualização inválida", preco=10.0, categoria="Lanche")
    produto_id = produto["id"]

    response = client.put(f"/produtos/{produto_id}", json={
        "nome": "Produto válido",
        "descricao": "Preço inválido",
        "preco": -10.0,
        "categoria": "Lanche"
    })
    assert response.status_code in (400, 422)

def test_criar_produto_com_campo_extra():
    response = client.post("/produtos/", json={
        "nome": "Produto Extra",
        "descricao": "Campo a mais",
        "preco": 15.0,
        "desconto": 5,  # Campo não permitido
        "categoria": "Lanche"
    })
    assert response.status_code == 422

def test_atualizar_produto_com_tipo_invalido(produto_factory):
    produto = produto_factory(nome="Produto", descricao="Original", preco=10.0, categoria="Lanche")
    produto_id = produto["id"]

    response = client.put(f"/produtos/{produto_id}", json={
        "nome": "Produto",
        "descricao": "Erro tipo",
        "preco": "dez",
        "categoria": "Lanche"
    })
    assert response.status_code == 422

def test_criar_produto_com_muitas_casas_decimais():
    response = client.post("/produtos/", json={
        "nome": "Produto Decimal",
        "descricao": "Valor com casas demais",
        "preco": 9.999999,
        "categoria": "Lanche"
    })
    assert response.status_code == 201
    produto = response.json()
    assert produto["preco"] == "10.00"  # Arredondado automaticamente

def test_verificar_dados_apos_criacao(produto_factory):
    produto = produto_factory(nome="Verificação", descricao="Comparar valores", preco=13.75, categoria="Lanche")
    assert produto["nome"] == "Verificação"

    get = client.get(f"/produtos/{produto['id']}")
    assert get.status_code == 200
    assert get.json()["preco"] == "13.75"

def test_listar_produtos_apos_insercoes_multiplas(produto_factory):
    p1 = produto_factory(nome="Produto 1", descricao="Teste 1", preco=10.0, categoria="Lanche")
    p2 = produto_factory(nome="Produto 2", descricao="Teste 2", preco=20.0, categoria="Lanche")

    lista = client.get("/produtos/")
    ids = [produto["id"] for produto in lista.json()]
    assert p1["id"] in ids
    assert p2["id"] in ids

# Testes de segurança

def test_sql_injection_no_nome():
    payload = {
        "nome": "Produto'; DROP TABLE produtos; --",
        "descricao": "Tentativa de SQL Injection",
        "preco": 12.0,
        "categoria": "Lanche"
    }
    response = client.post("/produtos/", json=payload)
    assert response.status_code in (201, 422)

    # Se criado, remove para não interferir com os testes
    if response.status_code == 201:
        client.delete(f"/produtos/{response.json()['id']}")

def test_xss_na_descricao():
    response = client.post("/produtos/", json={
        "nome": "Produto XSS",
        "descricao": "<script>alert('XSS')</script>",
        "preco": 13.0,
        "categoria": "Lanche"
    })
    assert response.status_code == 201
    produto = response.json()
    assert "<script>" not in produto["descricao"]
    client.delete(f"/produtos/{produto['id']}")

def test_payload_exagerado():
    nome_grande = "X" * 10000
    response = client.post("/produtos/", json={
        "nome": nome_grande,
        "descricao": "Teste de carga",
        "preco": 9.99,
        "categoria": "Lanche"
    })
    assert response.status_code in (400, 413, 422)

def test_verifica_existencia_tabela_produtos():
    """
    Verifica se a tabela produtos ainda está funcional após todos os testes,
    incluindo simulações de SQL Injection. Se falhar com 500, pode indicar exclusão da tabela.
    """
    response = client.get("/produtos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_criar_produto_com_categoria():
    produto_data = {
        "nome": "X-Burguer",
        "descricao": "Hambúrguer com queijo",
        "preco": 25.90,
        "categoria": "Lanche"
    }
    response = client.post("/produtos/", json=produto_data)
    assert response.status_code == 201
    assert response.json()["categoria"] == "Lanche"
    client.delete(f"/produtos/{response.json()['id']}")

def test_criar_produto_com_categoria_invalida():
    produto_data = {
        "nome": "Suco Detox",
        "descricao": "Suco verde",
        "preco": 12.00,
        "categoria": "Doce"
    }
    response = client.post("/produtos/", json=produto_data)
    assert response.status_code == 422


# Novo teste para listar produtos por categoria usando a fixture produto_factory

def test_listar_produtos_por_categoria(produto_factory):
    produto = produto_factory(nome="Coca-Cola", descricao="Refrigerante", preco=8.0, categoria="Bebida")
    produto_id = produto["id"]

    response = client.get(f"/produtos/categoria/Bebida")
    assert response.status_code == 200
    produtos = response.json()
    assert any(p["id"] == produto_id for p in produtos)

# Teste para listar produtos por categoria sem resultados
def test_listar_produtos_por_categoria_sem_resultados():
    # Utiliza uma categoria válida sem produtos cadastrados durante o teste
    response = client.get("/produtos/categoria/Acompanhamento")
    assert response.status_code == 200
    assert response.json() == []