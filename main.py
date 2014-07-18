import csv
import sys
from hqgmail.client import GmailClient, get_authenticated_service
from hqgmail.message import Message


def dump_search_results(filename, query, max_results):
    client = GmailClient(get_authenticated_service())
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'time', 'hour', 'minute', 'second', 'sender', 'snippet'])
        for i, msg in enumerate(client.iter_messages(query, max_results)):
            parsed = Message.from_api_result(msg)
            writer.writerow([
                parsed.date.date(),
                parsed.date.time(),
                parsed.date.hour,
                parsed.date.minute,
                parsed.date.second,
                parsed.sender,
                parsed.snippet,
            ])
            if i % 100 == 0:
                print '{0}/{1}: {2}'.format(i, max_results, parsed.date)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'usage: ./main.py [gmail search query] [max results] [filename]'
        sys.exit(-1)
    query = sys.argv[1]
    count = int(sys.argv[2])
    filename = sys.argv[3]
    dump_search_results(filename, query, count)
