classDiagram
    class Task {
        +str task_id
        +str title
        +str task_type
        +str time
        +int duration
        +str priority
        +bool completed
        +str recurrence
        +mark_complete()
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
        +get_pending_tasks() list
        +get_tasks_by_type(task_type) list
    }

    class Owner {
        +str name
        +str email
        +list pets
        +add_pet(pet)
        +remove_pet(pet_name)
        +get_all_tasks() list
    }

    class Scheduler {
        +list owners
        +add_owner(owner)
        +get_daily_schedule(owner) list
        +sort_tasks_by_time(tasks) list
        +filter_by_pet(tasks, pet_name) list
        +filter_by_status(tasks, completed) list
        +detect_conflicts(tasks) list
    }

    Owner "1" --> "0..*" Pet : owns
    Pet "1" --> "0..*" Task : has
    Scheduler "1" --> "0..*" Owner : manages
