from langgraph.graph import StateGraph, END
from langchain.schema import HumanMessage
from langchain.vectorstores.base import VectorStore
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import PromptTemplate

from models import AgentState


def build_graph(store: VectorStore, llm: BaseChatModel, prompt: PromptTemplate):
    retriever = store.as_retriever(k=15)
    def retrieve_node(state: AgentState):
        docs = retriever.invoke(state["question"])
        context = "\n\n".join([d.page_content for d in docs])
        state["context"] = context
        return state

    def prompt_node(state: AgentState):
        filled = prompt.format(
            question=state["question"],
            context=state["context"]
        )
        state["prompt"] = filled
        return state

    def generate_node(state: AgentState):
        resp = llm.invoke([HumanMessage(content=state["prompt"])])
        state["answer"] = resp.content
        return state

    graph_builder = StateGraph(AgentState)
    graph_builder.add_node("retrieve", retrieve_node)
    graph_builder.add_node("prompt", prompt_node)
    graph_builder.add_node("generate", generate_node)

    graph_builder.set_entry_point("retrieve")
    graph_builder.add_edge("retrieve", "prompt")
    graph_builder.add_edge("prompt", "generate")
    graph_builder.add_edge("generate", END)

    return graph_builder.compile()