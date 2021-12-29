from db_conn import engine
import pandas as pd

def lib_read_csv_file_bgg():
    file_name = "bgg.csv"
    data = pd.read_csv(file_name, sep=',',na_values=pd.NA)
    df = pd.DataFrame(data, columns = ['game','title','rating'])
    df = df.rename(columns= {'game': 'id', 'rating': 'vote'})
    df.dropna(how='any', inplace=True)  # escludiamo le reviews dove 'vote' è vuoto
    v_columns = ['id', 'title', 'vote']
    df = df.reset_index()[v_columns]
    return df

DF = lib_read_csv_file_bgg()

df_unique = DF[['id','title']].drop_duplicates()
db_game_records = engine.execute("SELECT COUNT(*) FROM game").fetchall()[0][0]

if db_game_records == 0: # 23,810
  df_unique.to_sql('game', engine, if_exists='append', index=False, chunksize=10000)

df_review = DF[['id', 'vote']]
df_review = df_review.rename(columns= {'id': 'id_game'})
df_review['id'] = df_review.index.values

db_review_records = engine.execute("SELECT COUNT(*) FROM review").fetchall()[0][0]
if db_review_records == 0: # 706,813
  df_review.to_sql('review', engine, if_exists='append', index=False, chunksize=10000)
