import asyncio
import sys

from bs4 import BeautifulSoup
import requests


class MMAMatrix(BeautifulSoup):
    """Return data holder class."""

    def __init__(self, content: bytes, fighter_url: str):
        self.fighter_url = fighter_url
        super().__init__(content, "html.parser")
        results = self.find("div", class_="c-hero__headline-suffix")
        rank_text, record_text = results.text.strip().replace("\n", "").split("•")
        self.rank = reconstruct_string(rank_text)
        self.win, self.loss, self.draw = reconstruct_string(record_text).split("-")

    def __str__(self):
        return f"W={self.win} L={self.loss} D={self.draw} rank={self.rank}"


async def fetch(fighter: str):
    """Handler class for scraping the UFC website."""
    print(f"Looking up {fighter}'s record...")
    base_url = "https://www.ufc.com/athlete/"
    tag = fighter.strip().lower().replace(" ", "-")
    full_url = base_url + tag
    page = requests.get(full_url)
    page.raise_for_status()
    return MMAMatrix(page.content, full_url)


def reconstruct_string(string: str) -> str:
    letter_pool = list()
    reconstructed_string = list()
    for index in range(0, len(string) - 1):
        char = string[index]
        if char != " ":
            letter_pool.append(char)
        else:
            word = "".join(letter_pool)
            reconstructed_string.append(word)
            letter_pool = list()

    return  " ".join([w for w in reconstructed_string if w != ""])


async def main():
    args = sys.argv
    if len(args) != 2:
        print("Invalid number of arguments specified.")
        return

    my_fighter = args[1]
    try:
        result = await fetch(my_fighter)
    except requests.exceptions.HTTPError as e:
        exit(e.__str__())
    print(f"Record found: {my_fighter} ({result.rank}): {result.fighter_url}.")
    print(f"{result.win}-{result.loss}-{result.draw}")


if __name__ == "__main__":
    asyncio.run(main())
