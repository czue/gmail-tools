from collections import defaultdict, namedtuple
from dateutil.parser import parse


class Message(object):

    def __init__(self, date, subject, snippet, sender):
        self.date = date
        self.subject = subject
        self.snippet = snippet
        self.sender = sender

    @classmethod
    def from_api_result(cls, result):
        headers_dict = defaultdict(lambda: [])
        for h in result['payload']['headers']:
            headers_dict[h['name']].append(h['value'])

        return cls(
            date=parse(headers_dict['Date'][0]),
            sender=headers_dict['From'][0],
            subject=headers_dict['Subject'][0],
            snippet=result['snippet'],
        )

    def to_row(self):
        return [
            self.date.strftime('%Y-%m-%d %H:%M:%S'),
            self.sender.encode('utf-8'),
            self.subject.encode('utf-8'),
            self.snippet.encode('utf-8'),
        ]

    @classmethod
    def from_row(cls, row):
        return cls(
            date=parse(row[0]),
            sender=row[1],
            subject=row[2],
            snippet=row[3],
        )

    def __unicode__(self):
        return '{}: {} - {}'.format(self.date, self.sender, self.snippet)
