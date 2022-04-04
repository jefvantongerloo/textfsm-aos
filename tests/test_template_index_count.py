import textfsm_aos
from textfsm_aos import templates
import importlib.resources as pkg_resources


def test_template_index_count():
    len_template_files = 0

    template_index = textfsm_aos.parser._get_template_index()
    len_template_index = len(template_index)

    template_files = pkg_resources.contents(templates)
    for template in template_files:
        if template.find("ale_") != -1:
            len_template_files += 1

    assert len_template_files == len_template_index
