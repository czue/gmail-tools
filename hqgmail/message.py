from collections import defaultdict
from dateutil.parser import parse


class Message(object):

    def __init__(self, date, snippet, sender):
        self.date = date
        self.snippet = snippet
        self.sender = sender

    @classmethod
    def from_api_result(cls, result):
        headers_dict = defaultdict(lambda: [])
        for h in result['payload']['headers']:
            headers_dict[h['name']].append(h['value'])

        return cls(
            date=parse(headers_dict['Date'][0]),
            snippet=result['snippet'],
            sender=headers_dict['From'][0],
        )

