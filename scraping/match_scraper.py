import glob
import json
import os
import pickle
import requests

from bs4 import BeautifulSoup
import pandas as pd


CWD = os.getcwd()
DIR = os.path.join(CWD,"datasets")
DIR_TEAMS = os.path.join(CWD,"scraping", "teams_set")

BASE_URL = "https://understat.com/match/"


def scrape_script_tags(match_id):
    """
    Takes a match_id (integer) to define a URL to be scraped.
    Returns a ResultSet object, class implemented by BeautifulSoup, with all
    the script tags in the URL.
    """
    URL = BASE_URL + str(match_id)

    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "lxml")
    soup_scripts = soup.find_all("script")
    return soup_scripts


def create_shots_list(soup_scripts):
    """
    Takes a ResultSet and returns a list of dictionaries containing all shots
    in a soccer match.
    """
    shots_string = soup_scripts[1].string
    start_index = shots_string.index("('")+2
    end_index = shots_string.index("')")
    json_string = shots_string[start_index:end_index]
    json_string = json_string.encode("utf8").decode("unicode_escape")
    shots_dict = json.loads(json_string)

    shots_home = shots_dict["h"]
    shots_away = shots_dict["a"]

    shots_list = shots_home + shots_away
    return shots_list


def generate_shots_dataset(iterable):
    """
    Takes an iterable object with matches_id. It is passed to a loop that
    goes through all matches and scrapes the data. Sometimes a Connection Error
    is raised when trying to scrape many matches at once, so might be a good
    idea to scrape only a few hundred matches each turn.
    Returns "empty_url_list", a list of matches_id not assigned to a match.
    Also returns a DataFrame with the shots of the matches scraped.
    """
    empty_url_list = []
    shots_list = []

    for match_id in iterable:
        print(match_id)
        soup_scripts = scrape_script_tags(match_id)
        if len(soup_scripts) == 0:
            empty_url_list.append(match_id)
        else:
            match_shots_list = create_shots_list(soup_scripts)
            shots_list.extend(match_shots_list)

    return empty_url_list, pd.DataFrame.from_dict(shots_list)


def generate_shots_csv(shots_df, file_name):
    """
    Takes a DataFrame of shots and a filename (string ending in .csv).
    Exports the DataFrame to a .csv file, creating folders if they don't exist.
    """
    os.makedirs(DIR, exist_ok=True)
    file_path = os.path.join(DIR, file_name)

    shots_df.to_csv(file_path,index=False)


def save_empty_url_list(empty_url_list, file_name):
    """
    Takes a list of matches_id not assigned to a match and a
    filename (string ending in .txt).
    Exports the list to a .txt file using pickle, creating folders if they
    don't exist.
    """
    os.makedirs(DIR, exist_ok=True)
    file_path = os.path.join(DIR, file_name)

    with open(file_path, "wb") as fp:
        pickle.dump(empty_url_list, fp)


def merge_shots_csvs():
    """
    Merges every .csv file with shots data into a single file.
    """

    csv_path = os.path.join(DIR, "*.csv")
    csv_list = glob.glob(csv_path)
    file_path = os.path.join(DIR, "shots_dataset.csv")

    df_list = []

    for file in csv_list:
        df_list.append(pd.read_csv(file))

    merged_df = pd.concat(df_list)
    merged_df["player"] = merged_df["player"].str.replace("&#039;", "'")
    merged_df.to_csv(file_path,index=False)


def merge_empty_url_lists():
    """
    Reads every "empty_url_list" .txt files and saves it into a single file.
    """

    txt_path = os.path.join(DIR, "empty*.txt")
    txt_list = glob.glob(txt_path)
    file_path = os.path.join(DIR, "empty_url.txt")

    empty_url_list = []

    for file in txt_list:
        with open(file, "rb") as fp:
            l = pickle.load(fp)
        empty_url_list.extend(l)

    with open(file_path, "wb") as fp:
        pickle.dump(empty_url_list, fp)


def open_teams_set(teams_file_name):
    """
    Opens a .txt file exported in the season_scraper.py module. Each league
    has a file, containing the name of every team that played at least a
    season between 2014 and 2020. The names are used to split the shots
    datasets in leagues.
    """

    file_path = os.path.join(DIR_TEAMS, teams_file_name)

    with open(file_path, "rb") as fp:
        teams_set = pickle.load(fp)

    return teams_set


def generate_shots_csvs_by_league_season(first_year, last_year):
    """
    Splits the shots dataset in a different .csv file for each combination of
    league/season. Selecting 2014 and 2020 as arguments, results in 42 files
    (6 leagues and 7 seasons).
    """
    leagues = ["EPL", "La_liga", "Bundesliga", "Serie_A", "Ligue_1", "RFPL"]
    years = list(range(first_year,last_year + 1))

    for league in leagues:
        for year in years:

            league_lower = league.lower()
            season_years = str(year)[-2:] + "-" + str(year+1)[-2:]

            shots_df_path = os.path.join(DIR, "shots_dataset.csv")
            output_file = "shots_" + league_lower + "_" + season_years + ".csv"
            output_dir = os.path.join(DIR, league_lower)
            os.makedirs(output_dir, exist_ok=True)
            file_path = os.path.join(output_dir, output_file)

            teams_set = open_teams_set(league + "_teams.txt")
            shots_df = pd.read_csv(shots_df_path)
            shots_league = shots_df[shots_df["h_team"].isin(teams_set)]
            filter_season = shots_league["season"]==year
            shots_season = shots_league.where(filter_season).dropna(subset=["season"])
            shots_season.to_csv(file_path,index=False)


def remove_forgotten_empty_urls():
    file_path = os.path.join(DIR, "empty_url backup.txt")
    with open(file_path, "rb") as fp:
        old_empty_url_list = pickle.load(fp)
    old_empty_url_list.sort()
    update_empty_url = old_empty_url_list[1734:]

    save_empty_url_list(update_empty_url, "empty_url_update.txt")


def update_shots_dataset(year):

    file_path = os.path.join(DIR, "empty_url_update.txt")
    with open(file_path, "rb") as fp:
        old_empty_url_list = pickle.load(fp)
    old_empty_url_list.sort()

    empty_url_list, shots_update = generate_shots_dataset(old_empty_url_list)
    save_empty_url_list(empty_url_list, "empty_url_update.txt")

    try:
        shots_update["player"] = shots_update["player"].str.replace("&#039;", "'")
    except KeyError:
        pass

    df_list = [shots_update]
    shots_file = os.path.join(DIR, "shots_dataset.csv")
    shots_dataset = pd.read_csv(shots_file)
    df_list.append(shots_dataset)
    merged_df = pd.concat(df_list)

    generate_shots_csv(merged_df, "shots_dataset.csv")
    generate_shots_csvs_by_league_season(year, year)


# update_shots_dataset(2020)
