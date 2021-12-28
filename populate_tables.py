
from db_conn import engine
import pandas as pd

def lib_read_csv_file_bgg():
    file_name = "bgg.csv"
    data = pd.read_csv(file_name, sep=',',na_values=None) 
    df = pd.DataFrame(data, columns = ['game','title','rating'])
    df = df.rename(columns= {'game': 'id', 'rating': 'vote'})
    df = df.where(pd.notnull(df), pd.NA)
    df.dropna(how='any', inplace=True)
    df = df.reset_index()
    return df

DF = lib_read_csv_file_bgg()

df_unique = DF[['id','title']].drop_duplicates()
if True:
  df_unique.to_sql('game', engine, if_exists='append', index=False, chunksize=10000)

df_review = DF[['id', 'vote']]
df_review = df_review.rename(columns= {'id': 'id_game'})
df_review['id'] = df_review.index.values

if True:
  df_review.to_sql('review', engine, if_exists='append', index=False, chunksize=10000)

