"""
This file expects "bad" CSV data via stdin in the format specified by the
schema in the `schema.json` file located in the project's `src/` directory.
"""

# Native imports
import codecs
import csv
import json
import io
import os
import platform
import sys
from typing import List, Union

# Module imports
from transformer import Transformer

def get_schema(file_name: str):
    """ This method retrieves the schema from a JSON configuration file.

    Parameters
    ----------
    file_name : str
        The name of the configuration file

    Returns
    -------
    dict
        The contents of the JSON file as a dictionary
    """

    # For our Windows friends
    delimiter: str = "/" if platform.system() is not "Windows" else "\\"

    # Get path to this file, regardless of where the program ran from
    root: str = delimiter.join(os.path.realpath(__file__).split(delimiter)[:-1])
    config: Union[dict, None] = None

    with open(delimiter.join([root, file_name, ])) as file:

        config = json.load(file)

    return config


def output(line: str) -> None:
    """ This method defines the output target for the operation.  It resides
    within a separate function to allow output redirection in the future per
    changing requirements.

    Parameters
    ----------
    line : str
        The line to send to an output source
    """

    # Using stdout.write because print will add a newline, but the
    # csv.writer has already created one
    sys.stdout.write(line)


if __name__ == "__main__": # Direct script execution

    SCHEMA: dict = get_schema("schema.json")
    TRANSFORMER: Transformer = Transformer()

    for row_index, line in enumerate(sys.stdin.buffer):

        safe_line: str = line.decode("utf-8", "replace") # Replace bad chars
        capture: io.StringIO = io.StringIO() # Simulate file-like object

        # This handles comma-separated values nested in quotes
        for row in csv.reader([safe_line]):

            writer: csv.writer = csv.writer(capture) # Construct csv writer

            if row_index > 0 or not SCHEMA["headers"]: # If not the header...

                processed: List = [] # Stores processed row data

                for col_index, col in enumerate(row): # For all columns...

                    try:
                        processed.append(str(TRANSFORMER.transform(
                            row, col, SCHEMA["columns"][col_index],
                        )))

                    except Exception as err:

                        sys.stderr.write(" ".join([
                            "Unable to process row {0}, col {1}:".format(
                                row_index, col_index
                            ),
                            "{0}\n".format(str(err))
                        ]))
                        processed = None # Skip the row on bad data

                        break
            else:
                processed = row # Write header row as-is

            if processed: # If no error occurred...

                writer.writerow(processed) # Write row to file-like object
                output(capture.getvalue()) # Send line data to output method
