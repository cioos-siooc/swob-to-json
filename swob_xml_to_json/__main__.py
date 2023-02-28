import json
import click
from swob_xml_to_json.swob_xml_to_json import swob_xml_to_json

@click.command()
@click.argument("filename", type=click.Path(exists=True))
def main(filename):
    """
    Handle command line interaction via click
    """
    record = swob_xml_to_json(filename)
    print(json.dumps(record, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
