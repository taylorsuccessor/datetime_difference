from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ResponseType(str, Enum):
    SECONDS = "seconds"
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"
    WEEKS = "weeks"
    YEARS = "years"


class DifferenceDatetimeRequest(BaseModel):
    from_datetime: datetime = Field(
        ..., example="2022-04-01T00:00:00+05:00", description="Datetime with timezone"
    )
    to_datetime: datetime = Field(
        ..., example="2022-04-01T00:00:00+00:00", description="Datetime with timezone"
    )
    response_type: Optional[ResponseType] = Field(
        example=",".join([t.value for t in ResponseType]),
        description="type of response",
    )


class DifferenceDatetimeResponse(BaseModel):
    days_number: float
    weekdays_number: float
    weeks_number: float
