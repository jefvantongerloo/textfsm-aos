"""Pytests for TextFSM_aos project."""

import yaml
import pytest
import textfsm_aos


def _get_raw(platform: str, command: str) -> str:
    """Get raw cli output."""
    command = str(command.replace(" ", "_"))
    with open(
        "tests/" + platform + "_" + command + "/" + platform + "_" + command + ".txt",
        "r",
        encoding="utf-8",
    ) as structured:
        raw = structured.read()
    return raw


def _get_benchmark(platform: str, command: str) -> dict:
    """Get benchmark structured datas."""
    # template_index = parser.search_template_index(platform, command)
    command = str(command.replace(" ", "_"))
    with open(
        "tests/" + platform + "_" + command + "/" + platform + "_" + command + ".yml",
        "r",
        encoding="utf-8",
    ) as structured:
        benchmark_parsed = yaml.safe_load(structured.read())
    return benchmark_parsed


@pytest.mark.parametrize("template", textfsm_aos.parser._get_template_index())
def test_parsed_data(template: dict):
    """Test parsed data against benchmark."""
    raw_data = _get_raw(template["platform"], template["command"])
    parsed_data = textfsm_aos.parser.parse(
        template["platform"], template["command"], raw_data
    )
    benchmark_data = _get_benchmark(template["platform"], template["command"])

    print(f"Parsed data: \n {parsed_data} \n")
    print(f"Benchmark data: \n {benchmark_data} \n")

    assert parsed_data == benchmark_data
