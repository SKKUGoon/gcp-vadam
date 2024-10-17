from prefect import flow, task
import os


@flow(name="test flow", log_prints=True)
def test_flow() -> str:
    test_task1()  # Flow can call tasks
    test_task2()
    check_env()  # Check inserted envs
    my_nested_flow("something something about you")  # Flow can call nested flows
    return "Hello, world!"


@task
def test_task1():
    print("Test Task 1!")


@task
def test_task2():
    print("Test Task 2!")


@task
def check_env():
    print("weather api", os.getenv("APIKEY_KOREA_WEATHER"))
    print("weather api", os.getenv("PG_HOST"))


@flow(name="nested flow")
def my_nested_flow(msg):
    print(f"Nestedflow says: {msg}")


if __name__ == "__main__":
    test_flow().deploy(
        name='prefect-test',
        work_pool_name='weather-work-pool',
        work_queue_name='weather-queue',
    )


