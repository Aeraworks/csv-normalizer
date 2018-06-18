# csv-normalizer

Reads `Bad` data from stdin and writes `NotBad` data to stdout


## Requirements

* Python == 3.6


## To Install

No installation / venv is required;  only native libraries are utilized


## To Run

To view output in console:

`cat sample-with-broken-utf8.csv | python src/main.py`

To send to a file, for viewing the results:

`cat sample-with-broken-utf8.csv | python src/main.py > scrubbed.csv`


# Timeframe

This took me a little over 5 hours;  it's been awhile since I worked with non-`UTF-8` encodings and parsing directly from `stdin`.  I also have a penchant for going overboard with both documentation and attempting to generate re-usable modules.
