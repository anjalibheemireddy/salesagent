from fastapi import FastAPI
from pydantic import BaseModel
from agent import run_agent, cart, checkout

app = FastAPI(title="Sales Agent Backend")

class UserMessage(BaseModel):
    message: str

@app.post("/chat")
def chat(msg: UserMessage):
    response = run_agent(msg.message)
    return {"user_message": msg.message, "assistant_response": response, "cart": cart}

@app.get("/cart")
def get_cart():
    return {"cart": cart}

@app.post("/checkout")
def do_checkout():
    checkout_response = checkout.run("")
    return {"checkout_message": checkout_response, "cart": cart}
