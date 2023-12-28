from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://api:SliceOfLyfe69@localhost:6969/item_db",
    echo = True)

Base = declarative_base()

SessionLocal = sessionmaker(bind = engine)

