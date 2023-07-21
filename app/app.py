from fastapi import FastAPI
from fastapi.responses import JSONResponse

from models import DocModel, QueryModel, DeleteSession
from database import create_db_and_tables
from vector_database import vector_database, db_conversation_chain
from data import load_n_split
from chat_session import ChatSession
from utils import count_tokens


app = FastAPI()
chat_session = ChatSession()


@app.on_event("startup")
def on_startup():
    """
    Event handler called when the application starts up.
    """
    create_db_and_tables()


@app.post("/doc_ingestion")
def add_documents(doc: DocModel):
    """
    Endpoint to add documents for ingestion.
    """
    docs = load_n_split(doc.dir_path)
    _ = vector_database(
        doc_text=docs,
        collection_name=doc.collection_name,
        embeddings_name=doc.embeddings_name
    )
    return JSONResponse(content={"message": "Documents added successfully"})


@app.post("/query")
def query_response(query: QueryModel):
    """
    Endpoint to process user queries.
    """
    # Check if there is a conversation history for the session
    stored_memory = chat_session.load_history(query.session_id)
    if len(stored_memory) == 0:
        stored_memory = None

    # Get conversation chain
    chain = db_conversation_chain(
        stored_memory=stored_memory,
        llm_name=query.llm_name,
        collection_name=query.collection_name
    )

    if query.llm_name == 'openai':
        result, cost = count_tokens(chain, query.text)
    else:
        result = chain(query.text)
        cost = None

    sources = list(set([doc.metadata['source'] for doc in
                        result['source_documents']]))
    answer = result['answer']
    chat_session.save_sess_db(query.session_id, query.text, answer)

    return {
        'answer': answer,
        "cost": cost,
        'source': sources
    }


@app.post("/delete")
def delete_session(session: DeleteSession):
    """
    Endpoint to delete a session from the database.
    """
    response = chat_session.delete_sess_db(session.session_id)
    return response
