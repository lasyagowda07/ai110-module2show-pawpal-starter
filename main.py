from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    # --------------------------------------------------
    # Create Owner
    # --------------------------------------------------
    owner = Owner(name="Lasya", email="lasya@email.com")

    # --------------------------------------------------
    # Create Pets
    # --------------------------------------------------
    dog = Pet(name="Mochi", species="dog", age=3)
    cat = Pet(name="Luna", species="cat", age=2)

    # Add pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)

    # --------------------------------------------------
    # Create Tasks (different times)
    # --------------------------------------------------
    task1 = Task(
        task_id="t1",
        title="Morning Walk",
        task_type="walking",
        time="08:00",
        duration=20,
        priority="high",
        recurrence="daily"
    )

    task2 = Task(
        task_id="t2",
        title="Feed Breakfast",
        task_type="feeding",
        time="09:00",
        duration=10,
        priority="high"
    )

    task3 = Task(
        task_id="t3",
        title="Play Time",
        task_type="play",
        time="10:30",
        duration=15,
        priority="medium"
    )

    # --------------------------------------------------
    # Assign Tasks to Pets
    # --------------------------------------------------
    dog.add_task(task1)
    dog.add_task(task2)

    cat.add_task(task3)

    # --------------------------------------------------
    # Create Scheduler
    # --------------------------------------------------
    scheduler = Scheduler()

    # --------------------------------------------------
    # Print Today's Schedule
    # --------------------------------------------------
    print("\n=== TODAY'S SCHEDULE ===\n")
    schedule = scheduler.get_daily_schedule(owner)

    for pet_name, task in schedule:
        print(f"{task}")

    # --------------------------------------------------
    # Optional: Show full summary (with conflicts)
    # --------------------------------------------------
    print("\n--- Detailed Summary ---\n")
    print(scheduler.daily_summary(owner))


if __name__ == "__main__":
    main()