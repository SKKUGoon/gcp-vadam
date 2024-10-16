from prefect import flow, task


@flow(name="test flow")
def test_flow() -> str:
    test_task1()  # Flow can call tasks
    test_task2()
    my_nested_flow()  # Flow can call nested flows
    return "Hello, world!"


@task
def test_task1():
    print("Test Task 1!")


@task
def test_task2():
    print("Test Task 2!")


@flow(name="nested flow")
def my_nested_flow(msg):
    print(f"Nestedflow says: {msg}")


if __name__ == "__main__":
    print(test_flow())