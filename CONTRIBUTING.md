## How to contribute

1. Fork and create a branch with naming `<platform>_<command>` (for example: ale_aos8_show_system).

2. Add TextFSM template file in templates folder with naming `<platform>_<command>.textfsm`.

3. Add entry in templates_index with attribute command and platform.

4. Add test folder in 'templates' with naming `<platform>_<command>`.

5. Add sample cli output file in newly created folder `<platform>_<command>.txt`.

6. Add expected parsed data from sample cli output in `<platform>_<command>.yml`.

7. Run linting `tox` and tests `pytest`.

## How to setup development environment

1. Install `Poetry` package manager via `pip install poetry`

2. Install dev dependencies and textfsm-aos package in development mode with `poetry install`

3. Open virtual environment `poetry shell`
