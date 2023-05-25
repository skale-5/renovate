"""Tests."""

import pathlib

from typing import Generator

import pytest

from click.testing import CliRunner

from cookiecutter_docs import cli


OUTPUT_FILE = "outputs/README.md"


@pytest.fixture
def create_output_file() -> Generator:
    """Create base file for all tests."""
    # before test - create resource
    file_path = pathlib.Path(OUTPUT_FILE)
    file_path.write_text("<!-- BEGIN_COOKIECUTTER_DOCS -->\n<!-- END_COOKIECUTTER_DOCS -->")

    yield file_path
    # after test - remove resource
    file_path.unlink()


# pylint: disable=W0613
def test_convert_json_to_markdown_only_verify(create_output_file: function) -> None:
    """Test with incomplete doc in cookiecutter.json (only verify)."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["--input-file", "tests/incomplete.json", "--output-file", OUTPUT_FILE, "--only-verify"],
    )
    with open(OUTPUT_FILE, "r") as f:
        content = f.read()

    assert result.exit_code == 1
    assert (
        content
        == """<!-- BEGIN_COOKIECUTTER_DOCS -->
<!-- END_COOKIECUTTER_DOCS -->"""
    )


# pylint: disable=W0613
def test_convert_json_to_markdown_strict(create_output_file: function) -> None:
    """Test with incomplete doc in cookiecutter.json (strict)."""

    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["--input-file", "tests/incomplete.json", "--output-file", OUTPUT_FILE, "--strict"],
    )
    with open(OUTPUT_FILE, "r") as f:
        content = f.read()

    assert result.exit_code == 1
    assert (
        content
        == """<!-- BEGIN_COOKIECUTTER_DOCS -->
<!-- END_COOKIECUTTER_DOCS -->"""
    )


# pylint: disable=W0613
def test_convert_json_to_markdown_incomplete(create_output_file: function) -> None:
    """Test with incomplete doc in cookiecutter.json."""

    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["--input-file", "tests/incomplete.json", "--output-file", OUTPUT_FILE],
    )
    with open(OUTPUT_FILE, "r") as f:
        content = f.read()

    assert result.exit_code == 0
    assert (
        content
        == """<!-- BEGIN_COOKIECUTTER_DOCS -->
|  Key   | Default | Description  |
| ------ | ------- | ------------ |
| input1 | value1  | description1 |
| input2 | value2  | description2 |
| input3 | value3  |              |

<!-- END_COOKIECUTTER_DOCS -->"""
    )


# pylint: disable=W0613
def test_convert_json_to_markdown_list(create_output_file: function) -> None:
    """Test with list in cookiecutter.json."""

    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["--input-file", "tests/list.json", "--output-file", OUTPUT_FILE],
    )
    with open(OUTPUT_FILE, "r") as f:
        content = f.read()

    assert result.exit_code == 0
    assert (
        content
        == """<!-- BEGIN_COOKIECUTTER_DOCS -->
|  Key   |                Default                 | Description  |
| ------ | -------------------------------------- | ------------ |
| input1 | ['value1', 'value2'] (Default: value1) | description1 |
| input2 | value2                                 | description2 |

<!-- END_COOKIECUTTER_DOCS -->"""
    )
