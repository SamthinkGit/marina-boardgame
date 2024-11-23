import nest_asyncio
from pyngrok import ngrok
from colorama import Fore, Style
import uvicorn

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.models import StoryResponder, Calificator, Calification
from backend.exercises import STORIES
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

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


class QuestionBody(BaseModel):
    question: str
    story_id: int


class ProposalBody(BaseModel):
    proposal: str
    story_id: int


story = StoryResponder()
calificator = Calificator()

STATIC_DIR = "static"


@app.get("/{file_path:path}")
async def serve_static(file_path: str):
    file_full_path = os.path.join(STATIC_DIR, file_path)

    if file_path == "" or file_path == "/":
        file_full_path = os.path.join(STATIC_DIR, "index.html")

    # Verificar si el archivo existe en la carpeta static
    if not os.path.isfile(file_full_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_full_path)


@app.post("/question/")
async def question(request: QuestionBody):
    print(request.question)
    try:
        context = STORIES[request.story_id]
    except KeyError:
        return {"response": "Invalid Key passed to backend."}
    response = story.query(question=request.question, story=context)
    return {"response": response}


@app.post("/response/")
async def response(request: ProposalBody):
    try:
        context = STORIES[request.story_id]
    except KeyError:
        return {"response": "Invalid Key passed to backend."}

    response: Calification = calificator.query(proposal=request.proposal, story=context)
    return {"response": f"{response.calification}: {response.question}"}


ngrok_tunnel = ngrok.connect(8000)
print(f"{Fore.CYAN}{Style.BRIGHT}{['='*100]}")
print(f"{Fore.GREEN}{Style.BRIGHT}🔥 -> Public URL: {ngrok_tunnel.public_url}")
print(f"{Fore.CYAN}{Style.BRIGHT}{['='*100]}")

nest_asyncio.apply()
uvicorn.run(app, port=8000)
