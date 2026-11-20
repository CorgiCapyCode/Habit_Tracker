"""
This module is used to load sample data to the database.

----- Description -----
This module deletes all entries from the existing database and then adds the sample data.

----- Functions -----
add_sample_data_to_habits:
add_sample_entries_to_history:
"""

import datetime
import sys
from random import randint

from sqlalchemy.orm import Session

from db.db_functions import add_new_entry_to_db
from db.db_setup import start_db, start_db_session
from habit_classes import Habit, HabitHistory

SAMPLE_DUE_DATE = datetime.date(2099, 12, 1)


def add_sample_data_to_habits(session: Session, data_lst: list) -> None:
    name = data_lst[0]
    description = data_lst[1]
    period = data_lst[2]
    active_status = data_lst[3]
    tracking_status = data_lst[4]
    creation_date = data_lst[5]
    start_date = data_lst[6]
    current_streak = data_lst[7]
    highscore = data_lst[8]
    total_fails = data_lst[9]
    next_due = data_lst[10]

    add_new_entry_to_db(session, name, description, period, active_status)

    habit_object = session.query(Habit).filter(Habit.habit_name == name).first()
    if habit_object:
        habit_object.habit_tracking_status = tracking_status
        habit_object.habit_creation_date = creation_date
        habit_object.habit_start_date = start_date
        habit_object.habit_current_streak = current_streak
        habit_object.habit_highscore_streak = highscore
        habit_object.habit_total_fails = total_fails
        habit_object.habit_next_due = next_due
    session.commit()


def add_sample_entries_to_history(session: Session, data_lst: list) -> None:
    name = data_lst[0]
    fail_or_completion_date_time = data_lst[1]
    corresponding_due_date = data_lst[2]
    type_of_completion = data_lst[3]
    history_entry = HabitHistory(
        name, fail_or_completion_date_time, corresponding_due_date, type_of_completion
    )
    session.add(history_entry)
    session.commit()


if __name__ == "__main__":
    user_input = input(
        "If you want to delete all current data and replace it with sample data type yes:   "
    )
    if user_input != "yes":
        print("Nothing changed")
        sys.exit()

    user_input_security = input(
        "LAST WARNING: THIS WILL DELETE ALL DATA. Are you sure? If so type YES:   "
    )
    if user_input_security != "YES":
        print("Nothing changed")
        sys.exit()

    engine = start_db(log=False)
    session = start_db_session(engine=engine)

    session.query(Habit).delete()
    session.query(HabitHistory).delete()
    session.commit()

    habits_to_add = [
        [
            "Clean Apartment",
            "Clean everything",
            7,
            True,
            True,
            datetime.date(2023, 10, 1),
            datetime.date(2023, 10, 1),
            4,
            4,
            0,
            SAMPLE_DUE_DATE,
        ],
        [
            "Do Sports",
            "Go to training",
            2,
            False,
            False,
            datetime.date(2023, 10, 1),
            None,
            0,
            0,
            0,
            None,
        ],
        [
            "Code in Python",
            "Work on Python skills",
            1,
            True,
            True,
            datetime.date(2023, 10, 1),
            datetime.date(2023, 10, 1),
            3,
            17,
            4,
            SAMPLE_DUE_DATE,
        ],
        [
            "Learn Spanish",
            "Spanish classes or hw",
            2,
            True,
            True,
            datetime.date(2023, 10, 1),
            datetime.date(2023, 10, 2),
            2,
            11,
            1,
            SAMPLE_DUE_DATE,
        ],
        [
            "Water plants",
            "Water plants",
            7,
            True,
            False,
            datetime.date(2023, 10, 1),
            datetime.date(2023, 10, 3),
            4,
            4,
            0,
            SAMPLE_DUE_DATE,
        ],
    ]
    for habit in habits_to_add:
        add_sample_data_to_habits(session, habit)

    habits = session.query(Habit).all()

    habit_1 = habits[0]
    habit_history_1 = [
        [
            habit_1.habit_name,
            datetime.datetime(
                2023, 10, 6, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_1.habit_start_date
            + datetime.timedelta(days=habit_1.habit_period * 1),
            True,
        ],
        [
            habit_1.habit_name,
            datetime.datetime(
                2023, 10, 9, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_1.habit_start_date
            + datetime.timedelta(days=habit_1.habit_period * 2),
            True,
        ],
        [
            habit_1.habit_name,
            datetime.datetime(
                2023, 10, 17, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_1.habit_start_date
            + datetime.timedelta(days=habit_1.habit_period * 3),
            True,
        ],
        [
            habit_1.habit_name,
            datetime.datetime(
                2023, 10, 28, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_1.habit_start_date
            + datetime.timedelta(days=habit_1.habit_period * 4),
            True,
        ],
    ]

    habit_2 = habits[2]
    habit_history_2 = [
        [
            habit_2.habit_name,
            datetime.datetime(
                2023, 10, 1, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_2.habit_start_date
            + datetime.timedelta(days=habit_2.habit_period * 1),
            True,
        ],
        [
            habit_2.habit_name,
            datetime.datetime(
                2023, 10, 2, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_2.habit_start_date
            + datetime.timedelta(days=habit_2.habit_period * 2),
            True,
        ],
        [
            habit_2.habit_name,
            datetime.datetime(
                2023, 10, 3, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_2.habit_start_date
            + datetime.timedelta(days=habit_2.habit_period * 3),
            True,
        ],
        [
            habit_2.habit_name,
            datetime.datetime(
                2023, 10, 4, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_2.habit_start_date
            + datetime.timedelta(days=habit_2.habit_period * 4),
            True,
        ],
        [
            habit_2.habit_name,
            datetime.datetime(
                2023, 10, 5, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_2.habit_start_date
            + datetime.timedelta(days=habit_2.habit_period * 5),
            True,
        ],
        [
            habit_2.habit_name,
            datetime.datetime(
                2023, 10, 6, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_2.habit_start_date
            + datetime.timedelta(days=habit_2.habit_period * 6),
            True,
        ],
        [
            habit_2.habit_name,
            datetime.datetime(
                2023, 10, 7, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_2.habit_start_date
            + datetime.timedelta(days=habit_2.habit_period * 7),
            True,
        ],
        [
            habit_2.habit_name,
            datetime.datetime(
                2023, 10, 8, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_2.habit_start_date
            + datetime.timedelta(days=habit_2.habit_period * 8),
            True,
        ],
        [
            habit_2.habit_name,
            datetime.datetime(
                2023, 10, 9, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_2.habit_start_date
            + datetime.timedelta(days=habit_2.habit_period * 9),
            True,
        ],
        [
            habit_2.habit_name,
            datetime.datetime(
                2023, 10, 10, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_2.habit_start_date
            + datetime.timedelta(days=habit_2.habit_period * 10),
            True,
        ],
        [
            habit_2.habit_name,
            datetime.datetime(
                2023, 10, 11, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_2.habit_start_date
            + datetime.timedelta(days=habit_2.habit_period * 11),
            True,
        ],
        [
            habit_2.habit_name,
            datetime.datetime(
                2023, 10, 12, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_2.habit_start_date
            + datetime.timedelta(days=habit_2.habit_period * 12),
            True,
        ],
        [
            habit_2.habit_name,
            datetime.datetime(
                2023, 10, 13, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_2.habit_start_date
            + datetime.timedelta(days=habit_2.habit_period * 13),
            True,
        ],
        [
            habit_2.habit_name,
            datetime.datetime(
                2023, 10, 14, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_2.habit_start_date
            + datetime.timedelta(days=habit_2.habit_period * 14),
            True,
        ],
        [
            habit_2.habit_name,
            datetime.datetime(
                2023, 10, 15, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_2.habit_start_date
            + datetime.timedelta(days=habit_2.habit_period * 15),
            True,
        ],
        [
            habit_2.habit_name,
            datetime.datetime(
                2023, 10, 16, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_2.habit_start_date
            + datetime.timedelta(days=habit_2.habit_period * 16),
            True,
        ],
        [
            habit_2.habit_name,
            datetime.datetime(
                2023, 10, 17, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_2.habit_start_date
            + datetime.timedelta(days=habit_2.habit_period * 17),
            True,
        ],
        [
            habit_2.habit_name,
            datetime.datetime(
                2023, 10, 19, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_2.habit_start_date
            + datetime.timedelta(days=habit_2.habit_period * 18),
            False,
        ],
        [
            habit_2.habit_name,
            datetime.datetime(
                2023, 10, 19, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_2.habit_start_date
            + datetime.timedelta(days=habit_2.habit_period * 19),
            True,
        ],
        [
            habit_2.habit_name,
            datetime.datetime(
                2023, 10, 21, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_2.habit_start_date
            + datetime.timedelta(days=habit_2.habit_period * 20),
            False,
        ],
        [
            habit_2.habit_name,
            datetime.datetime(
                2023, 10, 21, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_2.habit_start_date
            + datetime.timedelta(days=habit_2.habit_period * 21),
            True,
        ],
        [
            habit_2.habit_name,
            datetime.datetime(
                2023, 10, 22, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_2.habit_start_date
            + datetime.timedelta(days=habit_2.habit_period * 22),
            True,
        ],
        [
            habit_2.habit_name,
            datetime.datetime(
                2023, 10, 24, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_2.habit_start_date
            + datetime.timedelta(days=habit_2.habit_period * 23),
            False,
        ],
        [
            habit_2.habit_name,
            datetime.datetime(
                2023, 10, 24, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_2.habit_start_date
            + datetime.timedelta(days=habit_2.habit_period * 24),
            True,
        ],
        [
            habit_2.habit_name,
            datetime.datetime(
                2023, 10, 25, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_2.habit_start_date
            + datetime.timedelta(days=habit_2.habit_period * 25),
            False,
        ],
        [
            habit_2.habit_name,
            datetime.datetime(
                2023, 10, 26, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_2.habit_start_date
            + datetime.timedelta(days=habit_2.habit_period * 26),
            True,
        ],
        [
            habit_2.habit_name,
            datetime.datetime(
                2023, 10, 27, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_2.habit_start_date
            + datetime.timedelta(days=habit_2.habit_period * 27),
            True,
        ],
        [
            habit_2.habit_name,
            datetime.datetime(
                2023, 10, 28, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_2.habit_start_date
            + datetime.timedelta(days=habit_2.habit_period * 28),
            True,
        ],
    ]

    habit_3 = habits[3]
    habit_history_3 = [
        [
            habit_3.habit_name,
            datetime.datetime(
                2023, 10, 3, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_3.habit_start_date
            + datetime.timedelta(days=habit_3.habit_period * 1),
            True,
        ],
        [
            habit_3.habit_name,
            datetime.datetime(
                2023, 10, 5, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_3.habit_start_date
            + datetime.timedelta(days=habit_3.habit_period * 2),
            True,
        ],
        [
            habit_3.habit_name,
            datetime.datetime(
                2023, 10, 7, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_3.habit_start_date
            + datetime.timedelta(days=habit_3.habit_period * 3),
            True,
        ],
        [
            habit_3.habit_name,
            datetime.datetime(
                2023, 10, 9, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_3.habit_start_date
            + datetime.timedelta(days=habit_3.habit_period * 4),
            True,
        ],
        [
            habit_3.habit_name,
            datetime.datetime(
                2023, 10, 11, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_3.habit_start_date
            + datetime.timedelta(days=habit_3.habit_period * 5),
            True,
        ],
        [
            habit_3.habit_name,
            datetime.datetime(
                2023, 10, 13, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_3.habit_start_date
            + datetime.timedelta(days=habit_3.habit_period * 6),
            True,
        ],
        [
            habit_3.habit_name,
            datetime.datetime(
                2023, 10, 15, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_3.habit_start_date
            + datetime.timedelta(days=habit_3.habit_period * 7),
            True,
        ],
        [
            habit_3.habit_name,
            datetime.datetime(
                2023, 10, 17, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_3.habit_start_date
            + datetime.timedelta(days=habit_3.habit_period * 8),
            True,
        ],
        [
            habit_3.habit_name,
            datetime.datetime(
                2023, 10, 19, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_3.habit_start_date
            + datetime.timedelta(days=habit_3.habit_period * 9),
            True,
        ],
        [
            habit_3.habit_name,
            datetime.datetime(
                2023, 10, 21, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_3.habit_start_date
            + datetime.timedelta(days=habit_3.habit_period * 10),
            True,
        ],
        [
            habit_3.habit_name,
            datetime.datetime(
                2023, 10, 23, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_3.habit_start_date
            + datetime.timedelta(days=habit_3.habit_period * 11),
            True,
        ],
        [
            habit_3.habit_name,
            datetime.datetime(
                2023, 10, 26, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_3.habit_start_date
            + datetime.timedelta(days=habit_3.habit_period * 12),
            False,
        ],
        [
            habit_3.habit_name,
            datetime.datetime(
                2023, 10, 27, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_3.habit_start_date
            + datetime.timedelta(days=habit_3.habit_period * 13),
            True,
        ],
        [
            habit_3.habit_name,
            datetime.datetime(
                2023, 10, 29, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_3.habit_start_date
            + datetime.timedelta(days=habit_3.habit_period * 14),
            True,
        ],
    ]

    habit_4 = habits[4]
    habit_history_4 = [
        [
            habit_4.habit_name,
            datetime.datetime(
                2023, 10, 6, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_4.habit_start_date
            + datetime.timedelta(days=habit_4.habit_period * 1),
            True,
        ],
        [
            habit_4.habit_name,
            datetime.datetime(
                2023, 10, 9, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_4.habit_start_date
            + datetime.timedelta(days=habit_4.habit_period * 2),
            True,
        ],
        [
            habit_4.habit_name,
            datetime.datetime(
                2023, 10, 17, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_4.habit_start_date
            + datetime.timedelta(days=habit_4.habit_period * 3),
            True,
        ],
        [
            habit_4.habit_name,
            datetime.datetime(
                2023, 10, 28, randint(0, 23), randint(0, 59), randint(0, 59)
            ),
            habit_4.habit_start_date
            + datetime.timedelta(days=habit_4.habit_period * 4),
            True,
        ],
    ]
    for entry in habit_history_1:
        add_sample_entries_to_history(session, entry)

    for entry in habit_history_2:
        add_sample_entries_to_history(session, entry)

    for entry in habit_history_3:
        add_sample_entries_to_history(session, entry)

    for entry in habit_history_4:
        add_sample_entries_to_history(session, entry)
