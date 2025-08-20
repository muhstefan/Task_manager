import uuid
from enum import Enum

from sqlmodel import Field

from MyService.core.models.base import BaseModel


class TaskStatuses(str, Enum):
    created = "создано"
    in_progress = "в работе"
    completed = "завершено"


class Task(BaseModel, table=True):
    """
    Модель задачи (Task) для хранения информации о задачах в базе данных.
    Поля:
    - uuid: уникальный идентификатор задачи
    - name: название задачи, максимум 25 символов
    - description: описание задачи, максимум 255 символов
    - status: статус задачи (создано, в работе, завершено)
    """
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str = Field(..., max_length=25)
    description: str = Field(..., max_length=255)
    status: TaskStatuses = Field(default=TaskStatuses.created)
