import json
from datetime import timedelta


def daterange(start_date, end_date):
    """
    Create an iterator over the days between start and end
    Args:
        start_date (date)
        end_date (date)

    Returns: Generator yielding a date object

    """
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


class NameGetter:
    def __init__(self, fp):
        """Quick mapping between the fb id and the names."""
        self.data = json.load(open(fp))

    def __getitem__(self, item):
        return self.data[item]
