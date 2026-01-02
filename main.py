from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo de validação
class Tarefa(BaseModel):
    titulo: str
    descricao: str = ""
    concluida: bool = False

# Armazenar tarefas
tarefas = []
next_id = 1

@app.get("/")
def home():
    return {"message": "API está funcionando"}

# GET - Listar todas as tarefas
@app.get("/tarefas")
def mostrar_tarefas():
    return {"tarefas": tarefas}

# GET - Obter tarefa específica
@app.get("/tarefas/{tarefa_id}")
def obter_tarefa(tarefa_id: int):
    for tarefa in tarefas:
        if tarefa["id"] == tarefa_id:
            return tarefa
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")

# POST - Adicionar nova tarefa
@app.post("/tarefas")
def adicionar_tarefa(tarefa: Tarefa):
    global next_id
    nova_tarefa = {
        "id": next_id,
        "titulo": tarefa.titulo,
        "descricao": tarefa.descricao,
        "concluida": tarefa.concluida
    }
    tarefas.append(nova_tarefa)
    next_id += 1
    return {"message": "Tarefa adicionada com sucesso", "tarefa": nova_tarefa}

# DELETE - Deletar tarefa
@app.delete("/tarefas/{tarefa_id}")
def deletar_tarefa(tarefa_id: int):
    for i, tarefa in enumerate(tarefas):
        if tarefa["id"] == tarefa_id:
            tarefas.pop(i)
            return {"message": "Tarefa deletada com sucesso"}
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")

# PUT - Atualizar tarefa
@app.put("/tarefas/{tarefa_id}")
def atualizar_tarefa(tarefa_id: int, tarefa_atualizada: Tarefa):
    for i, tarefa in enumerate(tarefas):
        if tarefa["id"] == tarefa_id:
            tarefas[i] = {
                "id": tarefa_id,
                "titulo": tarefa_atualizada.titulo,
                "descricao": tarefa_atualizada.descricao,
                "concluida": tarefa_atualizada.concluida
            }
            return {"message": "Tarefa atualizada com sucesso", "tarefa": tarefas[i]}
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")