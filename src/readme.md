Web Scraping Bundesliga
==============================

Make a Etl who scraping data from comments and stats of games in this season of Bundesliga

Links:
* <https://www.foxsports.com./soccer/schedule?competition=4&season=2019&round=1&week=0&group=0&sequence=1>

* <https://www.scoreboard.com/uk/football/germany/bundesliga/results/>

Project Organization
------------

    ├── README.md                    <- The top-level README for developers using this project.
    |
    ├── commentary_game              <- Scripts to containing data with commentaries of games
    │   ├── data_gathering.py    
    │   ├── data_preparation.py  
    │   └── pipeline.py          
    │
    ├── data                    
    │   ├── comments.csv             <- Csv with data save from scraping of comments.
    │   └── game_stats.csv           <- Csv with data save from scraping of game stats.
    |
    ├── docs                         <- Folder contais data dictionaries                 
    │   ├── comments_dictionary.md  
    │   └── game_stats_dictionary.md 
    |
    ├── commentary_game              <- Scripts to containing data with stats of games
    │   ├── data_gathering.py    
    │   ├── data_preparation.py  
    │   └── pipeline.py   
    |
    ├── params.py                    <- Class with param's used in code
    │
    └── pipeline.py                  <- The ETL (extract-transform-load) pipeline containing the sequence of nodes
         
--------