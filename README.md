# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
Smarter Scheduling

The scheduling system was enhanced with several features to make it more intelligent and useful:
	•	Tasks are automatically sorted by time to create a clear daily schedule
	•	Tasks can be filtered by pet, status, type, and priority
	•	Recurring tasks (daily and weekly) automatically generate their next occurrence when completed
	•	Conflict detection identifies tasks scheduled at the same time and provides warning messages
	•	A summary view highlights completed tasks and scheduling conflicts

These improvements make the system more dynamic and closer to a real-world task planner.

Testing PawPal+

To verify the correctness of the PawPal+ system, an automated test suite was implemented using pytest.

How to run tests

Run the following command in the project root:
python -m pytest

What is tested

The test suite covers the core behaviors of the system:
	•	Sorting correctness: tasks are returned in chronological order
	•	Recurrence logic: completing a recurring task creates the next occurrence
	•	Conflict detection: tasks scheduled at the same time generate warning messages

Confidence Level 4/5
Features

The PawPal+ system includes several intelligent scheduling features:
	•	Sorting by time: Tasks are automatically ordered chronologically for a clear daily plan
	•	Priority-based scheduling: Tasks can also be sorted by priority (high to low)
	•	Task filtering: Tasks can be filtered by pet, type, priority, or completion status
	•	Recurring tasks: Daily and weekly tasks automatically generate the next occurrence when completed
	•	Conflict detection: Tasks scheduled at the same time are flagged with warnings
	•	Schedule summary: A readable summary shows all tasks and highlights conflicts and completion status


DEMO:
<a href="/Users/lasyar/Documents/project/codepath/ai110-module2show-pawpal-starter/pawpal_demo.png" target="_blank">
<img src='/course_images/ai110/pawpal_app.png' title='PawPal App' alt='PawPal App' class='center-block' />
</a>
