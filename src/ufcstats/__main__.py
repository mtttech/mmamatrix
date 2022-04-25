import sys
import time

from ufcstats import UFCSiteScraper, UFCError


def main():
    args = sys.argv
    if len(args) != 2:
        print("Invalid number of arguments specified.")
        return

    my_fighter = args[1]
    print(f"Looking up {my_fighter}'s record...")
    time.sleep(1.2)
    
    try:
        s = UFCSiteScraper(my_fighter)
        #print(s.__str__())
        r = s.scrape()
        #print(r.__str__())
    except UFCError as e:
        exit(e.__str__())
    else:
        print(f"A record was found for {my_fighter}.")
        time.sleep(1.2)
        print(f"{r.win}-{r.loss}-{r.draw}")


if __name__ == "__main__":
    main()
