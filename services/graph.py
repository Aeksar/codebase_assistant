from langgraph.graph import StateGraph, END
from langchain.schema import HumanMessage
from langchain.vectorstores.base import VectorStore
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import PromptTemplate

from models import AgentState

from .ranker import rerank
from .prompt import REWRITE_TAMPLATE

def build_graph(store: VectorStore, llm: BaseChatModel, prompt: PromptTemplate):
    retriever = store.as_retriever(k=20)
    

    def rewrite_node(state: AgentState):
        r_chain = REWRITE_TAMPLATE | llm
        resp = r_chain.invoke({"question": state["question"]})
        state["rewritten"] = resp.content
        print(resp.content)
        return state
    
    def retrieve_node(state: AgentState):
        docs = retriever.invoke(state["rewritten"])
        ranked = rerank(state["rewritten"], docs, top_k=10)
        state["context"] = "\n\n".join([d.page_content for d in ranked])
        try:
            print(docs[0].page_content)
        except IndexError:
            pass
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
    graph_builder.add_node("rewritten", rewrite_node)
    graph_builder.add_node("retrieve", retrieve_node)
    graph_builder.add_node("prompt", prompt_node)
    graph_builder.add_node("generate", generate_node)

    graph_builder.set_entry_point("rewritten")
    graph_builder.add_edge("rewritten", "retrieve")
    graph_builder.add_edge("retrieve", "prompt")
    graph_builder.add_edge("prompt", "generate")
    graph_builder.add_edge("generate", END)

    return graph_builder.compile()