# Habit Tracker

A simple desktop habit tracker built with Python, Tkinter, and SQLAlchemy.

## General

### Content

This application lets you create, edit, delete, and track habits. It stores habits and their history in a SQLite database and provides Tkinter windows for the main list, habit history, high scores, and messages.

The repository uses a `src` layout, a Hatchling-based package configuration, a lockfile, and unit tests. `error_code.md` documents the numeric message codes used by the GUI.

### Python version

The project requires Python 3.12 or newer (`requires-python = ">=3.12"` in `pyproject.toml`).

### Libraries

Runtime dependencies:

* SQLAlchemy `>=2.0.23` (the lockfile currently resolves 2.1.9)

Standard-library modules used by the application:

* datetime
* os
* random (sample-data script only)
* sys
* tkinter
* unittest

Development and build tooling:

* Hatchling (build backend)
* pytest (configured for test discovery)
* Ruff
* uv (recommended for dependency and environment management)

### Comments and documentation

Project Python files do not use structural comments. Documentation is kept in module, class, and function docstrings; there are no separate per-module documentation files.

## Project layout

```text
.
├── error_code.md
├── habit_tracker.db
├── LICENSE.txt
├── README.md
├── pyproject.toml
├── uv.lock
└── src/
    ├── main.py
    ├── habit_classes.py
    ├── update_loop.py
    ├── db/
    │   ├── __init__.py
    │   ├── add_sample_data.py
    │   ├── db_filter_functions.py
    │   ├── db_functions.py
    │   ├── db_history_functions.py
    │   ├── db_object_functions.py
    │   ├── db_setup.py
    │   └── db_standard_entries.py
    ├── tests/
    │   ├── __init__.py
    │   └── function_test.py
    └── ui/
        ├── __init__.py
        ├── create_new_change_habit_window.py
        ├── habit_history_window.py
        ├── main_window.py
        └── pop_up_windows.py
```

`habit_tracker.db` is created automatically if it does not exist.

## Module / file overview

### Application modules

* `src/main.py` — Entry point; creates the database session, asks whether to add standard habits, and starts the GUI.
* `src/habit_classes.py` — SQLAlchemy models for habits and habit history.
* `src/update_loop.py` — Periodically checks due dates and updates streaks, failures, and tracking status.

### Database modules (`src/db/`)

* `db_setup.py` — Creates the engine, database tables, and session.
* `db_functions.py` — Adds, deletes, and modifies habits.
* `db_object_functions.py` — Updates individual habit attributes such as active/tracking status and streaks.
* `db_history_functions.py` — Adds and deletes habit-history entries.
* `db_filter_functions.py` — Filters habits, history entries, names, and high-score results.
* `db_standard_entries.py` — Lists used to create the standard habits.
* `add_sample_data.py` — Standalone script that replaces the database contents with sample data.

### UI modules (`src/ui/`)

* `main_window.py` — Main application window with filters, habit table, and action buttons.
* `create_new_change_habit_window.py` — Form for creating or editing a habit.
* `habit_history_window.py` — Window that displays and filters habit history.
* `pop_up_windows.py` — High-score window and message/info dialogs.

### Tests and other files

* `src/tests/function_test.py` — Unit tests for the main database functions.
* `error_code.md` — Numeric message codes shown by the GUI.
* `habit_tracker.db` — SQLite database.
* `LICENSE.txt` — License information.
* `pyproject.toml` — Package metadata, dependencies, console script, and pytest configuration.
* `uv.lock` — Locked dependency versions.
* `README.md` — This file.

## Installation

1. Make sure Python 3.12 or newer is installed.
2. Make sure Tkinter is available. On some Linux distributions it is a separate system package, for example `python3-tk`.
3. Clone or download this repository.
4. Install the project and its dependencies:

```bash
uv sync
```

Alternatively, with pip:

```bash
python -m pip install -e .
```

Both commands install SQLAlchemy and make the `habit-tracker` console script available.

## Run instructions

### Run the main application

From the repository root:

```bash
uv run habit-tracker
```

Without uv, after installing the project:

```bash
python src/main.py
```

If you installed dependencies manually without installing the package, add `src` to `PYTHONPATH`:

```bash
PYTHONPATH=src python src/main.py
```

The application first asks:

```text
If you want to add the standard values type: yes
```

The input is case-sensitive: only the exact lowercase word `yes` adds the standard habits. Any other input skips them. Afterward the Tkinter GUI opens.

The standard and sample data each create five habits. The standard data includes one passive habit, and the sample data includes one passive habit plus one active habit whose tracking status is false. Use the `Show tracked/not tracked habits` filter to include passive habits.

### Run the unit tests

From the repository root:

```bash
uv run python -m pytest
```

Without uv:

```bash
PYTHONPATH=src python -m pytest
```

The tests are `unittest.TestCase` classes in `src/tests/function_test.py`, so they can also be run directly:

```bash
uv run python -m unittest tests.function_test
```

All three commands run the same 32 tests.

### Run the sample-data script

From the repository root:

```bash
uv run python src/db/add_sample_data.py
```

Without uv:

```bash
PYTHONPATH=src python src/db/add_sample_data.py
```

The script asks two confirmation questions:

1. `yes` confirms that current data should be replaced.
2. `YES` confirms the final deletion.

Any other answer leaves the database unchanged. The script deletes all existing habits and history entries and then adds five sample habits. The next due dates in the sample data are fixed to `2099-12-01`, but the history timestamps are randomized. Before working with the application normally, it is recommended to delete the sample data through the GUI and create your own habits or use the standard habits.

## Problems running the application

* Check that Python 3.12 or newer is being used.
* Check that SQLAlchemy is installed and at least version 2.0.23.
* Run commands from the repository root, or set `PYTHONPATH=src` when running modules directly.
* If Tkinter is missing, install the Tkinter package provided by your operating system or Python distribution.
* If the console script is not found, run `uv sync` or `python -m pip install -e .` again.

## Additional information on how to use the application

### GUI

The GUI is intentionally simple.

* Tables are displayed without scrollbars.
* Text may not fit in every window; resize the window if needed.
* Selecting several habits and clicking `Change Habit` opens one edit window per selected habit.

### Usage

Create a habit, choose its periodicity, and mark it complete when the due date arrives. The main window shows status information such as current streak, high score, failures, and due date. The history window shows completion and failure entries, and the high-score button shows habits with the best streak.

## Adjusting the application

### Add, modify, or remove standard habits

To add or adjust standard habits:

1. Open `src/db/db_standard_entries.py`.
2. Edit the lists while keeping the same length and using these types:
   * name: `str`
   * description: `str`
   * period: `int`
   * active status: `bool`
3. The in-app form currently supports periods 1, 2, and 7 (daily, every other day, and weekly). The main-window filters also recognize 1, 2, and 7, so using other integers is possible but they will not appear in those filtered views.

To remove standard habits completely:

1. Open `src/main.py`.
2. Remove the imports of `add_standard_habits_to_db` and the `db.db_standard_entries` lists.
3. Remove the `input(...)` line and the following `if input_for_standard_habits == "yes":` block.
4. Remove the `InputMessageWindow` import if it is no longer used in `main.py`.
5. Optionally delete `src/db/db_standard_entries.py`.

To skip the prompt but still add standard habits on every start, remove only the `input(...)` line and make the `add_standard_habits_to_db(...)` call unconditional. Be aware that duplicate names are reported if the habits already exist.

### Periodicity: add choices

To add a new periodicity choice:

1. Open `src/ui/create_new_change_habit_window.py`.
2. In `CreateChangeHabitWindow.__init__`, add the label to `self.period_option_lst`.
3. In the same initialization block, add an `elif` branch that maps the stored integer to the new list index.
4. In `convert_period_to_integer`, add an `elif` branch before the `else` that maps the label back to the number of days.

To add a matching filter button:

1. Open `src/ui/main_window.py`.
2. In `MainWindow.__init__`, create a button using `lambda: self.click_show_period(<days>)`.
3. In the widget-placement section of the same method, add the button to `second_row_widgets`.
4. Open `src/db/db_filter_functions.py` and update `filter_habits`, which currently has hard-coded checks for `(1, 2, 7)`.

Adding buttons can affect the layout; adjust the grid placement if necessary.

### Periodicity: make it free of choice

The history window uses free-form input and validation. Use `src/ui/habit_history_window.py` as a reference:

1. Replace the periodicity dropdown in `src/ui/create_new_change_habit_window.py` with an entry field.
2. Add validation comparable to the history-window filters.
3. Update `filter_habits` in `src/db/db_filter_functions.py` to work with arbitrary values, following the pattern used by `filter_for_history_entries`.

## Styling guidelines

The code tries to follow PEP 8 and PEP 257:

* https://peps.python.org/pep-0008/
* https://peps.python.org/pep-0257/

Ruff is included as a development dependency. Format and lint the code with:

```bash
uv run ruff format .
uv run ruff check .
```

All Python files are formatted with Ruff; documentation is kept in docstrings rather than structural comments.

## Final words

This is the original course project, with the repository restructured into the current `src` layout and updated build tooling. If you find documentation mistakes, please open an issue in GitHub.
