import os
import json
import re
import argparse
import sys

# Relations between organisations (plan-of-action §8). Each org page may carry one line
#   relations: [{"type": "member_of", "target": "310", "since": "", "until": "", "source": "https://…", "status": "documented"}]
# stored on one side only; the other side's view ("members", …) is generated here.
RELATION_TYPES = {"member_of", "affiliated_with", "coalition_partner", "split_from", "merged_into", "successor_of"}
RELATION_STATUSES = {"self_declared", "documented", "disputed"}
RELATION_FIELDS = ("type", "target", "since", "until", "source", "status")

def extract_frontmatter(content):
    """Extract frontmatter from markdown content"""
    pattern = r'^---\n(.*?)\n---'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        frontmatter = {}
        for line in match.group(1).split('\n'):
            if ':' in line:
                # Split only on first colon
                key, value = line.split(':', 1)
                # Remove quotes and whitespace
                key = key.strip()
                if key == "relations":
                    frontmatter[key] = json.loads(value.strip() or "[]")
                    continue
                # Remove quotes and whitespace
                value = value.strip().strip('"\'')
                frontmatter[key] = value
        return frontmatter
    return None

def process_directory(directory_path, output_file):
    """Process all markdown files in directory and create JSON"""
    entries = []
    
    # Walk through all files in directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.md'):
            file_path = os.path.join(directory_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    frontmatter = extract_frontmatter(content)
                    if frontmatter:
                        entries.append(frontmatter)
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

    relations = build_relations(entries)

    # Write to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=4)

    relations_file = os.path.join(os.path.dirname(output_file), "relations.json")
    with open(relations_file, 'w', encoding='utf-8') as f:
        json.dump(relations, f, ensure_ascii=False, indent=1)

    print(f"Successfully processed {len(entries)} files into {output_file}")
    print(f"{sum(len(r['out']) for r in relations.values())} relations written to {relations_file}")


def build_relations(entries):
    """Org id -> {"out": relations it declares, "in": relations others declare about it}.

    A relation without a public source, or with an unknown type, status or target, stops the build:
    no connection is shown without a source (plan-of-action rule 5)."""
    by_id = {e.get("id"): e for e in entries if not e.get("deleted_at")}
    ref = lambda oid: {"id": oid, "name_fa": by_id[oid].get("name_fa", ""),
                       "name_en": by_id[oid].get("name_en", ""), "pageLink": by_id[oid].get("pageLink", "")}
    out, errors = {}, []
    for e in by_id.values():
        for r in e.get("relations") or []:
            where = f"{e.get('title')} (id {e.get('id')})"
            unknown = set(r) - set(RELATION_FIELDS)
            if unknown: errors.append(f"{where}: unknown relation fields {sorted(unknown)}")
            if r.get("type") not in RELATION_TYPES: errors.append(f"{where}: unknown relation type {r.get('type')!r}")
            if r.get("status") not in RELATION_STATUSES: errors.append(f"{where}: unknown relation status {r.get('status')!r}")
            if not str(r.get("source", "")).startswith(("https://", "http://")): errors.append(f"{where}: relation to {r.get('target')} has no source URL")
            if r.get("target") not in by_id: errors.append(f"{where}: relation target {r.get('target')!r} is not an organisation")
            if r.get("target") == e.get("id"): errors.append(f"{where}: relation to itself")
            rel = {k: r.get(k, "") for k in RELATION_FIELDS if k != "target"}
            if r.get("target") in by_id:
                out.setdefault(e["id"], {"out": [], "in": []})["out"].append(rel | {"org": ref(r["target"])})
                out.setdefault(r["target"], {"out": [], "in": []})["in"].append(rel | {"org": ref(e["id"])})
    if errors:
        sys.exit("Invalid relations:\n  " + "\n  ".join(errors))
    return out

def main():
    parser = argparse.ArgumentParser(description='Convert markdown frontmatter to JSON')
    parser.add_argument('directory', help='Directory containing markdown files')
    parser.add_argument('--output', '-o', default='output.json', help='Output JSON file path')
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory")
        return
    
    process_directory(args.directory, args.output)

if __name__ == "__main__":
    main()
