from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage
import random

class Estado(MessagesState):
    nombre: str
    edad: int

def nodo_1(estado: Estado):
    nuevo_estado: dict = {}
    if estado.get("nombre") is None:
        nuevo_estado["nombre"] = "Juan"
    else:
        # estado["mensajes"].append(AIMessage(content="Hola, ¿cómo estás?"))
        nuevo_estado["edad"] = random.randint(18, 99)

from langgraph.graph import StateGraph, START, END

builder = StateGraph(Estado)
builder.add_node("Node", nodo_1)
builder.add_edge(START, "Node")
builder.add_edge("Node", END)

agente = builder.compile()

