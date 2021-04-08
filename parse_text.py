import textfsm
import os
from tabulate import tabulate
from rich import print
from rich.table import Table


def get_templates_dir():
    templates_dir = os.environ.get("TEMPLATES_DIR")
    if templates_dir is None:
        package_dir = os.path.dirname(__file__)
        templates_dir = os.path.join(package_dir, "templates/")

    return templates_dir


def get_test_dir():
    test_dir = os.environ.get("TEST_DIR")
    if test_dir is None:
        package_dir = os.path.dirname(os.path.dirname(__file__))
        test_dir = os.path.join(package_dir, "test/")

    return test_dir


def rich_table(items):
    """Generate Rich terminal tables"""

    table = Table(title="Variables")

    table.add_column("Key", justify="left", style="bold cyan")
    table.add_column("Value", justify="left", style="bold yellow")

    for item in fsm_results:
        for key, value in item.items():
            table.add_row(key, value)

    return table


# Raw "show microcode" input
input_file = open(
    get_test_dir() + "alcatel_aos6_show_interface_status.txt", encoding="utf-8"
)
raw_text_data = input_file.read()
input_file.close()

# Run the text through the FSM.
# The argument 'template' is a file handle and 'raw_text_data' is a
# string with the content from the show_microcode.txt file
template = open(get_templates_dir() + "alcatel_aos6_show_interface_status.textfsm")

re_table = textfsm.TextFSM(template)
fsm_results = re_table.ParseText(raw_text_data)

# Generate rich table
print(fsm_results)
print(tabulate(fsm_results, headers=re_table.header))

var = 1
