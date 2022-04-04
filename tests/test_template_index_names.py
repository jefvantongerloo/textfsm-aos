import textfsm_aos
from textfsm_aos import templates
import importlib.resources as pkg_resources


def test_template_index_names():
    template_files_ale = []
    template_index_ale = []
    template_files = pkg_resources.contents(templates)
    template_index = textfsm_aos.parser._get_template_index()

    for template in template_files:
        if template.find("ale_") != -1:
            template_files_ale.append(template.split(".")[0])

    for template in template_index:
        template_index_ale.append(
            template["platform"]
            + "_"
            + template["command"].replace(" ", "_")
            + ".textfsm"
        )

    assert template_index_ale.sort() == template_files_ale.sort()
