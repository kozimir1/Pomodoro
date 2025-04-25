from handlers.ping import router as ping_router
from handlers.tasks import router as task_router
from handlers.categories import router as category_router

routers = (task_router, category_router, ping_router)
