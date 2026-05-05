# Chroma local (RAG con Gemini)

Esta guia usa Chroma en local para un RAG sencillo con Gemini.

## 1) Dependencias

```bash
python -m pip install -U langchain langchain-google-genai chromadb
```

## 2) Variables de entorno

```bash
# API key para Gemini
setx GOOGLE_API_KEY "TU_API_KEY"

# Opcional: carpeta para persistir Chroma
setx CHROMA_PERSIST_DIR ".chroma"

# Opcional: carpeta con documentos para indexar
setx CHROMA_DOCS_PATH "docs"
```

## 3) Como se crea el vector store

El archivo [src/agents/rag.py](src/agents/rag.py) hace lo siguiente:

- Lee archivos .md, .mdx y .txt desde CHROMA_DOCS_PATH.
- Parte los textos en chunks con solapamiento.
- Genera embeddings con Gemini (modelo `text-embedding-004`).
- Persiste el indice en CHROMA_PERSIST_DIR.

Si ya existe la carpeta de persistencia, reutiliza el indice.

## 4) Probar rapido

1) Coloca tus archivos en la carpeta indicada por CHROMA_DOCS_PATH.
2) Ejecuta tu agente como normalmente lo haces.
3) El primer run crea el indice. Los siguientes lo reutilizan.
