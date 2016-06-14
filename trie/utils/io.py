import json


def write_json_to_file(data, output_file):
    """Write data to an output file as json."""
    with open(output_file, 'w') as outfile:
        json.dump(data, outfile)
