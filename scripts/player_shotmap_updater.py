import pandas as pd
import numpy as np
import logging


def player_shotmap_updater(shotmap_filepath, player_event_filepath):
    """
    Compile augmented shotmap data with player event statistics and save the result.

    Parameters:
    - shotmap_filepath (str): The file path to the augmented shotmap CSV file.
    - player_event_filepath (str): The file path to the player event statistics CSV file.

    Returns:
    int: Returns 0 upon successful completion.

    This function reads an augmented shotmap CSV file and player event statistics CSV file,
    merges the relevant player data with the shotmap data based on event and player IDs,
    and saves the compiled dataframe back to the augmented shotmap file.

    Example usage:
    augmented_shotmap_compilier('augmented_shotmap.csv', 'player_event_stats.csv')
    """
    logging.info('Player Shotmap Updater started...')

    # read in the augmented shotmap and player events dataframe to make merges
    player_df = pd.read_csv(player_event_filepath, index_col='Unnamed: 0')
    shotmap_df = pd.read_csv(
        shotmap_filepath, index_col='Unnamed: 0')

    # check which player.id, event.id tuples are in the shotmap vs player stats dfs
    new_player_event_ids = np.unique(
        player_df[['player.id', 'event.id']].values, axis=0)
    stored_player_event_ids = np.unique(
        shotmap_df[['player.id', 'event.id']], axis=0)

    # check if any rows are not in the shotmap dataframe
    stored_player_event_ids_tuples = [tuple(row)
                                      for row in stored_player_event_ids]

    # check the difference between the two set lists
    new_player_event_ids = np.array([row for row in new_player_event_ids if tuple(
        row) not in stored_player_event_ids_tuples])

    if new_player_event_ids.shape[0] == 0:
        logging.warning('WARNING: No new player event data to merge')
        logging.info('Player Shotmap Updater successfully exited')
        return 0

    # just drop the whole column and remerge it back on to manage the mismatch in lengths that would be created otherwise
    try:
        shotmap_df = shotmap_df.drop(
            columns=['statistics.minutesPlayed', 'statistics.expectedAssists'], axis=1)
    except KeyError as e:
        logging.warning(
            f"WARNING: {e.args}, were not found in the augmented_shotmap df when trying to refresh data")

    shotmap_df = shotmap_df.merge(right=player_df[['player.id', 'event.id', 'statistics.minutesPlayed', 'statistics.expectedAssists']], how='left', on=[
        'player.id', 'event.id'])

    # save the augmented shotmap dataframe
    shotmap_df.to_csv(shotmap_filepath)
    logging.info('Player Shotmap Updater sucessfully exited')
    return 0
