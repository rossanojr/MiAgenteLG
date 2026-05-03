### Configurar repositorio local para git
<!--  -->
```bash
git config --local user.name "Juan Rossano"
git config --local user.email "juanrossano@gmail.com"
```

# Vaciar cualquier helper previo (opcional, pero buena práctica si quieres aislarlo)
```bash
git config --local credential.helper ""
```

# Usar el manejador de credenciales de Windows (permite login web)
```bash
git config --local credential.helper manager
```

# Aislar la credencial guardada a la ruta específica de este repositorio
```bash
git config --local credential.useHttpPath true
```


```bash
pip cache purge
```

```bash
python -m pip install --upgrade pip
```


```bash
python -m pip install -U langgraph langchain langchain-openai "langchain[google-genai]"
```


```bash
python -m pip install langchain-groq
```


```bash
python -m pip install -qU langchain langchain-openrouter
```


```bash
python -m pip install -qU langchain "langchain[google-genai]"
```


```bash
python -m pip install -U langchain-groq
```

```bash
python -m pip install -qU langgraph langchain langchain-openai langchain-google-genai langchain-groq langchain-openrouter langchain-ollama
```



```bash
python -m pip install -U "langgraph-cli[inmem]"
python -m pip install "langgraph-cli[inmem]"
```


```bash
langgraph dev
```

```bash
python -m pip install langchain-ollama
```


### Env with UV

```sh
# Install uv

curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version

# deactivate the virtual environment
deactivate
rm -rf .venv

## init
uv init
uv venv

# add dependencies
uv add langgraph langchain langchain-google-genai
uv add langchain-groq langchain-openrouter langchain-ollama
uv add "fastapi[standard]"

# add dev dependencies
uv add "langgraph-cli[inmem]" --dev
uv add ipykernel --dev
uv add grandalf --dev

# run the agent
uv run langgraph dev

# install the project
uv pip install -e .
```

