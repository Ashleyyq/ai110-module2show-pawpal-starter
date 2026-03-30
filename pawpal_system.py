from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Task — dataclass, represents one care activity
# ---------------------------------------------------------------------------

PRIORITY_MAP = {"low": 1, "medium": 2, "high": 3}

@dataclass
class Task:
    description: str
    duration: int               # in minutes
    frequency: str              # e.g. "daily", "twice a day"
    priority: str               # "low", "medium", or "high"
    completed: bool = False     # tracks whether this task is done

    def get_priority_score(self) -> int:
        """Convert priority string to a number for sorting (higher = more urgent)."""
        return PRIORITY_MAP.get(self.priority, 0)

    def is_feasible(self, remaining_time: int) -> bool:
        """Return True if this task can fit within the remaining time budget."""
        return self.duration <= remaining_time

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


# ---------------------------------------------------------------------------
# Pet — dataclass, stores pet details and owns a list of tasks
# ---------------------------------------------------------------------------

@dataclass
class Pet:
    name: str
    species: str
    special_needs: str = ""
    tasks: list = field(default_factory=list)   # list of Task objects belonging to this pet

    def get_needs(self) -> str:
        """Return a description of the pet's special needs."""
        if self.special_needs:
            return f"{self.name} has special needs: {self.special_needs}"
        return f"{self.name} has no special needs."

    def add_task(self, task: Task) -> None:
        """Add a care task for this pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a care task for this pet."""
        if task in self.tasks:
            self.tasks.remove(task)


# ---------------------------------------------------------------------------
# Owner — manages multiple pets and provides access to all their tasks
# ---------------------------------------------------------------------------

class Owner:
    def __init__(self, name: str, available_time: int, preferences: Optional[dict] = None):
        self.name = name
        self.available_time = available_time        # total minutes available today
        self.preferences: dict = preferences or {}  # e.g. {"preferred_walk_time": "morning"}
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list."""
        self.pets.append(pet)

    def get_available_time(self) -> int:
        """Return the owner's total available time in minutes."""
        return self.available_time

    def update_preferences(self, prefs: dict) -> None:
        """Update owner preferences with new key-value pairs."""
        self.preferences.update(prefs)

    def get_all_tasks(self) -> list[Task]:
        """Collect and return all tasks across every pet the owner has."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


# ---------------------------------------------------------------------------
# Scheduler — the "brain" that retrieves, organizes, and manages tasks
# ---------------------------------------------------------------------------

class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.schedule: list[Task] = []   # final ordered plan after generate_plan()

    def generate_plan(self) -> list[tuple]:
        """Sort all pet tasks by priority and fit as many as possible into the owner's time budget."""
        all_pairs = [(task, pet) for pet in self.owner.pets for task in pet.tasks]
        sorted_pairs = sorted(all_pairs, key=lambda pair: pair[0].get_priority_score(), reverse=True)

        remaining_time = self.owner.get_available_time()
        self.schedule = []

        for task, pet in sorted_pairs:
            if task.is_feasible(remaining_time):
                self.schedule.append((task, pet))
                remaining_time -= task.duration

        return self.schedule

    def explain_plan(self) -> str:
        """Return a human-readable schedule ranked by priority, showing pet name per task."""
        if not self.schedule:
            return "No tasks could be scheduled. Check available time or task list."

        lines = [f"Daily plan for {self.owner.name}:\n"]
        time_used = 0

        for i, (task, pet) in enumerate(self.schedule, start=1):
            lines.append(
                f"{i}. [{task.priority.upper()}] {pet.name}: {task.description} ({task.duration} min)"
            )
            time_used += task.duration

        lines.append(f"\nTotal time: {time_used} / {self.owner.available_time} min used.")
        return "\n".join(lines)
