from pawpal_system import Task, Pet


# ------------------------------------------
# Test 1: Task Completion
# ------------------------------------------

def test_task_completion():
    task = Task(
        task_id="t1",
        title="Feed",
        task_type="feeding",
        time="08:00",
        duration=10,
        priority="high"
    )

    # Initially should be False
    assert task.completed == False

    # Mark complete
    task.mark_complete()

    # Now should be True
    assert task.completed == True


# ------------------------------------------
# Test 2: Task Addition to Pet
# ------------------------------------------

def test_add_task_to_pet():
    pet = Pet(name="Mochi", species="dog", age=3)

    task = Task(
        task_id="t2",
        title="Walk",
        task_type="walking",
        time="09:00",
        duration=20,
        priority="medium"
    )

    # Initially no tasks
    assert len(pet.tasks) == 0

    # Add task
    pet.add_task(task)

    # Now should have 1 task
    assert len(pet.tasks) == 1