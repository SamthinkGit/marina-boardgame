import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

os.environ["OPENAI_API_KEY"] = (
    "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"  # noqa
)


class StoryResponder:

    def __init__(self, instructions: str) -> None:
        llm = ChatOpenAI(model="gpt-4o-mini")
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=instructions),
                MessagesPlaceholder("history"),
                MessagesPlaceholder("input"),
            ]
        )
        self.history: list[BaseMessage] = []
        self.chain = prompt | llm

    def query(self, user_input: str) -> None:
        response = self.chain.invoke(
            input={"history": self.history, "input": [HumanMessage(content=user_input)]}
        )
        self.history.extend(
            [HumanMessage(content=user_input), AIMessage(content=response.content)]
        )
        return response.content


if __name__ == "__main__":
    sr = StoryResponder("From now on you must try to convince me to buy some pancakes.")
    while True:
        question = input("Input: ")
        print(f"AI: {sr.query(question)}")
