"""cookiecutter-docs CLI."""

import json
import logging
import sys

from collections import OrderedDict
from typing import Any, List

import click

from pytablewriter import MarkdownTableWriter

from .models.entry import Entry


PREFIX_DOC = "_DOC_"


@click.command()
@click.option("--input-file", "input_file", default="cookiecutter.json", help="JSON input file")
@click.option("--output-file", "output_file", default="README.md", help="Markdown output file")
@click.option(
    "--anchor-start",
    "anchor_start",
    default="<!-- BEGIN_COOKIECUTTER_DOCS -->",
    help="Start of the anchor",
)
@click.option(
    "--anchor-stop",
    "anchor_stop",
    default="<!-- END_COOKIECUTTER_DOCS -->",
    help="Start of the anchor",
)
@click.option(
    "--strict",
    default=False,
    help="If true, exit 1 when documentation is not complete in JSON file",
    is_flag=True,
)
@click.option(
    "--only-verify",
    "only_verify",
    default=False,
    help="Only check that the MarkDown documentation is up to date.",
    is_flag=True,
)
def convert_json_to_markdown(
    input_file: str,
    output_file: str,
    anchor_start: str = "<!-- BEGIN_COOKIECUTTER_DOCS -->",
    anchor_stop: str = "<!-- END_COOKIECUTTER_DOCS -->",
    strict: bool = False,
    only_verify: bool = False,
) -> None:
    try:
        with open(input_file, "r") as json_file:
            data: OrderedDict[str, Any] = json.load(json_file, object_pairs_hook=OrderedDict)
    except FileNotFoundError:
        logging.critical("Json file cannot be found.")
        sys.exit(1)
    except json.JSONDecodeError:
        logging.critical("Json file cannot be decoded.")
        sys.exit(1)

    table: List[Entry] = []
    critical = False
    for k, v in data.items():
        if not k.startswith("_"):
            description = data.get(f"{PREFIX_DOC}{k}") if data.get(f"{PREFIX_DOC}{k}") is not None else ""
            if description == "":
                logging.warning(f"Description is not valid for value {k}")
                if strict:
                    CRITICAL = True
            else:
                if isinstance(v, list):
                    table.append(
                        Entry(
                            key=k,
                            value=f"{str(v)} (Default: {v[0]})",
                            description=str(description),
                        )
                    )
                else:
                    table.append(Entry(key=k, value=v, description=str(description)))
    if CRITICAL:
        sys.exit(1)

    table_md = MarkdownTableWriter(
        table_name="",
        margin=1,
        headers=["Key", "Default", "Description"],
        value_matrix=[[e.key, e.value, e.description] for e in table],
    )

    try:
        with open(output_file, "r") as markdown_file:
            content = markdown_file.read()
    except FileNotFoundError:
        logging.critical("Markdown file cannot be found")
        sys.exit(1)

    start_index = content.find(anchor_start)
    end_index = content.find(anchor_stop)
    if start_index == -1 or end_index == -1:
        logging.info("No anchors found to inject markdown table")
        sys.exit(0)

    updated_content = content[: start_index + len(anchor_start)] + "\n" + str(table_md) + "\n" + content[end_index:]

    if only_verify:
        if updated_content != content:
            logging.critical("Documentation is not up to date.")
            sys.exit(1)
        else:
            logging.info("Documentation is up to date.")
            sys.exit(0)

    # Écriture du contenu mis à jour dans le fichier Markdown
    try:
        with open(output_file, "w") as markdown_file:
            markdown_file.write(updated_content)
        logging.info("Markdown injection success.")
        sys.exit(0)
    except IOError:
        logging.info("Fail to inject markdown.")
        sys.exit(1)


if __name__ == "__main__":
    convert_json_to_markdown()
