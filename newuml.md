classDiagram
    class Task {
        +str task_id
        +str title
        +str task_type
        +str time
        +int duration
        +str priority
        +str recurrence
        +bool completed
        +str pet_name
        +str created_day
        +date due_date
        +mark_complete()
        +mark_incomplete()
        +is_due_today() bool
        +__str__() str
    }

    class Pet {
        +str name
        +str species
        +int age
        +list tasks
        +add_task(task)
        +remove_task(task_id)
        +get_task_by_id(task_id) Task
        +get_pending_tasks() list
        +get_completed_tasks() list
        +get_tasks_by_type(task_type) list
        +get_tasks_by_priority(priority) list
        +reset_daily_tasks()
        +summary() str
        +__str__() str
    }

    class Owner {
        +str name
        +str email
        +list pets
        +add_pet(pet)
        +remove_pet(pet_name)
        +get_pet(pet_name) Pet
        +get_all_tasks() list
        +get_all_pending_tasks() list
        +get_all_tasks_by_type(task_type) list
        +reset_all_daily_tasks()
        +__str__() str
    }

    class Scheduler {
        +get_daily_schedule(owner) list
        +get_schedule_by_priority(owner) list
        +sort_by_time(tasks) list
        +filter_by_pet(tasks, pet_name) list
        +filter_by_status(tasks, completed) list
        +filter_by_type(tasks, task_type) list
        +filter_by_priority(tasks, priority) list
        +mark_task_complete(owner, pet_name, task_id)
        +detect_conflicts(tasks) list
        +get_conflict_warnings(tasks) list
        +daily_summary(owner) str
    }

    Owner "1" --> "0..*" Pet : owns
    Pet "1" --> "0..*" Task : has
    Scheduler ..> Owner : uses
    Scheduler ..> Pet : accesses via Owner
    Scheduler ..> Task : organizes