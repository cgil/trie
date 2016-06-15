import json


def write_json_to_file(data, output_file):
    """Write data to an output file as json."""
    with open(output_file, 'w') as outfile:
        json.dump(data, outfile)


def get_json_from_file(file_path):
    """Gets json from a file."""
    with open(file_path, 'r') as infile:
        data = json.load(infile)
    return data
