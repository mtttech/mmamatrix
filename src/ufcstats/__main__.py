import sys
import time

from ufcstats import UFCScraper, UFCScraperError


def main():
    args = sys.argv
    if len(args) != 2:
        print("Invalid number of arguments specified.")
        return

    my_fighter = args[1]
    print(f"Looking up {my_fighter}'s record...")
    time.sleep(1.2)
    
    try:
        s = UFCScraper(my_fighter).scrape()
    except UFCScraperError as e:
        exit(e)
    else:
        print(f"A record was found for {my_fighter}.")
        time.sleep(1.2)

        print(f"{s.win}-{s.loss}-{s.draw}")
        time.sleep(1.2)


if __name__ == "__main__":
    main()
