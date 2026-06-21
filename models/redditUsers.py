from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Float

from databaseConnections.MySQLConnections import BASE_MODELS


class RedditUser(BASE_MODELS):
    __tablename__ = "subreddit_leaderboard"

    id = Column(Integer, primary_key=True, index=True)
    subreddit = Column(String(255), nullable=False)
    subreddit_name_prefixed = Column(String(255), nullable=False)
    created_utc = Column(Float, nullable=False)
    subreddit_subscribers = Column(Integer, nullable=False)