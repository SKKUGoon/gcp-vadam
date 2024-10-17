# VaDaM, Various Data Modules 

For each data science projects, we need data. This module creates data modules for each dataset, and containerize it.

---

## Orchestration tool

For data orchestration tool, we use [prefect](https://docs.prefect.io/3.0/get-started/install). The github package only installs the client part for minimal installation size

```
pip install -U prefect-client
```

```python
from prefect import flow, task

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
```

## Data

[comment]: <> (| URL | <Some URL> |)
[comment]: <> (|-----|------------|)

#### 1. Weather

| KEY | VALUE                               |
|-----|-------------------------------------|
| URL | [기상예보](https://apihub.kma.go.kr/) |
| USE | Baseball TOTO, HECON |
| KEY | `APIKEY_KOREA_WEATHER` |
