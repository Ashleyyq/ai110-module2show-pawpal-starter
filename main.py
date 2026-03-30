"""Demo script for PawPal+ — tests conflict detection."""
from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler

# --- Owner ---
owner = Owner(name="Jordan", available_time=90)

# --- Pets ---
dog = Pet(name="Mochi", species="dog")
cat = Pet(name="Luna", species="cat")

owner.add_pet(dog)
owner.add_pet(cat)

today = date.today()

# Intentional conflict: both tasks at 08:00
dog.add_task(Task(
    description="Give Mochi his meal", duration=5,
    frequency="daily", priority="high",
    scheduled_time="08:00", due_date=today
))
cat.add_task(Task(
    description="Clean Luna's litter", duration=10,
    frequency="daily", priority="medium",
    scheduled_time="08:00", due_date=today  # same time as above — conflict!
))

# No conflict
dog.add_task(Task(
    description="Evening walk", duration=30,
    frequency="daily", priority="high",
    scheduled_time="18:00", due_date=today
))

# --- Generate and sort schedule ---
scheduler = Scheduler(owner)
scheduler.generate_plan()
scheduler.sort_tasks_by_time()

print("=" * 45)
print("   TODAY'S SCHEDULE")
print("=" * 45)
print(scheduler.explain_plan())

# --- Conflict detection ---
print()
print("=" * 45)
print("   CONFLICT CHECK")
print("=" * 45)
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  WARNING: {warning}")
else:
    print("  No conflicts found.")
