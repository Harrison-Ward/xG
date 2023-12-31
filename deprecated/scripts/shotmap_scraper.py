from bs4 import BeautifulSoup
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
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.sofascore.com/',
            'Origin': 'https://www.sofascore.com',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'If-None-Match': 'W/"8acfad2dd3"',
            'Cache-Control': 'max-age=0',
            # Requests doesn't support trailers
            # 'TE': 'trailers',
        }

    # add present timestamp to header dict
    headers["If-Modified-Since"] = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S")

    # specificy the game with event_id data
    target = f'https://api.sofascore.com/api/v1/event/{event_id}/shotmap'

    # fetch data and convert to dict
    response = requests.get(target, headers=headers)
    shots_data = response.json()['shotmap']
    shots = pd.DataFrame.from_dict(shots_data)

    # take name slug and id info from player name
    shots['name'] = shots.player.apply(lambda x: dict(x)['slug'])
    shots['playerId'] = shots.player.apply(lambda x: dict(x)['id'])

    # unpack player coordinates into seperate vars
    shots['player_x'] = shots.playerCoordinates.apply(lambda x: dict(x)['x'])
    shots['player_y'] = shots.playerCoordinates.apply(lambda x: dict(x)['y'])
    shots['player_z'] = shots.playerCoordinates.apply(lambda x: dict(x)['z'])

    # unpack goal mouth coordiantes
    shots['goalMouth_x'] = shots.goalMouthCoordinates.apply(
        lambda x: dict(x)['x'])
    shots['goalMouth_y'] = shots.goalMouthCoordinates.apply(
        lambda x: dict(x)['y'])
    shots['goalMouth_z'] = shots.goalMouthCoordinates.apply(
        lambda x: dict(x)['z'])

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
               'goalMouthLocation', 'goalMouthCoordinates', 'draw', 'blockCoordinates'], axis=1, inplace=True)

    shots.to_csv(f'../datasets/{event_id}_shotmap.csv')


def dataset_agglomerator(path: str):
    valid_files = []
    for file in os.listdir(path):
        fname, ftype = file.split('.')
        if fname != '' and ftype == 'csv':
            valid_files.append(file)

    parent = pd.read_csv(
        f'datasets/{valid_files[0]}').drop('Unnamed: 0', axis=1)

    for file in valid_files[0:]:
        child = pd.read_csv(f'datasets/{file}').drop('Unnamed: 0', axis=1)
        parent = pd.concat([parent, child], sort=True)

    parent.to_csv('../datasets/cumulative_shotmap.csv')


if __name__ == '__main__':
    events = [11352437, 11352309, 11352407, 10385726, 10385723, 10385694,
              10385651, 10385647, 10385604, 10385610, 10385575, 10385562,
              10385544, 10385504, 10865877, 10385492, 11047942, 10385488,
              10385477, 10865869, 10385466, 10385442, 10980654, 10385437,
              10913242, 10385433, 10909914, 10385414, 10385397, 11352504,
              11352447, 11352495, 11352456, 11352466, 11352524, 11352515,
              11352484, 11352346, 11352418, 11352337, 11352389, 11352358, 
              11352428, 11352367, 11352399, 11352327, 11352316, 11352255, 
              11352254, 11352252, 11352253, 11352250, 11352251, 11352303, 
              11352561, 11352551, 11352594, 1352570, 11352543, 11352551]

    for event_id in events:
        shotmap_extractor(event_id=event_id, headers=None)

    dataset_agglomerator('datasets')
