"""
This module contains functions to handle the database objects.

----- Description -----
The functions in this module are for adjusting single or multiple values on
existing database objects.
For creating and deleting objects see the module db_functions.

----- Functions -----
change_active_passive_status:    Switches habits between tracked and passive.
manage_active_passive_status:    Applies the reset or setup steps required by
                                the new status.
manage_passive_habits:           Calls the reset functions for a passive habit.
manage_tracking_status:          Manages the tracking status for a list of habit
                                names.
switch_active_passive_status:    Switches the status of a single habit between
                                actively tracked and passive.
setup_active_habits:             Sets the start date and the next due date for
                                active habits, when activated.
reset functions:                 Reset individual values to their defaults,
                                such as the current streak.
set_tracking_status_to_true:     Sets the tracking status to True.
streak_calculator:               Calculates and updates the current streak and
                                the highscore streak.
"""

import datetime

from sqlalchemy.orm import Session

from db.db_filter_functions import filter_db_for_names
from db.db_history_functions import create_new_history_entry
from habit_classes import Habit


def change_active_passive_status(session: Session, names: list[str]) -> None:
    """
    This function starts the process of changing a habit from active to passive
    or vice versa.

    ----- Description -----
    This function calls the needed functions to change the status of a habit
    from active to passive or vice versa.
    The process consists of three steps:
    1. Get the related habit objects from the list of input names.
    2. Call the actual switch function.
    3. Call the function to further process the habit according to the new
    status (e.g. setup a due date)

    ----- Arguments -----
    session (Session):  Containing the reference to the database session.
    names (list):       A list of habit names that is used to receive the
                        related objects.
    """

    habit_entries = filter_db_for_names(session=session, names=names)

    for habit_entry in habit_entries:
        switch_active_passive_status(session=session, habit_object=habit_entry)
        manage_active_passive_status(session=session, habit_object=habit_entry)


def manage_active_passive_status(session: Session, habit_object: Habit) -> None:
    """
    This function manages habits according to their status of being active or
    passive.

    ----- Description -----
    This function takes a habit object as input and calls functions depending
    on its active status.

    ----- Arguments -----
    session (Session):      Containing the reference to the database session.
    habit_object (Habit):   A habit object that will be changed according to
                            its status.
    """
    if habit_object.habit_active_status is True:
        setup_active_habits(session=session, habit_object=habit_object)
    else:
        manage_passive_habits(session=session, habit_object=habit_object)


def manage_passive_habits(session: Session, habit_object: Habit) -> None:
    """
    This function calls the needed reset functions for passive habits.

    ----- Description -----
    This function will reset several things for an inactive habit. E.g. the
    next due date.
    It does so by calling the relevant reset functions.

    ----- Arguments -----
    session (Session):      Containing the reference to the database session.
    habit_object (Habit):   A habit object that will be reset.
    """
    reset_start_date(session=session, habit_object=habit_object)
    reset_next_due(session=session, habit_object=habit_object)
    reset_total_fails(session=session, habit_object=habit_object)
    reset_current_streak(session=session, habit_object=habit_object)
    reset_tracking_status(session=session, habit_object=habit_object)


def manage_tracking_status(session: Session, names: list[str]) -> list[int]:
    """
    This function manages the tracking status for a list of habit names.

    ----- Description -----
    This function uses the list of habit names to get the related objects and
    then sets the status to True if not already to mark the habit as completed.
    If the user tries to mark a not tracked habit as complete, then function
    will return an error code.
    Further this function will start the process of adjusting the streak values
    of the habit.

    ----- Arguments -----
    session (Session):  Containing the reference to the database session.
    names (list):       A list of habit names that is used to receive the
    related objects.

    ----- Returns -----
    function_status_message (list): A list of error codes.
    """
    function_status_message = []
    habit_entries = filter_db_for_names(session=session, names=names)
    for habit_entry in habit_entries:
        if (
            habit_entry.habit_active_status is True
            and habit_entry.habit_tracking_status is False
        ):
            set_tracking_status_to_true(session=session, habit_object=habit_entry)
            streak_calculator(session=session, habit_object=habit_entry)
        elif habit_entry.habit_active_status is False:
            function_status_message.append(200)
        elif habit_entry.habit_tracking_status is True:
            function_status_message.append(201)

    return function_status_message


def switch_active_passive_status(session: Session, habit_object: Habit) -> None:
    """
    This function switches the status of active_status from true to false and
    reverse.

    ----- Arguments -----
    session (Session):      Containing the reference to the database session.
    habit_object (Habit):   A habit object that will be changed.
    """
    habit_object.habit_active_status = not habit_object.habit_active_status
    session.commit()


def setup_active_habits(session: Session, habit_object: Habit) -> None:
    """
    This function sets up active habits.

    ----- Description -----
    The function uses a habit object and sets up a start date and a next due
    date if not existing.
    It is used after a habit object is set to active.

    ----- Arguments -----
    session (Session):      Containing the reference to the database session.
    habit_object (Habit):   A habit object that will be changed.
    """
    if habit_object.habit_start_date is None:
        habit_object.habit_start_date = datetime.date.today()
    if habit_object.habit_next_due is None:
        habit_object.habit_next_due = (
            habit_object.habit_start_date
            + datetime.timedelta(days=habit_object.habit_period)
        )
    session.commit()


def reset_current_streak(session: Session, habit_object: Habit) -> None:
    """
    Resetting the current streak to default value: 0

    ----- Arguments -----
    session (Session):      Containing the reference to the database session.
    habit_object (Habit):   A habit object that will be changed.
    """
    habit_object.habit_current_streak = 0
    session.commit()


def reset_tracking_status(session: Session, habit_object: Habit) -> None:
    """
    Resetting the tracking status to default value: False

    ----- Arguments -----
    session (Session):      Containing the reference to the database session.
    habit_object (Habit):   A habit object that will be changed.
    """
    habit_object.habit_tracking_status = False
    session.commit()


def reset_start_date(session: Session, habit_object: Habit) -> None:
    """
    Resetting the start date to default value: None

    ----- Arguments -----
    session (Session):      Containing the reference to the database session.
    habit_object (Habit):   A habit object that will be changed.
    """
    habit_object.habit_start_date = None
    session.commit()


def reset_next_due(session: Session, habit_object: Habit) -> None:
    """
    Resetting the next due date to default value: None

    ----- Arguments -----
    session (Session):      Containing the reference to the database session.
    habit_object (Habit):   A habit object that will be changed.
    """
    habit_object.habit_next_due = None
    session.commit()


def reset_total_fails(session: Session, habit_object: Habit) -> None:
    """
    Resetting the total number of fails to default value: 0

    ----- Arguments -----
    session (Session):      Containing the reference to the database session.
    habit_object (Habit):   A habit object that will be changed.
    """
    habit_object.habit_total_fails = 0
    session.commit()


def set_tracking_status_to_true(session: Session, habit_object: Habit) -> None:
    """
    Sets the tracking status to True.

    ----- Description -----
    This function sets the tracking status to True and calls the function to
    create a new entry in the history.

    ----- Arguments -----
    session (Session):      Containing the reference to the database session.
    habit_object (Habit):   A habit object that will be changed.
    """
    habit_object.habit_tracking_status = True
    session.commit()
    create_new_history_entry(session=session, habit_object=habit_object)


def streak_calculator(session: Session, habit_object: Habit) -> None:
    """
    Calculating the current and highscore streak.

    ----- Description -----
    This function increases the current streak value of a habit object.
    If the current streak is higher than the highscore, the highscore will be
    updated.

    ----- Arguments -----
    session (Session):      Containing the reference to the database session.
    habit_object (Habit):   A habit object that will be changed.
    """
    habit_object.habit_current_streak = habit_object.habit_current_streak + 1
    habit_object.habit_highscore_streak = max(
        habit_object.habit_highscore_streak, habit_object.habit_current_streak
    )
    session.commit()
