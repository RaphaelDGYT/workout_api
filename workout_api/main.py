from fastapi_pagination import Page, add_pagination, paginate
from requests import session
from fastapi import FastAPI, Query
from workout_api.atleta.schemas import Atleta
from workout_api.contrib.schemas import BaseSchema
from workout_api.routers import api_router

app = FastAPI(title='WorkoutApi')
app.include_router(api_router)

@app.get("/atletas")
def get_atletas(nome: str = Query(None), cpf: str = Query(None)):
    query = session.query(Atleta)
    if nome:
        query = query.filter(Atleta.nome.ilike(f"%{nome}%"))
    if cpf:
        query = query.filter(Atleta.cpf == cpf)
    return query.all()

@app.get("/atletas")
def get_all_atletas():
    atletas = session.query(
        Atleta.nome,
        Atleta.centro_treinamento,
        Atleta.categoria
    ).all()
    return atletas

@app.post("/atletas")
def create_atleta(atleta: Atleta(BaseSchema)): 
    try:
        new_atleta = Atleta(**atleta.dict())
        session.add(new_atleta)
        session.commit()
        return new_atleta
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=303,
            detail=f"Já existe um atleta cadastrado com o cpf: {atleta.cpf}"
        )
@app.get("/atletas", response_model=Page[Atleta])
def get_paginated_atletas():
    atletas = session.query(Atleta).all()
    return paginate(atletas)

add_pagination(app)
