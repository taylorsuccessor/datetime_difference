from fastapi import FastAPI
from app.models import DifferenceDatetimeRequest, DifferenceDatetimeResponse
from app.utls import DifferenceDatetime


app = FastAPI()


@app.post("/api/difference-between-dates")
def difference_between_dates(
    request: DifferenceDatetimeRequest,
) -> DifferenceDatetimeResponse:
    """
    to calculate the difference between two dates
    and convert it to required format
    """
    return DifferenceDatetime(request).response()
