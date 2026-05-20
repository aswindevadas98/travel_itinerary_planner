import os
import warnings

from travel_itinerary_planner.crew import TravelItineraryPlanner

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run_crew(destination: str, trip_duration: int, interests: str) -> dict:
    """
    Run the TravelItineraryPlanner crew with the given inputs.
    Returns a dict with each task's output.
    """
    os.makedirs("output", exist_ok=True)

    inputs = {
        "destination": destination,
        "trip_duration": trip_duration,
        "interests": interests,
    }

    result = TravelItineraryPlanner().crew().kickoff(inputs=inputs)

    return {
        "destination_brief": result.tasks_output[0].raw,
        "day_by_day_plan":   result.tasks_output[1].raw,
        "budget_breakdown":  result.tasks_output[2].raw,
    }