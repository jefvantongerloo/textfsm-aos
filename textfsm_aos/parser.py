"""Textfsm-aos.parse."""
import importlib.resources as pkg_resources
import yaml
from textfsm import TextFSM
from . import templates


def _get_template_index() -> list:
    """Get textfsm template index."""
    template_index = yaml.safe_load(
        pkg_resources.read_text(templates, "templates_index.yml")
    )
    return template_index


def _search_template_index(platform: str, command: str) -> dict:
    """Search entry in template index based on command."""
    template_index = _get_template_index()
    for item in template_index:
        if item["command"] == command and item["platform"] == platform:
            return item
    return None


def _parse_textfsm(template: dict, data: str) -> list:
    """Parse semi-structured cli output to json."""
    template_name = str(template["command"]).replace(" ", "_") + ".textfsm"
    template_path = template["platform"] + "_" + template_name
    template = pkg_resources.open_text(templates, template_path)

    with open(template.name, encoding="utf-8") as file:
        template = TextFSM(file)

    parsed_result = template.ParseText(data)
    structured_response = [dict(zip(template.header, pr)) for pr in parsed_result]

    return structured_response


def parse(platform: str, command: str, data: str) -> list:
    """Parse output with TextFSM to return structured data.

    Args:
        platform: Network operating system - 'ale_aos6' or 'ale_aos8'
        command: CLI command
        data: Raw data returned from transport

    Returns:
        output: structured data (dict)
    """
    template_index = _search_template_index(platform, command)
    if template_index:
        structured_response = _parse_textfsm(template_index, data)
    else:
        raise Exception(
            f"Unable to find platform:{platform} or command:{command} in supported values."
        )

    return structured_response
