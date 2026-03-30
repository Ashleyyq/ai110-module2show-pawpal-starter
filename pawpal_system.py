from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Pet — dataclass, holds basic info about a pet
# ---------------------------------------------------------------------------

@dataclass
class Pet:
    name: str
    species: str
    special_needs: str = ""

    def get_needs(self) -> str:
        """Return a description of the pet's special needs."""
        pass


# ---------------------------------------------------------------------------
# Task — dataclass, represents one care activity
# ---------------------------------------------------------------------------

PRIORITY_MAP = {"low": 1, "medium": 2, "high": 3}

@dataclass
class Task:
    title: str
    description: str
    duration: int          # in minutes
    frequency: str         # e.g. "daily", "twice a day"
    priority: str          # "low", "medium", or "high"

    def get_priority_score(self) -> int:
        """Convert priority string to a number for sorting (higher = more urgent)."""
        pass

    def is_feasible(self, remaining_time: int) -> bool:
        """Return True if this task can fit within the remaining time budget."""
        pass


# ---------------------------------------------------------------------------
# Owner — regular class, holds owner info and preferences
# ---------------------------------------------------------------------------

class Owner:
    def __init__(self, name: str, available_time: int, preferences: Optional[dict] = None):
        self.name = name
        self.available_time = available_time          # total minutes available today
        self.preferences: dict = preferences or {}   # e.g. {"preferred_walk_time": "morning"}

    def get_available_time(self) -> int:
        """Return the owner's total available time in minutes."""
        pass

    def update_preferences(self, prefs: dict) -> None:
        """Update owner preferences with new key-value pairs."""
        pass


# ---------------------------------------------------------------------------
# Planner — orchestrates scheduling across owner, pets, and tasks
# ---------------------------------------------------------------------------

class Planner:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.pets: list[Pet] = []
        self.tasks: list[Task] = []
        self.schedule: list[Task] = []   # final ordered plan

    def add_task(self, task: Task) -> None:
        """Add a task to the task list."""
        pass

    def remove_task(self, task: Task) -> None:
        """Remove a task from the task list."""
        pass

    def generate_plan(self) -> list[Task]:
        """Sort tasks by priority and fit them into the owner's available time."""
        pass

    def explain_plan(self) -> str:
        """Return a human-readable explanation of the generated schedule."""
        pass
