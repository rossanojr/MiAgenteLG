from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

from langchain.chat_models import init_chat_model
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langgraph.graph import END, START, MessagesState, StateGraph
from pydantic import BaseModel, Field

CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "rag_docs")
CHROMA_PERSIST_DIR = Path(os.getenv("CHROMA_PERSIST_DIR", ".chroma"))
CHROMA_DOCS_PATH = Path(os.getenv("CHROMA_DOCS_PATH", "docs"))


def _load_local_texts(folder: Path) -> list[str]:
	if not folder.exists():
		return []

	texts: list[str] = []
	for path in folder.rglob("*"):
		if not path.is_file():
			continue
		if path.suffix.lower() not in {".md", ".mdx", ".txt"}:
			continue
		try:
			texts.append(path.read_text(encoding="utf-8"))
		except OSError:
			continue
	return texts


def _split_texts(texts: Iterable[str]) -> list[str]:
	splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
	chunks: list[str] = []
	for text in texts:
		chunks.extend(splitter.split_text(text))
	return chunks


def get_vectorstore() -> Chroma:
	embeddings = GoogleGenerativeAIEmbeddings(model="text-embedding-004")

	if CHROMA_PERSIST_DIR.exists() and any(CHROMA_PERSIST_DIR.iterdir()):
		return Chroma(
			collection_name=CHROMA_COLLECTION,
			embedding_function=embeddings,
			persist_directory=str(CHROMA_PERSIST_DIR),
		)

	texts = _split_texts(_load_local_texts(CHROMA_DOCS_PATH))
	if texts:
		return Chroma.from_texts(
			texts=texts,
			embedding=embeddings,
			collection_name=CHROMA_COLLECTION,
			persist_directory=str(CHROMA_PERSIST_DIR),
		)

	return Chroma(
		collection_name=CHROMA_COLLECTION,
		embedding_function=embeddings,
		persist_directory=str(CHROMA_PERSIST_DIR),
	)


llm = init_chat_model("google:gemini-1.5-flash", temperature=1)
retriever = get_vectorstore().as_retriever(search_kwargs={"k": 3})


class State(MessagesState):
	customer_name: str
	phone: str
	my_age: str


class ContactInfo(BaseModel):
	"""Contact information for a person."""

	name: str = Field(description="The name of the person")
	email: str = Field(description="The email address of the person")
	phone: str = Field(description="The phone number of the person")
	age: str = Field(description="The age of the person")


llm_with_structured_output = init_chat_model("google:gemini-1.5-flash", temperature=0)
llm_with_structured_output = llm_with_structured_output.with_structured_output(
	schema=ContactInfo
)


def extractor(state: State):
	history = state["messages"]
	customer_name = state.get("customer_name", None)
	new_state: State = {}
	if customer_name is None or len(history) >= 10:
		schema = llm_with_structured_output.invoke(history)
		new_state["customer_name"] = schema.name
		new_state["phone"] = schema.phone
		new_state["my_age"] = schema.age
	return new_state


def _retrieve_context(query: str) -> str:
	if hasattr(retriever, "invoke"):
		docs = retriever.invoke(query)
	else:
		docs = retriever.get_relevant_documents(query)
	return "\n\n".join(doc.page_content for doc in docs)


def conversation(state: State):
	new_state: State = {}
	history = state["messages"]
	last_message = history[-1]
	customer_name = state.get("customer_name", "John Doe")
	context = _retrieve_context(last_message.text)

	system_message = (
		"You are a helpful assistant that can answer questions about the customer "
		f"{customer_name}.\n"
		"Use the following context when relevant:\n"
		f"{context}"
	)
	ai_message = llm.invoke([("system", system_message), ("user", last_message.text)])
	new_state["messages"] = [ai_message]
	return new_state


builder = StateGraph(State)
builder.add_node("conversation", conversation)
builder.add_node("extractor", extractor)

builder.add_edge(START, "extractor")
builder.add_edge("extractor", "conversation")
builder.add_edge("conversation", END)

agent = builder.compile()
