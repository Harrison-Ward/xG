import datetime
import requests
import pandas as pd
import numpy as np
import logging


# find the headers the api needs to accept you
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

# valid columns to keep from the returned json object
valid_columns = ['event.tournament.uniqueTournament.hasEventPlayerStatistics',
                 'event.season.name',
                 'event.season.year',
                 'event.season.id',
                 'event.roundInfo.round',
                 'event.customId',
                 'event.status.code',
                 'event.status.description',
                 'event.status.type',
                 'event.winnerCode',
                 'event.venue.city.name',
                 'event.venue.stadium.name',
                 'event.venue.stadium.capacity',
                 'event.venue.id',
                 'event.referee.name',
                 'event.referee.slug',
                 'event.referee.yellowCards',
                 'event.referee.redCards',
                 'event.referee.yellowRedCards',
                 'event.referee.games',
                 'event.referee.id',
                 'event.referee.country.alpha2',
                 'event.referee.country.name',
                 'event.homeTeam.name',
                 'event.homeTeam.slug',
                 'event.homeTeam.shortName',
                 'event.homeTeam.userCount',
                 'event.homeTeam.manager.name',
                 'event.homeTeam.manager.slug',
                 'event.homeTeam.manager.id',
                 'event.homeTeam.manager.country.alpha2',
                 'event.homeTeam.manager.country.name',
                 'event.homeTeam.venue.city.name',
                 'event.homeTeam.venue.stadium.name',
                 'event.homeTeam.venue.stadium.capacity',
                 'event.homeTeam.venue.id',
                 'event.homeTeam.venue.country.alpha2',
                 'event.homeTeam.venue.country.name',
                 'event.homeTeam.nameCode',
                 'event.homeTeam.disabled',
                 'event.homeTeam.national',
                 'event.homeTeam.type',
                 'event.homeTeam.id',
                 'event.homeTeam.country.alpha2',
                 'event.homeTeam.country.name',
                 'event.homeTeam.subTeams',
                 'event.homeTeam.fullName',
                 'event.homeTeam.teamColors.primary',
                 'event.homeTeam.teamColors.secondary',
                 'event.homeTeam.teamColors.text',
                 'event.homeTeam.foundationDateTimestamp',
                 'event.awayTeam.name',
                 'event.awayTeam.slug',
                 'event.awayTeam.shortName',
                 'event.awayTeam.userCount',
                 'event.awayTeam.manager.name',
                 'event.awayTeam.manager.slug',
                 'event.awayTeam.manager.id',
                 'event.awayTeam.manager.country.alpha2',
                 'event.awayTeam.manager.country.name',
                 'event.awayTeam.venue.city.name',
                 'event.awayTeam.venue.stadium.name',
                 'event.awayTeam.venue.stadium.capacity',
                 'event.awayTeam.venue.id',
                 'event.awayTeam.venue.country.alpha2',
                 'event.awayTeam.venue.country.name',
                 'event.awayTeam.nameCode',
                 'event.awayTeam.type',
                 'event.awayTeam.id',
                 'event.awayTeam.country.alpha2',
                 'event.awayTeam.country.name',
                 'event.awayTeam.subTeams',
                 'event.awayTeam.fullName',
                 'event.awayTeam.teamColors.primary',
                 'event.awayTeam.teamColors.secondary',
                 'event.awayTeam.teamColors.text',
                 'event.awayTeam.foundationDateTimestamp',
                 'event.homeScore.current',
                 'event.homeScore.display',
                 'event.homeScore.period1',
                 'event.homeScore.period2',
                 'event.homeScore.normaltime',
                 'event.awayScore.current',
                 'event.awayScore.display',
                 'event.awayScore.period1',
                 'event.awayScore.period2',
                 'event.awayScore.normaltime',
                 'event.time.injuryTime1',
                 'event.time.injuryTime2',
                 'event.time.currentPeriodStartTimestamp',
                 'event.changes.changes',
                 'event.changes.changeTimestamp',
                 'event.hasGlobalHighlights',
                 'event.hasXg',
                 'event.hasEventPlayerStatistics',
                 'event.hasEventPlayerHeatMap',
                 'event.detailId',
                 'event.crowdsourcingDataDisplayEnabled',
                 'event.id',
                 'event.defaultPeriodCount',
                 'event.defaultPeriodLength',
                 'event.currentPeriodStartTimestamp',
                 'event.startTimestamp',
                 'event.slug',
                 'event.finalResultOnly',
                 'event.fanRatingEvent']

headers["If-Modified-Since"] = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S")


def compile_events(competition_id_head='11352', competition='premier-league'):
    """
    Collects match data for events in the specified competition.

    Parameters:
    competition_id_head (str, optional): The competition ID prefix. Default is '11352'.
    competition (str, optional): The competition name or slug. Default is 'premier-league'.

    Returns:
    None

    This function retrieves match data for events in the specified competition using the SofaScore API.
    It generates event IDs, checks their validity, and compiles valid events into a DataFrame.
    The resulting DataFrame is filtered to include only specified columns ('valid_columns') and saved
    to a CSV file named '23_24_premier_league_events.csv' in the '../datasets/' directory.

    Note:
    - The function relies on external variables 'headers' and 'valid_columns' to be defined.
    - The default values for 'competition_id_head' and 'competition' are set for Premier League data.
    """

    event_id_stubs = []
    for i in range(1000):
        event_id = str(i)
        pad_length = 3 - len(event_id)
        if pad_length != 0:
            event_id = "0" * pad_length + event_id
        event_id_stubs.append(event_id)

    # test whether the event id corresponds with a valid event
    event_id_response_codes = []
    for event_id in event_id_stubs:
        event_id_response_codes.append(tuple((event_id, requests.get(
            f'https://api.sofascore.com/api/v1/event/{competition_id_head}{event_id}', headers=headers).json())))

    valid_events, invalid_events = [], []
    for event_id, event_json in event_id_response_codes:
        try:
            if event_json['event']['tournament']['slug'] == competition and event_json['event']['awayTeam']['country']['name'] == 'England':
                valid_events.append(
                    tuple((event_json['event']['event.id'], event_json)))
        except KeyError:
            invalid_events.append(tuple((event_id, event_json)))

    premier_league_events = [event[1] for event in valid_events]

    premier_league_df = pd.json_normalize(premier_league_events)
    premier_league_df = premier_league_df[valid_columns]
    premier_league_df.to_csv('/Users/harrisonward/Desktop/CS/Git/xG/datasets/23_24_premier_league_events.csv')


def update_event_df(filepath: str, headers=headers, valid_columns=None):
    """
    Updates an event DataFrame with new information from an external API.

    Parameters:
    filepath (str): The file path to the CSV containing the event data.
    valid_columns(list): list of columns in the target csv
    headers: list of headers from the users machine used to propogate the api request

    Returns:
    None

    This function reads an event DataFrame from a CSV file located at 'filepath'.
    It then checks for new events that have not started yet, fetches their updated JSON data
    from an API, and identifies events that have been marked as 'finished'.
    The completed event information is appended to the DataFrame, and rows with out-of-date
    data are dropped. Finally, the updated DataFrame is saved back to the CSV file.

    Note:
    - The 'filepath' should point to a CSV file with the following columns:
      - 'event.id': Unique identifier for each event.
      - 'event.status.type': Status of the event, e.g., 'notstarted' or 'finished'.
      - Other columns as needed for event data.
    - The function relies on external variables 'headers' and 'valid_columns' to be defined.
    """
    logging.info('Event Scraper searching for updated event info...')
    # init lists to hold updated event info
    updated_event_info, new_completed_events, new_completed_events_ids = [], [], []

    # follow the laziest possible procedure to check for new events, check every unstarted event
    event_df = pd.read_csv(filepath, index_col='Unnamed: 0')
    uncompleted_events = event_df['event.id'][event_df['event.status.type']
                                              == 'notstarted'].values

    # if the valid_columns var not provided assume its the same as the event_df
    if valid_columns is None:
        valid_columns = event_df.columns

    # fetch updated json data for the uncompleted events
    for event_id in uncompleted_events:
        updated_event_info.append(requests.get(
            f'https://api.sofascore.com/api/v1/event/{event_id}', headers=headers).json())

    # check if the event has been completed
    for event in updated_event_info:
        if event['event']['status']['type'] == 'finished':
            new_completed_events.append(event)
    
    if len(new_completed_events) == 0:
        logging.warning('WARNING: No new events found')
        logging.info('Event Scraper successfully exited\n\n\n')
        exit(0)
    
    # append the updated json info to the end of the df
    for event in new_completed_events:
        new_completed_events_ids.append(event['event']['id'])

    # drop the rows in the dataframe that have the out of date data
    event_df = event_df[~event_df['event.id'].isin(new_completed_events_ids)]

    # append the updated data to the df and save
    event_df = pd.concat([event_df, pd.json_normalize(
        new_completed_events)[valid_columns]], sort=True)
    
    # print the event_id and slug event scraped
    home_team_names = event_df['event.homeTeam.name'].loc[event_df['event.id'].isin(new_completed_events_ids)]
    away_team_names = event_df['event.awayTeam.name'].loc[event_df['event.id'].isin(new_completed_events_ids)]

    match_titles = [f'{home} vs {away}' for home,away in zip(home_team_names, away_team_names)]

    for match in match_titles:
        logging.info(f'New Event Added: {match}\n')
    
    # save and exit
    event_df.to_csv(filepath)

    logging.info(f'Event Scraper succesfully updated {len(match_titles)} new events\n')
    logging.info(f'Event Scraper succesfully exited\n')
    return 0

