import os
from textfsm import clitable
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


def clitable_to_dict(cli_table):
    """Convert TextFSM cli_table object to list of dictionaries."""
    objs = []
    for row in cli_table:
        temp_dict = {}
        for index, element in enumerate(row):
            temp_dict[cli_table.header[index].lower()] = element
        objs.append(temp_dict)

    return objs


# Raw "show microcode" input
input_file = open(get_test_dir() + "alcatel_aos6_show_vlan.txt", encoding="utf-8")
raw_text_data = input_file.read()
input_file.close()

cli_table = clitable.CliTable("index", get_templates_dir())
cli_table.ParseCmd(raw_text_data, {"Platform": "aos6", "Command": "show vlan"})

print(clitable_to_dict(cli_table))
