from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class TripDurationInput(BaseModel):
    num_days: int = Field(..., description="The number of days for the trip.")


class TripDurationValidator(BaseTool):
    name: str = "TripDurationValidator"
    description: str = (
        "Validates whether a trip duration is too short, ideal, or too long. "
        "Input the number of days and it returns a recommendation."
    )
    args_schema: type[BaseModel] = TripDurationInput

    def _run(self, num_days: int) -> str:
        if num_days < 3:
            return (
                f"{num_days} day(s) is too short — this will only be a surface-level trip. "
                "Consider extending to at least 3 days for a meaningful experience."
            )
        elif num_days <= 10:
            return (
                f"{num_days} days is an ideal trip duration. "
                "Proceed with building a full day-by-day itinerary."
            )
        else:
            return (
                f"{num_days} days is too long for a single trip. "
                "Consider splitting into two separate trips for a better experience."
            )