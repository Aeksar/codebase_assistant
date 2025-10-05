import subprocess
from langchain.output_parsers import PydanticOutputParser

from services import get_llm
from models.namer import OutputModel
from services.prompt import NAMER_TAMPLATE


def get_git_diff():
    return subprocess.check_output(["git", "diff", "HEAD"]).decode("utf-8")

def main():

    parser = PydanticOutputParser(pydantic_object=OutputModel)
    llm = get_llm()
    chain = NAMER_TAMPLATE | llm | parser

    diff = get_git_diff()
    # if not diff:
    #     raise Exception("Diff is empty")
    fromat_instruction = parser.get_format_instructions()
    res = chain.invoke({"context": diff, "format_instruction": fromat_instruction})
    return res


if __name__ == "__main__":
    res: OutputModel = main()
    print(res)