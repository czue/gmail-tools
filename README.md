# gmail-tools


Tools for querying your gmail inbox.
Right now this just supports passing in a search term to your inbox, and dumping the results in a machine readable csv format for future analysis.

## Setup

See the quickstart guide for instructions on how to get setup with a gmail developer app: https://developers.google.com/gmail/api/quickstart/quickstart-python.

Save the authentication file you download as `client_secret_localhost.json`.

Run!


# Usage

This is the structure of a query:


```
./main.py [gmail search query] [max results] [filename]
```

For example, to find the last 1000 cloudant timeouts in your inbox you could run:

```
./main.py "the request could not be processed in a reasonable amount of time." 1000 cloudant-timeouts.csv
```
