from dataclasses import dataclass, field
from datetime import date, timedelta
from collections import defaultdict


# ---------------------------------------------------------------------------
# Task — a single care activity
# ---------------------------------------------------------------------------

@dataclass
class Task:
    task_id: str
    title: str
    task_type: str
    time: str
    duration: int
    priority: str
    recurrence: str = "none"
    completed: bool = False
    pet_name: str = ""
    created_day: str = field(default_factory=lambda: date.today().strftime("%A"))
    due_date: date = field(default_factory=date.today)

    def mark_complete(self):
        """Mark the task as completed."""
        self.completed = True

    def mark_incomplete(self):
        """Mark the task as not completed."""
        self.completed = False

    def is_due_today(self) -> bool:
        """Check if the task should appear in today's schedule."""
        return self.due_date == date.today() and not self.completed

    def __str__(self) -> str:
        """Return a readable string representation of the task."""
        status = "✓" if self.completed else "○"
        pet = f"[{self.pet_name}] " if self.pet_name else ""
        return (
            f"{status} {self.time} | {pet}{self.title} "
            f"({self.duration} min, {self.priority} priority)"
        )


# ---------------------------------------------------------------------------
# Pet — stores pet details and a list of tasks
# ---------------------------------------------------------------------------

@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to the pet."""
        if any(t.task_id == task.task_id for t in self.tasks):
            raise ValueError(f"Task '{task.task_id}' already exists for {self.name}.")
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, task_id: str):
        """Remove a task by its ID."""
        original = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.task_id != task_id]
        if len(self.tasks) == original:
            raise ValueError(f"No task '{task_id}' found for {self.name}.")

    def get_task_by_id(self, task_id: str) -> Task:
        """Return a task by its ID."""
        for t in self.tasks:
            if t.task_id == task_id:
                return t
        raise ValueError(f"Task '{task_id}' not found for {self.name}.")

    def get_pending_tasks(self) -> list:
        """Return all incomplete tasks."""
        return [t for t in self.tasks if not t.completed]

    def get_completed_tasks(self) -> list:
        """Return all completed tasks."""
        return [t for t in self.tasks if t.completed]

    def get_tasks_by_type(self, task_type: str) -> list:
        """Return tasks matching a given type."""
        return [t for t in self.tasks if t.task_type == task_type]

    def get_tasks_by_priority(self, priority: str) -> list:
        """Return tasks matching a given priority."""
        return [t for t in self.tasks if t.priority == priority]

    def reset_daily_tasks(self):
        """Reset all daily recurring tasks."""
        for task in self.tasks:
            if task.recurrence == "daily":
                task.mark_incomplete()

    def summary(self) -> str:
        """Return a summary of the pet's task progress."""
        total = len(self.tasks)
        done = len(self.get_completed_tasks())
        return f"{self.name} ({self.species}, {self.age}y) — {done}/{total} tasks done"

    def __str__(self) -> str:
        """Return the pet summary string."""
        return self.summary()


# ---------------------------------------------------------------------------
# Owner — manages multiple pets and exposes all their tasks
# ---------------------------------------------------------------------------

class Owner:
    def __init__(self, name: str, email: str):
        self.name: str = name
        self.email: str = email
        self.pets: list = []

    def add_pet(self, pet: Pet):
        """Add a pet to the owner."""
        if any(p.name == pet.name for p in self.pets):
            raise ValueError(f"A pet named '{pet.name}' already exists.")
        self.pets.append(pet)

    def remove_pet(self, pet_name: str):
        """Remove a pet by name."""
        original = len(self.pets)
        self.pets = [p for p in self.pets if p.name != pet_name]
        if len(self.pets) == original:
            raise ValueError(f"No pet named '{pet_name}' found.")

    def get_pet(self, pet_name: str) -> Pet:
        """Return a pet by name."""
        for p in self.pets:
            if p.name == pet_name:
                return p
        raise ValueError(f"No pet named '{pet_name}' found.")

    def get_all_tasks(self) -> list:
        """Return all tasks across pets."""
        return [(pet.name, task) for pet in self.pets for task in pet.tasks]

    def get_all_pending_tasks(self) -> list:
        """Return all incomplete tasks across pets."""
        return [(pn, t) for pn, t in self.get_all_tasks() if not t.completed]

    def get_all_tasks_by_type(self, task_type: str) -> list:
        """Return all tasks of a given type across pets."""
        return [(pn, t) for pn, t in self.get_all_tasks() if t.task_type == task_type]

    def reset_all_daily_tasks(self):
        """Reset daily recurring tasks for all pets."""
        for pet in self.pets:
            pet.reset_daily_tasks()

    def __str__(self) -> str:
        """Return a summary of the owner."""
        return f"Owner: {self.name} ({self.email}) | {len(self.pets)} pet(s)"


# ---------------------------------------------------------------------------
# Scheduler — the brain
# ---------------------------------------------------------------------------

class Scheduler:
    """Organizes and manages tasks without storing state."""

    def get_daily_schedule(self, owner: Owner) -> list:
        """Return today's tasks sorted by time."""
        all_tasks = owner.get_all_tasks()
        due_today = [(pn, t) for pn, t in all_tasks if t.is_due_today()]
        return self.sort_by_time(due_today)

    def get_schedule_by_priority(self, owner: Owner) -> list:
        """Return today's tasks sorted by priority and time."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        due_today = [(pn, t) for pn, t in owner.get_all_tasks() if t.is_due_today()]
        return sorted(
            due_today,
            key=lambda item: (priority_order.get(item[1].priority, 9), item[1].time),
        )

    def sort_by_time(self, tasks: list) -> list:
        """Sort tasks by time."""
        return sorted(tasks, key=lambda item: item[1].time)

    def filter_by_pet(self, tasks: list, pet_name: str) -> list:
        """Filter tasks by pet."""
        return [(pn, t) for pn, t in tasks if pn == pet_name]

    def filter_by_status(self, tasks: list, completed: bool) -> list:
        """Filter tasks by completion status."""
        return [(pn, t) for pn, t in tasks if t.completed == completed]

    def filter_by_type(self, tasks: list, task_type: str) -> list:
        """Filter tasks by type."""
        return [(pn, t) for pn, t in tasks if t.task_type == task_type]

    def filter_by_priority(self, tasks: list, priority: str) -> list:
        """Filter tasks by priority."""
        return [(pn, t) for pn, t in tasks if t.priority == priority]

    def mark_task_complete(self, owner: Owner, pet_name: str, task_id: str):
        """Mark a task complete and create the next recurring task if applicable."""
        pet = owner.get_pet(pet_name)
        task = pet.get_task_by_id(task_id)
        task.mark_complete()

        if task.recurrence == "daily":
            next_due_date = task.due_date + timedelta(days=1)
        elif task.recurrence == "weekly":
            next_due_date = task.due_date + timedelta(days=7)
        else:
            return None

        new_task = Task(
            task_id=f"{task.task_id}_{next_due_date.isoformat()}",
            title=task.title,
            task_type=task.task_type,
            time=task.time,
            duration=task.duration,
            priority=task.priority,
            recurrence=task.recurrence,
            due_date=next_due_date,
        )

        pet.add_task(new_task)
        return new_task

    def detect_conflicts(self, tasks: list) -> list:
        """Find tasks scheduled at the same time."""
        buckets = defaultdict(list)
        for pet_name, task in tasks:
            buckets[task.time].append((pet_name, task))
        return [group for group in buckets.values() if len(group) > 1]

    def get_conflict_warnings(self, tasks: list) -> list:
        """Return warning messages for tasks that share the same time."""
        conflicts = self.detect_conflicts(tasks)
        warnings = []
        for group in conflicts:
            time_slot = group[0][1].time
            names = ", ".join(f"{pet_name}: {task.title}" for pet_name, task in group)
            warnings.append(f"Warning: conflict at {time_slot} -> {names}")
        return warnings

    def daily_summary(self, owner: Owner) -> str:
        """Return a formatted daily schedule with conflict warnings."""
        schedule = self.get_daily_schedule(owner)
        conflicts = self.detect_conflicts(schedule)
        conflict_times = {t.time for group in conflicts for _, t in group}

        lines = [f"=== Daily Schedule for {owner.name} ==="]
        if not schedule:
            lines.append("  No tasks due today.")
        else:
            for pet_name, task in schedule:
                warning = " ⚠ CONFLICT" if task.time in conflict_times else ""
                lines.append(f"  {task}{warning}")

        if conflicts:
            lines.append("\n⚠ Conflicts detected:")
            for group in conflicts:
                time_slot = group[0][1].time
                names = ", ".join(f"{pn}: {t.title}" for pn, t in group)
                lines.append(f"  {time_slot} → {names}")

        done = len(self.filter_by_status(schedule, completed=True))
        lines.append(f"\n{done}/{len(schedule)} tasks completed.")
        return "\n".join(lines)