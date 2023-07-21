from fastapi import HTTPException
from sqlmodel import Session, delete
from database import engine, QueryDB


class ChatSession:
    """
    Class for loading and saving chat session history to a database.
    """

    @staticmethod
    def load_history(session_id):
        """
        Loads a chat session from the database and returns a list
            of the conversations.

        :param session_id: ID of the chat session
        :return: List containing query and responses from the database
        """
        with Session(engine) as session:
            # Retrieve the conversation for the given session ID
            statement = f"SELECT * FROM querydb WHERE \
                session_id = '{session_id}'"
            # Execute the SQL statement to select all rows where
            # the session and client match
            results = session.exec(statement)
            # Create a list from the result set
            results = [i for i in results]
          
        # Create a list of conversation entries from the results
        result = [
            {'type': 'human', 'data': {'content': tup[1],
                                       'additional_kwargs': {},
                                       'example': False}}
            for tup in results
        ] + [
            {'type': 'ai', 'data': {'content': tup[2],
                                    'additional_kwargs': {},
                                    'example': False}}
            for tup in results
        ]

        return result

    @staticmethod
    def save_sess_db(session_id, query, answer):
        """
        Saves a chat session to the database.

        :param session_id: ID of the chat session
        :param query: Query string from the user
        :param answer: Response string from the AI
        """
        db = QueryDB(query=query, answer=answer, session_id=session_id)
        with Session(engine) as session:
            session.add(db)
            session.commit()
            session.refresh(db)

    @staticmethod
    def delete_sess_db(session_id):
        """
        Delete session from the database
        :param session_id: ID of the chat session
        """
        with Session(engine) as session:
            # Delete the specified session from the query database
            query = delete(QueryDB).where(QueryDB.session_id == session_id)
            result = session.execute(query)
            if result.rowcount == 0:
                raise HTTPException(status_code=404,
                                    detail=f"Session id {session_id} not found")
            session.commit()
            return {'message': f"Session id {session_id} Deleted"}
