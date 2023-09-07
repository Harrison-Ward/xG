import pandas as pd
import requests

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


def shotmap_extractor(event_filepath, shotmap_filepath):
    # load the event df and the list of finished events
    event_df = pd.read_csv(event_filepath)
    completed_event_ids = event_df['event.id'][event_df['event.status.type']
                                               == 'finished'].values

    # check if event id is already in the shot map dataframe
    shotmap_df = pd.read_csv(shotmap_filepath)
    completed_shotmap_event_ids = shotmap_df['event.id'].values

    # pull shotmap data from the web
    new_shotmaps = []
    for event_id in completed_event_ids:
        if event_id not in completed_shotmap_event_ids:
            new_shotmaps.append(requests.get(
                f'https://api.sofascore.com/api/v1/event/{event_id}/shotmap', headers=headers).json())

    # add event.id and match data to the shotmap
    unpacked_shotmap_dfs = []
    for i, shot_maps in enumerate(new_shotmaps):
        try:
            temp_df = pd.json_normalize(shot_maps['shotmap'])
            temp_df['event.id'] = completed_event_ids[i]
            shotmap_df = pd.concat([shotmap_df, temp_df], sort=True)
        except KeyError:
            pass

    # merge in home and away team and match slug
    shotmap_df = shotmap_df.drop('Unnamed: 0', axis=1)
    shotmap_df.to_csv(shotmap_filepath)


if __name__ == '__main__':
    shotmap_extractor('/Users/harrisonward/Desktop/CS/Git/xG/datasets/23_24_premier_league_events.csv',
                      '/Users/harrisonward/Desktop/CS/Git/xG/datasets/23_24_shotmaps.csv')
