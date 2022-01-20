from db_conn import engine
import pandas as pd
import matplotlib.pyplot as plt


def plot_charts():
  v_mean = pd.read_sql("SELECT mean FROM rating WHERE m_percentile = 10 ORDER BY mean ASC", engine)['mean'].tolist()
  v_rating_p10 = pd.read_sql("SELECT rating FROM rating WHERE m_percentile = 10 ORDER BY rating ASC", engine)['rating'].tolist()
  v_rating_p50 = pd.read_sql("SELECT rating FROM rating WHERE m_percentile = 50 ORDER BY rating ASC", engine)['rating'].tolist()
  v_rating_p80 = pd.read_sql("SELECT rating FROM rating WHERE m_percentile = 80 ORDER BY rating ASC", engine)['rating'].tolist()

  n_bins = 20
  plt.hist(v_mean, bins=n_bins, label='Mean', histtype='step')
  plt.hist(v_rating_p10, bins=n_bins, label='Rating (p10)', histtype='step')
  plt.hist(v_rating_p50, bins=n_bins, label='Rating (p50)', histtype='step')
  plt.hist(v_rating_p80, bins=n_bins, label='Rating (p80)', histtype='step')

  plt.legend(loc="upper left")
  plt.show()
