from os import getenv


CORS_ORIGIN = getenv("CORS_ORIGIN", "*").replace(' ', '').split(',')
HOST = getenv("HOST", "localhost")
USER = getenv("USER", "root")
PASSWORD = getenv("PASSWORD", "password")
DATABASE = getenv("DATABASE", "reddit_leaderboards")
DB_INDEX = int(getenv("DB_INDEX", "0"))
PAGE_LIMIT = int(getenv("PAGE_LIMIT", "10"))