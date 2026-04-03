from typing import Optional, Literal
from openenv.core.env_server.types import Action, Observation
from pydantic import Field

class TicketAction(Action): # (Keeping name for compatibility with existing create_app call, or I'll update app.py too)
    food: Literal["burger", "salad", "rice"]


class TicketObservation(Observation): # (Keeping name for compatibility)
    hunger: int = Field(ge=0, le=10)
    budget: int = Field(ge=0, le=100)
    health: int = Field(ge=0, le=10)
    info: Optional[dict] = None