from lib_compute_ranking import compute_our_rating
from lib_charts import plot_charts

import add_tables
import populate_tables
compute_our_rating(m_percentile=10)
compute_our_rating(m_percentile=50)
compute_our_rating(m_percentile=80)
plot_charts()
