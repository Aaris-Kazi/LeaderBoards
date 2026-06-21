from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, declarative_base
from threading import Lock

from appConstant import MAX_OVERFLOW, POOL_SIZE, POOL_PRE_PING, SQLALCHEMY_DATABASE_URL

class Base(DeclarativeBase):
    pass

BASE_MODELS = declarative_base()

class MySQLConnections:

    _instance = None
    _lock = Lock()

    def __new__(cls):

        if cls._instance is None:

            with cls._lock:

                if cls._instance is None:
                    cls._instance = super().__new__(cls)

                    cls._instance.engine = create_engine(

                        SQLALCHEMY_DATABASE_URL,

                        pool_size=POOL_SIZE,
                        max_overflow=MAX_OVERFLOW,
                        pool_pre_ping=POOL_PRE_PING,
                        echo=True
                    )

                    # print(type(cls._instance.engine))
                    

                    cls._instance.SessionLocal = sessionmaker(

                        bind=cls._instance.engine,
                        autocommit=False,
                        autoflush=False
                    )
                    # print(type(cls._instance.SessionLocal))

                    print("MySQLConnections instance created.")

        return cls._instance

    def get_session(self) -> sessionmaker:
        return self.SessionLocal()
    
