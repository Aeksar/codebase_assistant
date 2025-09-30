from langchain_mistralai import ChatMistralAI

from config import cfg
from services import load, get_store, build_graph, PROMPT
from services.loader import get_repo_metadata
from services.store import load_to_store


def main():
    repo_url = input("Enter repository url: ")
    user, repo = get_repo_metadata(repo_url)
    # data = load(repo_url)
    store = get_store(f"snippets_{user}_{repo}")
    # load_to_store(store, data)
    llm = ChatMistralAI(
        model=cfg.LLM_MODELS,
        temperature=0,
        mistral_api_key=cfg.MISTRAL_API_KEY
    )
    graph = build_graph(store, llm, PROMPT)
    while True:
        question = input("Question:")
        response = graph.invoke({"question": question})
        print(f"Answer: {response["answer"]}")
        print("-" * 20)


if __name__ == "__main__":
    main()
