import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+.

This app helps a pet owner manage pets, add care tasks, and generate a daily schedule
using the backend logic built in `pawpal_system.py`.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and recurrence.
"""
    )

with st.expander("What this app can do", expanded=True):
    st.markdown(
        """
- Add pets
- Add tasks for each pet
- View all current tasks
- Generate a sorted daily schedule
- View priority-based scheduling
- Detect time conflicts
"""
    )

# --------------------------------------------------
# Session state setup
# --------------------------------------------------

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", email="jordan@email.com")

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

# --------------------------------------------------
# Owner inputs
# --------------------------------------------------

st.divider()
st.subheader("Owner Info")

owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
owner_email = st.text_input("Owner email", value=st.session_state.owner.email)

st.session_state.owner.name = owner_name
st.session_state.owner.email = owner_email

# --------------------------------------------------
# Add pet section
# --------------------------------------------------

st.divider()
st.subheader("Add a Pet")

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
pet_age = st.number_input("Pet age", min_value=0, max_value=30, value=3)

if st.button("Add Pet"):
    try:
        new_pet = Pet(name=pet_name, species=species, age=int(pet_age))
        st.session_state.owner.add_pet(new_pet)
        st.success(f"{pet_name} added successfully.")
    except ValueError as e:
        st.error(str(e))

if st.session_state.owner.pets:
    st.markdown("### Current Pets")
    for pet in st.session_state.owner.pets:
        st.write(pet.summary())
else:
    st.info("No pets added yet.")

# --------------------------------------------------
# Add task section
# --------------------------------------------------

st.divider()
st.subheader("Add a Task")

if st.session_state.owner.pets:
    pet_names = [pet.name for pet in st.session_state.owner.pets]

    selected_pet = st.selectbox("Choose pet", pet_names)
    task_title = st.text_input("Task title", value="Morning walk")
    task_type = st.selectbox(
        "Task type",
        ["feeding", "walking", "medication", "grooming", "play"]
    )
    task_time = st.text_input("Task time (HH:MM)", value="08:00")
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    recurrence = st.selectbox("Recurrence", ["none", "daily", "weekly"])

    if st.button("Add Task"):
        try:
            pet = st.session_state.owner.get_pet(selected_pet)
            task_id = f"{selected_pet}_{task_title}_{task_time}"

            task = Task(
                task_id=task_id,
                title=task_title,
                task_type=task_type,
                time=task_time,
                duration=int(duration),
                priority=priority,
                recurrence=recurrence,
            )

            pet.add_task(task)
            st.success(f"Task added for {selected_pet}.")
        except ValueError as e:
            st.error(str(e))
else:
    st.info("Add at least one pet before adding tasks.")

# --------------------------------------------------
# Show current tasks
# --------------------------------------------------

st.divider()
st.subheader("Current Tasks")

all_tasks = st.session_state.owner.get_all_tasks()

if all_tasks:
    task_rows = []
    for pet_name, task in all_tasks:
        task_rows.append(
            {
                "Pet": pet_name,
                "Title": task.title,
                "Type": task.task_type,
                "Time": task.time,
                "Duration": task.duration,
                "Priority": task.priority,
                "Recurrence": task.recurrence,
                "Due Date": str(task.due_date),
                "Completed": task.completed,
            }
        )
    st.table(task_rows)
else:
    st.info("No tasks yet. Add one above.")

# --------------------------------------------------
# Build schedule
# --------------------------------------------------

st.divider()
st.subheader("Build Schedule")

schedule_view = st.radio(
    "Choose schedule view",
    ["Sorted by Time", "Sorted by Priority"],
    horizontal=True
)

if st.button("Generate Schedule"):
    scheduler = st.session_state.scheduler
    owner = st.session_state.owner

    if schedule_view == "Sorted by Time":
        schedule = scheduler.get_daily_schedule(owner)
    else:
        schedule = scheduler.get_schedule_by_priority(owner)

    warnings = scheduler.get_conflict_warnings(schedule)

    if schedule:
        st.success("Schedule generated successfully.")

        schedule_rows = []
        for pet_name, task in schedule:
            schedule_rows.append(
                {
                    "Time": task.time,
                    "Pet": pet_name,
                    "Task": task.title,
                    "Type": task.task_type,
                    "Duration": task.duration,
                    "Priority": task.priority,
                    "Recurrence": task.recurrence,
                }
            )

        st.markdown("### Today's Schedule")
        st.table(schedule_rows)

        high_priority = scheduler.filter_by_priority(schedule, "high")
        if high_priority:
            st.markdown("### High Priority Tasks")
            for pet_name, task in high_priority:
                st.write(f"• {task.time} — {pet_name}: {task.title}")

    else:
        st.info("No tasks due today.")

    if warnings:
        st.markdown("### Conflict Warnings")
        for warning in warnings:
            st.warning(warning)

    st.markdown("### Schedule Summary")
    st.text(scheduler.daily_summary(owner))