from sqlalchemy.orm import Session
from redis import Redis

from appConstant import LEADERBOARD_KEY, PAGE_LIMIT
from models import RedditUser


class CommonService:

    INSERT_QUERY = """
            INSERT INTO subreddit_leaderboard 
            (`subreddit`, `subreddit_name_prefixed`, `subreddit_subscribers`, `created_utc`) 
            VALUES (:subreddit, :subreddit_name_prefixed, :subreddit_subscribers, :created_utc) 
            ON DUPLICATE KEY UPDATE subreddit_subscribers = :subreddit_subscribers;
            """
    
    def get_page_data(self, db: Session, page: int = 1) -> dict[str, any]:
        users = db.query(RedditUser).order_by(
                RedditUser.subreddit_subscribers.desc()
            ).offset(
                (page - 1) * PAGE_LIMIT
            ).limit(PAGE_LIMIT).all()
        
        rank = (page - 1) * PAGE_LIMIT + 1
    
        return  {
            "users": [
                
                {
                    "rank": rank,
                    "id": u.id,
                    "subreddit": u.subreddit,
                    "subscribers": u.subreddit_subscribers
                }
                for rank, u in enumerate(users, start=rank)
            ]
        }
    
    def get_user_data(self, db: Session, redis_client: Redis, subreddit: str) -> dict[str, any]:
        user = db.query(RedditUser).filter(
                RedditUser.subreddit == subreddit
            ).first()
        
        if not user:
            return {"error": "User not found"}
        
        listRank: list = redis_client.zrevrange(
            LEADERBOARD_KEY,
            0,
            -1
        )

        rank = listRank.index(user.subreddit)

        return {
                "id": user.id,
                "subreddit": subreddit,
                "subscribers": user.subreddit_subscribers,
                "rank": rank + 1
                }
        

    def insert_data(self, db: Session, redis_client: Redis, data: dict) -> dict[str, any]:
        """
        Inserts data into the database.

        :param db: SQLAlchemy Session object
        :param redis_client: Redis client object
        :param data: Dictionary containing the data to be inserted
        :return: The inserted model instance
        """


        subreddit = data["subreddit"]
        subscribers = data["subreddit_subscribers"]

        user = db.query(RedditUser).filter(
                RedditUser.subreddit == subreddit
            ).first()
        

        if user :
            user.subreddit_name_prefixed = data[
                "subreddit_name_prefixed"
            ]

            user.created_utc = data[
                "created_utc"
            ]

            user.subreddit_subscribers = subscribers

        else :
            user = RedditUser(

                subreddit=subreddit,

                subreddit_name_prefixed=data[
                    "subreddit_name_prefixed"
                ],

                created_utc=data[
                    "created_utc"
                ],

                subreddit_subscribers=subscribers

            )

        db.add(user)

        db.commit()
        db.refresh(user)


        redis_client.zadd(
            LEADERBOARD_KEY,
            {subreddit: subscribers}
        )

        rank = redis_client.zrevrank(
            LEADERBOARD_KEY,
            subreddit
        )

            
        return {
                "id": user.id,
                "subreddit": subreddit,
                "subscribers": subscribers,
                "rank": rank + 1
                }