from typing import Optional

from sqlmodel import Field, SQLModel

from MyService.core.models.tables import TaskStatuses


class TaskCreate(SQLModel):
    """
      Модель для создания новой задачи.
      Используется при приёме данных в запросе на создание задачи.
      UUID задачи не передаётся, так как он генерируется автоматически на уровне базы данных или модели.

      Атрибуты:
      - name (str): Название задачи, обязательно, максимум 25 символов.
      - description (str): Описание задачи, обязательно, максимум 255 символов.
      - status (Optional[TaskStatuses]): Статус задачи, по умолчанию "создано".
      """
    name: str = Field(..., max_length=25)
    description: str = Field(..., max_length=255)
    status: Optional[TaskStatuses] = TaskStatuses.created


# Модель для обновления задачи - все поля опциональны
class TaskUpdate(SQLModel):
    """
    Модель для обновления задачи.

    Используется для частичного обновления (PATCH/PUT запроса).
    Все поля опциональны, позволяя обновлять только необходимые свойства.

    Атрибуты:
    - name (Optional[str]): Новое название задачи, максимум 25 символов.
    - description (Optional[str]): Новое описание задачи, максимум 255 символов.
    - status (Optional[TaskStatuses]): Новый статус задачи, если требуется обновить.
    """
    name: Optional[str] = Field(None, max_length=25)
    description: Optional[str] = Field(None, max_length=255)
    status: Optional[TaskStatuses] = None
