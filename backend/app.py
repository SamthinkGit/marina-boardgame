from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.models import StoryResponder, Calificator, Response, Calification
from backend.exercises import STORIES

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


class QuestionBody(BaseModel):
    question: str
    story_id: int


class ProposalBody(BaseModel):
    proposal: str
    story_id: int


story = StoryResponder()
calificator = Calificator()


@app.post("/question/")
async def question(request: QuestionBody):
    try:
        context = STORIES[request.story_id]
    except KeyError:
        return {"response": "Invalid Key passed to backend."}
    response: Response = story.query(question=request.question, story=context)
    return {"response": response.answer}


@app.post("/response/")
async def response(request: ProposalBody):
    try:
        context = STORIES[request.story_id]
    except KeyError:
        return {"response": "Invalid Key passed to backend."}

    response: Calification = calificator.query(proposal=request.proposal, story=context)
    return {"response": f"{response.calification}: {response.question}"}
