# Note: chat_id's are stored as strings because the int is too large to be stored in a PSQL database.
import threading
from sqlalchemy import Column, String, Integer
from tg_bot.modules.sql import SESSION, BASE


class Connection(BASE):
    __tablename__ = "connection"
    user_id = Column(Integer, primary_key=True)
    chat_id = Column(String(14))

    def __init__(self, user_id, chat_id):
        self.user_id = user_id
        self.chat_id = str(chat_id) #Ensure String

Connection.__table__.create(checkfirst=True)
CONNECTION_INSERTION_LOCK = threading.RLock()

def connect(user_id, chat_id):
    with CONNECTION_INSERTION_LOCK:
        prev = SESSION.query(Connection).get((int(user_id)))
        if prev:
            SESSION.delete(prev)
        connect_to_chat = Connection(int(user_id), chat_id)
        SESSION.add(connect_to_chat)
        SESSION.commit()
        return True

def get_connected_chat(user_id):
    try:
        return SESSION.query(Connection).get((int(user_id)))
    finally:
        SESSION.close()


def disconnect(user_id):
    with CONNECTION_INSERTION_LOCK:
        disconnect = SESSION.query(Connection).get((int(user_id)))
        if disconnect:
            SESSION.delete(disconnect)
            SESSION.commit()
            return True

        else:
            SESSION.close()
            return False
