import pytest

from .utils import create_random_task, create_partial_task


@pytest.mark.asyncio(loop_scope="module")
async def test_create_task(create_task, async_client):
    print("test 1: Создание task")


@pytest.mark.asyncio(loop_scope="module")
async def test_change_task_put(create_task, async_client):
    task_data_update = await create_random_task()
    response = await async_client.put(f"/api/v1/tasks/{create_task['uuid']}/", json=task_data_update)
    assert response.status_code == 200
    changed_task = response.json()
    assert changed_task["name"] == task_data_update["name"]
    assert changed_task["status"] == task_data_update["status"]
    assert changed_task["description"] == task_data_update["description"]
    print("test 2: PUT")


@pytest.mark.asyncio(loop_scope="module")
async def test_change_task_patch(create_task, async_client):
    task_data_partial = await create_partial_task()
    response = await async_client.put(f"/api/v1/tasks/{create_task['uuid']}/", json=task_data_partial)
    assert response.status_code == 200
    changed_task = response.json()
    assert changed_task["description"] == task_data_partial["description"]
    assert changed_task["status"] == task_data_partial["status"]
    print("test 3: PATCH")


@pytest.mark.asyncio(loop_scope="module")
async def test_delete_task(create_task, async_client):
    response = await async_client.delete(f"/api/v1/tasks/{create_task['uuid']}/")
    assert response.status_code == 204
    print("test 4: DELETE")


@pytest.mark.asyncio(loop_scope="module")
async def test_get_tasks(create_some_tasks, async_client):
    response = await async_client.get("/api/v1/tasks/")
    assert response.status_code == 200
    print("test 5: GET ALL")
