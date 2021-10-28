import json
import os
import pickle
import requests

from bs4 import BeautifulSoup
import pandas as pd


CWD = os.getcwd()
DIR = os.path.join(CWD,"datasets")
DIR_TEAMS = os.path.join(CWD,"scraping", "teams_set")

BASE_LEAGUE_URL = "https://understat.com/league/"


def scrape_script_tags_season(season):
    """
    Takes a string with a league/season combination, e.g., "EPL_2020"
    to define a URL to be scraped.
    Returns a ResultSet object, class implemented by BeautifulSoup, with all
    the script tags in the URL.
    """
    URL = BASE_LEAGUE_URL + season
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "lxml")
    soup_scripts = soup.find_all("script")
    return soup_scripts


def generate_players_dict(season):
    """
    Takes a ResultSet and a string with a league/season combination.
    Returns a list of dictionaries with data on every player for the season.
    """
    soup_scripts = scrape_script_tags_season(season)

    script = soup_scripts[3].string

    start_index = script.index("('")+2
    end_index = script.index("')")
    json_string = script[start_index:end_index]
    json_string = json_string.encode("utf8").decode("unicode_escape")
    players_dict = json.loads(json_string)
    return players_dict


def generate_players_csv(first_year, last_year):
    """
    Takes initial and final years so that the datasets generated with
    generate_players_dict function can de exported to .csv files.
    """
    leagues = ["EPL", "La_liga", "Bundesliga", "Serie_A", "Ligue_1", "RFPL"]
    years = list(range(first_year,last_year + 1))

    for league in leagues:
        for year in years:
            season = league + "/" + str(year)

            league_lower = league.lower()
            season_years = str(year)[-2:] + "-" + str(year+1)[-2:]

            output_file = "players_" + league_lower + "_" + season_years + ".csv"
            output_dir = os.path.join(DIR, league_lower)
            os.makedirs(output_dir, exist_ok=True)

            file_path = os.path.join(output_dir, output_file)

            players_dict = generate_players_dict(season)
            players_df = pd.DataFrame.from_dict(players_dict)
            players_df.to_csv(file_path,index=False)


def generate_set_of_teams(first_year, last_year):
    """
    Scrapes the names of the teams for every league/season combination. The
    data is aggregated, resulting in a set for every league. Using pickle the
    sets are exported to be used in the match_scraper.py module.
    """
    leagues = ["EPL", "La_liga", "Bundesliga", "Serie_A", "Ligue_1", "RFPL"]
    years = list(range(first_year,last_year + 1))


    for league in leagues:
        teams_list = []

        for year in years:
            season = league + "/" + str(year)

            soup_scripts = scrape_script_tags_season(season)
            script = soup_scripts[2].string

            start_index = script.index("('")+2
            end_index = script.index("')")
            json_string = script[start_index:end_index]
            json_string = json_string.encode("utf8").decode("unicode_escape")
            script_dict = json.loads(json_string)

            df = pd.DataFrame.from_dict(script_dict).T
            teams = df["title"].tolist()
            teams_list.extend(teams)

        teams_set = set(teams_list)

        output_file = league + "_teams.txt"
        os.makedirs(DIR_TEAMS, exist_ok=True)

        file_path = os.path.join(DIR_TEAMS, output_file)

        with open(file_path, "wb") as fp:
            pickle.dump(teams_set, fp)