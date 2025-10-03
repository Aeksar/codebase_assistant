from langchain_core.documents import Document
from base64 import b64decode
import requests

from config import cfg, logger


class GitHubLoader:
    def __init__(self, repo_url: str):
        self.headers = {"Authorization": f"token {cfg.GITHUB_API_KEY}"}
        user, repo = self.get_repo_metadata(repo_url)
        self.api_url = f"https://api.github.com/repos/{user}/{repo}/git/trees/main?recursive=100"

    @staticmethod
    def decode(data: str):
        decoded_bytes = b64decode(data)
        decoded_text = decoded_bytes.decode('utf-8')
        logger.debug(decoded_text[:200] + "\n..." if len(decoded_text) > 200 else decoded_text)
        return decoded_text

    @staticmethod
    def get_repo_metadata(url: str):
        user, repo = url.removeprefix("https://github.com/").split("/")
        return user, repo

    def _get_files_data(self, url: str):
        logger.debug(f"Start get urls from {url}")
        files_url = []
        response = requests.get(url, headers=self.headers)
        data = response.json()
        tree = data["tree"]
        for node in tree:
            if node["type"] == "blob":
                files_url.append(node["url"])
                # extensions.append(node["path"].split(".")[-1])

        return files_url

    def _get_file_content(self, url: str):
        try:
            logger.debug("Start get content for", url)
            response = requests.get(url, headers=self.headers)
            data = response.json()
            encoded_content = data["content"]
            if encoded_content:
                content = self._decode(encoded_content)
                return content
        except Exception as e:
            logger.error(f"Error getting content for {url}: {e}")
            return


    def load(self, ) -> list[str]:
        urls = self._get_files_data(self.api_url)
        all_data = []

        for url in urls:
            data = self._get_file_content(url)
            if data:
                all_data.append(data)
        
        return all_data
    

def get_loader(repo_url: str):
    return GitHubLoader(repo_url)