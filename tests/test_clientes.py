import pytest
from app.infrastructure.db.database import SessionLocal
from app.models.cliente import Cliente as ClienteORM
from app.models.produto import Produto as ProdutoORM
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

@pytest.fixture(autouse=True)
def resetar_banco():
    session = SessionLocal()
    try:
        session.query(ProdutoORM).delete()
        session.query(ClienteORM).delete()
        session.commit()
    finally:
        session.close()

@pytest.fixture
def cliente_factory():
    clientes_criados = []
    emails_usados = set()
    cpfs_usados = set()

    def criar_cliente(nome="Cliente Teste", email=None, telefone="11999999999", cpf=None):
        if email is None or email in emails_usados:
            email = f"teste_{uuid.uuid4().hex[:8]}@email.com"
        if not cpf or cpf in cpfs_usados:
            cpf = f"{uuid.uuid4().int % 10**11:011d}"

        emails_usados.add(email)
        cpfs_usados.add(cpf)

        response = client.post("/clientes", json={
            "nome": nome,
            "email": email,
            "telefone": telefone,
            "cpf": cpf
        })
        assert response.status_code == 201, f"Erro ao criar cliente: {response.status_code} - {response.text}"
        cliente = response.json()
        clientes_criados.append(cliente["id"])
        return cliente

    yield criar_cliente

    for cliente_id in clientes_criados:
        client.delete(f"/clientes/{cliente_id}")

def test_criar_cliente(cliente_factory):
    cpf = f"{uuid.uuid4().int % 10**11:011d}"
    cliente = cliente_factory(nome="João Silva", email="joao@example.com", telefone="11999998888", cpf=cpf)
    assert cliente["nome"] == "João Silva"
    assert cliente["email"] == "joao@example.com"
    assert cliente["telefone"] == "11999998888"
    assert cliente["cpf"] == cpf
    assert "id" in cliente

def test_listar_clientes():
    response = client.get("/clientes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_buscar_cliente_por_id(cliente_factory):
    cpf = f"{uuid.uuid4().int % 10**11:011d}"
    cliente = cliente_factory(nome="Maria Oliveira", email="maria@example.com", telefone="11912345678", cpf=cpf)
    response = client.get(f"/clientes/{cliente['id']}")
    assert response.status_code == 200
    assert response.json()["email"] == "maria@example.com"

def test_atualizar_cliente(cliente_factory):
    cpf = f"{uuid.uuid4().int % 10**11:011d}"
    cliente = cliente_factory(nome="Carlos Dias", email="carlos@example.com", telefone="11987654321", cpf=cpf)
    response = client.put(f"/clientes/{cliente['id']}", json={
        "nome": "Carlos D.",
        "email": "carlosd@example.com",
        "telefone": "11876543210",
        "cpf": cpf
    })

    assert response.status_code == 200
    assert response.json()["nome"] == "Carlos D."

def test_deletar_cliente(cliente_factory):
    cpf = f"{uuid.uuid4().int % 10**11:011d}"
    cliente = cliente_factory(nome="Ana Souza", email="ana@example.com", telefone="11911112222", cpf=cpf)

    delete_response = client.delete(f"/clientes/{cliente['id']}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/clientes/{cliente['id']}")
    assert get_response.status_code == 404

def test_campos_obrigatorios():
    response = client.post("/clientes", json={})
    assert response.status_code == 422

def test_criar_cliente_com_email_invalido():
    response = client.post("/clientes", json={
        "nome": "Fulano Teste",
        "email": "email-invalido",
        "telefone": "11999998888",
        "cpf": "12345678901"
    })
    assert response.status_code == 422
    assert "email" in str(response.json())

@pytest.mark.parametrize("telefone_invalido", [
    "12345",
    "abcdefghij",
    "119999988881",
    "(11)99999-8888",
    ""
])
def test_criar_cliente_com_telefone_invalido(telefone_invalido):
    cpf = f"{uuid.uuid4().int % 10**11:011d}"
    response = client.post("/clientes", json={
        "nome": "Teste",
        "email": f"teste_{uuid.uuid4().hex[:8]}@email.com",
        "telefone": telefone_invalido,
        "cpf": cpf
    })
    assert response.status_code == 422
    assert "telefone" in str(response.json())

def test_criar_cliente_com_telefone_valido(cliente_factory):
    cpf = f"{uuid.uuid4().int % 10**11:011d}"
    cliente = cliente_factory(telefone="11999998888", cpf=cpf)
    assert cliente["telefone"] == "11999998888"

def test_criar_cliente_com_telefone_com_caracteres_especiais():
    response = client.post("/clientes", json={
        "nome": "Usuário Malicioso",
        "email": f"malicioso_{uuid.uuid4().hex[:8]}@email.com",
        "telefone": "+55(11)99999-8888",
        "cpf": "12345678901"
    })
    assert response.status_code == 422
    assert "telefone" in str(response.json())

def test_criar_cliente_com_nome_script():
    cpf = f"{uuid.uuid4().int % 10**11:011d}"
    response = client.post("/clientes", json={
        "nome": "<script>alert('xss')</script>",
        "email": "teste@seguro.com",
        "telefone": "11999998888",
        "cpf": cpf
    })
    assert response.status_code == 422

def test_criar_cliente_com_email_sql_injection():
    response = client.post("/clientes", json={
        "nome": "SQL Tester",
        "email": f"teste_{uuid.uuid4().hex[:8]}@'; DROP TABLE clientes;--",
        "telefone": "11999998888",
        "cpf": "12345678901"
    })
    assert response.status_code == 422

def test_criar_cliente_email_duplicado(cliente_factory):
    email = f"duplicado_{uuid.uuid4().hex[:8]}@email.com"
    cliente_factory(email=email)
    cpf_unico = f"{uuid.uuid4().int % 10**11:011d}"
    response = client.post("/clientes", json={
        "nome": "Outro Nome",
        "email": email,
        "telefone": "11988887777",
        "cpf": cpf_unico
    })
    assert response.status_code == 409

def test_criar_cliente_com_nome_extremo():
    nome_longo = "A" * 10000
    response = client.post("/clientes", json={
        "nome": nome_longo,
        "email": f"teste_{uuid.uuid4().hex[:8]}@email.com",
        "telefone": "11999998888",
        "cpf": "12345678901"
    })
    assert response.status_code == 422

def test_criar_cliente_com_tipo_errado():
    response = client.post("/clientes", json={
        "nome": 123456,
        "email": f"teste_{uuid.uuid4().hex[:8]}@email.com",
        "telefone": "11999998888",
        "cpf": "12345678901"
    })
    assert response.status_code == 422