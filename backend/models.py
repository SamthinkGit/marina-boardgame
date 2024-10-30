import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.pydantic_v1 import BaseModel, Field
from typing import Literal
import traceback


class Response(BaseModel):
    answer: Literal["Sí", "No", "Irrelevante", "Especifica la pregunta"] = Field(
        description="Respuesta"
    )


class Calification(BaseModel):
    question: str = Field("Haz una pregunta generica sobre el contenido que falta. (e. g. ¿Por que ha pasado X?, "
                          "¿Donde ha ocurrido?, ¿Quien fue el responsable?). Si no falta nada devuelva Success.")
    calification: int = Field(
        description="Numero del 0 al 100 representando el porcentaje de la historia adivinada "
        "(siendo 0 nada y 100 todo)"
    )


os.environ["OPENAI_API_KEY"] = (
    "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"  # noqa
)


class StoryResponder:

    def __init__(self) -> None:
        llm = ChatOpenAI(model="gpt-4o-mini").with_structured_output(Response)
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    A partir de ahora vas a responder preguntas sobre una historia que se te va a proveer.
                    Para cada pregunta, solo puedes reponder con "Si", "No", "Irrelevante" o "Especifica
                    la pregunta"
                    La historia sobre la que vas a obtener información es la siguiente:
                    {story}
                    """,
                ),
                ("human", "{question}"),
            ]
        )
        self.chain = prompt | llm

    def query(self, question: str, story: str) -> str:
        try:
            return self.chain.invoke(
                input={"story": story, "question": question}
            ).answer
        except Exception:
            return (
                "Ha habido un error al generar la respuesta. Inténtalo de nuevo.\n Error:"
                + traceback.format_exc()
            )


class Calificator:

    def __init__(self) -> None:
        llm = ChatOpenAI(model="gpt-4o-mini").with_structured_output(Calification)
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    A partir de ahora vas a calificar si una breve descripcion que dara el usuario, contiene
                    los puntos clave sobre una historia que te voy a dar. Asi pues, si todos los puntos mas importantes
                    (independientemente de los detalles y palabras usadas) estan presentes en la respuesta del usuario,
                    le daras la maxima puntuacion, mientras que si dice cosas incorrectas o faltan puntos clave de 
                    la historia devolveras una calificación baja.

                    La historia es la siguiente:
                    ```
                    {story}
                    ```
                    """,
                ),
                ("human", "{proposal}"),
            ]
        )
        self.chain = prompt | llm

    def query(self, proposal: str, story: str) -> Calification:
        try:
            response = self.chain.invoke(
                input={"story": story, "proposal": proposal}
            )
            return response
        except Exception:
            return (
                "Ha habido un error al generar la respuesta. Inténtalo de nuevo.\n Error:"
                + traceback.format_exc()
            )


if __name__ == "__main__":
    from exercises import STORIES

    story = STORIES[0]
    #    sr = StoryResponder()
    #    while True:
    #        question = input("Input: ")
    #        print(f"AI: {sr.query(question=question, story=story)}")
    calificator = Calificator()
    while True:
        proposal = input("Solution: ")
        response = calificator.query(proposal=proposal, story=story)
        print(f"AI: {response.calification}: {response.question}")
