import re
import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def valid_time(value: str) -> bool:
    """Return True if value matches HH:MM format (e.g. 08:00)."""
    return bool(re.match(r"^\d{2}:\d{2}$", value))


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

if "owner" not in st.session_state:
    st.session_state.owner = None
if "pets" not in st.session_state:
    st.session_state.pets = []
if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

# ---------------------------------------------------------------------------
# Section 1: Owner Info
# ---------------------------------------------------------------------------

st.subheader("Owner Info")

owner_name     = st.text_input("Owner name", value="Jordan")
available_time = st.number_input("Available time today (minutes)", min_value=1, max_value=480, value=60)

if st.button("Save Owner"):
    st.session_state.owner     = Owner(name=owner_name, available_time=int(available_time))
    st.session_state.scheduler = None   # reset schedule when owner changes
    st.success(f"Saved — {owner_name} has {available_time} min today.")

st.divider()

# ---------------------------------------------------------------------------
# Section 2: Add a Pet
# ---------------------------------------------------------------------------

st.subheader("Add a Pet")

pet_name      = st.text_input("Pet name", value="Mochi")
species       = st.selectbox("Species", ["dog", "cat", "other"])
special_needs = st.text_input("Special needs (optional)", value="")

if st.button("Add Pet"):
    if st.session_state.owner is None:
        st.warning("Please save an owner first.")
    else:
        new_pet = Pet(name=pet_name, species=species, special_needs=special_needs)
        st.session_state.owner.add_pet(new_pet)
        st.session_state.pets.append(new_pet)
        st.session_state.scheduler = None   # reset schedule when pets change
        st.success(f"'{pet_name}' added.")

if st.session_state.pets:
    for pet in st.session_state.pets:
        st.write(f"- **{pet.name}** ({pet.species}) — {pet.get_needs()}")

st.divider()

# ---------------------------------------------------------------------------
# Section 3: Add a Task
# ---------------------------------------------------------------------------

st.subheader("Add a Task")

if st.session_state.pets:
    pet_options       = {pet.name: pet for pet in st.session_state.pets}
    selected_pet_name = st.selectbox("Assign task to", list(pet_options.keys()))

    task_description = st.text_input("Task description", value="Walk around the block")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col2:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col3:
        # removed "twice a day" — not supported by recurrence logic
        frequency = st.selectbox("Frequency", ["daily", "weekly"])
    with col4:
        scheduled_time = st.text_input("Time (HH:MM)", value="", placeholder="e.g. 08:00")

    if st.button("Add Task"):
        time_value = scheduled_time.strip()
        if time_value and not valid_time(time_value):
            st.error("Please enter time in HH:MM format, e.g. 08:00")
        else:
            new_task = Task(
                description    = task_description,
                duration       = int(duration),
                frequency      = frequency,
                priority       = priority,
                scheduled_time = time_value if time_value else None,
            )
            pet_options[selected_pet_name].add_task(new_task)
            st.session_state.scheduler = None   # reset schedule when tasks change
            st.success(f"Task added to {selected_pet_name}.")

    # current task list per pet
    for pet in st.session_state.pets:
        if pet.tasks:
            st.write(f"**{pet.name}'s tasks:**")
            rows = [
                {
                    "Priority": t.priority.upper(),
                    "Task": t.description,
                    "Duration (min)": t.duration,
                    "Time": t.scheduled_time or "—",
                    "Frequency": t.frequency,
                }
                for t in pet.tasks
            ]
            st.table(rows)
else:
    st.info("Add a pet first before adding tasks.")

st.divider()

# ---------------------------------------------------------------------------
# Section 4: Generate Schedule
# ---------------------------------------------------------------------------

st.subheader("Today's Schedule")

if st.button("Generate Schedule"):
    if st.session_state.owner is None:
        st.warning("Please save an owner first.")
    elif not st.session_state.pets or not st.session_state.owner.get_all_tasks():
        st.warning("Please add at least one pet and one task first.")
    else:
        scheduler = Scheduler(st.session_state.owner)
        scheduler.generate_plan()
        scheduler.sort_tasks_by_time()
        st.session_state.scheduler = scheduler
        st.success("Schedule generated!")

if st.session_state.scheduler:
    scheduler      = st.session_state.scheduler
    all_tasks      = st.session_state.owner.get_all_tasks()
    total_tasks    = len(all_tasks)
    scheduled_ids  = set(id(t) for t, _ in scheduler.schedule)
    skipped        = [t for t in all_tasks if id(t) not in scheduled_ids]

    # --- Metrics ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Tasks available", total_tasks)
    col2.metric("Tasks scheduled", len(scheduler.schedule))
    col3.metric("Tasks skipped",   len(skipped))

    # --- Conflict warnings ---
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        st.error("Schedule conflicts detected — two tasks are set at the same time:")
        for conflict in conflicts:
            st.warning(conflict)

    # --- Scheduled tasks table ---
    if scheduler.schedule:
        st.markdown("#### Scheduled Tasks")
        rows = []
        for task, pet in scheduler.schedule:
            rows.append({
                "Time":           task.scheduled_time or "—",
                "Pet":            pet.name,
                "Task":           task.description,
                "Duration (min)": task.duration,
                "Priority":       task.priority.upper(),
                "Frequency":      task.frequency,
            })
        st.table(rows)

        total_used      = sum(t.duration for t, _ in scheduler.schedule)
        total_available = scheduler.owner.available_time
        st.caption(
            f"Time used: {total_used} min / {total_available} min available "
            f"— {total_available - total_used} min remaining."
        )

    # --- Skipped tasks table ---
    if skipped:
        st.markdown("#### Skipped Tasks (did not fit in available time)")
        # build pet lookup so we can show which pet each skipped task belongs to
        task_to_pet = {id(t): p for p in st.session_state.pets for t in p.tasks}
        skipped_rows = []
        for task in skipped:
            pet = task_to_pet.get(id(task))
            skipped_rows.append({
                "Pet":            pet.name if pet else "—",
                "Task":           task.description,
                "Duration (min)": task.duration,
                "Priority":       task.priority.upper(),
                "Frequency":      task.frequency,
                "Reason":         "Not enough time",
            })
        st.table(skipped_rows)

    st.divider()

    # --- Filter tools ---
    # Build a combined list of ALL tasks (scheduled + skipped) with their pet and status
    task_to_pet  = {id(t): p for p in st.session_state.pets for t in p.tasks}
    all_with_pet = [
        (t, task_to_pet[id(t)])
        for t in st.session_state.owner.get_all_tasks()
        if id(t) in task_to_pet
    ]

    st.subheader("Filter All Tasks")
    col_a, col_b = st.columns(2)

    with col_a:
        pet_names  = ["All pets"] + [pet.name for pet in st.session_state.pets]
        filter_pet = st.selectbox("Filter by pet", pet_names)

    with col_b:
        filter_status = st.selectbox("Filter by status", ["All", "Scheduled", "Skipped", "Completed"])

    filtered = all_with_pet

    if filter_pet != "All pets":
        filtered = [(t, p) for t, p in filtered if p.name == filter_pet]

    if filter_status == "Scheduled":
        filtered = [(t, p) for t, p in filtered if id(t) in scheduled_ids]
    elif filter_status == "Skipped":
        filtered = [(t, p) for t, p in filtered if id(t) not in scheduled_ids]
    elif filter_status == "Completed":
        filtered = [(t, p) for t, p in filtered if t.completed]

    if filtered:
        filter_rows = [
            {
                "Status":         "Completed" if t.completed else ("Scheduled" if id(t) in scheduled_ids else "Skipped"),
                "Time":           t.scheduled_time or "—",
                "Pet":            p.name,
                "Task":           t.description,
                "Duration (min)": t.duration,
                "Priority":       t.priority.upper(),
            }
            for t, p in filtered
        ]
        st.table(filter_rows)
    else:
        st.info("No tasks match the selected filters.")
