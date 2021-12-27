from db_conn import (
    my_Base, 
    engine, 
    table_names, 
)

from cl_db import (
    db_game,
    db_review,
    db_rating
)


if "game" not in table_names:
    my_Base.metadata.tables["game"].create(bind=engine, checkfirst=True)
    print("   'game' table added to database.")

if "review" not in table_names:
    my_Base.metadata.tables["review"].create(bind=engine, checkfirst=True)
    print("   'review' table added to database.")

if "rating" not in table_names:
    my_Base.metadata.tables["rating"].create(bind=engine, checkfirst=True)
    print("   'rating' table added to database.")
