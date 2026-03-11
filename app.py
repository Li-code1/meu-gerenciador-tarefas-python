from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# Inicialização da aplicação com metadados para o Swagger
app = FastAPI(
    title="Gerenciador de Tarefas V2",
    description="API para gerenciamento de tarefas com validação Pydantic e documentação de erros.",
    version="2.0.0"
)

# Passo 1: Modelo Pydantic para validação de dados
class Tarefa(BaseModel):
    nome: str
    descricao: str
    concluida: bool = False  # Padrão False caso não seja enviado

# Banco de dados em memória
tarefas_db: List[Tarefa] = []

# --- ROTAS DA API ---

@app.get("/tarefas", response_model=List[Tarefa], summary="Listar todas as tarefas")
def listar_tarefas():
    """Retorna a lista completa de tarefas cadastradas."""
    return tarefas_db

@app.post(
    "/tarefas", 
    status_code=201, 
    summary="Adicionar uma nova tarefa",
    responses={400: {"description": "Erro de validação: Tarefa já existente"}}
)
def adicionar_tarefa(tarefa: Tarefa):
    """Cria uma nova tarefa e a adiciona ao banco de dados."""
    if any(t.nome.lower() == tarefa.nome.lower() for t in tarefas_db):
        raise HTTPException(status_code=400, detail="Essa tarefa já existe.")
    
    tarefas_db.append(tarefa)
    return {"mensagem": "Tarefa adicionada com sucesso!", "tarefa": tarefa}

@app.put(
    "/tarefas/{nome_tarefa}", 
    summary="Marcar tarefa como concluída",
    responses={404: {"description": "Tarefa não encontrada"}}
)
def concluir_tarefa(nome_tarefa: str):
    """Localiza uma tarefa pelo nome e altera o status 'concluida' para True."""
    for tarefa in tarefas_db:
        if tarefa.nome.lower() == nome_tarefa.lower():
            tarefa.concluida = True
            return {"mensagem": f"Tarefa '{nome_tarefa}' marcada como concluída."}
    
    raise HTTPException(status_code=404, detail="Tarefa não encontrada.")

@app.delete(
    "/tarefas/{nome_tarefa}", 
    summary="Remover uma tarefa",
    responses={404: {"description": "Tarefa não encontrada"}}
)
def remover_tarefa(nome_tarefa: str):
    """Remove uma tarefa da lista com base no nome fornecido."""
    for index, tarefa in enumerate(tarefas_db):
        if tarefa.nome.lower() == nome_tarefa.lower():
            tarefas_db.pop(index)
            return {"mensagem": f"Tarefa '{nome_tarefa}' removida com sucesso."}
    
    raise HTTPException(status_code=404, detail="Tarefa não encontrada.")