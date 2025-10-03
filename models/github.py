from pydantic import BaseModel


__all__ = ["TreeModel", "FileModel", "RepoMetadata"]

class BaseFile(BaseModel):
    sha: str
    size: int
    url: str

class FileNode(BaseFile, BaseModel):
    path: str
    mode: str
    type: str

class FileModel(BaseFile, BaseModel):
    content: str
    encoding: str
    node_id: str


class TreeModel(BaseModel):
    sha: str
    url: str
    tree: list[FileNode]
    trucated: bool


class RepoMetadata(BaseModel):
    user: str
    name: str