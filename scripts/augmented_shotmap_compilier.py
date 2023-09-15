import pandas as pd
import logging

def augmented_shotmap_compilier(augmented_shotmap_filepath, player_event_filepath):
    """
    Compile augmented shotmap data with player event statistics and save the result.

    Parameters:
    - augmented_shotmap_filepath (str): The file path to the augmented shotmap CSV file.
    - player_event_filepath (str): The file path to the player event statistics CSV file.

    Returns:
    int: Returns 0 upon successful completion.

    This function reads an augmented shotmap CSV file and player event statistics CSV file,
    merges the relevant player data with the shotmap data based on event and player IDs,
    and saves the compiled dataframe back to the augmented shotmap file.

    Example usage:
    augmented_shotmap_compilier('augmented_shotmap.csv', 'player_event_stats.csv')
    """
    logging.info('Augmented Shotmap compilier started...')
    # read in the augmented shotmap and player events dataframe to make merges
    player_df = pd.read_csv(player_event_filepath, index_col='Unnamed: 0')
    augmented_shotmap_df = pd.read_csv(augmented_shotmap_filepath, index_col='Unnamed: 0')

    # take the data we are interested in from the player dataframe
    player_match_data = player_df[['event.id', 'player.id', 'statistics.minutesPlayed', 'statistics.expectedAssists', 'player.position']]

    # merge the player data on the event and player id
    augmented_shotmap_df = augmented_shotmap_df.merge(right=player_match_data, how='left', left_on=['event.id', 'player.id'], right_on=['event.id', 'player.id'])

    # save the augmented shotmap dataframe 
    augmented_shotmap_df.to_csv(augmented_shotmap_filepath)
    logging.info('Augmented Shotmap compilier sucessfully exited...')
    return 0