from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from sqlmodel import SQLModel

from MyService.api_v1 import router as router_v1
from MyService.core.config import settings
from MyService.core.models import db_helper


# контекстный менеджер в котором можно создать БД и что-то сделать после завершения
@asynccontextmanager
async def lifespan(app: FastAPI):
    async  with db_helper.engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router_v1, prefix=settings.api_v1_prefix)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
