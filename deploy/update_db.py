from supabase import create_client, Client
import os
import json


url: str = os.getenv("SUPABASE_URL", "")
key: str = os.getenv("SUPABASE_KEY", "")
users_email: str = os.getenv("SUPABASE_USERS_EMAIL", "")
users_password: str = os.getenv("SUPABASE_USERS_PASSWORD", "")


supabase: Client = create_client(url, key)

# a function that gets the logo of an entity


def get_logo(entity):
    # if a .png file exists with this id in /logos folder, return it
    # otherwise, return a placeholder
    if os.path.exists(f"../static/logos/{entity.get('id', '')}.png"):
        return f"logos/{entity.get('id', '')}.png"
    else:
        return "logos/temporary.png"


def reshape_data(entity):
    reshaped_entity = {
        "id": entity.get("id", ""),
        "logo": f"logos/{entity.get("id", "")}.png",
        "pageLink": entity.get("pageLink", ""),
        "markForEdit": "" if not entity.get("markForEdit") else entity.get("markForEdit"),
        "org_type": entity.get("org_type", ""),
        "name_fa": entity.get("name_fa", ""),
        "name_en": entity.get("name_en", ""),
        "name_short": entity.get("name_short", ""),
        "location": entity.get("location", ""),
        "post_location": entity.get("post_location", ""),
        "internetAddress": entity.get("internetAddress", ""),
        "contact": entity.get("contact", ""),
        "phone": entity.get("phone", ""),
        "about": entity.get("about", ""),
        "expertise": entity.get("expertise", ""),
        "activities": entity.get("activities", ""),
        "history": entity.get("history", ""),
        "manifest": entity.get("manifest", ""),
        "codeOfConduct": entity.get("codeOfConduct", ""),
        "estimationOfMembers": "" if entity.get("estimationOfMembers") == -1 else entity.get("estimationOfMembers"),
        "projects": entity.get("projects", ""),
        "others1": entity.get("others1", ""),
        "others2": entity.get("others2", ""),
        "political_orientation": entity.get("political_orientation", ""),
        "social_instagram": entity.get("social_instagram", []),
        "social_x": entity.get("social_x", []),
        "social_facebook": entity.get("social_facebook", []),
        "name": entity.get("name", "")
    }
    return reshaped_entity


def main():
    user = supabase.auth.sign_in_with_password({
        "email": users_email,
        "password": users_password
    })

    data = supabase.table("Entities").select("*").execute()

    # all data len

    reshaped_data = [reshape_data(entity) for entity in data.data]

    this_file_path = os.path.abspath(__file__)
    this_dir_path = os.path.dirname(this_file_path)
    data_file_path = os.path.join(
        this_dir_path, '..', 'static', 'data', "data.json")

    # Write reshaped data to a json file
    with open(data_file_path, "w", encoding='utf-8') as json_file:
        json.dump(reshaped_data, json_file, ensure_ascii=False, indent=4)

    # cancel all threads
    threads = os.sched_getaffinity(0)
    # close
    os._exit(0)


if __name__ == "__main__":
    main()
