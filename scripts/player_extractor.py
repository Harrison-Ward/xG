import pandas as pd
import numpy as np
import requests
import logging


def player_extractor_compiler(shotmap_filepath, headers):
    # read in the shotmap and find player, event id pairs
    shotmap_df = pd.read_csv(shotmap_filepath, index_col='Unnamed: 0')
    player_event_ids = np.unique(
        shotmap_df[['player.id', 'event.id']].values, axis=0)

    # request player statitstics by event
    player_event_stats = []
    for player_id, event_id in player_event_ids:
        json_data = requests.get(
            f'https://api.sofascore.com/api/v1/event/{event_id}/player/{player_id}/statistics', headers=headers).json()
        player_event_stats.append(json_data)

    # create data frame and add event_id to each row of the dataframe
    player_event_stats_df = pd.json_normalize(player_event_stats)
    player_event_stats_df['event.id'] = player_event_ids[::,1]

    # export the dataframe to csv
    player_event_stats_df.to_csv('/Users/harrisonward/Desktop/23_24_player_event_stats.csv')



def player_extractor_updater(shotmap_filepath, player_event_filepath, headers):
    # read in both the shotmap and player_event stats
    shotmap_df = pd.read_csv(shotmap_filepath, index_col='Unnamed: 0')
    player_event_stats_df = pd.read_csv(player_event_filepath, index_col='Unnamed: 0')

    # record the new and stored player_event pairings
    all_player_event_ids = np.unique(shotmap_df[['player.id', 'event.id']].values, axis=0)
    stored_player_event_ids = np.unique(player_event_stats_df[['player.id', 'event.id']].values, axis=0)

    # create tuple for each row
    all_player_event_ids_set = [tuple(row) for row in all_player_event_ids]
    stored_player_event_ids_set = [tuple(row) for row in stored_player_event_ids]

    # check the difference between the two set lists
    new_player_event_ids = np.array([row for row in all_player_event_ids if tuple(row) not in stored_player_event_ids_set])

    # request new player statitstics by event
    new_player_event_stats = []
    for player_id, event_id in new_player_event_ids:
        json_data = requests.get(
            f'https://api.sofascore.com/api/v1/event/{event_id}/player/{player_id}/statistics', headers=headers).json()
        new_player_event_stats.append(json_data)
    
    # create a short dataframe of new player event data to append to the existing dataframe
    new_player_event_stats_df = pd.json_normalize(new_player_event_stats)
    new_player_event_stats_df['event.id'] = new_player_event_ids[::,1]

    # concatenate the new dataframe and existing dataframe
    player_event_stats_df = pd.concat([player_event_stats_df, new_player_event_stats_df], sort=True,  verify_integrity=False, ignore_index=True)

    # export the dataframe to csv
    player_event_stats_df.to_csv('/Users/harrisonward/Desktop/23_24_player_event_stats2.csv')

if __name__ == '__main__':
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

    # player_extractor_compiler(shotmap_filepath='/Users/harrisonward/Desktop/CS/Git/xG/datasets/23_24_shotmaps.csv',
    #                  headers=headers)
    
    player_extractor_updater(shotmap_filepath='/Users/harrisonward/Desktop/CS/Git/xG/datasets/23_24_shotmaps.csv',
                             player_event_filepath= '/Users/harrisonward/Desktop/player_event_stats.csv',
                             headers=headers)
