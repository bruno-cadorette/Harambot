import datetime
import json
from collections import defaultdict

import numpy as np
import pandas as pd

from harambot.lib.utils import daterange


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


def get_cumsum(dt):
    dt = dt.sort_values('timestamp').groupby('senderID')
    cumsum_data = {}
    msg_count = defaultdict(list)
    msg_per_day = defaultdict(lambda: defaultdict(list))
    all_timestamps = []

    # Message per user per day
    for senderId in dt.groups.keys():
        msgs = dt.get_group(senderId)
        for msg in msgs.values:
            txt, type, _, timestamp, reactions, = msg
            timestamp = datetime.datetime.fromtimestamp(int(timestamp) / 1000.).date()
            all_timestamps.append(timestamp)
            msg_per_day[senderId][timestamp].append((txt, reactions))
    start = min(all_timestamps)
    end = max(all_timestamps)

    # Get the count per user per day between `start` and `end`
    for date in daterange(start, end):
        for senderId in dt.groups.keys():
            msg_count[senderId].append(len(msg_per_day[senderId][date]))

    # Compute the cumsum
    for senderId, count in msg_count.items():
        cumsum_data[senderId] = np.cumsum(count)

    return cumsum_data, list(daterange(start, end))


def get_emote_per_user(dt):
    """
    Get the emotes received and given by each user
    Args:
        dt (Dataframe): data from `read`

    Returns:
        (Dataframe, Dataframe), received and given count
    """
    dt = dt.sort_values('timestamp').groupby('senderID')
    emotes_per_person_received = defaultdict(lambda: defaultdict(int))
    emotes_per_person_given = defaultdict(lambda: defaultdict(int))
    for senderId in dt.groups.keys():
        msgs = dt.get_group(senderId)
        for msg in msgs.values:
            txt, type, _, timestamp, reactions, = msg
            for react in reactions:
                emotes_per_person_received[senderId][react['reaction']] += 1
                emotes_per_person_given[react['userID']][react['reaction']] += 1
    return pd.DataFrame.from_dict(emotes_per_person_received), pd.DataFrame.from_dict(emotes_per_person_given)
