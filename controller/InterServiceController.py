from exceptions import ApplicationException
from routing import v1_router
from fastapi.responses import JSONResponse
from fastapi import Depends
from utils import FetchRequest, CommonService
from utils.db import get_db, get_redis_db

from sqlalchemy.orm import Session
from redis import Redis

fetch_request = FetchRequest()
common_service = CommonService()

@v1_router.get("/leaderboard")
async def get_leaderboard(db: Session = Depends(get_db)):
    data = common_service.get_page_data(db)
    return JSONResponse(content=data, status_code=200)


@v1_router.get("/leaderboard/{page}")
async def get_leaderboard(page: int, db: Session = Depends(get_db)):
    if page < 1:
        return JSONResponse(content={"error": "Page number must be greater than 0"}, status_code=400)
    
    data = common_service.get_page_data(db, page)
    return JSONResponse(content=data, status_code=200)


@v1_router.get("/leaderboard/reddit/{subreddit}")
async def get_leaderboard_user(subreddit: str, db: Session = Depends(get_db), redis_client: Redis = Depends(get_redis_db)):
    data = common_service.get_user_data(db, redis_client, subreddit)
    return JSONResponse(content=data, status_code=200)


@v1_router.post("/leaderboard")
async def post_leaderboard(request: dict, db: Session = Depends(get_db), redis_client: Redis = Depends(get_redis_db)):
    try:
        subreddit = request.get("subreddit")
        result = await fetch_request.fetch(subreddit)
        resp = common_service.insert_data(db, redis_client, result)
        data = {"data": resp}
        return JSONResponse(content=data, status_code=201)
    except ApplicationException as e:
        return JSONResponse(content={"error": str(e.message)}, status_code=e.code)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)