import pytest
from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date, timedelta


# --------------------------------------------------
# Test 1: Sorting Correctness
# --------------------------------------------------

def test_sorting_by_time():
    owner = Owner("Test", "test@email.com")
    pet = Pet("Mochi", "dog", 3)
    owner.add_pet(pet)

    # Add tasks OUT OF ORDER
    t1 = Task("1", "Late Task", "play", "10:30", 15, "medium")
    t2 = Task("2", "Early Task", "feeding", "08:00", 10, "high")
    t3 = Task("3", "Mid Task", "walk", "09:00", 20, "high")

    pet.add_task(t1)
    pet.add_task(t2)
    pet.add_task(t3)

    scheduler = Scheduler()
    schedule = scheduler.get_daily_schedule(owner)

    times = [task.time for _, task in schedule]

    assert times == ["08:00", "09:00", "10:30"]


# --------------------------------------------------
# Test 2: Recurrence Logic
# --------------------------------------------------

def test_recurring_task_creation():
    owner = Owner("Test", "test@email.com")
    pet = Pet("Mochi", "dog", 3)
    owner.add_pet(pet)

    task = Task(
        task_id="t1",
        title="Daily Walk",
        task_type="walking",
        time="08:00",
        duration=20,
        priority="high",
        recurrence="daily"
    )

    pet.add_task(task)

    scheduler = Scheduler()

    new_task = scheduler.mark_task_complete(owner, "Mochi", "t1")

    # Check original task is completed
    assert task.completed is True

    # Check new task exists
    assert new_task is not None
    assert new_task.due_date == date.today() + timedelta(days=1)
    assert new_task.completed is False


# --------------------------------------------------
# Test 3: Conflict Detection
# --------------------------------------------------

def test_conflict_detection():
    owner = Owner("Test", "test@email.com")
    pet1 = Pet("Mochi", "dog", 3)
    pet2 = Pet("Luna", "cat", 2)

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    # SAME TIME → should conflict
    t1 = Task("1", "Walk", "walking", "08:00", 20, "high")
    t2 = Task("2", "Feed", "feeding", "08:00", 10, "high")

    pet1.add_task(t1)
    pet2.add_task(t2)

    scheduler = Scheduler()
    schedule = scheduler.get_daily_schedule(owner)

    warnings = scheduler.get_conflict_warnings(schedule)

    assert len(warnings) > 0
    assert "08:00" in warnings[0]