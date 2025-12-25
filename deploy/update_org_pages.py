import json
import os
import datetime
import re

this_file_path = os.path.abspath(__file__)
this_dir_path = os.path.dirname(this_file_path)
json_file_path = os.path.join(
    this_dir_path, "..", "static", "data", "data.json")
output_dir = os.path.join(this_dir_path, "..", "src", "content", "org-pages")


def log(message):
    print(f"{datetime.datetime.now()} - {message}")


def _(t):
    return str(t).replace("\n", "").replace("\r", "").strip().replace('"', "'")


def getMarkdownContent(entry: dict, title: str):
    return f"""---
title: "{_(title)}"
id: "{_(entry.get('id', ''))}"
org_type: "{_(entry.get('org_type', ''))}"
pageLink: "{_(entry.get('pageLink', ''))}"
logo: "{_(entry.get('logo', ''))}"
name_fa: "{_(entry.get('name_fa', ''))}"
name_en: "{_(entry.get('name_en', ''))}"
name_short: "{_(entry.get('name_short', ''))}"
location: "{_(entry.get('location', ''))}"
post_location: "{_(entry.get('post_location', ''))}"
internetAddress: "{_(entry.get('internetAddress', ''))}"
contact: "{_(entry.get('email', ''))}"
phone: "{_(entry.get('phone', ''))}"
about: "{_(entry.get('about', ''))}"
expertise: "{_(entry.get('expertise', ''))}"
history: "{_(entry.get('history', ''))}"
manifest: "{_(entry.get('manifest', ''))}"
coc: "{_(entry.get('coc', ''))}"
estimationOfMembers: "{_(entry.get('estimationOfMembers', ''))}"
political_orientation: "{_(entry.get('political_orientation', ''))}"
markForEdit: "{_(entry.get('markForEdit', ''))}"
social_telegram: "{_(entry.get('social_telegram', ''))}"
social_facebook: "{_(entry.get('social_facebook', ''))}"
social_youtube: "{_(entry.get('social_youtube', ''))}"
social_x: "{_(entry.get('social_x', ''))}"
social_instagram: "{_(entry.get('social_instagram', ''))}"
created_at: "{_(entry.get('created_at', ''))}"
updated_at: "{_(entry.get('updated_at', ''))}"
mark_for_delete: "{_(entry.get('mark_for_delete', ''))}"
delete_reason: "{_(entry.get('delete_reason', ''))}"
deleted_at: "{_(entry.get('deleted_at', ''))}"
headerBg: "background-image: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%);"
---
"""


def getTitle(entry: dict):
    title = entry.get("name_fa")
    if title == "":
        title = entry.get("name_en")
    if title == "":
        title = str(entry.get("name_short"))
    if title == "":
        title = str(entry.get("id"))
    title = title.strip()
    title = title.replace(" ", "-")

    return title


def delete_all_pages():
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        os.remove(file_path)
        log("File deleted: " + file_path)


def mapIDtoFileName(output_dir):
    mapped = {}
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)

        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read()

        delimiter_positions = [
            m.start() for m in re.finditer(r"^---$", content, re.MULTILINE)
        ]

        if len(delimiter_positions) >= 2:
            section_content = content[delimiter_positions[0]
                : delimiter_positions[1]]
            id_pattern = re.compile(r'id:\s*"(.*?)"')
            match = id_pattern.search(section_content)
            if match:
                id_from_file = match.group(1)
                mapped[id_from_file] = filename
            else:
                log(
                    "No ID found in delimited section of file, the file will be deleted: "
                    + file_path
                )
                os.remove(file_path)
        else:
            log(
                "No delimited section found in file, the file will be deleted: "
                + file_path
            )
            os.remove(file_path)
    return mapped


def update_file_content(file_path, entry, title):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        split_by = content.split("---")
        if len(split_by) < 2:
            log(f"File {file_path} is not in the correct format")
            os.remove(file_path)
            create_new_file(file_path, entry, title)
            return
        file_header = split_by[1]
        correct_header = getMarkdownContent(entry, title=getTitle(entry)).split("---")[
            1
        ]

        def to_dict(inp):
            output_dict = {}
            for obj in inp:
                if obj == "":
                    continue
                key = obj.split(":")[0].strip()
                value = ":".join(obj.split(":")[1:]).strip()
                output_dict[key] = value
            return output_dict

        file_header_s = to_dict(file_header.split("\n"))
        correct_header_s = to_dict(correct_header.split("\n"))

        missmatch = False
        for key in correct_header_s.keys():
            if key not in file_header_s.keys():
                missmatch = True
                file_header_s[key] = correct_header_s[key]
            elif file_header_s[key] != correct_header_s[key]:
                missmatch = True
                file_header_s[key] = correct_header_s[key]

        new_file_header = "\n".join(
            [f"{key}: {value}" for key, value in file_header_s.items()]
        )
        new_file_content = (
            split_by[0] + "---\n" + new_file_header + "\n---\n" + split_by[2]
        )

        if missmatch:
            log(f"Header mismatch in file: {file_path}")
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(new_file_content)
                log(f"File updated: {file_path}")

    except Exception as e:
        log(f"Error updating file {file_path}: {e}")


def create_new_file(file_path, entry, title):
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(getMarkdownContent(entry, title))
            log(f"File created: {file_path}")
    except Exception as e:
        log(f"Error creating file {file_path}: {e}")


def process_entry(entry, output_dir, mapped_file):
    title = getTitle(entry)
    filename = title + ".md"
    file_path = os.path.join(output_dir, filename)
    entry["pageLink"] = f"/op/{title}"
    entry_id = str(entry.get("id"))
    if entry_id in mapped_file:
        filename = mapped_file[entry_id]
        file_path = os.path.join(output_dir, filename)
        correct_title = f"{title}.md"
        if filename != correct_title:
            log(f"{filename} != {correct_title}")
            new_file_path = os.path.join(output_dir, correct_title)
            os.rename(file_path, new_file_path)
            file_path = new_file_path
            mapped_file[entry_id] = correct_title
            log(f"File renamed: {file_path} -> {new_file_path}")
        update_file_content(file_path, entry, title)
    else:
        create_new_file(file_path, entry, title)


def main():
    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    os.makedirs(output_dir, exist_ok=True)

    mapped_file = mapIDtoFileName(output_dir)

    for entry in data:
        process_entry(entry, output_dir, mapped_file)

    with open(json_file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # delete_all_pages()
    main()
