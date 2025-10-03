import requests

from config import cfg, logger
from models.github import FileModel, TreeModel, RepoMetadata
from utils.crypto import decode_b64

class GitHubLoader:
    def __init__(self, repo_url: str):
        self.headers = {"Authorization": f"token {cfg.GITHUB_API_KEY}"}
        repo_metadata = self.get_repo_metadata(repo_url)
        self.api_url = f"https://api.github.com/repos/{repo_metadata.user}/{repo_metadata.name}/git/trees/main?recursive=100"

    @staticmethod
    def get_repo_metadata(url: str):
        user, name = url.removeprefix("https://github.com/").split("/")
        return RepoMetadata(user=user, name=name)

    def _get_files_data(self, url: str):
        logger.debug(f"Start get urls from {url}")
        response = requests.get(url, headers=self.headers)
        data = TreeModel.model_validate_json(response.json())
        return (node for node in data.tree if node.type == "blob")
        # )) return [node for node in TreeModel.model_validate_json(requests.get(url, headers=self.headers).json()).tree if node.type == "blob"]

    def _get_file_content(self, url: str):
        try:
            logger.debug("Start get content for", url)
            response = requests.get(url, headers=self.headers)
            data = FileModel.model_validate_json(response.json())
            if data.content:
                decode_content = decode_b64(data.content)
                return decode_content
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