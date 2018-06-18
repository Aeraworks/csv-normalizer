""" Class export """

# Native imports
from datetime import datetime, timedelta
from typing import List, Union

class Transformer(object):
    """ Transforms row data according to a defined transformer configuration """

    def __init__(self):

        pass

    def transform(self, row: List[str], col: str,
                  transform_props: Union[dict, None]) -> str:
        """ This method calls the appropriate transform method on a value.

        Parameters
        ----------
        row : List
            A list of all columns in the row
        col : str
            The value to transform
        transform_props : Union[dict, None]
            Parameters to utilize for the transform operation

        Returns
        -------
        str
            The transformed value
        """

        if transform_props is not None: # If a transform should run...

            # If the transformation is a custom transform...
            if transform_props["transform"].startswith("custom_"):

                # Send row and column data to custom transformer method
                return getattr(self, transform_props["transform"])(row, col)

            kwargs = {} if "kwargs" not in transform_props \
                else transform_props["kwargs"]

            # Retrieve the appropriate transform method from class
            return getattr(self, transform_props["transform"])(col, **kwargs)

        return col # Return the original column value if no transform specified

    @staticmethod
    def upper(val: str) -> str:
        """ This method uppercases a string

        Parameters
        ----------
        val : str
            The string to convert to uppercase

        Returns
        -------
        str
            The string in uppercase format
        """

        # Python 3 handles uppercase for non-english characters - hooray!
        return val.upper()

    @staticmethod
    def iso8601(val: str, input_format: str,
                timedelta_hours: int=0) -> str:
        """ This method parses a timestamp, adjusts the timedelta as needed, and
        returns an ISO-8601 formatted version of the timestamp.  In the future,
        this function should probably take additional kwargs for other timedelta
        parameters.

        Parameters
        ----------
        val : str
            The timestamp to parse
        input_format : str
            A string representing the strptime input pattern to use for parsing
            See:
        timedelta_hours : int=0
            The timedelta, in hours, to apply to the original date

        Returns
        -------
        str
            An ISO-8601 formatted date, adjusted via timedelta parameters
        """

        date_val: datetime = datetime.strptime(val, input_format)

        return (date_val + timedelta(hours=timedelta_hours)).isoformat()

    @staticmethod
    def duration(val: str) -> str:
        """ This method generates a floating point second representation of a
        duration string

        Parameters
        ----------
        val : str
            A string representing a duration;  expected format is HH:MM:SS.MS

        Returns
        -------
        str
            A floating second representation of a duration, as a string

        """

        time_parts = val[0:val.index(".")].split(":")

        # 60 min/hr * 60 sec/min
        hrs_sec = int(time_parts[ 0 ]) * 60 * 60
        minutes_sec = int(time_parts[ 1 ]) * 600 # 60 sec/min

        return str(hrs_sec + minutes_sec + int(time_parts[ 2 ])) + \
            "." + val[val.index(".") + 1:]

    @staticmethod
    def zip_code(val: Union[str, int]) -> str:
        """ This method takes a zip code value and adds leading zeros as needed

        Parameters
        ----------
        val : Union[str, int]
            The zip code value to format

        Returns
        -------
        str
            The formatted zip code value, with leading zeroes attached
        """

        result: str = ""

        for dummy in range(0, (5 - len(val))):

            result += "0"

        return result + str(val)

    @classmethod
    def custom_total_duration(cls, row: List[str], val: str) -> str:
        """ This method defines a custom transformation used in the
        "TotalDuration" column.

        Parameters
        ----------
        row : List
            A list of all columns in the row
        col : str
            The value to transform

        Returns
        -------
        str
            The transformed value
        """

        return round(
            float(cls.duration(row[4])) + float(cls.duration(row[5])),
            6
        )
