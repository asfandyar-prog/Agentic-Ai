from fastapi import FastAPI
from pydantic import BaseModel
from Agentic.agent import Agent

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_agent(request: QuestionRequest):
    agent = Agent()
    result = agent.run_agent(request.question)
    return {"answer": result}