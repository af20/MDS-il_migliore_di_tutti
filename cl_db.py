
from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    Sequence,
    Float, 
    Date, 
    DateTime, 
    Boolean, 
    and_,
    ForeignKey
)

from db_conn import (
    my_Base, 
    engine, 
    session, 
    table_names, 
)



class db_game(my_Base):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False) 


class db_review(my_Base):
    __tablename__ = "review"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_game = Column(Integer, ForeignKey('game.id'))
    vote = Column(Integer, nullable=False) 

    "SELECT COUNT(id) FROM review WHERE id_game = 111111"

class db_rating(my_Base):
    __tablename__ = "rating"

    id_game = Column(Integer, ForeignKey('game.id'), primary_key=True)
    rating = Column(Integer)




'''
TABELLA 1
  'game'
    id = int
    title = str
  

'''