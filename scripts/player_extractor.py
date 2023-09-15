import pandas as pd
import numpy as np
import requests
import logging


def player_event_compiler(shotmap_filepath, player_event_filepath, headers):
    """
    Extracts player statistics by event from a shotmap CSV file and compiles them into a new CSV file.

    Parameters:
    - shotmap_filepath (str): The file path to the shotmap CSV file containing player and event data.
    - player_event_filepath (str): The file path to save the compiled player event statistics as a CSV file.
    - headers (dict): A dictionary containing headers for making HTTP requests (e.g., authorization).

    Returns:
    None

    This function reads the shotmap CSV file, extracts unique player and event ID pairs, 
    requests player statistics for each pair from an API, compiles the statistics into a DataFrame, 
    and exports the DataFrame as a CSV file.

    Example usage:
    player_extractor_compiler('shotmap.csv', 'player_event_stats.csv', {'Authorization': 'Bearer <token>'})
    """
    logging.info('Player Events Extractor compiling new Player Events data...')
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
    player_event_stats_df['event.id'] = player_event_ids[::, 1]

    # export the dataframe to csv
    player_event_stats_df.to_csv(player_event_filepath)
    logging.info(
        f'Player Events Compilier succesfully added {player_event_stats.shape[0]} new shotmaps\n')
    logging.info(f'Player Events Compilier succesfully exited\n\n\n')


def player_event_updater(shotmap_filepath, player_event_filepath, headers):
    """
    Update and append player statistics by event from a shotmap CSV file to an existing player event statistics CSV file.

    Parameters:
    - shotmap_filepath (str): The file path to the shotmap CSV file containing player and event data.
    - player_event_filepath (str): The file path to the existing player event statistics CSV file.
    - headers (dict): A dictionary containing headers for making HTTP requests (e.g., authorization).

    Returns:
    None

    This function reads both the shotmap and existing player event statistics CSV files, 
    identifies new player-event pairings in the shotmap, requests statistics for these new pairs from an API, 
    and appends the new player event statistics to the existing CSV file.

    Example usage:
    player_extractor_updater('shotmap.csv', 'player_event_stats.csv', {'Authorization': 'Bearer <token>'})
    """
    logging.info(
        'Player Events Updater searching for new player events data...')
    # read in both the shotmap and player_event stats
    shotmap_df = pd.read_csv(shotmap_filepath, index_col='Unnamed: 0')
    player_event_stats_df = pd.read_csv(
        player_event_filepath, index_col='Unnamed: 0')

    # record the new and stored player_event pairings
    all_player_event_ids = np.unique(
        shotmap_df[['player.id', 'event.id']].values, axis=0)
    stored_player_event_ids = np.unique(
        player_event_stats_df[['player.id', 'event.id']].values, axis=0)

    # create tuple for each row
    stored_player_event_ids_set = [tuple(row)
                                   for row in stored_player_event_ids]

    # check the difference between the two set lists
    new_player_event_ids = np.array([row for row in all_player_event_ids if tuple(
        row) not in stored_player_event_ids_set])

    # exit if no new events are found
    if new_player_event_ids.shape[0] == 0:
        logging.warning('WARNING: No new player event data found')
        logging.info('Player Updater successfully exited\n\n\n')
        return 0

    # request new player statitstics by event
    new_player_event_stats = []
    for player_id, event_id in new_player_event_ids:
        json_data = requests.get(
            f'https://api.sofascore.com/api/v1/event/{event_id}/player/{player_id}/statistics', headers=headers).json()
        new_player_event_stats.append(json_data)

    # create a short dataframe of new player event data to append to the existing dataframe
    new_player_event_stats_df = pd.json_normalize(new_player_event_stats)
    new_player_event_stats_df['event.id'] = new_player_event_ids[::, 1]

    # concatenate the new dataframe and existing dataframe
    player_event_stats_df = pd.concat(
        [player_event_stats_df, new_player_event_stats_df], sort=True,  verify_integrity=False, ignore_index=True)

    # export the dataframe to csv
    player_event_stats_df.to_csv(player_event_filepath)
    logging.info(
        f'Player Events Updater succesfully added {new_player_event_stats.shape[0]} new shotmaps\n')
    logging.info(f'Player Events Updater succesfully exited\n\n\n')
