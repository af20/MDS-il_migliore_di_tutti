# MDS-il_migliore_di_tutti

**Procedura**
- Creare un database, esempio "CREATE DATABASE mds_il_migliore_di_tutti"
- Lanciare lo script "flow.py". Questo script fa le seguenti cose:
  - crea le 3 tabelle
  - popola le tabelle leggendo il file "bgg.csv"
  - calcola il nostro rating con 3 criteri diversi (in base alla scelta percentile*) e la media
  - printa il grafico, 4 linee contenente la distribuzione di frequenza:
    - della media
    - rating con percentile* 10
    - rating con percentile* 50
    - rating con percentile* 80

**Spiegazione della formula**
https://stats.stackexchange.com/questions/6418/rating-system-taking-account-of-number-of-votes
WR = (v / (v+**m**)) * R + (**m** / (v+**m**)) * C
        - _R_ = media voti del gioco
        - _v_ = n° di voti
        - _m_ = spiegando con 2 esempi:
          - nel sito IMDB, 'm' è il n°minimo di voti richiesti per essere nella Top 250, ed attualmente sono 3000
          - se ho osservato 5 voti per un gioco, aggiunge **'m'** voti uguali alla media globale.
        - _C_ = la media globale the mean vote across the whole report  6.42)

*Il percentile utilizzato per calcolare il rating si riferisce alla scelta del parametro **m**. Quindi, se scegliamo un percentile 10, andiamo a scegliere **m** uguale al numero di voti che ha il gioco che nel 10% inferiore di tutti i giochi.
