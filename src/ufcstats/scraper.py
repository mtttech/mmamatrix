from bs4 import BeautifulSoup
import requests


class UFCScraperError(Exception):
    pass


class UFCScraper:

    UFC_URL = "https://www.ufc.com/athlete/"

    def __init__(self, fighter):
        self.fighter_tag = fighter.strip().lower().replace(" ", "-")
        # print(self.fighter_tag)

    def scrape(self):
        fighter_url = self.UFC_URL + self.fighter_tag
        fighter_page = requests.get(fighter_url)
        if fighter_page.status_code != 200:
            raise UFCScraperError(f"Subject '{fighter_url}' not found.")

        return UFCScraperStatObject(fighter_page.content)


class UFCScraperStatObject(BeautifulSoup):
    def __init__(self, content):
        super().__init__(content, "html.parser")
        results = self.find("div", class_="c-hero__headline-suffix")
        fighter_stat_string = (
            results.text.strip().replace(" ", "").replace("\n", "").split("•")
        )
        fighter_stats = fighter_stat_string[1]
        fighter_stats = fighter_stats[: fighter_stats.find("(")]
        fighter_stats = fighter_stats.split("-")
        self.wins, self.losses, self.draws = fighter_stats
