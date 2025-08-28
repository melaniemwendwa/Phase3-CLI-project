from sqlalchemy.orm import declarative_base

Base = declarative_base()

def init_db(engine):
    """
    Import models so they are registered with Base, then create all tables.
    """
    # models import ensures classes are defined on Base
    import db.models  
    Base.metadata.create_all(engine)
