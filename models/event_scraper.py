import datetime
import requests
import pandas as pd
import numpy as np


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

headers["If-Modified-Since"] = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S")


def compile_events(competition_id_head='11352', competition='premier-league'):
    """A function desgined to collect all match data for events in the specified competition"""

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
            if event_json['event']['tournament']['slug'] == competition:
                valid_events.append(tuple((event_id, event_json)))
        except KeyError:
            invalid_events.append(tuple((event_id, event_json)))

    for event_id, event_json in valid_events:
        event_json['event_id'] = f'{competition_id_head}{event_id}'

    premier_league_events = [event_json for event_id, event_json in valid_events]

    valid_columns = "event_id, event.tournament.uniqueTournament.hasEventPlayerStatistics, event.season.name, event.season.year, event.season.id, event.roundInfo.round, event.customId, event.status.code, event.status.description, event.status.type, event.winnerCode, event.attendance, event.venue.city.name, event.venue.stadium.name, event.venue.stadium.capacity, event.venue.id, event.referee.name, event.referee.slug, event.referee.yellowCards, event.referee.redCards, event.referee.yellowRedCards, event.referee.games, event.referee.id, event.referee.country.alpha2, event.referee.country.name, event.homeTeam.name, event.homeTeam.slug, event.homeTeam.shortName, event.homeTeam.userCount, event.homeTeam.manager.name, event.homeTeam.manager.slug, event.homeTeam.manager.id, event.homeTeam.manager.country.alpha2, event.homeTeam.manager.country.name, event.homeTeam.venue.city.name, event.homeTeam.venue.stadium.name, event.homeTeam.venue.stadium.capacity, event.homeTeam.venue.id, event.homeTeam.venue.country.alpha2, event.homeTeam.venue.country.name, event.homeTeam.nameCode, event.homeTeam.disabled, event.homeTeam.national, event.homeTeam.type, event.homeTeam.id, event.homeTeam.country.alpha2, event.homeTeam.country.name, event.homeTeam.subTeams, event.homeTeam.fullName, event.homeTeam.teamColors.primary, event.homeTeam.teamColors.secondary, event.homeTeam.teamColors.text, event.homeTeam.foundationDateTimestamp, event.awayTeam.name, event.awayTeam.slug, event.awayTeam.shortName, event.awayTeam.userCount, event.awayTeam.manager.name, event.awayTeam.manager.slug, event.awayTeam.manager.id, event.awayTeam.manager.country.alpha2, event.awayTeam.manager.country.name, event.awayTeam.venue.city.name, event.awayTeam.venue.stadium.name, event.awayTeam.venue.stadium.capacity, event.awayTeam.venue.id, event.awayTeam.venue.country.alpha2, event.awayTeam.venue.country.name, event.awayTeam.nameCode, event.awayTeam.type, event.awayTeam.id, event.awayTeam.country.alpha2, event.awayTeam.country.name, event.awayTeam.subTeams, event.awayTeam.fullName, event.awayTeam.teamColors.primary, event.awayTeam.teamColors.secondary, event.awayTeam.teamColors.text, event.awayTeam.foundationDateTimestamp, event.homeScore.current, event.homeScore.display, event.homeScore.period1, event.homeScore.period2, event.homeScore.normaltime, event.awayScore.current, event.awayScore.display, event.awayScore.period1, event.awayScore.period2, event.awayScore.normaltime, event.time.injuryTime1, event.time.injuryTime2, event.time.currentPeriodStartTimestamp, event.changes.changes, event.changes.changeTimestamp, event.hasGlobalHighlights, event.hasXg, event.hasEventPlayerStatistics, event.hasEventPlayerHeatMap, event.detailId, event.crowdsourcingDataDisplayEnabled, event.id, event.defaultPeriodCount, event.defaultPeriodLength, event.currentPeriodStartTimestamp, event.startTimestamp, event.slug, event.finalResultOnly, event.fanRatingEvent, event.homeRedCards, event.awayRedCards".split(
        ', ')

    premier_league_df = pd.json_normalize(premier_league_events)
    premier_league_df = premier_league_df[valid_columns]
    premier_league_df.to_csv('../datasets/23_24_premier_league_events.csv')


def refresh_events(filepath, competition_id_head='11352', competition='premier-league'):
    """Function to check the status of pre-fetched events in the events dataframe"""
    
    updated_event_info, new_completed_events = [], []
    # load the precompiled events df and check which events still haven't been completed
    event_df = pd.read_csv(filepath)
    uncompleted_events = event_df['event.id'][event_df['event.status.type']=='notstarted'].values

    # fetch updated json data for the uncompleted events
    for event_id in uncompleted_events:
        updated_event_info.append(requests.get(
            f'https://api.sofascore.com/api/v1/event/{competition_id_head}{event_id}', headers=headers).json())

    # check if the event has been completed 
    for event in updated_event_info:
        if event['event']['status']['type'] == 'finished':
            new_completed_events.append(event)
    
    # replace the data in event df with new data
    for event in updated_event_info:
        event_id = event['event']['event.id']

        

    