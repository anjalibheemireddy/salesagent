import pandas as pd
from langchain_core.messages import HumanMessage, AIMessage
from langchain.tools import tool
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# Load CSV inventory

inventory_df = pd.read_csv(r"C:\Users\theja\Desktop\Projects\salesagent_fastapi\products.csv")


# Memory

memory = []

def add_user_message(text: str):
    memory.append(HumanMessage(content=text))

def add_ai_message(text: str):
    memory.append(AIMessage(content=text))

def get_memory():
    return memory


cart = []


# Tools

@tool
def search_products_by_type(product_type: str = "") -> str:
    """Search products by type and return top 5 from CSV only."""
    results = inventory_df[inventory_df["product_type"].str.lower() == product_type.lower()]
    if results.empty:
        return f"No products found for type '{product_type}'."
    
    results = results.head(5)
    message = "Top products:\n"
    for idx, row in enumerate(results.itertuples(), start=1):
        avail = "Available" if row.available else "Out of stock"
        message += f"{idx}. {row.product_name} (${row.price}) - {avail}\n"
    return message


@tool
def check_inventory(product_name: str = "") -> bool:
    """Check if a product is in stock."""
    row = inventory_df[inventory_df["product_name"].str.lower() == product_name.lower()]
    if row.empty:
        return False
    return bool(row.iloc[0]["available"])

@tool
def add_to_cart(product_name: str = "") -> str:
    """Add product to cart if available."""
    global cart
    if not product_name:
        return "No product specified."
    
    if not check_inventory.run(product_name):
        return f"Product '{product_name}' is out of stock or does not exist."
    
    cart.append(product_name)
    return f"You added '{product_name}' to your cart. Would you like to checkout?"

@tool
def checkout(dummy_input: str = "") -> str:
    """Checkout all items in the cart."""
    global cart
    if not cart:
        return "Your cart is empty."
    
    purchased = ", ".join(cart)
    cart.clear()
    return f"Thank you for shopping! You purchased: {purchased}. Would you like anything else?"

#initialise llm
llm = ChatGroq(model="llama-3.1-8b-instant", api_key=GROQ_API_KEY)



def extract_product_name(user_input: str, llm_response: str) -> str:
    user_input_lower = user_input.lower()
    if "buy" in user_input_lower:
        return user_input_lower.split("buy")[-1].strip()
    if "add" in user_input_lower:
        return user_input_lower.split("add")[-1].replace("to cart", "").strip()
    return user_input.strip()
def map_number_to_product(product_type: str, choice: str) -> str:
    """
    Maps a number (like '3') to actual product name from CSV top 5.
    """
    results = inventory_df[inventory_df["product_type"].str.lower() == product_type.lower()].head(5)
    try:
        idx = int(choice.strip()) - 1
        if 0 <= idx < len(results):
            return results.iloc[idx]["product_name"]
    except:
        pass
    return choice  # fallback to the original input


#agent
def run_agent(user_input: str) -> str:
    add_user_message(user_input)
    active_cart = cart  
    system_prompt = f"""
You are a helpful sales assistant.
You have access to these tools:
- search_products_by_type(product_type)
- check_inventory(product_name)
- add_to_cart(product_name)
- checkout()

Conversation memory: {get_memory()}
Current cart: {active_cart}
"""
    response = llm.invoke([HumanMessage(content=system_prompt), HumanMessage(content=user_input)])
    add_ai_message(response.content)

    
    if "buy" in user_input.lower():
        parts = user_input.lower().split()
        for i, p in enumerate(parts):
            if p.isdigit():  
                if i + 1 < len(parts):
                    product_type = parts[i + 1]
                    product_name = map_number_to_product(product_type, p)
                    cart_response = add_to_cart.run(product_name)
                    add_ai_message(cart_response)
                    response.content += "\n" + cart_response
                    break
        else:  
            product_name = extract_product_name(user_input, response.content)
            cart_response = add_to_cart.run(product_name)
            add_ai_message(cart_response)
            response.content += "\n" + cart_response

    # Checkout
    if "checkout" in user_input.lower() or "proceed to checkout" in user_input.lower():
        checkout_response = checkout.run("")
        add_ai_message(checkout_response)
        response.content = checkout_response

    return response.content
