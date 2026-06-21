from redis import Redis

from appConstant import DB_INDEX, REDIS_HOST
from appConstant.Constants import DB_PORT
from singletons import Singleton


class RedisConnections(metaclass=Singleton):

    def __init__(self):

        try:
            self.client = Redis(

                host=REDIS_HOST,
                port=DB_PORT,
                db=DB_INDEX,
                decode_responses=True
            )

            self.client.ping()

            print("RedisConnections instance created.")
        except Exception as e:
            print(f"Error connecting to Redis due to :: {e}")
            # raise e


    def get_client(self):
        return self.client

