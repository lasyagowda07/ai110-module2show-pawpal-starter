from dataclasses import dataclass, field
from datetime import date


# ---------------------------------------------------------------------------
# Task — smallest unit of work for a pet
# ---------------------------------------------------------------------------

@dataclass
class Task:
    task_id: str
    title: str
    task_type: str          # "feeding", "walking", "medication", etc.
    time: str               # 24h format, e.g. "08:00"
    duration: int           # minutes
    priority: str           # "low", "medium", "high"
    recurrence: str = "none"  # "none", "daily", "weekly"
    completed: bool = False

    def mark_complete(self):
        """Mark this task as done."""
        self.completed = True

    def is_due_today(self) -> bool:
        """Return True if this task should appear in today's schedule."""
        if self.recurrence == "daily":
            return True
        if self.recurrence == "weekly":
            # Due on the same weekday it was originally set
            # TODO: store and compare the original weekday
            return True
        return not self.completed  # "none" recurrence: show until completed

    def __str__(self) -> str:
        status = "done" if self.completed else "pending"
        return f"{self.time} | {self.title} ({self.duration} min) [{self.priority}] [{status}]"


# ---------------------------------------------------------------------------
# Pet — owns a list of tasks
# ---------------------------------------------------------------------------

@dataclass
class Pet:
    name: str
    species: str            # "dog", "cat", "rabbit", etc.
    age: int                # in years
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task_id: str):
        """Remove a task by its ID."""
        self.tasks = [t for t in self.tasks if t.task_id != task_id]

    def get_pending_tasks(self) -> list:
        """Return all tasks that are not yet completed."""
        return [t for t in self.tasks if not t.completed]

    def get_tasks_by_type(self, task_type: str) -> list:
        """Return all tasks matching a given type (e.g. 'feeding')."""
        return [t for t in self.tasks if t.task_type == task_type]


# ---------------------------------------------------------------------------
# Owner — owns a list of pets
# ---------------------------------------------------------------------------

class Owner:
    def __init__(self, name: str, email: str):
        self.name: str = name
        self.email: str = email
        self.pets: list = []

    def add_pet(self, pet: Pet):
        """Register a pet under this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str):
        """Remove a pet by name."""
        self.pets = [p for p in self.pets if p.name != pet_name]

    def get_all_tasks(self) -> list:
        """Flatten and return every task across all pets."""
        all_tasks = []
        for pet in self.pets:
            for task in pet.tasks:
                all_tasks.append((pet.name, task))
        return all_tasks  # list of (pet_name, Task) tuples

    def __str__(self) -> str:
        return f"Owner: {self.name} | {len(self.pets)} pet(s)"


# ---------------------------------------------------------------------------
# Scheduler — organizes and filters tasks into a daily schedule
# ---------------------------------------------------------------------------

class Scheduler:
    def __init__(self):
        self.owners: list = []

    def add_owner(self, owner: Owner):
        """Register an owner with the scheduler."""
        self.owners.append(owner)

    def get_daily_schedule(self, owner: Owner) -> list:
        """Return all due-today tasks for an owner, sorted by time."""
        all_tasks = owner.get_all_tasks()
        due_today = [(pet_name, task) for pet_name, task in all_tasks if task.is_due_today()]
        return self.sort_tasks_by_time(due_today)

    def sort_tasks_by_time(self, tasks: list) -> list:
        """Sort (pet_name, Task) tuples by task time ascending."""
        return sorted(tasks, key=lambda item: item[1].time)

    def filter_by_pet(self, tasks: list, pet_name: str) -> list:
        """Narrow a task list down to a specific pet."""
        return [(pn, t) for pn, t in tasks if pn == pet_name]

    def filter_by_status(self, tasks: list, completed: bool) -> list:
        """Filter tasks by completion status."""
        return [(pn, t) for pn, t in tasks if t.completed == completed]

    def detect_conflicts(self, tasks: list) -> list:
        """
        Return groups of tasks that share the same time slot.
        Each conflict is a list of (pet_name, Task) tuples.
        """
        from collections import defaultdict
        time_buckets = defaultdict(list)
        for pet_name, task in tasks:
            time_buckets[task.time].append((pet_name, task))
        return [group for group in time_buckets.values() if len(group) > 1]
