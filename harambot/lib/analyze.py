import json
import numpy as np
import pandas as pd
import datetime


def read(fp, keep_event=False):
    """
    Read the json file and only keep messages and events if selected.
    Args:
        fp (str): filepath to the json file
        keep_event (boolean): Keep 'event' type or not (Can cause error to parse senderID)

    Returns: DataFrame

    """
    columns = ['body', 'type', 'senderID', 'timestamp', 'messageReactions'] + (['eventData'] if keep_event else [])
    accepted_types = ['message'] + (['event'] if keep_event else [])
    dt = pd.DataFrame(json.load(open(fp)))
    dt = dt[columns]
    dt = dt[np.isin(dt.type, accepted_types)]
    return dt


def get_first_message(dt):
    """
    Get the first message for each user
    Args:
        dt (Dataframe): result from `read`

    Returns: Dataframe with the first message

    """
    dt = dt.sort_values('timestamp').groupby('senderID').first()
    dt = dt.sort_values('timestamp')
    dt['timestamp'] = dt['timestamp'].apply(lambda k: datetime.datetime.fromtimestamp(int(k) / 1000.))
    return dt
