import json
import csv
import argparse
import logging
from pathlib import Path

def json_to_csv(json_path, debug=False):
    # Setup logging
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=log_level, format='%(levelname)s: %(message)s')
    
    # Validate input path
    json_path = Path(json_path)
    if not json_path.exists():
        raise FileNotFoundError(f"JSON file not found: {json_path}")
    
    logging.debug(f"Reading JSON from: {json_path}")
    
    # Read JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            logging.debug(f"Loaded {len(data)} records from JSON")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")

    # Validate data structure
    if not isinstance(data, list):
        raise TypeError("JSON must contain a list of objects")
    if not data:
        raise ValueError("JSON file is empty")
    
    headers = list(data[0].keys())
    logging.debug(f"Headers found: {headers}")
    
    # Write to CSV
    csv_path = json_path.parent / f"{json_path.stem}.csv"
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
            logging.debug(f"Written {len(data)} rows to CSV")
    except IOError as e:
        raise IOError(f"Error writing CSV file: {e}")
    
    return csv_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert JSON file to CSV')
    parser.add_argument('json_file', help='Path to JSON file')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    args = parser.parse_args()

    try:
        output_path = json_to_csv(args.json_file, args.debug)
        print(f"Successfully converted JSON to CSV: {output_path}")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)