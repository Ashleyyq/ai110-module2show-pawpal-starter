from pawpal_system import Task, Pet, Owner, Scheduler

# --- Owner ---
owner = Owner(name="Jordan", available_time=60)

# --- Pets ---
dog = Pet(name="Mochi", species="dog", special_needs="needs 2 walks a day")
cat = Pet(name="Luna", species="cat")

owner.add_pet(dog)
owner.add_pet(cat)

# --- Tasks for Mochi ---
dog.add_task(Task(description="Walk around the block", duration=30, frequency="daily", priority="high"))
dog.add_task(Task(description="Give Mochi his morning meal", duration=5, frequency="daily", priority="high"))
dog.add_task(Task(description="Brush Mochi's coat", duration=20, frequency="weekly", priority="low"))

# --- Tasks for Luna ---
cat.add_task(Task(description="Clean Luna's litter box", duration=10, frequency="daily", priority="medium"))
cat.add_task(Task(description="Play with Luna using a feather toy", duration=15, frequency="daily", priority="low"))

# --- Generate and print schedule ---
scheduler = Scheduler(owner)
scheduler.generate_plan()

print("=" * 40)
print("        TODAY'S SCHEDULE")
print("=" * 40)
print(scheduler.explain_plan())
print("=" * 40)
