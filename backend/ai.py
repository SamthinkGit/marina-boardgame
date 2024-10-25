from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_openai import ChatOpenAI

app = FastAPI()

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Permite solicitudes desde cualquier origen. Cambia esto por el dominio específico en producción
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los encabezados
)


class RequestBody(BaseModel):
    input: str


@app.post("/generate_response/")
async def generate_response(request: RequestBody):
    llm = ChatOpenAI()
    response = llm.invoke(request.input)
    return {"response": response.content}
