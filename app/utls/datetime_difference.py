import numpy as np
from typing import Callable
from app.models import (
    ResponseType,
    DifferenceDatetimeResponse,
    DifferenceDatetimeRequest,
)


class DifferenceDatetime:

    seconds_converter_formila: dict[ResponseType, Callable[[float], float]] = {
        ResponseType.SECONDS: lambda v: v,
        ResponseType.MINUTES: lambda v: v / 60,
        ResponseType.HOURS: lambda v: v / (60 * 60),
        ResponseType.DAYS: lambda v: v / (60 * 60 * 24),
        ResponseType.WEEKS: lambda v: v / (60 * 60 * 24 * 7),
        ResponseType.YEARS: lambda v: v / (60 * 60 * 24 * 364),
    }

    def __init__(self, input_data: DifferenceDatetimeRequest):
        self.input_data = input_data
        self.seconds_different = (
            input_data.to_datetime - input_data.from_datetime
        ).total_seconds()

    def get_days_different(self) -> float:
        """
        this method takes the different in seconds
        that we saved on the constructor then
        convert it to the target requered out put
        the default output is days but the request
        can convert it to any other type of units
        """
        return self._format_output(self.seconds_different, ResponseType.DAYS)

    def get_weekdays_different(self) -> float:

        """
        this function uses numpy built in function busday_count
        https://numpy.org/doc/stable/reference/generated/numpy.busday_count.html
        then we convert it to second after that we give the required output
        the default is days
        """
        from_date = self.input_data.from_datetime.strftime("%Y-%m-%d")
        to_date = self.input_data.to_datetime.strftime("%Y-%m-%d")
        weekdays_seconds = np.busday_count(from_date, to_date) * (60 * 60 * 24)
        return self._format_output(weekdays_seconds, ResponseType.DAYS)

    def get_weeks_different(self) -> float:
        """
        this method takes the different in seconds
        that we saved on the constructor then
        convert it to the target requered out put
        the default output is weeks but the request
        can convert it to any other type of units
        """
        return self._format_output(self.seconds_different, ResponseType.WEEKS)

    def _format_output(self, value, convert_to) -> float:
        """
        return the required output format (seconds, minutes ...)
        using seconds_converter_formila to convert seconds
        if the request contains one unit to convert the response to
        it will take it otherwise it will take convert_to that
        passed to the function
        """
        convert_to = (
            self.input_data.response_type
            if self.input_data.response_type
            else convert_to
        )
        return round(self.seconds_converter_formila[convert_to](value), 3)

    def response(self) -> DifferenceDatetimeResponse:
        """
        build the response model to be return to the client
        """
        return DifferenceDatetimeResponse(
            days_number=self.get_days_different(),
            weekdays_number=self.get_weekdays_different(),
            weeks_number=self.get_weeks_different(),
        )
