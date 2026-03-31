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
    # Create Tasks
    # --------------------------------------------------
    task1 = Task(
        task_id="t1",
        title="Play Time",
        task_type="play",
        time="10:30",
        duration=15,
        priority="medium"
    )

    task2 = Task(
        task_id="t2",
        title="Morning Walk",
        task_type="walking",
        time="08:00",
        duration=20,
        priority="high",
        recurrence="daily"
    )

    task3 = Task(
        task_id="t3",
        title="Feed Breakfast",
        task_type="feeding",
        time="08:00",
        duration=10,
        priority="high"
    )

    task4 = Task(
        task_id="t4",
        title="Weekly Grooming",
        task_type="grooming",
        time="11:00",
        duration=30,
        priority="medium",
        recurrence="weekly"
    )

    # --------------------------------------------------
    # Assign Tasks to Pets
    # --------------------------------------------------
    dog.add_task(task1)
    dog.add_task(task2)

    cat.add_task(task3)
    cat.add_task(task4)

    # --------------------------------------------------
    # Create Scheduler
    # --------------------------------------------------
    scheduler = Scheduler()

    # --------------------------------------------------
    # Print today's schedule
    # --------------------------------------------------
    print("\n=== TODAY'S SCHEDULE (SORTED BY TIME) ===\n")
    schedule = scheduler.get_daily_schedule(owner)
    for pet_name, task in schedule:
        print(task)

    # --------------------------------------------------
    # Detect and print conflict warnings
    # --------------------------------------------------
    print("\n=== CONFLICT WARNINGS ===\n")
    warnings = scheduler.get_conflict_warnings(schedule)

    if warnings:
        for warning in warnings:
            print(warning)
    else:
        print("No conflicts detected.")

    # --------------------------------------------------
    # Mark recurring tasks complete
    # --------------------------------------------------
    print("\n=== MARK RECURRING TASKS COMPLETE ===\n")

    next_daily = scheduler.mark_task_complete(owner, "Mochi", "t2")
    print("Completed task: Morning Walk")
    if next_daily:
        print(
            f"Created next daily task -> {next_daily.title}, "
            f"due on {next_daily.due_date}"
        )

    next_weekly = scheduler.mark_task_complete(owner, "Luna", "t4")
    print("Completed task: Weekly Grooming")
    if next_weekly:
        print(
            f"Created next weekly task -> {next_weekly.title}, "
            f"due on {next_weekly.due_date}"
        )

    # --------------------------------------------------
    # Show all tasks after recurring automation
    # --------------------------------------------------
    print("\n=== ALL TASKS AFTER AUTOMATING RECURRING TASKS ===\n")
    for pet_name, task in owner.get_all_tasks():
        print(
            f"{task.task_id} | {pet_name} | {task.title} | "
            f"time={task.time} | due={task.due_date} | "
            f"recurrence={task.recurrence} | completed={task.completed}"
        )

    # --------------------------------------------------
    # Show today's schedule again after completion
    # --------------------------------------------------
    print("\n=== TODAY'S SCHEDULE AFTER COMPLETING RECURRING TASKS ===\n")
    updated_schedule = scheduler.get_daily_schedule(owner)
    for pet_name, task in updated_schedule:
        print(task)

    # --------------------------------------------------
    # Detailed summary
    # --------------------------------------------------
    print("\n--- DETAILED SUMMARY ---\n")
    print(scheduler.daily_summary(owner))


if __name__ == "__main__":
    main()