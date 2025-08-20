from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from MyService.core.models import db_helper


# Получаем стандартную сессию нашей главной БД \ Нужно чтобы при желании перезаписать эту зависимость.
async def get_db(session: AsyncSession = Depends(db_helper.session_dependency)):
    yield session
