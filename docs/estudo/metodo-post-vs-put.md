📦 O que é HTTP? (Rápido contexto)

HTTP (HyperText Transfer Protocol) é o protocolo de comunicação da web.
Toda vez que você faz uma requisição para uma API, você está enviando uma mensagem HTTP, que tem:
	•	Um verbo (método HTTP): como POST, GET, PUT, DELETE
	•	Um endpoint (URL)
	•	Cabeçalhos e, às vezes, um corpo (body), contendo dados.

Os métodos HTTP indicam qual é a intenção da requisição.

⸻

🧩 Diferenças conceituais entre POST e PUT

📌 POST — Criar um novo recurso
	•	Significa: “Crie um novo recurso subordinado ao endpoint indicado.”
	•	Usa quando não existe ainda.
	•	A aplicação que recebe o POST geralmente cria:
	•	Uma nova entrada no banco de dados.
	•	Gera um ID único para o novo recurso.
	•	Retorna o recurso criado ou um status 201 Created.

Exemplo prático no seu sistema:

POST /produtos
{
  "nome": "X-Burger",
  "descricao": "Hamburguer artesanal com cheddar",
  "preco": 29.90
}

🔍 Por trás dos panos:
	•	O FastAPI pega o JSON recebido.
	•	Usa o Schema Pydantic para validar.
	•	Passa os dados para o service.
	•	O service cria uma nova instância do model Produto.
	•	O SQLAlchemy gera um comando INSERT no banco.
	•	Banco de dados cria um novo registro e gera um id.

⸻

📌 PUT — Atualizar ou substituir um recurso existente
	•	Significa: “Coloque este recurso no lugar do atual.”
	•	Usa quando você já sabe qual é o recurso que está alterando.
	•	Espera-se que o cliente envie todos os dados do recurso, não só as mudanças parciais.
	•	Normalmente, o resultado esperado é: 200 OK ou 204 No Content.

Exemplo prático:

PUT /produtos/1
{
  "nome": "X-Burger Premium",
  "descricao": "Agora com molho especial",
  "preco": 34.90
}

🔍 Por trás dos panos:
	•	FastAPI recebe a requisição e valida com o Schema Pydantic.
	•	Passa para o service.
	•	O service busca o produto existente pelo ID.
	•	Atualiza todos os campos informados.
	•	O SQLAlchemy gera um comando UPDATE no banco de dados.
	•	Banco atualiza os dados do produto no registro correspondente.

⸻

📖 Importante: diferença de “Intenção”

Comparativo	POST	PUT
Objetivo	Criar novo recurso	Atualizar ou substituir recurso existente
Necessidade de ID?	Não, o servidor geralmente gera	Sim, você precisa indicar qual recurso
Resultado esperado	Novo recurso criado (201 Created)	Recurso existente atualizado (200 OK ou 204 No Content)
Operação no banco	INSERT INTO produtos ...	UPDATE produtos SET ... WHERE id = ...
Uso em APIs REST	Criar entradas	Atualizar entradas



⸻

🧩 O que acontece em baixo nível:
	1.	Requisição é enviada com o método HTTP (POST ou PUT).
	2.	A API recebe o método e decide qual rota e qual lógica interna executar.
	3.	Os dados são validados com o schema Pydantic.
	4.	O service é chamado para executar a ação apropriada.
	5.	O ORM (SQLAlchemy) transforma a ação em comando SQL (INSERT ou UPDATE).
	6.	O banco de dados executa e retorna o resultado para a API.
	7.	A API responde para o cliente com o status apropriado e, opcionalmente, os dados.

⸻

✅ Conclusão:

📌 POST → Você está dizendo para o servidor: “Crie isso para mim!”
📌 PUT → Você está dizendo: “Pegue estes dados e atualize esse recurso que já existe!”

E o importante: por trás dos panos, o que muda não é só a forma de chamar, mas a intenção e a operação real no banco de dados.