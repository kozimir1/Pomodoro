from handlers.ping import router as ping_router
from handlers.tasks import router as task_router
from handlers.user import router as user_router
from handlers.categories import router as category_router
from handlers.auth import router as auth_router


routers = (task_router, category_router, ping_router, user_router, auth_router)
