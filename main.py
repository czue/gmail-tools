#!/usr/bin/env python
from collections import defaultdict

import csv
import json
import sys
from hqgmail.client import GmailClient, get_authenticated_service
from hqgmail.message import Message


def dump_search_results(filename, query, max_results):
    client = GmailClient(get_authenticated_service())
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'sender', 'subject', 'snippet'])
        for i, msg in enumerate(client.iter_messages(query, max_results)):
            parsed = Message.from_api_result(msg)
            try:
                writer.writerow(parsed.to_row())
            except Exception as e:
                print u'error with message {}: e'.format(parsed)
            if i % 100 == 0:
                print '{0}/{1}: {2}'.format(i, max_results, parsed.date)


def dump_raw_verbose(input_filename, output_filename):
    with open(input_filename, 'rb') as f_in:
        reader = csv.reader(f_in)
        with open(output_filename, 'wb') as f_out:
            writer = csv.writer(f_out)
            writer.writerow(['date', 'time', 'hour', 'minute', 'second', 'sender', 'subject', 'snippet', 'short_subject', 'short_snippet'])
            first = True
            for i, row in enumerate(reader):
                if first:
                    first = False
                    continue
                parsed = Message.from_row(row)
                try:
                    writer.writerow([
                        parsed.date.date(),
                        parsed.date.time(),
                        parsed.date.hour,
                        parsed.date.minute,
                        parsed.date.second,
                        parsed.sender,
                        parsed.subject,
                        parsed.snippet,
                        parsed.subject[:50],
                        parsed.snippet[:50],
                    ])
                except Exception as e:
                    print u'error with message {}: e'.format(parsed)


def dump_stats(filename):
    by_email = defaultdict(lambda: 0)
    by_date = defaultdict(lambda: 0)
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        first = True
        for i, row in enumerate(reader):
            if first:
                first = False
            else:
                parsed = Message.from_row(row)
                by_email[parsed.sender] += 1
                by_date[parsed.date.date().isoformat()] += 1

    with open('user-{}'.format(filename), 'wb') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(['email', 'count'])
        for email in sorted(by_email.keys()):
            writer.writerow([email, by_email[email]])

    with open('date-{}'.format(filename), 'wb') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(['date', 'count'])
        for date in sorted(by_date.keys()):
            writer.writerow([date, by_date[date]])

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'usage: ./main.py [gmail search query] [max results] [filename]'
        sys.exit(-1)
    query = sys.argv[1]
    count = int(sys.argv[2])
    filename = sys.argv[3]
    dump_search_results(filename, query, count)
    dump_raw_verbose(filename, 'verbose-{}'.format(filename))
    dump_stats(filename)
