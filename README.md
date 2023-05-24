# Cookiecutter-docs

[![pipeline status](https://git.sk5.io/skale-5/docker-images/cookiecutter-docs/badges/main/pipeline.svg?ignore_skipped=true)](https://git.sk5.io/skale-5/docker-images/cookiecutter-docs/-/commits/main)
[![Latest Release](https://git.sk5.io/skale-5/docker-images/cookiecutter-docs/-/badges/release.svg)](https://git.sk5.io/skale-5/docker-images/cookiecutter-docs/-/releases)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)


`cookiecutter-docs` is inspired from terraform-docs to autogenerate the documentation from cookiecutter.json to a markdown file.

As for now, cookiecutter does not support YAML on his configuration file (only JSON).

To simulate the ability to add a description to each input variable, we use a workaround only available in cookiecutter > 2.x:

Here is an example of a `cookiecutter.json` file:

```json
{
  "input1": "value1",
  "input2": "value2",
  "input3": "value3",

  "_DOC_input1": "description1",
  "_DOC_input2": "description2",
  "_DOC_input3": "description3"
}
```

## Installation

Require Python >= 3.8

### Remote (recommended)
```bash
pip install -U git+ssh://git@git.sk5.io/skale-5/docker-images/cookiecutter-docs.git@vX.Y.Z
```


# Available flags

| Flag           | Description                                              | Default                          |
| -------------- | -------------------------------------------------------- | -------------------------------- |
| --input-file   | JSON file to configure cookiecutter                      | cookiecutter.json                |
| --output-file  | Markdown file to inject documentation                    | README.md                        |
| --anchor-start | Beginning line where the mardown is injected             | <!-- BEGIN_COOKIECUTTER_DOCS --> |
| --anchor-stop  | Ending line where the mardown is injected                | <!-- END_COOKIECUTTER_DOCS -->   |
| --strict       | Returns an error if the JSON file is not well documented | False                            |
| --only-verify  | Do not override the file, only compare it                | False                            |


## Usage

### CLI

```bash
cookiecutter-docs --input-file cookiecutter.json --output-file README.md
```

### Docker

```bash
docker run --rm -it -v $(pwd):/data skale-5/cookiecutter-docs --input-file data/cookiecutter.json --output-file data/README.md
```

### Pre-commits

```yaml
repos:
  - repo: git@git.sk5.io:skale-5/docker-images/cookiecutter-docs.git
    rev: main
    hooks:
      - id: cookiecutter-docs
```

### CI

```yaml
cookiecutter-docs:
  stage: quality
  image:
    name: "skale5/cookiecutter-docs"
    entrypoint: [""]
  script:
    - cookiecutter-docs --only-verify --strict
```
