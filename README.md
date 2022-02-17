# MDS-il_migliore_di_tutti

__**Procedura**__

- Creare il database: "CREATE DATABASE mds_il_migliore_di_tutti"
- Creare/modificare il file .env, inserendo le credenziali per accedere al DB.
  In particolare, è necessario valorizzare correttamente la variabile DB_URL, la modifica della variabile ENV è invece facoltativa.
- Lanciare lo script "MAIN.py". Questo script:
  - crea le 3 tabelle (add_tables.py)
  - popola le tabelle leggendo i dati dal file "bgg.csv" (populate_tables.py)
  - calcola il 'nostro' rating, utilizzando sempre la stessa formula ma con 3 criteri diversi (in base alla scelta del percentile*). Calcola inoltre anche la media, mediana e stdev dei voti per ciascun gioco. (lib_compute_ranking/compute_our_rating.py)
  - crea il grafico con le 4 linee (lib_charts/plot_charts.py), che rappresentano la distribuzione di frequenza:
    - della media
    - del rating con percentile* 10
    - del rating con percentile* 50
    - del rating con percentile* 80


__**Spiegazione della formula**__

WR = (v / (v+**m**)) * R + (**m** / (v+**m**)) * C
- _R_ = media voti del gioco
- _v_ = n° di voti
- _m_ = spiegando con 2 esempi:
  - nel sito IMDB, 'm' è il n°minimo di voti richiesti per essere nella Top 250, ed attualmente sono 3000
  - se ho osservato 5 voti per un gioco, aggiunge **'m'** voti uguali alla media globale.
- _C_ = la media globale the mean vote across the whole report  6.42)

*Il percentile utilizzato per calcolare il rating si riferisce alla scelta del parametro **m**. Quindi, se scegliamo un percentile 10, andiamo a scegliere **m** uguale al numero di voti che ha il gioco che nel 10% inferiore di tutti i giochi. Il percentile è calcolato prendendo in considerazione tutti i voti di tutti i giochi. 
- Più scegliamo un percentile alto (quindi un **m** alto), più tutti i rating tenderanno alla media globale. 
- Se scegliamo **m** = 0 il randing sarà uguale alla media

Fonte: https://stats.stackexchange.com/questions/6418/rating-system-taking-account-of-number-of-votes
