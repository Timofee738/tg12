from aiogram import Router

from app.users.handler import users_router
from app.admin.handler import admins_router
from app.classes.handler import classes_router


def get_handlers_router() -> Router:
    main_router = Router()

    main_router.include_routers(
        users_router,
        admins_router,
        classes_router
    )

    return main_router