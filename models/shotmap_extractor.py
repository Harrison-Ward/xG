import pandas as pd
import numpy as np
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
    """
    Extracts and updates shotmap data from SofaScore API and merges it with event information.

    Parameters:
    - event_filepath (str): Filepath to the CSV file containing event data.
    - shotmap_filepath (str): Filepath to the CSV file containing shotmap data.

    The function performs the following steps:
    1. Loads the event data from the provided CSV file.
    2. Filters and extracts completed event IDs.
    3. Merges relevant event information (home and away team, match details) into a DataFrame.
    4. Checks if the event IDs are already present in the shotmap DataFrame.
    5. Retrieves shotmap data from the SofaScore API for new events.
    6. Integrates shotmap data with event details.
    7. Determines the team the shooter plays for and their opponent.
    8. Saves the updated shotmap data to the specified CSV file.

    Note: The function relies on external data sources and assumes specific column names in the CSV files.

    """
    # load the event df and the list of finished events
    event_df = pd.read_csv(event_filepath)
    completed_event_ids = event_df['event.id'][event_df['event.status.type']
                                               == 'finished'].values
    
    

    # merge in home and away team and match slug
    event_info_df = event_df[['event.awayTeam.slug', 'event.homeTeam.slug',
                              'event.slug', 'event.winnerCode', 'event.awayTeam.name', 'event.homeTeam.name', 'event.id']]

    # check if event id is already in the shot map dataframe
    shotmap_df = pd.read_csv(shotmap_filepath, index_col='Unnamed: 0')
    completed_shotmap_event_ids_set = set(shotmap_df['event.id'].values)

    # pull shotmap data from the web
    new_shotmaps = []
    for event_id in completed_event_ids:
        if event_id not in completed_shotmap_event_ids_set:
            print(f"Processing event_id: {event_id}")
            new_shotmaps.append(requests.get(
                f'https://api.sofascore.com/api/v1/event/{event_id}/shotmap', headers=headers).json())

    # add event.id, match data, and binary vars to the shotmap
    for i, shot_maps in enumerate(new_shotmaps):
        if completed_event_ids[i] not in completed_shotmap_event_ids_set:
            try:
                # merge in event data from the events df
                temp_df = pd.json_normalize(shot_maps['shotmap'])
                temp_df['event.id'] = completed_event_ids[i]
                temp_df = temp_df.merge(
                    event_info_df, how='left', left_on='event.id', right_on='event.id')

                # create binary variables from the event data
                temp_df = pd.concat([temp_df, pd.get_dummies(
                    temp_df.situation, prefix='shot_sit')], axis=1)
                temp_df = pd.concat([temp_df, pd.get_dummies(
                    temp_df.isHome, prefix='homeTeam')], axis=1)
                temp_df = pd.concat([temp_df, pd.get_dummies(
                    temp_df.shotType, prefix='outcome')], axis=1)
                temp_df = pd.concat([temp_df, pd.get_dummies(
                    temp_df.bodyPart, prefix='bodyPart')], axis=1)

                # determine the team the shooter plays for and their opponent
                temp_df['team'] = np.where(
                    temp_df['isHome'], temp_df['event.homeTeam.name'], temp_df['event.awayTeam.name'])
                temp_df['opponent'] = np.where(
                    temp_df['isHome'] == False, temp_df['event.homeTeam.name'], temp_df['event.awayTeam.name'])

                # add the new temporary df to the shotmap data
                print(completed_event_ids[i])
                shotmap_df = pd.concat([shotmap_df, temp_df], sort=True, verify_integrity=True, ignore_index=True)
            except KeyError:
                print(
                    f'\nWarning: polluted data\nPolluted Event Id:{completed_event_ids[i]}')

    # save updated shotmap csv
    shotmap_df.to_csv(shotmap_filepath)


if __name__ == '__main__':
    shotmap_extractor('/Users/harrisonward/Desktop/CS/Git/xG/datasets/23_24_premier_league_events.csv',
                      '/Users/harrisonward/Desktop/CS/Git/xG/datasets/23_24_shotmaps.csv')
