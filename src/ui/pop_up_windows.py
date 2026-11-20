"""
This module contains two smaller helper windows.

----- Classes -----
ShowHighscoreWindow:    Class to open a window that shows the habits with the
                        highscore streak.
InputMessageWindow:     Class to open a window to give the user feedback about
                        warnings and errors.
"""

import tkinter as tk
from tkinter import ttk

from db.db_filter_functions import (
    filter_for_highscore_objects_in_db,
    search_for_highscore_in_db,
)


class ShowHighscoreWindow:
    """
    Creates a window to show the user the habits having the highest streak.

    ----- Attributes -----
    session (Session):      Containing the reference to the database session.
    highscore_root (tk.Tk): Representation of the main Tkinter window. There
    are more attributes, like for frames, labels, buttons etc, as well as for
    data handling within the class.

    ----- Methods -----
    load_highscore_data_to_table:   Loads the data from the database into the
                                    table.
    click_close_window:             Closes the window.
    """

    def __init__(self, session):
        """
        Constructor for the ShowHighscoreWindow class.

        ----- Arguments -----
        session (Session):  Containing the reference to the database session.
        """

        self.highscore_root = tk.Tk()
        self.highscore_root.geometry("400x400")
        self.highscore_root.title("High Score Streak - Habit Tracker")
        self.highscore_root.grid_columnconfigure(0, weight=1)

        self.highscore_frame = tk.Frame(self.highscore_root)
        self.highscore_frame.grid(sticky="nsew")
        self.subframe_table = tk.Frame(self.highscore_frame)
        self.subframe_table.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.subframe_close_button = tk.Frame(self.highscore_frame)
        self.subframe_close_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.highscore_frame.grid_columnconfigure(0, weight=1)
        self.highscore_frame.grid_columnconfigure(1, weight=1)
        self.subframe_table.grid_columnconfigure(0, weight=1)
        self.subframe_close_button.grid_columnconfigure(0, weight=1)

        self.session = session

        self.close_button = tk.Button(
            self.subframe_close_button,
            text="Close window",
            command=self.click_close_window,
        )

        column_lst = [
            "habit_name",
            "habit_highscore_streak",
        ]
        self.habit_highscore_table = ttk.Treeview(
            self.subframe_table, column=column_lst, show="headings"
        )
        for entry in column_lst:
            formatted_heading = " ".join(entry.split("_")).capitalize()
            self.habit_highscore_table.heading(
                entry, text=formatted_heading, anchor=tk.W
            )
            self.habit_highscore_table.column(entry, minwidth=50)
        self.load_highscore_data_to_table()

        self.habit_highscore_table.grid(
            row=0, column=0, padx=10, pady=10, sticky="nsew"
        )
        self.close_button.grid(row=0, column=0, padx=10, pady=10, sticky="e")

    def load_highscore_data_to_table(self):
        """
        This function is used to load the habit entries in the database into
        the table.

        ----- Description -----
        This function finds the highest value in the highscore column and then
        filters all habits that have this value, in case several habits share
        the same highscore.
        """
        highscore_value = search_for_highscore_in_db(session=self.session)
        highscore_objects = filter_for_highscore_objects_in_db(
            session=self.session, highscore_value=highscore_value
        )

        for highscore_habit in highscore_objects:
            self.habit_highscore_table.insert(
                parent="",
                index="end",
                value=(
                    highscore_habit.habit_name,
                    highscore_habit.habit_highscore_streak,
                ),
            )

    def click_close_window(self):
        """
        Closes the window.
        """
        self.highscore_root.destroy()


class InputMessageWindow:
    """
    Creates a window that displays the error and warnings.

    ----- Attributes -----
    message_codes (list):   List of error codes.

    ----- Methods -----
    click_close_window:     Closes the window.
    """

    def __init__(self, message_codes):
        """
        Constructor of the class.

        ----- Arguments -----
        message_codes (list):   List of error codes.
        """
        messages = {
            0: "Habit successfully added to the database.",
            1: "ERROR: A habit with this name already exists.",
            100: "WARNING: Name was converted to a string.",
            101: "WARNING: Description was converted to a string.",
            112: "ERROR: Active status was not a boolean. No data added.",
            113: "ERROR: Periodicity was not an integer. No data added.",
            114: "ERROR: Name cannot be None or empty.",
            120: "ERROR: Standard periodicity does not contain only integers.",
            121: "ERROR: Standard active status does not contain only booleans.",
            122: "ERROR: Standard lists have different lengths.",
            123: "ERROR: Not all inputs are lists.",
            200: (
                "ERROR: Habit tracking status cannot be changed; "
                "habit is marked as passive."
            ),
            201: "WARNING: Habit already marked as complete for this due date.",
            301: "Name of habit changed.",
            302: "Description of habit changed.",
            303: "Periodicity of habit changed.",
            304: "Active status of habit changed.",
            401: "WARNING: No name changed.",
            402: "WARNING: No description changed.",
            403: "WARNING: No periodicity changed.",
            404: "WARNING: No active status changed.",
            411: "WARNING: Description is None. Set to default.",
            412: "WARNING: Periodicity is None or empty. Set to default 1.",
            413: "WARNING: Active status is None or empty. Set to default False.",
        }

        if message_codes:
            self.input_message_root = tk.Tk()
            self.input_message_root.geometry("480x280")
            self.input_message_root.title("Information - Habit Tracker")
            self.input_message_frame = tk.Frame(self.input_message_root)
            self.input_message_frame.pack(fill="both", expand=True)
            self.ok_button = tk.Button(
                self.input_message_frame,
                text="OK",
                command=self.click_close_window,
                width=15,
            )
            self.ok_button.pack(padx=10, pady=10)
            for code in message_codes:
                message_text = messages.get(code, f"Unknown error: Code {code}")
                label = tk.Label(self.input_message_frame, text=message_text)
                label.pack(anchor="w", padx=10, pady=10)

    def click_close_window(self):
        """
        Closes the window.
        """
        self.input_message_root.destroy()
