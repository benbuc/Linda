# LINDA

## Installation Instructions

1. Download Linda: `git clone https://www.github.com/benbuc/Linda.git`

1. Rename `configsample.ini` to `lindaconfig.ini`: `mv configsample.ini lindaconfig.ini`

1. Put in your E-Mail Data and Settings into `lindaconfig.ini`

1. Execute `Linda.py` as often as you want: `python3 Linda.py`. You could - for example - use a cronjob to run Linda every minute.

1. Setup your Services using `LindaSetup.py` by running: `python3 LindaSetup.py`. Linda will do her best to guide you through the process.

### Development Setup

1. Install [poetry](https://github.com/python-poetry/poetry)
   ```bash
   curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
   ```
1. Install the dependencies
   ```bash
   poetry install
   ```
1. Install the [pre-commit](https://github.com/pre-commit/pre-commit) hooks
   ```bash
   pre-commit install
   ```

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
