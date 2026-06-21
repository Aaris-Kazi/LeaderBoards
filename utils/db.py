from databaseConnections import MySQLConnections, RedisConnections


db = MySQLConnections()
redisDb = RedisConnections()


def get_db():

    session = db.get_session()

    try:
        yield session

    finally:
        session.close()

def get_redis_db():

    redis_client = redisDb.get_client()

    try:
        yield redis_client

    finally:
        redis_client.close()
