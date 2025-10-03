import subprocess

from langchain.prompts import PromptTemplate
from langchain_mistralai import ChatMistralAI
from langchain.output_parsers import PydanticOutputParser

from pydantic import BaseModel, Field
from typing import Optional

from config import cfg
from services import get_llm

class OutputModel(BaseModel):
    commit_name: Optional[str] = Field(description="Commit name", max_length=60, default=None)
    error: Optional[str] = Field(description="Field for error message if it been", default=None)


parser = PydanticOutputParser(pydantic_object=OutputModel)

llm = get_llm()

template="""
    You're a smart assistant in coming up with names for commits.
    Task: To come up with names for a commit based on its description in context
    Context:
    {context}

    Response format:
    {format_instruction}


    IMPORTANT:
        MAX LENGTH: 30
        IF CONTEXT IS EMPTY RETURN ERROR WHERE YOU SAY ABOUT IT
"""


prompt = PromptTemplate.from_template(template)

def get_git_diff():
    return subprocess.check_output(["git", "diff", "HEAD"]).decode("utf-8")



def main():
    chain = prompt | llm | parser

    diff = get_git_diff()
    # if not diff:
    #     raise Exception("Diff is empty")
    fromat_instruction = parser.get_format_instructions()
    res = chain.invoke({"context": diff, "format_instruction": fromat_instruction})
    return res


if __name__ == "__main__":
    res: OutputModel = main()
    print(res)