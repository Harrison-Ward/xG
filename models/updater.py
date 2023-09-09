from event_scraper import update_event_df
from shotmap_extractor import shotmap_extractor
import datetime
import subprocess

def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.sofascore.com/',
        'Origin': 'https://www.sofascore.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'If-None-Match': 'W/"8acfad2dd3"',
        'Cache-Control': 'max-age=0',
    }

    headers["If-Modified-Since"] = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S")

    # might change this so that the main function takes in an argv
    # add some logging to keep track of the number of events, and events updated
    update_event_df(
        filepath='/Users/harrisonward/Desktop/CS/Git/xG/datasets/23_24_premier_league_events copy.csv', headers=headers)
    shotmap_extractor(shotmap_filepath='/Users/harrisonward/Desktop/CS/Git/xG/datasets/23_24_shotmaps2.csv',
                      event_filepath='/Users/harrisonward/Desktop/CS/Git/xG/datasets/23_24_premier_league_events copy.csv', headers=headers)

    # push updates to github
    # if you werent a fucking idiot these would all take thier arguments from argv but ...
    subprocess.run(["/Users/harrisonward/Desktop/CS/Git/xG/update_on_github.sh"])


if __name__ == '__main__':
    main()
