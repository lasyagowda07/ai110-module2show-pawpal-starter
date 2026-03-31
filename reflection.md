# PawPal+ Project Reflection

## 1. System Design
Core Actions:
	•	Add a pet so the owner can manage multiple animals in one place
	•	Add or schedule tasks for each pet, including details like time, duration, and priority
	•	View a daily schedule that organizes tasks in a clear and prioritized order
**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
My initial design for PawPal+ was based on four main classes: Owner, Pet, Task, and Scheduler. I chose these classes because they match the main parts of the problem and helped me keep the system simple and organized.

The Owner class represents the person using the app. It stores basic information like the owner’s name, email, and the list of pets they manage. Its responsibility is to add and remove pets and collect all tasks across pets when needed.

The Pet class represents each individual pet. It stores information like the pet’s name, species, age, and its list of tasks. Its responsibility is to manage tasks for that pet, such as adding a task, removing a task, and getting pending tasks or tasks by type.

The Task class represents a single pet care activity, such as feeding, walking, or medication. It stores the task ID, title, type, time, duration, priority, recurrence, and completion status. Its responsibility is to represent one unit of work and provide actions like marking a task as complete and checking whether it is due today.

The Scheduler class is the main logic layer of the system. It is responsible for building the daily schedule using the tasks stored under each pet and owner. It can sort tasks by time, filter them by pet or completion status, generate a daily schedule, and detect conflicts when multiple tasks happen at the same time.

Overall, I designed the system so that each class has a clear responsibility. Owner manages pets, Pet manages tasks, Task stores activity details, and Scheduler handles the scheduling logic. This made the design modular and easier to test and extend later.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---
Yes, my design changed during implementation after reviewing the class structure. One key change was adding a reference to the pet inside the Task class, so tasks always know which pet they belong to. This made the system more reliable when tasks are used outside of grouped data.

I also fixed the weekly recurrence logic. Initially, weekly tasks were showing up every day, so I added a way to store the original day and compare it with the current day.

Another improvement was adding validation to methods like removing pets or tasks, so they raise errors instead of failing silently.

Finally, I simplified the Scheduler by making it stateless, since it only needs to process data rather than store it.

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
My scheduler mainly considers time, task status, recurrence, and in some cases priority. Time is the main constraint because tasks need to be ordered correctly throughout the day. Task status also matters because completed tasks should not continue appearing in the current daily schedule. Recurrence is important because daily and weekly tasks need to generate the next occurrence automatically after completion.

I also added support for priority-based sorting through a separate scheduler method. This allows higher priority tasks to be surfaced first when needed, even though the default daily schedule is primarily organized by time.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
One tradeoff my scheduler makes is that it only checks for conflicts based on exact matching time values. It does not consider overlapping durations between tasks. For example, if one task runs from 08:00 to 08:30 and another starts at 08:15, the system will not detect this as a conflict.

This tradeoff keeps the implementation simple and efficient, since comparing exact time strings is straightforward and fast. For this project, it is reasonable because the goal is to demonstrate basic scheduling logic rather than build a fully optimized time management system. More complex overlap detection could be added in future improvements if needed.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
