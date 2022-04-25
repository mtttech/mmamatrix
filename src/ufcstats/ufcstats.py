from bs4 import BeautifulSoup
import requests


class UFCError(Exception):
    pass


class UFCSiteScraper:
    """Handler class for scraping the UFC website."""

    BASE_URL = "https://www.ufc.com/athlete/"

    def __init__(self, fighter: str):
        self.fighter_name = fighter
        self.fighter_tag = self.fighter_name.strip().lower().replace(" ", "-")

    def __str__(self):
        return f"fighter_name={self.fighter_name} fighter_tag={self.fighter_tag}"

    def scrape(self):
        fighter_url = self.BASE_URL + self.fighter_tag
        fighter_page = requests.get(fighter_url)
        status_code = fighter_page.status_code
        if status_code != 200:
            raise UFCError(f"There was an error locating '{self.fighter_name}' ({status_code}).")

        return UFCStatObject(fighter_page.content)


class UFCStatObject(BeautifulSoup):
    """Holder class for the fighter's stats."""

    def __init__(self, content: bytes):
        super().__init__(content, "html.parser")
        results = self.find("div", class_="c-hero__headline-suffix")
        fighter_string = (
            results.text.strip().replace(" ", "").replace("\n", "").split("•")
        )
        fighter_stats = fighter_string[1][: fighter_string[1].find("(")]
        self.win, self.loss, self.draw = fighter_stats.split("-")

    def __str__(self):
        return f"W={self.win} L={self.loss} D={self.draw}"