"""This module contains the basis for the database.

----- Description -----

This module creates the base class for the habit classes.
It further contains functions to create a database or connect to an existing
one and creates a session for it.

----- Classes -----
BaseClass:  Basic class from SQLAlchemy.

----- Functions -----
start_db:           Checks if the database exists and creates it if necessary.
start_db_session:   Starts the session that can be used to interact with the
                    database.
"""

import os

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

DB_FILE = "habit_tracker.db"

BaseClass = declarative_base()


def start_db(log: bool = False) -> Engine:
    """
    Starts the database and creates one, if not existing

    ----- Arguments -----
    log (bool): Sets the status of echo. With log = False the database will not
                display all information in the command line (default: False).

    ----- Returns -----
    engine (Engine):    The connection to the database and starting point to
                        start a session.
    """
    engine = create_engine(f"sqlite:///{DB_FILE}", echo=log)
    if not os.path.isfile(DB_FILE):
        BaseClass.metadata.create_all(engine)
    return engine


def start_db_session(engine: Engine) -> Session:
    """
    Starts a session based on the engine

    ----- Arguments -----
    engine (Engine): Is used to establish a session to the connected database.

    ----- Returns -----
    session (Session):  Containing the reference to the database session.
    """
    session_factory = sessionmaker(engine)
    session = session_factory()
    return session
