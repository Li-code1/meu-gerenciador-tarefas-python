from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Gerenciador de Tarefas")

# Modelo de dados para a Tarefa
class Tarefa(BaseModel):
    nome: str
    descricao: str
    concluida: bool = False

# Banco de dados em memória (Lista de dicionários)
tarefas_db = []

# 1. Rota para Listar as Tarefas
@app.get("/tarefas", response_model=List[Tarefa])
def listar_tarefas():
    return tarefas_db

# 2. Rota para Adicionar uma Tarefa
@app.post("/tarefas", status_code=201)
def adicionar_tarefa(tarefa: Tarefa):
    # Verifica se já existe uma tarefa com esse nome para evitar duplicatas simples
    for t in tarefas_db:
        if t["nome"] == tarefa.nome:
            raise HTTPException(status_code=400, detail="Tarefa já existe.")
    
    nova_tarefa = tarefa.dict()
    tarefas_db.append(nova_tarefa)
    return {"mensagem": "Tarefa adicionada com sucesso!", "tarefa": nova_tarefa}

# 3. Rota para Marcar como Concluída
@app.put("/tarefas/{nome_tarefa}")
def concluir_tarefa(nome_tarefa: str):
    for tarefa in tarefas_db:
        if tarefa["nome"].lower() == nome_tarefa.lower():
            tarefa["concluida"] = True
            return {"mensagem": f"Tarefa '{nome_tarefa}' marcada como concluída."}
    
    raise HTTPException(status_code=404, detail="Tarefa não encontrada.")

# 4. Rota para Remover uma Tarefa
@app.delete("/tarefas/{nome_tarefa}")
def remover_tarefa(nome_tarefa: str):
    for index, tarefa in enumerate(tarefas_db):
        if tarefa["nome"].lower() == nome_tarefa.lower():
            tarefas_db.pop(index)
            return {"mensagem": f"Tarefa '{nome_tarefa}' removida com sucesso."}
    
    raise HTTPException(status_code=404, detail="Tarefa não encontrada.")