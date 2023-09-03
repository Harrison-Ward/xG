from bs4 import BeautifulSoup
import csv
import requests
import datetime
import pandas as pd
import os


def shotmap_extractor(event_id: str, headers=None):
    # default header arguments to my data
    if headers is None:
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

    # add present timestamp to header dict
    headers["If-Modified-Since"] = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S")

    # specificy the game with event_id data
    target = f'https://api.sofascore.com/api/v1/event/{event_id}/shotmap'

    # fetch data and convert to dict
    response = requests.get(target, headers=headers)
    shots_data = response.json()['shotmap']
    shots = pd.DataFrame.from_dict(shots_data)
    shots = shots.fillna(0)

    # take name slug and id info from player name
    shots['name'] = shots.player.apply(lambda x: dict(x)['slug'])
    shots['playerId'] = shots.player.apply(lambda x: dict(x)['id'])

    # unpack player coordinates into seperate vars
    shots['player_x'] = shots.playerCoordinates.apply(
        lambda x: dict(x)['x'])
    shots['player_y'] = shots.playerCoordinates.apply(
        lambda x: dict(x)['y'])
    shots['player_z'] = shots.playerCoordinates.apply(
        lambda x: dict(x)['z'])

    # unpack goal mouth coordiantes
    shots['goalMouth_x'] = shots.goalMouthCoordinates.apply(
        lambda x: dict(x)['x'])
    shots['goalMouth_y'] = shots.goalMouthCoordinates.apply(
        lambda x: dict(x)['y'])
    shots['goalMouth_z'] = shots.goalMouthCoordinates.apply(
        lambda x: dict(x)['z'])

    # unpack block location coordiantes
    shots['blockCoordinates_x'] = shots.blockCoordinates.apply(
        lambda x: dict(x)['x'] if x != 0 else 0)
    shots['blockCoordinates_y'] = shots.blockCoordinates.apply(
        lambda x: dict(x)['y'] if x != 0 else 0)
    shots['blockCoordinates_z'] = shots.blockCoordinates.apply(
        lambda x: dict(x)['z'] if x != 0 else 0)

    # one-hot-encode situations
    shots = pd.concat([shots, pd.get_dummies(
        shots.situation, prefix='shot_sit')], axis=1)
    shots = pd.concat([shots, pd.get_dummies(
        shots.isHome, prefix='homeTeam')], axis=1)
    shots = pd.concat([shots, pd.get_dummies(
        shots.shotType, prefix='outcome')], axis=1)
    shots = pd.concat([shots, pd.get_dummies(
        shots.bodyPart, prefix='bodyPart')], axis=1)

    # clean up extra columns
    shots.drop(['player', 'isHome', 'shotType', 'situation', 'playerCoordinates', 'bodyPart',
               'goalMouthLocation', 'goalMouthCoordinates', 'blockCoordinates', 'draw'], axis=1, inplace=True)

    shots.to_csv(
        f'/Users/harrisonward/Desktop/CS/Git/xG/datasets/game_shotmaps/{event_id}_shotmap.csv')


def dataset_agglomerator(path: str):
    valid_files = []
    for file in os.listdir(path):
        fname, ftype = file.split('.')
        if fname != '' and ftype == 'csv':
            valid_files.append(file)

    parent = pd.read_csv(
        f'datasets/game_shotmaps/{valid_files[0]}').drop('Unnamed: 0', axis=1)

    for file in valid_files[0:]:
        child = pd.read_csv(
            f'datasets/game_shotmaps/{file}').drop('Unnamed: 0', axis=1)
        parent = pd.concat([parent, child], sort=True)

    parent.to_csv(
        '/Users/harrisonward/Desktop/CS/Git/xG/datasets/23_24_cumulative_shotmap.csv')


if __name__ == '__main__':
    # open list of completed games
    with open('/Users/harrisonward/Desktop/CS/Git/xG/datasets/23_24_finished_events.csv') as file:
        events = pd.read_csv(file)

  # extract and compile game shot maps into a cumulative map
        for i, event_id in enumerate(events.event_id):
            try:
                shotmap_extractor(event_id=event_id, headers=None)
            except KeyError:
                pass

    dataset_agglomerator(
        '/Users/harrisonward/Desktop/CS/Git/xG/datasets/game_shotmaps')
