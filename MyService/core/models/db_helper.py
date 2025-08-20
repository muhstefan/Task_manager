from asyncio import current_task

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session

from MyService.core.config import settings


class DataBaseHelper:
    """
     Вспомогательный класс для работы с асинхронной базой данных через SQLAlchemy Async.

     Аргументы:
     - url (str): URL подключения к базе данных.
     - echo (bool): Включение логирования SQL-запросов для отладки (по умолчанию False).

     Атрибуты:
     - engine: Асинхронный движок базы данных SQLAlchemy.
     - session_factory: Фабрика для создания асинхронных сессий базы данных.

     Методы:
     - get_scoped_session(): Возвращает scoped-сессию, привязанную к текущей асинхронной задаче.
       Это позволяет использовать одну сессию на всю цепочку вызовов в рамках одного запроса,
       что может экономить ресурсы при множестве обращений к базе.

     - session_dependency(): Асинхронный генератор для Dependency Injection в FastAPI,
       предоставляющий новую сессию на каждый запрос. Сессия автоматически
       закрывается после использования.

     - scoped_session_dependency(): Асинхронный генератор для Dependency Injection,
       предоставляющий scoped-сессию, которая живёт на протяжении всего запроса,
       объединяя все обращения в одну сессию.
     """

    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            pool_pre_ping=True,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,  # Подготовка к комиту
            expire_on_commit=False
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task
        )
        return session

    async def session_dependency(self):
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(self):
        session = self.get_scoped_session()
        yield session
        await session.close()


db_helper = DataBaseHelper(
    url=settings.db_url,
    echo=settings.db_echo
)
