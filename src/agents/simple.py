from typing import Optional
from typing_extensions import NotRequired
import random

from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage
#from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END

# llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.9)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.7,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

class Estado(MessagesState):
    nombre: NotRequired[str]
    edad: NotRequired[int]

def nodo_1(estado: Estado):
    nuevo_estado: dict = {}
    if estado.get("nombre") is None:
        nuevo_estado["nombre"] = "Juan"
    else:
        # estado["messages"].append(AIMessage(content="Hola, ¿cómo estás?"))
        nuevo_estado["edad"] = random.randint(18, 99)
    historial = estado.get("messages", [])
    mensaje_ai = llm.invoke(historial)
    nuevo_estado["messages"] = [mensaje_ai]
    return nuevo_estado


builder = StateGraph(Estado)
builder.add_node("Node", nodo_1)
builder.add_edge(START, "Node")
builder.add_edge("Node", END)

agente = builder.compile()

