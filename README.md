# LINDA

## Installation Instructions

1. Download Linda: `git clone https://www.github.com/benbuc/Linda.git` and `cd` into the newly created folder.

2. Copy `.env_example`to `.env` and put email settings

3. Optionall install [poetry](https://github.com/python-poetry/poetry) if not already installed.
   ```bash
   curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
   ```

4. Install project. This will create a virtual environment with all the python dependencies
   ```bash
   poetry install
   ```

5. Now a virtual environment was created in the current folder. You can enter this environment using:
   ```bash
   poetry shell
   ```

6. Inside this environment you can run Linda using the command `runlinda`. Optionally (for example when using a cronjob) you can use this command from outside the virtual environment to achieve the same effect
   ```bash
   runlinda # from inside the virtual environment
   poetry run runlinda # from outside the venv
   ```
    You can execute Linda as often as you want to check for new values from a cronjob.
7. There is a helper command to aid the creation of new services: `setuplinda`. This can be run equally to the prior step.

> :warning: **Executing untrusted Services, Triggers or Actions could run arbitrary code**: Linda uses jsonpickle which could run arbitrary code during the deserialization process!

## `Service`

## `Trigger`
A Trigger implements a checker. You can ask the Trigger whether it is triggered.


| Method          | Description           |
| --------------- | --------------------- |
| `isTriggered()` | will return a boolean |

| Init Variable | Description                                                                |
| ------------- | -------------------------------------------------------------------------- |
| `datapath`    | The path where the Trigger is allowed to save data it needs for the future |
| `name`        | a unique name for the Trigger                                              |

### `DeviationTriggerTwoThresholds`
The `DeviationTriggerTwoThresholds` checks whether a given value exceeds the threshold (trigger threshold) and then triggers once. It then does not trigger again until the value crossed the reset threshold.

These methods usually should not be called from outside the Trigger, but are explained here for reference.

| Method               | Description                                                    |
| -------------------- | -------------------------------------------------------------- |
| `loadCurrent()`      | Tries to read the current value from `datafile` and returns it |
| `getStateFilepath()` | Assembles filepath for file holding the current trigger state  |
| `getState()`         | Loads the current trigger state from file                      |
| `setState()`         | Saves the current trigger state to file                        |

| Init Variable       | Description                                                                                                                                                 |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `trigger_threshold` | The threshold which has to be crossed (in direction from `reset_threshold` for the trigger to fire                                                          |
| `reset_threshold`   | when fired, trigger becomes active again, when the reset threshold is crossed again, to prevent triggering multiple times                                   |
| `datafile`          | The filepath where the input data will be stores. This file has to be created by the user. It must be a text file containing a single number (e.g. `32.67`) |