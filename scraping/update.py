import match_scraper as ms
import season_scraper as ss


# # Once a season, update sets of teams and matches_id to be scraped
# ms.patch_empty_url_list()
# ss.generate_set_of_teams(2021, 2021)

# Updates the shots datasets and the players datasets
ms.update_shots_dataset(2021)
ss.generate_players_csv(2021,2021)
