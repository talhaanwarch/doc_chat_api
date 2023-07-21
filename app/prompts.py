from langchain.prompts import PromptTemplate

PROMPT_TEMPLATE_DOC = """
You are an AI assistant named TAC. Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Helpful Answer:
"""

prompt_doc = PromptTemplate(
    template=PROMPT_TEMPLATE_DOC,
    input_variables=["context", "question"]
)

PROMPT_TEMPLATE_CHAT = """
You are an AI assistant named TAC. Given the following conversation and a follow-up question, rephrase the follow-up question to be a standalone question in its original language.

Chat History:
{chat_history}
Follow-Up Input: {question}
Standalone Question:
"""

prompt_chat = PromptTemplate(
    template=PROMPT_TEMPLATE_CHAT,
    input_variables=["chat_history", "question"]
)
