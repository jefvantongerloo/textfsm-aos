"""Textfsm-aos.parse."""
import yaml
import importlib.resources as pkg_resources
from scrapli.helper import textfsm_parse
from . import templates


def _get_template_index() -> dict:
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
    structured_response = textfsm_parse(template, data)
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
        return structured_response
    else:
        raise Exception(
            "Unable to find platform:{0} or command:{1} in supported values.".format(
                platform, command
            )
        )
