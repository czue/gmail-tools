# gmail-tools


Tools for querying your gmail inbox.
Right now this just supports passing in a search term to your inbox, and dumping the results in a machine readable csv format for future analysis,
as well as some simple stats (messages by date and username).
There are multiple output files.

## Setup

See the quickstart guide for instructions on how to get setup with a gmail developer app: https://developers.google.com/gmail/api/quickstart/quickstart-python. When setting up your OAuth credentials, set Redirect URIs to 'http://localhost:8080/'.

Save the authentication file you download as `client_secret.json`.

Run!


## Usage

This is the structure of a query:


```
./main.py [gmail search query] [max results] [filename]
```

For example, to find the last 1000 messages to a particular label in your inbox you could run:

```
./main.py label:my-label 1000 mylabel-dump.csv
```
