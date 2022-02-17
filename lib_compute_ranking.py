import pandas as pd
import numpy as np
from db_conn import engine
from datetime import datetime, date

'''
- leggiamo i giochi dal DB
- li cicliamo
  - leggiamo le reviews
  - calcolo rating nostro
  - append nella tabella 'rating'
'''

def support_get_rating(C, m, R, v):
  # C: global_avg_vote, m: min_votes, R: Mean, v: Len
  ''' https://stats.stackexchange.com/questions/6418/rating-system-taking-account-of-number-of-votes
      weighted rating (WR) = (v / (v+m)) * R + (m / (v+m)) * C , where:
        - R = average for the movie (mean) = (Rating)
        - v = number of votes for the movie = (votes)
        - m = minimum number of votes required to be listed in the Top 250 (currently 3000)
              se ho osservato 5 voti, aggiungi ai 5 voti 'N' voti (es. 4 con percentile_10) uguali alla media generale (es. 6.42) ==> 10
        - C = the mean vote across the whole report (currently 6.42)
      Se: 
        - 'm' = 0 ---> tutti i ratings saranno uguali alla media individuale
        - 'm' = infinito ---> tutti i ratings saranno uguali a C (global_avg_vote)
  '''
  WR = (v / (v+m)) * R + (m / (v+m)) * C
  return round(WR,2)


def support_get_mean_median_stdev(v_votes):
  if len(v_votes) == 0:
    return None, None, None
  elif len(v_votes) == 1:
    return v_votes[0], v_votes[0], 0
  else:
    Mean = round(np.mean(v_votes),2)
    Median = round(np.median(v_votes),2)
    Std = round(np.std(v_votes),2)
    return Mean, Median, Std


def support_get_id_games_to_rank(min_votes):
  '''
    Estrae l'id dei giochi su cui va calcolato il ranking. Escludendo quelli su cui:
      - non è presente alcuna review (in realtà tutti hanno almeno una review)
      - è già calcolato, per quel 'min_votes'
  '''
  my_dict = {}
  s_id_games = set(pd.read_sql("SELECT id FROM game ORDER BY id ASC", engine)['id'].tolist())
  s_id_games_no_reviews = set(pd.read_sql("SELECT id_game, COUNT(*) FROM review GROUP BY id_game HAVING COUNT(*) = 0", engine)['id_game'].tolist())
  s_id_games = (s_id_games.difference(s_id_games_no_reviews))
  my_dict['len_games_all'] = len(s_id_games)

  s_id_games_rating_m = set(pd.read_sql("SELECT id_game FROM rating WHERE min_votes = " + str(min_votes), engine)['id_game'].tolist())  
  s_id_games = (s_id_games.difference(s_id_games_rating_m))
  
  my_dict['len_games_done'] = len(s_id_games_rating_m)
  my_dict['v_id_games_todo'] = sorted(list(s_id_games))
  return my_dict


def support_get_global_average_vote():
  query = "SELECT AVG(vote) FROM review"
  global_avg = pd.read_sql(query, engine).iloc[0][0] # same of => result = engine.execute(query).fetchall()[0][0]
  return round(global_avg, 2)


def compute_our_rating(m_percentile: int, delete_existing: bool = None, use_given_m = None):
  assert type(m_percentile) == int and m_percentile > 0 and m_percentile <= 100, "Error, bad 'm_percentile' choosen, choose an integer value between 0 and 100 (both included)."
  assert delete_existing in [None, True, False], "Error, bad 'delete_existing' choosen, choose a value in [None, True, False]"
  assert use_given_m == None or (type(use_given_m) == int and use_given_m >= 0), "Error, bad 'use_given_m' choosen, choose None or an integer number >= 0."

  time_start = datetime.now()
  if use_given_m == None: # calcolo 'm' come percentile del numero delle recensioni di tutti i giochi
    query = "SELECT COUNT(id) FROM review GROUP BY id_game ORDER BY COUNT(id) DESC"
    v_count = pd.read_sql(query, engine)['count'].tolist()
    min_votes = m = int(np.percentile(v_count, m_percentile))
  else: # oppure utilizzo un 'm' a piacere (numero intero > 0)
    min_votes = use_given_m
    m_percentile = None

  if delete_existing == True: # cancello i ratings, per quel 'min_votes'      un plus, non utilizzato
    query = "DELETE FROM rating WHERE min_votes = " + str(min_votes)
    engine.execute(query)

  my_dict = support_get_id_games_to_rank(min_votes) # lista degli id_game, su cui andiamo a calcolare il ranking
  # v_id_games_todo   len_games_all   len_games_done
  global_avg_vote = C = support_get_global_average_vote()

  query_insert = """INSERT INTO rating (id_game, min_votes, m_percentile, global_avg, count, mean, median, std, rating)
                  VALUES( %(id_game)s,%(min_votes)s,%(m_percentile)s,%(global_avg)s,%(count)s,%(mean)s,%(median)s,%(std)s,%(rating)s)"""

  for i, id_game in enumerate(my_dict['v_id_games_todo']):
    if i % 100 == 0:
      perc_done = round((( i + my_dict['len_games_done'] ) / my_dict['len_games_all'])*100,2)
      print(i, '/', my_dict['len_games_all'], ' | ', perc_done, '%   |   time delta:', str(datetime.now() - time_start))
    
    query = "SELECT vote FROM review WHERE id_game = " + str(id_game) + " ORDER BY vote DESC"
    v_votes = pd.read_sql(query, engine)['vote'].tolist()
    Mean, Median, Std = support_get_mean_median_stdev(v_votes)
    Len = len(v_votes)
    Rating = support_get_rating(global_avg_vote, min_votes, Mean, Len)
    params = {
      'id_game': id_game,
      'min_votes': min_votes,
      'm_percentile': m_percentile,
      'global_avg': global_avg_vote,
      'count': Len,
      'mean': Mean,
      'median': Median,
      'std': Std,
      'rating': Rating
    }
    engine.execute(query_insert, params)

