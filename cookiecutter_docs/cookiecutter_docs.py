"""cookiecutter-docs CLI."""

import json
import sys

from collections import OrderedDict
from typing import Any, List

import click

from pytablewriter import MarkdownTableWriter

from .models.entry import Entry
from .version import __version__


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
@click.option(
    "--version",
    default=False,
    help="Print CLI version.",
    is_flag=True,
)
def cli(
    input_file: str,
    output_file: str,
    anchor_start: str = "<!-- BEGIN_COOKIECUTTER_DOCS -->",
    anchor_stop: str = "<!-- END_COOKIECUTTER_DOCS -->",
    strict: bool = False,
    only_verify: bool = False,
    version: bool = False,
) -> None:
    if version:
        click.echo(__version__)
        sys.exit(0)

    try:
        with open(input_file, "r") as json_file:
            data: OrderedDict[str, Any] = json.load(json_file, object_pairs_hook=OrderedDict)
    except FileNotFoundError:
        click.echo(click.style("Json file cannot be found.", fg="red"), err=True)
        sys.exit(1)
    except json.JSONDecodeError:
        click.echo(click.style("Json file cannot be decoded.", fg="red"), err=True)
        sys.exit(1)

    table: List[Entry] = []
    critical = False
    for k, v in data.items():
        if not k.startswith("_"):
            description = data.get(f"{PREFIX_DOC}{k}") if data.get(f"{PREFIX_DOC}{k}") is not None else ""
            if description == "":
                click.echo(
                    click.style(f"Description is not valid for value {k}", fg="yellow"),
                    err=True,
                )
                if strict:
                    critical = True
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
    if critical:
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
        click.echo(click.style("Markdown file cannot be found", fg="red"), err=True)
        sys.exit(1)

    start_index = content.find(anchor_start)
    end_index = content.find(anchor_stop)
    if start_index == -1 or end_index == -1:
        click.echo("No anchors found to inject markdown table")
        sys.exit(0)

    updated_content = content[: start_index + len(anchor_start)] + "\n" + str(table_md) + "\n" + content[end_index:]

    if only_verify:
        if updated_content != content:
            click.echo(click.style("Documentation is not up to date.", fg="red"), err=True)
            sys.exit(1)
        else:
            click.echo("Documentation is up to date.")
            sys.exit(0)

    # Écriture du contenu mis à jour dans le fichier Markdown
    try:
        with open(output_file, "w") as markdown_file:
            markdown_file.write(updated_content)
        click.echo("Markdown injection success.")
        sys.exit(0)
    except IOError:
        click.echo(click.style("Fail to inject markdown.", fg="red"), err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
