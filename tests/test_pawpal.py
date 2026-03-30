import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet


def test_mark_complete():
    task = Task(description="Walk around the block", duration=30, frequency="daily", priority="high")
    assert task.completed == False
    task.mark_complete()
    assert task.completed == True


def test_add_task_increases_count():
    pet = Pet(name="Mochi", species="dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task(description="Give Mochi his morning meal", duration=5, frequency="daily", priority="high"))
    assert len(pet.tasks) == 1
