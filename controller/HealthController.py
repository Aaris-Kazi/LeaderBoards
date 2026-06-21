from routing import health_router

status = {"status": "success"}


@health_router.get("/health")
async def index():
    return status