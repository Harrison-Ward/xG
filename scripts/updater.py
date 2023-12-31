#!/opt/anaconda3/envs/cs109b/bin/python
from player_shotmap_updater import player_shotmap_updater
from event_scraper import event_updater
from shotmap_extractor import shotmap_updater
from player_extractor import player_event_updater
import datetime
import subprocess
import logging

logging.basicConfig(level=logging.INFO, filename='/Users/harrisonward/Desktop/CS/Git/xG/scripts/logs/updater.log',
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

    datasets_path_head = '/Users/harrisonward/Desktop/CS/Git/xG/datasets'
    scripts_path_head = '/Users/harrisonward/Desktop/CS/Git/xG/scripts'

    # update the events df with up to date event data
    event_updater(
        event_filepath=f'{datasets_path_head}/23_24_premier_league_events.csv', headers=headers)

    # pull new shotmaps for newly finished games
    shotmap_updater(shotmap_filepath=f'{datasets_path_head}/23_24_shotmaps.csv',
                    event_filepath=f'{datasets_path_head}/23_24_premier_league_events.csv', headers=headers)

    # pull new player stats for newly finished games
    player_event_updater(shotmap_filepath=f'{datasets_path_head}/23_24_shotmaps.csv',
                         player_event_filepath=f'{datasets_path_head}/23_24_player_event_stats.csv', headers=headers)

    # merge the player stats into the augemented shotmap
    player_shotmap_updater(shotmap_filepath=f'{datasets_path_head}/23_24_shotmaps.csv',
                                player_event_filepath=f'{datasets_path_head}/23_24_player_event_stats.csv')

    # push the updates in the datasets to github
    subprocess.run(
        [f'{scripts_path_head}/update_on_github.sh'])


if __name__ == '__main__':
    main()
