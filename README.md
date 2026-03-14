# 🚀 Gerenciador de Tarefas Pro (V3) - FastAPI

Este projeto é uma API robusta para gerenciamento de tarefas (To-Do List), desenvolvida para o curso **Backend em Python da EBAC**. Nesta versão, a aplicação conta com segurança por autenticação, controle de fluxo de dados por paginação e filtros de ordenação.

---

## 🛠️ Tecnologias Utilizadas

* **Python**
* **FastAPI**: Framework web de alta performance e documentação automática.
* **Poetry**: Gerenciamento moderno de dependências e ambientes virtuais.
* **Pydantic**: Validação rigorosa de tipos e esquemas de dados.
* **HTTP Basic Auth**: Implementação de segurança para acesso aos endpoints.

---

## 📋 Funcionalidades Avançadas

* **Segurança**: Todos os endpoints são protegidos. Requer usuário e senha para acesso.
* **Paginação**: O endpoint de listagem permite controlar a quantidade de dados retornados (`page` e `size`).
* **Ordenação**: Suporte para ordenar as tarefas alfabeticamente por `nome` ou `descricao`.
* **Validação Automática**: Tratamento de erros **422** (dados inválidos), **401** (não autorizado) e **400** (parâmetros de busca incorretos).

---

## 🚀 Como Instalar e Rodar

1. **Clone o repositório:**
```bash
git clone https://github.com/Li-code1/meu-gerenciador-tarefas-python.git
cd meu-gerenciador-tarefas-python

```


2. **Instale as dependências com o Poetry:**
```bash
poetry install

```


3. **Inicie o servidor:**
```bash
poetry run uvicorn app:app --reload

```



---

## 🧪 Testando com Postman

### 🔑 Credenciais de Acesso

Para qualquer requisição, configure a aba **Authorization** no Postman:

* **Type:** Basic Auth
* **Username:** `admin`
* **Password:** `ebac123`

"⚠️ Nota de Segurança: As credenciais utilizadas neste projeto (admin/ebac123) são apenas para fins de teste e demonstração do desafio. Em um ambiente de produção, seriam utilizadas variáveis de ambiente (.env) e senhas criptografadas em banco de dados."

### 1. Criar uma Tarefa (POST)

* **URL:** `http://127.0.0.1:8000/tarefas`
* **Body (JSON):**
```json
{
  "nome": "Estudar Autenticação",
  "descricao": "Praticar Basic Auth no FastAPI",
  "concluida": false
}

```



### 2. Listar com Paginação e Ordenação (GET)

* **URL Exemplo:** `http://127.0.0.1:8000/tarefas?page=1&size=2&ordenar_por=nome`
* **Parâmetros:**
* `page`: Número da página (ex: 1).
* `size`: Itens por página (ex: 5).
* `ordenar_por`: Campo para ordem (`nome` ou `descricao`).



### 3. Concluir e Remover (PUT/DELETE)

* **URLs:** `http://127.0.0.1:8000/tarefas/{nome_da_tarefa}`

---

## 🧪 Evidências de Testes (Postman)

## 🧪 Evidências de Testes (Postman)

| Funcionalidade | Descrição | Print do Teste |
| :--- | :--- | :--- |
| **Autenticação** | Erro 401 sem credenciais | ![401](screenshots/auth_error.png) |
| **Página 1** | Listagem com `size=2` | ![Paginação](screenshots/paginacao.png) |
| **Ordenação** | Ordenado por `nome` | ![Ordenação](screenshots/ordenacao.png) |
| **Criação** | POST com sucesso (201) | ![POST](screenshots/post_sucesso.png) |
---

## 📖 Documentação Automática (Swagger)

Com o servidor rodando, acesse a documentação interativa para testar os filtros e a segurança:

* **Swagger UI:** [http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs)

---

Desenvolvido por **Liliane Lima** ✨


