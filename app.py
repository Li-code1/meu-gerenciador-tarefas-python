from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Gerenciador de Tarefas V2")

class Tarefa(BaseModel):
    nome: str
    descricao: str
    concluida: bool = False  

tarefas_db: List[Tarefa] = []

@app.get("/tarefas", response_model=List[Tarefa])
def listar_tarefas():
    
    return tarefas_db

@app.post("/tarefas", status_code=201)
def adicionar_tarefa(tarefa: Tarefa):
    # Verificação simples para evitar nomes duplicados
    if any(t.nome.lower() == tarefa.nome.lower() for t in tarefas_db):
        raise HTTPException(status_code=400, detail="Essa tarefa já existe.")
    
    tarefas_db.append(tarefa)
    return {"mensagem": "Tarefa adicionada com sucesso!", "tarefa": tarefa}

@app.put("/tarefas/{nome_tarefa}")
def concluir_tarefa(nome_tarefa: str):
    for tarefa in tarefas_db:
        if tarefa.nome.lower() == nome_tarefa.lower():
            tarefa.concluida = True
            return {"mensagem": f"Tarefa '{nome_tarefa}' marcada como concluída."}
    
    raise HTTPException(status_code=404, detail="Tarefa não encontrada.")

@app.delete("/tarefas/{nome_tarefa}")
def remover_tarefa(nome_tarefa: str):
    for index, tarefa in enumerate(tarefas_db):
        if tarefa.nome.lower() == nome_tarefa.lower():
            tarefas_db.pop(index)
            return {"mensagem": f"Tarefa '{nome_tarefa}' removida com sucesso."}
    
    raise HTTPException(status_code=404, detail="Tarefa não encontrada.")