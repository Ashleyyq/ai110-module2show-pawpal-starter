"""Tests for PawPal+ scheduling logic."""
import sys
import os
from datetime import date, timedelta
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet, Owner, Scheduler


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_owner(minutes=120):
    """Return a basic Owner with the given available time."""
    return Owner(name="Jordan", available_time=minutes)


def make_task(description="Walk", duration=10, frequency="daily",
              priority="medium", scheduled_time=None, due_date=None):
    """Return a Task with sensible defaults."""
    return Task(
        description=description,
        duration=duration,
        frequency=frequency,
        priority=priority,
        scheduled_time=scheduled_time,
        due_date=due_date,
    )


# ---------------------------------------------------------------------------
# Original tests
# ---------------------------------------------------------------------------

def test_mark_complete():
    """Task starts incomplete and flips to complete after mark_complete()."""
    task = make_task()
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_count():
    """Adding a task to a pet increases its task list by one."""
    pet = Pet(name="Mochi", species="dog")
    assert len(pet.tasks) == 0
    pet.add_task(make_task())
    assert len(pet.tasks) == 1


# ---------------------------------------------------------------------------
# Sorting correctness
# ---------------------------------------------------------------------------

def test_sort_tasks_by_time_chronological():
    """Tasks added out of order come out in chronological order after sorting."""
    owner = make_owner()
    dog = Pet(name="Mochi", species="dog")
    owner.add_pet(dog)

    dog.add_task(make_task(description="Evening walk",   scheduled_time="18:00", priority="high"))
    dog.add_task(make_task(description="Morning meal",   scheduled_time="08:00", priority="high"))
    dog.add_task(make_task(description="Midday check",   scheduled_time="12:00", priority="high"))

    scheduler = Scheduler(owner)
    scheduler.generate_plan()
    scheduler.sort_tasks_by_time()

    times = [task.scheduled_time for task, _ in scheduler.schedule]
    assert times == sorted(times), f"Expected sorted times but got {times}"


def test_sort_pushes_untimed_tasks_to_end():
    """Tasks without a scheduled_time appear after all timed tasks."""
    owner = make_owner()
    dog = Pet(name="Mochi", species="dog")
    owner.add_pet(dog)

    dog.add_task(make_task(description="No time task",  scheduled_time=None,    priority="high"))
    dog.add_task(make_task(description="Morning meal",  scheduled_time="08:00", priority="high"))

    scheduler = Scheduler(owner)
    scheduler.generate_plan()
    scheduler.sort_tasks_by_time()

    last_task, _ = scheduler.schedule[-1]
    assert last_task.scheduled_time is None


# ---------------------------------------------------------------------------
# Recurrence logic
# ---------------------------------------------------------------------------

def test_daily_task_creates_next_occurrence():
    """Marking a daily task complete creates a new task due the next day."""
    today = date.today()
    task = make_task(frequency="daily", due_date=today)
    next_task = task.next_occurrence()

    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.completed is False


def test_weekly_task_creates_next_occurrence():
    """Marking a weekly task complete creates a new task due 7 days later."""
    today = date.today()
    task = make_task(frequency="weekly", due_date=today)
    next_task = task.next_occurrence()

    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=7)


def test_non_recurring_task_returns_none():
    """A task with an unrecognized frequency returns None for next_occurrence()."""
    task = make_task(frequency="twice a day")
    assert task.next_occurrence() is None


def test_mark_task_complete_adds_next_to_pet():
    """Scheduler.mark_task_complete() auto-adds the next occurrence to the pet."""
    owner = make_owner()
    dog = Pet(name="Mochi", species="dog")
    owner.add_pet(dog)

    today = date.today()
    dog.add_task(make_task(frequency="daily", due_date=today, priority="high"))

    scheduler = Scheduler(owner)
    scheduler.generate_plan()

    task, pet = scheduler.schedule[0]
    scheduler.mark_task_complete(task, pet)

    assert len(dog.tasks) == 2                           # original + new occurrence
    assert dog.tasks[1].due_date == today + timedelta(days=1)


# ---------------------------------------------------------------------------
# Conflict detection
# ---------------------------------------------------------------------------

def test_detect_conflict_same_time():
    """Two tasks at the same scheduled_time should produce a conflict warning."""
    owner = make_owner()
    dog = Pet(name="Mochi", species="dog")
    cat = Pet(name="Luna",  species="cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(make_task(description="Feed Mochi", scheduled_time="08:00", priority="high"))
    cat.add_task(make_task(description="Feed Luna",  scheduled_time="08:00", priority="high"))

    scheduler = Scheduler(owner)
    scheduler.generate_plan()
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]


def test_no_conflict_different_times():
    """Tasks at different times should produce no conflict warnings."""
    owner = make_owner()
    dog = Pet(name="Mochi", species="dog")
    owner.add_pet(dog)

    dog.add_task(make_task(description="Morning meal", scheduled_time="08:00", priority="high"))
    dog.add_task(make_task(description="Evening walk", scheduled_time="18:00", priority="high"))

    scheduler = Scheduler(owner)
    scheduler.generate_plan()

    assert scheduler.detect_conflicts() == []


def test_no_conflict_for_untimed_tasks():
    """Tasks with no scheduled_time should never be flagged as conflicts."""
    owner = make_owner()
    dog = Pet(name="Mochi", species="dog")
    owner.add_pet(dog)

    dog.add_task(make_task(description="Task A", scheduled_time=None, priority="high"))
    dog.add_task(make_task(description="Task B", scheduled_time=None, priority="high"))

    scheduler = Scheduler(owner)
    scheduler.generate_plan()

    assert scheduler.detect_conflicts() == []


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_empty_pet_no_crash():
    """A pet with no tasks should produce an empty schedule without crashing."""
    owner = make_owner()
    owner.add_pet(Pet(name="Mochi", species="dog"))

    scheduler = Scheduler(owner)
    scheduler.generate_plan()

    assert scheduler.schedule == []


def test_zero_available_time_schedules_nothing():
    """An owner with zero minutes available should get an empty schedule."""
    owner = make_owner(minutes=0)
    dog = Pet(name="Mochi", species="dog")
    owner.add_pet(dog)
    dog.add_task(make_task(duration=10, priority="high"))

    scheduler = Scheduler(owner)
    scheduler.generate_plan()

    assert scheduler.schedule == []
