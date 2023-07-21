from sqlmodel import Field, SQLModel, create_engine
from typing import Optional


class QueryDB(SQLModel, table=True):
    """
    Database class to store query and answer in database
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    query: str
    answer: str
    session_id: str


sqlite_file_name = "sqlite.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=False, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
