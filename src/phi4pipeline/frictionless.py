import json

from os import PathLike
from string import Template


def load_formatted_datapackage(
    template_path: PathLike, format_args: dict[str, str]
) -> dict:

    with open(template_path, encoding='utf-8') as file:
        template_str = file.read()
    template = Template(template_str)
    datapackage = json.loads(template.substitute(**format_args))
    for resource in datapackage['resources']:
        resource['bytes'] = int(resource['bytes'])
    return datapackage
