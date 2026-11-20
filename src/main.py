"""
Starts the application.

----- Description -----
This module starts the application when executed as the main file.
It sets up the database, creates a session for database interaction, asks
whether standard habits should be added, and then starts the main window.
"""

from db.db_functions import add_standard_habits_to_db
from db.db_setup import start_db, start_db_session
from db.db_standard_entries import (
    standard_habit_active_status,
    standard_habit_description,
    standard_habit_name,
    standard_habit_period,
)
from ui.main_window import MainWindow
from ui.pop_up_windows import InputMessageWindow
from update_loop import loop_for_update_due_date


def main():
    engine = start_db(log=False)
    session = start_db_session(engine=engine)

    input_for_standard_habits = input(
        "If you want to add the standard values type: yes\n"
    )
    if input_for_standard_habits == "yes":
        status_add_standard_habits = add_standard_habits_to_db(
            session,
            standard_habit_name,
            standard_habit_description,
            standard_habit_period,
            standard_habit_active_status,
        )
        InputMessageWindow(message_codes=status_add_standard_habits)

    app = MainWindow(session=session)
    app.main_root.after(
        0, lambda: loop_for_update_due_date(session=session, main_window=app)
    )
    app.main_root.mainloop()


if __name__ == "__main__":
    main()
