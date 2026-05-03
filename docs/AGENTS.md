** Google Gemini

# pip install -qU langchain "langchain[google-genai]"
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="google_genai:gemini-2.5-flash-lite",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)

** Open Router

# pip install -qU langchain langchain-openrouter
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="openrouter:anthropic/claude-sonnet-4-6",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)

** Groq

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

# Inicializar el modelo
# Tip: Llama-3.3-70b es excelente para agentes complejos
model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    # api_key="tu_api_key" (opcional si no usas variables de entorno)
)

# Prueba rápida
respuesta = model.invoke([HumanMessage(content="Hola, ¿cómo puedes ayudarme como agente?")])
print(respuesta.content)

