import pandas as pd

# import the events df 
events_df = pd.read_csv('/Users/harrisonward/Desktop/CS/Git/xG/datasets/23_24_premier_league_events.csv')

# store the events that have happend 
finished_event_ids = events_df['event_id'][events_df['event.status.type']=='finished']

# write the events to a csv
finished_event_ids.to_csv('/Users/harrisonward/Desktop/CS/Git/xG/datasets/23_24_finished_events.csv')