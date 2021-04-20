## UNDERSTAT - SHOTS DATASET



As many people interested in soccer analytics know, [Understat](https://understat.com/) is an amazing source of information. They provide Expected Goals (xG) stats for every shot taken in the top 5 leagues in Europe, as well as the Russian league.

After watching an awesome [tutorial](https://www.youtube.com/watch?v=IsR5FrjNmro) by [McKay Johns](https://www.youtube.com/channel/UCmqincDKps3syxvD4hbODSg) (great channel btw, loads of resources for beginners in soccer analytics), I decided to write some code to scrape all the shots data available at Understat. As a consequence I managed to generate this dataset, containing shots data of season 2014/2015, up to every match played in the 2020/2021 season, for the top division on the following countries:



England - EPL

Spain - La Liga

Germany - Bundesliga

Italy - Serie A

France - Ligue 1

Russia - RFPL



![](/home/douglas/Desktop/shots_data.png)



Besides shots data, I also managed to scrape very detailed season stats on every single player that took part in these matches.



![](/home/douglas/Desktop/players_data.png)



The datasets have been split into folders for every league, so every folder has 7 .csv files for shots data and 7 .csv files for players data (1 for every season since 14/15).  I plan on updating the datasets pretty often, at least 3 or 4 times a week, but I will also upload the Python code that generates and updates the datasets. Feel free to play with it and suggest improvements (hit me up on [twitter](https://twitter.com/douglasantifa)).



### Shots columns:

**id -** Unique identifier number for every shot

**minute -** Time of the shot

**result -** Goal, MissedShots, SavedShot, BlockedShot, ShotOnPost, OwnGoal

**X -** X coordinate of the shot, between 0 and 1

**Y -** Y coordinate of the shot, between 0 and 1

**xG -** Number Between 0 and 1, describing the Expected Goals of the shot, calculated by the Understat xG model

**player -** Player that made the shot

**h_a -** Home/away team

**player_id -** Unique identifier number for every player

**situation -** OpenPlay, FromCorner, SetPiece, DirectFreekick, Penalty

**season -** The year when the season started, so season 2014/2015 is 2014, season 2015/2016 is 2015

**shotType -** RightFoot, LeftFoot, Head, OtherBodyPart

**match_id -** Unique identifier number for every match

**h_team -** Home team

**a_team -** Away team

**h_goals -** Goals scored by home team

**a_goals -** Goals scored by away team

**date -** Date of the match

**player_assisted -** Player that assisted the shot

**lastAction -** Last action before the shot (None, Pass, Cross, Aerial, Standard, TakeOn, Rebound...) 



### Players columns:

**id -** Unique identifier number for every player

**player_name -** Player name

**games -** Total amount of games played

**time -** Total amount of minutes played

**goals -** Total amount of goals scored

**xG -** Sum of Expected Goals of every shot, calculated by the Understat xG model

**assists -** Total amount of assists

**xA -** Sum of Expected Goals of shots from a player's key passes

**shots -** Total amount of shots

**key_passes -** Total amount of key passes

**yellow_cards -** Total amount of yellow cards

**red_cards -** Total amount of red cards

**position -** Every position played during the season

**team_title -** Name of the team

**npg -** Non penalty goals

**npxG -** Sum of Expected Goals of every shot, excluding penalties

**xGChain -** Total xG of every possession the player is involved in

**xGBuildup -** Total xG of every possession the player is involved in without key passes and shots



