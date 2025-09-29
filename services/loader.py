from langchain_core.documents import Document
from base64 import b64decode
import requests

from config import cfg, logger


__all__ = ["load"]

headers = {"Authorization": f"token {cfg.GITHIB_API_KEY}"}

def decode(data: str):
    decoded_bytes = b64decode(data)
    decoded_text = decoded_bytes.decode('utf-8')
    logger.debug(decoded_text[:200] + "\n..." if len(decoded_text) > 200 else decoded_text)
    return decoded_text

def get_repo_metadata(url: str):
    user, repo = url.removeprefix("https://github.com/").split("/")
    return user, repo

def get_files_data(url: str):
    logger.debug(f"Start get urls from {url}")
    files_url = []
    response = requests.get(url, headers=headers)
    data = response.json()
    tree = data["tree"]
    for node in tree:
        if node["type"] == "blob":
            files_url.append(node["url"])
            # extensions.append(node["path"].split(".")[-1])

    return files_url

def get_file_content(url: str):
    try:
        print("Start get content for", url)
        response = requests.get(url, headers=headers)
        data = response.json()
        encoded_content = data["content"]
        if encoded_content:
            content = decode(encoded_content)
            return content
    except Exception as e:
        logger.error(f"Error getting content for {url}: {e}")
        return


def load(repo_url: str) -> list[str]:
    user, repo = get_repo_metadata(repo_url)
    api_url = f"https://api.github.com/repos/{user}/{repo}/git/trees/main?recursive=100"
    urls = get_files_data(api_url)
    all_data = []

    for url in urls:
        data = get_file_content(url)
        if data:
            all_data.append(data)
    
    return all_data