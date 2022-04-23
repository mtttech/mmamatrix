from bs4 import BeautifulSoup
import requests


class UFCScraperError(Exception):
    pass


class UFCScraper:
    """Handles scraping the UFC website."""

    BASE_URL = "https://www.ufc.com/athlete/"

    def __init__(self, fighter):
        self.fighter_name = fighter
        self.fighter_tag = self.fighter_name.strip().lower().replace(" ", "-")

    def __str__(self):
        return f"fighter_name={self.fighter_name} fighter_tag={self.fighter_tag}"

    def scrape(self):
        fighter_url = self.BASE_URL + self.fighter_tag
        fighter_page = requests.get(fighter_url)
        status_code = fighter_page.status_code
        if status_code != 200:
            raise UFCScraperError(f"There was an error locating '{self.fighter_name}' ({status_code}).")

        return UFCScraperStatObject(fighter_page.content)


class UFCScraperStatObject(BeautifulSoup):
    """Stores a fighter's record."""

    def __init__(self, content):
        super().__init__(content, "html.parser")
        results = self.find("div", class_="c-hero__headline-suffix")
        fighter_string = (
            results.text.strip().replace(" ", "").replace("\n", "").split("•")
        )
        fighter_stats = fighter_string[1][: fighter_string[1].find("(")]
        self.wins, self.losses, self.draws = fighter_stats.split("-")

    def __str__(self):
        return f"W={self.wins} L={self.losses} D={self.draws}"