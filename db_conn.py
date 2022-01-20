import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

my_Base = declarative_base()
table_names = []

from dotenv import load_dotenv
load_dotenv()


POSTGRES_URL = os.environ["DB_URL"]
engine = create_engine(f"postgresql+psycopg2://"+POSTGRES_URL, pool_pre_ping=True)

# try:
#   engine = create_engine(f"postgresql+psycopg2://"+POSTGRES_URL, pool_pre_ping=True)
#   conn = engine.connect()
#   print("Connected to the 'mds_il_migliore_di_tutti' database. Created session: 'session'.")
# except:
#   raise Exception("I am unable to connect to the 'datasets' database.")

'''
CREATE DATABASE mds_il_migliore_di_tutti
'''