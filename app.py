from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import List, Optional, Annotated 
import secrets

app = FastAPI(
    title="Gerenciador de Tarefas Pro - V3",
    description="API com Autenticação, Paginação e Ordenação (SonarLint Optimized).",
    version="3.0.1"
)

security = HTTPBasic()

# --- Função de Autenticação ---
def autenticar(credentials: HTTPBasicCredentials = Depends(security)):
    usuario_correto = secrets.compare_digest(credentials.username, "admin")
    senha_correta = secrets.compare_digest(credentials.password, "ebac123")
    
    if not (usuario_correto and senha_correta):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas.",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

UserDep = Annotated[str, Depends(autenticar)]

class Tarefa(BaseModel):
    nome: str
    descricao: str
    concluida: bool = False

tarefas_db: List[Tarefa] = []

# --- ROTAS ---

@app.get(
    "/tarefas", 
    response_model=List[Tarefa],
    responses={400: {"description": "Parâmetros inválidos"}}
)
def listar_tarefas(
    usuario: UserDep,
    page: int = 1,
    size: int = 5,
    ordenar_por: Optional[str] = None
):
    if page < 1 or size < 1:
        raise HTTPException(status_code=400, detail="Página e tamanho devem ser > 0.")

    resultado = tarefas_db.copy()

    if ordenar_por:
        if ordenar_por not in ["nome", "descricao"]:
            raise HTTPException(status_code=400, detail="Campo inválido.")
        resultado.sort(key=lambda x: getattr(x, ordenar_por).lower())

    inicio = (page - 1) * size
    return resultado[inicio:inicio + size]

@app.post(
    "/tarefas", 
    status_code=201,
    responses={
        400: {"description": "Tarefa já existe"}, 
        401: {"description": "Não autorizado"}
    }
)
def adicionar_tarefa(tarefa: Tarefa, usuario: UserDep):
    if any(t.nome.lower() == tarefa.nome.lower() for t in tarefas_db):
        raise HTTPException(status_code=400, detail="Essa tarefa já existe.")
    
    tarefas_db.append(tarefa)
    return {"mensagem": f"Tarefa adicionada por {usuario}!"}

@app.put(
    "/tarefas/{nome_tarefa}",
    responses={
        404: {"description": "Não encontrada"},
        401: {"description": "Não autorizado"}
    }
)
def concluir_tarefa(nome_tarefa: str, usuario: UserDep): 
    for tarefa in tarefas_db:
        if tarefa.nome.lower() == nome_tarefa.lower():
            tarefa.concluida = True
            return {"mensagem": "Tarefa atualizada."}
    raise HTTPException(status_code=404, detail="Tarefa não encontrada.")

@app.delete(
    "/tarefas/{nome_tarefa}",
    responses={
        404: {"description": "Não encontrada"},
        401: {"description": "Não autorizado"}
    }
)
def remover_tarefa(nome_tarefa: str, usuario: UserDep): 
    for index, tarefa in enumerate(tarefas_db):
        if tarefa.nome.lower() == nome_tarefa.lower():
            tarefas_db.pop(index)
            return {"mensagem": "Tarefa removida."}
    raise HTTPException(status_code=404, detail="Tarefa não encontrada.")