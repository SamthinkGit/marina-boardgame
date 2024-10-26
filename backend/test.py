from exercises import STORIES
from models import StoryResponder

if __name__ == "__main__":
    sr = StoryResponder(STORIES[1])
    while True:
        question = input("Input: ")
        print(f"AI: {sr.query(question)}")
