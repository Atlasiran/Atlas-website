import json
import argparse
import logging
from pathlib import Path

def find_unexpected_fields(json_path, debug=False):
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
    
    # Get all unique keys from all records
    all_keys = set()
    for item in data:
        all_keys.update(item.keys())
    
    # Get keys from first record
    expected_keys = set(data[0].keys())
    
    # Find unexpected keys
    unexpected = all_keys - expected_keys
    
    # Report findings
    if unexpected:
        logging.warning(f"Found unexpected fields: {unexpected}")
        for idx, item in enumerate(data):
            unexpected_in_item = {k: item[k] for k in item.keys() if k in unexpected}
            if unexpected_in_item:
                logging.warning(f"Record {idx} has unexpected fields: {unexpected_in_item}")
    else:
        logging.info("No unexpected fields found")
    
    # Check for missing required fields
    required_fields = {'title', 'id', 'org_type', 'pageLink'}
    missing_required = [idx for idx, item in enumerate(data) 
                       if not all(field in item for field in required_fields)]
    
    if missing_required:
        logging.error(f"Records missing required fields: {missing_required}")
    
    return bool(unexpected or missing_required)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check JSON data integrity')
    parser.add_argument('json_file', help='Path to JSON file')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    args = parser.parse_args()

    try:
        has_issues = find_unexpected_fields(args.json_file, args.debug)
        exit_code = 1 if has_issues else 0
        exit(exit_code)
    except Exception as e:
        logging.error(f"Error: {e}")
        exit(1)