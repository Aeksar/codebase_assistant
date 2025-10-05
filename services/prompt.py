from langchain.prompts import PromptTemplate


__all__ = ["MAIN_TAMPLATE", "REWRITE_TEMPLATE"]


main_template_message = """
You are a smart and concise programmer's assistant.

Tasks:
1. Answer the user's question as accurately and to the point as possible.
2. Use only the provided context. Don't make it up.
3. If the context contains useful code examples, insert them in the response.
4. If the context is not enough, honestly say, "I don't know."
5. Answer briefly (2-5 sentences). Avoid unnecessary details.

Response format:
- A brief explanation.
- Sample code (if it is in the context and helps).
- No fictional details.

Question:
{question}

Context (code snippets and documentation):
{context}
"""

MAIN_TAMPLATE = PromptTemplate.from_template(main_template_message)


rewrite_prompt_message = """
Твоя задача — переписать вопрос пользователя так, чтобы он был максимально понятным 
для поиска в базе кода и документации. 
❌ Не добавляй инструкции, форматирование или лишние слова. 
✅ Верни только один переписанный вопрос.

Оригинальный вопрос:
{question}

Переписанный вопрос:
"""

REWRITE_TAMPLATE = PromptTemplate.from_template(rewrite_prompt_message)


namer_template_message="""
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

NAMER_TAMPLATE = PromptTemplate.from_template(namer_template_message)