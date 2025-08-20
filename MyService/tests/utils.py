from faker import Faker

from MyService.core.models import TaskStatuses

fake = Faker('ru_RU')


async def create_random_task():
    return {
        "name": fake.sentence(nb_words=2)[:25],
        "description": fake.sentence()[:255],
        "status": fake.random_element(elements=[status.value for status in TaskStatuses])
    }


async def create_partial_task():
    return {
        "description": fake.sentence()[:255],
        "status": fake.random_element(elements=[status.value for status in TaskStatuses])
    }
