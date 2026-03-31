from dataclasses import dataclass, field
from datetime import date
from collections import defaultdict


# ---------------------------------------------------------------------------
# Task — a single care activity
# ---------------------------------------------------------------------------

@dataclass
class Task:
    task_id: str
    title: str
    task_type: str           # "feeding", "walking", "medication", "grooming", "play"
    time: str                # 24h format, e.g. "08:00"
    duration: int            # minutes
    priority: str            # "low", "medium", "high"
    recurrence: str = "none" # "none", "daily", "weekly"
    completed: bool = False
    pet_name: str = ""       # set automatically by Pet.add_task()
    created_day: str = field(default_factory=lambda: date.today().strftime("%A"))

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def mark_complete(self):
        """Mark this task as done."""
        self.completed = True

    def mark_incomplete(self):
        """Reopen a task (e.g. for recurring reset)."""
        self.completed = False

    def is_due_today(self) -> bool:
        """Return True if this task should appear in today's schedule."""
        if self.recurrence == "daily":
            return True
        if self.recurrence == "weekly":
            return date.today().strftime("%A") == self.created_day
        # "none": show once until completed
        return not self.completed

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def __str__(self) -> str:
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
    species: str             # "dog", "cat", "rabbit", etc.
    age: int                 # in years
    tasks: list = field(default_factory=list)

    # ------------------------------------------------------------------
    # Task management
    # ------------------------------------------------------------------

    def add_task(self, task: Task):
        """Add a task to this pet. Sets task.pet_name automatically."""
        if any(t.task_id == task.task_id for t in self.tasks):
            raise ValueError(f"Task '{task.task_id}' already exists for {self.name}.")
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, task_id: str):
        """Remove a task by ID. Raises if not found."""
        original = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.task_id != task_id]
        if len(self.tasks) == original:
            raise ValueError(f"No task '{task_id}' found for {self.name}.")

    def get_task_by_id(self, task_id: str) -> Task:
        """Fetch a single task by ID. Raises if not found."""
        for t in self.tasks:
            if t.task_id == task_id:
                return t
        raise ValueError(f"Task '{task_id}' not found for {self.name}.")

    # ------------------------------------------------------------------
    # Filtering
    # ------------------------------------------------------------------

    def get_pending_tasks(self) -> list:
        """All tasks not yet completed."""
        return [t for t in self.tasks if not t.completed]

    def get_completed_tasks(self) -> list:
        """All tasks that are done."""
        return [t for t in self.tasks if t.completed]

    def get_tasks_by_type(self, task_type: str) -> list:
        """All tasks matching a type, e.g. 'feeding'."""
        return [t for t in self.tasks if t.task_type == task_type]

    def get_tasks_by_priority(self, priority: str) -> list:
        """All tasks matching a priority level."""
        return [t for t in self.tasks if t.priority == priority]

    # ------------------------------------------------------------------
    # Daily reset — call once per day for recurring tasks
    # ------------------------------------------------------------------

    def reset_daily_tasks(self):
        """Mark all daily recurring tasks as incomplete for a fresh day."""
        for task in self.tasks:
            if task.recurrence == "daily":
                task.mark_incomplete()

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def summary(self) -> str:
        total = len(self.tasks)
        done = len(self.get_completed_tasks())
        return f"{self.name} ({self.species}, {self.age}y) — {done}/{total} tasks done"

    def __str__(self) -> str:
        return self.summary()


# ---------------------------------------------------------------------------
# Owner — manages multiple pets and exposes all their tasks
# ---------------------------------------------------------------------------

class Owner:
    def __init__(self, name: str, email: str):
        self.name: str = name
        self.email: str = email
        self.pets: list = []

    # ------------------------------------------------------------------
    # Pet management
    # ------------------------------------------------------------------

    def add_pet(self, pet: Pet):
        """Register a pet. Raises if a pet with the same name already exists."""
        if any(p.name == pet.name for p in self.pets):
            raise ValueError(f"A pet named '{pet.name}' already exists.")
        self.pets.append(pet)

    def remove_pet(self, pet_name: str):
        """Remove a pet by name. Raises if not found."""
        original = len(self.pets)
        self.pets = [p for p in self.pets if p.name != pet_name]
        if len(self.pets) == original:
            raise ValueError(f"No pet named '{pet_name}' found.")

    def get_pet(self, pet_name: str) -> Pet:
        """Fetch a pet by name. Raises if not found."""
        for p in self.pets:
            if p.name == pet_name:
                return p
        raise ValueError(f"No pet named '{pet_name}' found.")

    # ------------------------------------------------------------------
    # Cross-pet task access
    # ------------------------------------------------------------------

    def get_all_tasks(self) -> list:
        """
        Return every task across all pets as (pet_name, Task) tuples.
        Used by Scheduler as the main data source.
        """
        return [
            (pet.name, task)
            for pet in self.pets
            for task in pet.tasks
        ]

    def get_all_pending_tasks(self) -> list:
        """All incomplete tasks across every pet."""
        return [(pn, t) for pn, t in self.get_all_tasks() if not t.completed]

    def get_all_tasks_by_type(self, task_type: str) -> list:
        """All tasks of a specific type across every pet."""
        return [(pn, t) for pn, t in self.get_all_tasks() if t.task_type == task_type]

    # ------------------------------------------------------------------
    # Daily reset
    # ------------------------------------------------------------------

    def reset_all_daily_tasks(self):
        """Reset recurring daily tasks for all pets. Call at the start of each day."""
        for pet in self.pets:
            pet.reset_daily_tasks()

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        return f"Owner: {self.name} ({self.email}) | {len(self.pets)} pet(s)"


# ---------------------------------------------------------------------------
# Scheduler — the brain: retrieves, organizes, and manages tasks
# ---------------------------------------------------------------------------

class Scheduler:
    """
    Stateless engine. Takes Owner/Pet data in, returns organized results out.
    Does not store any state of its own.
    """

    # ------------------------------------------------------------------
    # Schedule retrieval
    # ------------------------------------------------------------------

    def get_daily_schedule(self, owner: Owner) -> list:
        """
        Return all tasks due today for an owner, sorted by time.
        Output: sorted list of (pet_name, Task) tuples.
        """
        all_tasks = owner.get_all_tasks()
        due_today = [(pn, t) for pn, t in all_tasks if t.is_due_today()]
        return self.sort_by_time(due_today)

    def get_schedule_by_priority(self, owner: Owner) -> list:
        """
        Return today's due tasks sorted by priority (high → medium → low),
        then by time within each priority group.
        """
        priority_order = {"high": 0, "medium": 1, "low": 2}
        due_today = [(pn, t) for pn, t in owner.get_all_tasks() if t.is_due_today()]
        return sorted(due_today, key=lambda item: (priority_order.get(item[1].priority, 9), item[1].time))

    # ------------------------------------------------------------------
    # Sorting
    # ------------------------------------------------------------------

    def sort_by_time(self, tasks: list) -> list:
        """Sort (pet_name, Task) tuples by time ascending."""
        return sorted(tasks, key=lambda item: item[1].time)

    # ------------------------------------------------------------------
    # Filtering
    # ------------------------------------------------------------------

    def filter_by_pet(self, tasks: list, pet_name: str) -> list:
        """Return only tasks belonging to a specific pet."""
        return [(pn, t) for pn, t in tasks if pn == pet_name]

    def filter_by_status(self, tasks: list, completed: bool) -> list:
        """Return tasks matching the given completion status."""
        return [(pn, t) for pn, t in tasks if t.completed == completed]

    def filter_by_type(self, tasks: list, task_type: str) -> list:
        """Return tasks matching a specific type, e.g. 'medication'."""
        return [(pn, t) for pn, t in tasks if t.task_type == task_type]

    def filter_by_priority(self, tasks: list, priority: str) -> list:
        """Return tasks matching a specific priority level."""
        return [(pn, t) for pn, t in tasks if t.priority == priority]

    # ------------------------------------------------------------------
    # Conflict detection
    # ------------------------------------------------------------------

    def detect_conflicts(self, tasks: list) -> list:
        """
        Find tasks scheduled at the same time.
        Returns a list of conflict groups — each group is a list of
        (pet_name, Task) tuples sharing the same time slot.
        """
        buckets = defaultdict(list)
        for pet_name, task in tasks:
            buckets[task.time].append((pet_name, task))
        return [group for group in buckets.values() if len(group) > 1]

    # ------------------------------------------------------------------
    # Summary report
    # ------------------------------------------------------------------

    def daily_summary(self, owner: Owner) -> str:
        """Print a readable daily schedule with conflict warnings."""
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
                times = group[0][1].time
                names = ", ".join(f"{pn}: {t.title}" for pn, t in group)
                lines.append(f"  {times} → {names}")

        done = len(self.filter_by_status(schedule, completed=True))
        lines.append(f"\n{done}/{len(schedule)} tasks completed.")
        return "\n".join(lines)
