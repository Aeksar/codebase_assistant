from config import cfg
from services import (
    get_loader, 
    get_store, 
    build_graph, 
    get_llm,
    PROMPT
    )
from services.store import load_to_store


def main():
    repo_url = input("Enter repository url: ")

    
    loader = get_loader(repo_url)
    user, repo = loader.get_repo_metadata(repo_url)
    store = get_store(f"snippets_{user}_{repo}")
    llm = get_llm()
    
    # data = load(repo_url)
    # load_to_store(store, data)

    graph = build_graph(store, llm, PROMPT)
    while True:
        question = input("Question:")
        response = graph.invoke({"question": question})
        print(f"Answer: {response["answer"]}")
        print("-" * 20)


if __name__ == "__main__":
    main()
