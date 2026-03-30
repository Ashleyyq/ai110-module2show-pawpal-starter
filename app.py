import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# ---------------------------------------------------------------------------
# Session state — initialize once, persist across reruns
# ---------------------------------------------------------------------------

if "owner" not in st.session_state:
    st.session_state.owner = None

if "pets" not in st.session_state:
    st.session_state.pets = []

if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

# ---------------------------------------------------------------------------
# Section 1: Owner setup
# ---------------------------------------------------------------------------

st.subheader("Owner Info")

owner_name = st.text_input("Owner name", value="Jordan")
available_time = st.number_input("Available time today (minutes)", min_value=1, max_value=480, value=60)

if st.button("Save Owner"):
    st.session_state.owner = Owner(name=owner_name, available_time=int(available_time))
    st.success(f"Owner '{owner_name}' saved with {available_time} minutes available.")

st.divider()

# ---------------------------------------------------------------------------
# Section 2: Add a pet
# ---------------------------------------------------------------------------

st.subheader("Add a Pet")

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
special_needs = st.text_input("Special needs (optional)", value="")

if st.button("Add Pet"):
    if st.session_state.owner is None:
        st.warning("Please save an owner first.")
    else:
        new_pet = Pet(name=pet_name, species=species, special_needs=special_needs)
        st.session_state.owner.add_pet(new_pet)
        st.session_state.pets.append(new_pet)
        st.success(f"Pet '{pet_name}' added.")

if st.session_state.pets:
    st.write("Current pets:")
    for pet in st.session_state.pets:
        needs = pet.get_needs()
        st.write(f"- **{pet.name}** ({pet.species}) — {needs}")

st.divider()

# ---------------------------------------------------------------------------
# Section 3: Add a task to a pet
# ---------------------------------------------------------------------------

st.subheader("Add a Task")

if st.session_state.pets:
    pet_options = {pet.name: pet for pet in st.session_state.pets}
    selected_pet_name = st.selectbox("Assign task to", list(pet_options.keys()))

    col1, col2, col3 = st.columns(3)
    with col1:
        task_description = st.text_input("Task description", value="Walk around the block")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    frequency = st.selectbox("Frequency", ["daily", "twice a day", "weekly"])

    if st.button("Add Task"):
        new_task = Task(
            description=task_description,
            duration=int(duration),
            frequency=frequency,
            priority=priority,
        )
        pet_options[selected_pet_name].add_task(new_task)
        st.success(f"Task added to {selected_pet_name}.")

    # show all current tasks per pet
    for pet in st.session_state.pets:
        if pet.tasks:
            st.write(f"**{pet.name}'s tasks:**")
            for task in pet.tasks:
                st.write(f"  - [{task.priority.upper()}] {task.description} ({task.duration} min, {task.frequency})")
else:
    st.info("Add a pet first before adding tasks.")

st.divider()

# ---------------------------------------------------------------------------
# Section 4: Generate schedule
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
        st.session_state.scheduler = scheduler
        st.success("Schedule generated!")

if st.session_state.scheduler:
    st.text(st.session_state.scheduler.explain_plan())
