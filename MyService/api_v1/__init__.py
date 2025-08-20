from fastapi import APIRouter


from MyService.api_v1.tasks.views import router as tasks_games_router

router = APIRouter()
router.include_router(router=tasks_games_router, prefix="/tasks")