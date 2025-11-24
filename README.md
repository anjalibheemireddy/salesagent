# 🛒 Sales Agent Chatbot

A conversational  sales assistant that helps users search, and purchase products from an inventory. This system uses **Streamlit** for the frontend, **FastAPI** as a backend API layer, and **LangChain with Groq LLM** for natural language understanding and tool integration.

---

## Prerequisites

- Python 3.11 or higher
- Pip for dependency management
- Groq API key (for LLM access)

---

## Installation

1. Clone the repository:
```bash
git clone <repository_url>
cd salesagent_fastapi
```

2. Create a virtual python environment in this repo
```bash
conda create -p venv python=3.12 -y
```
Any other method can also be used to create python environment.


3. Activate python environment
```bash
conda activate ./venv
```

5. Install dependencies using Poetry:
```bash
pip install -r requirements.txt
```

6. Create a `.env` file in the project root with your API keys:
```
GROQ_API_KEY=your_groq_key
```

## Usage

FastAPI Backend 
```bash
uvicorn main:app --reload
```

Run Streamlit Frontend
```bash
streamlit run app.py
```


## Interacting with the Chatbot

Ask for products:
"I want to buy a phone"
"Show me tablets under $300"

Add items to the cart:
"Add Xiaomi Redmi 9 to cart"

Checkout:
"checkout"

## Features

- Search products by type or price range

- Check inventory availability

- Add items to cart, Checkout items and clear cart

## Workflow

1. User Interaction

Type a query in Streamlit UI

The agent interprets intent using Groq LLM

2. Product Search

Searches CSV inventory for relevant products

Returns top 5 matching items

3. Cart Management

Adds selected items to the cart

Checks inventory before adding

4. Checkout

Clears cart after purchase

Conversation memory is retained for future queries

## License

This project is licensed under the terms included in the LICENSE file.

## Author

Anjali Bheemireddy (anjalinature156@gmail.com)
