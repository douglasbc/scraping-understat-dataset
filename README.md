## UNDERSTAT - SHOTS DATASET



As many people interested in soccer analytics know, [Understat](https://understat.com/) is an amazing source of information. They provide Expected Goals (xG) stats for every shot taken in the top 5 leagues in Europe, as well as the Russian league.

After watching an awesome [tutorial](https://www.youtube.com/watch?v=IsR5FrjNmro) by [McKay Johns](https://www.youtube.com/channel/UCmqincDKps3syxvD4hbODSg) (great channel btw, loads of resources for beginners in soccer analytics), I decided to write some code to scrape all the shots data available at Understat. As a consequence I managed to generate this dataset, containing shots data of season 2014/2015, up to every match played in the 2021/2022 season, for the top division on the following countries:



England - EPL

Spain - La Liga

Germany - Bundesliga

Italy - Serie A

France - Ligue 1

Russia - RFPL



![](https://github.com/douglasbc/scraping-understat-dataset/blob/main/documentation/shots_data.png)

Besides shots data, I also managed to scrape very detailed season stats on every single player that took part in these matches.



![](https://github.com/douglasbc/scraping-understat-dataset/blob/main/documentation/players_data.png)



The datasets have been split into folders for every league, so every folder has 8 .csv files for shots data and 8 .csv files for players data (1 for every season since 14/15). The full dataset, with every league and season combined is also available at the "datasets" folder. I plan on updating the datasets everyday, but I also uploaded the Python code that generates and updates the datasets. Feel free to play with it and suggest improvements (hit me up on [twitter](https://twitter.com/douglasantifa)). To update it by yourself, just save "scraping" and "datasets" on the same folder, run Python with this folder as the current working directory and then run the update.py script, that is located in "scraping".

Most of the columns in the datasets are pretty straightforward, but some aren't. So I uploaded a couple of .pdf files in "documentation", explaining every column.