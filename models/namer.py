from pydantic import BaseModel, Field
from typing import Optional


class OutputModel(BaseModel):
    commit_name: Optional[str] = Field(description="Commit name", max_length=60, default=None)
    error: Optional[str] = Field(description="Field for error message if it been", default=None)
