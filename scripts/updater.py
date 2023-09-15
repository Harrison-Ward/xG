from event_scraper import update_event_df
from shotmap_extractor import shotmap_extractor
from player_extractor import player_event_updater
import datetime
import subprocess
import logging

logging.basicConfig(level=logging.INFO, filename='scripts/logs/updater.log',
                    filemode='a', format='%(asctime)s: %(message)s')


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

    path_header = '/Users/harrisonward/Desktop/CS/Git/xG/datasets'

    update_event_df(
        filepath=f'{path_header}/23_24_premier_league_events.csv', headers=headers)
    
    shotmap_extractor(shotmap_filepath=f'{path_header}/23_24_shotmaps.csv',
                      event_filepath=f'{path_header}/23_24_premier_league_events.csv', headers=headers)
    
    player_event_updater(shotmap_filepath=f'{path_header}/23_24_shotmaps.csv',
                             player_event_filepath=f'{path_header}/23_24_player_event_stats.csv', headers=headers)

    subprocess.run(
        ["/Users/harrisonward/Desktop/CS/Git/xG/scripts/update_on_github.sh"])


if __name__ == '__main__':
    main()
