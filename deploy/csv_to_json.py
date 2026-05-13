#!/usr/bin/env python3
"""
Convert the Atlas CSV export to data.json format, preserving IDs where possible.
Only imports rows with Status == 'Done'.

Usage:
    python3 deploy/csv_to_json.py

Reads:  data/Export 2025-05 Atlas of Iranian Civil Society Data Base - Source of Truth.csv
Writes: static/data/data.json
"""

import csv
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(
    SCRIPT_DIR, "..", "data",
    "Export 2025-05 Atlas of Iranian Civil Society Data Base - Source of Truth.csv",
)
DATA_JSON_PATH = os.path.join(SCRIPT_DIR, "..", "static", "data", "data.json")
PARTIES_JSON_PATH = os.path.join(SCRIPT_DIR, "..", "static", "data", "political_parties.json")
POLITICAL_ORG_TYPES = {"حزب", "سازمان سیاسی", "شورا / کنگره / ائتلاف"}
LOGOS_DIR = os.path.join(SCRIPT_DIR, "..", "static", "logos")

# ---------------------------------------------------------------------------
# Column name constants (exact strings from the CSV header)
# ---------------------------------------------------------------------------
COL_STATUS   = "Status"
COL_UPDATED  = "تاریخ به روز رسانی میلادی"
COL_NAME_FA  = "نام فارسی*"
COL_ORG_TYPE = "نوع نهاد*"
COL_NAME_EN  = "نام لاتین*"
COL_NAME_SHORT = "نام کوتاه"
COL_FOUNDED  = "سال تاسیس"
COL_LOCATION = "مکان جغرافیایی / مکان اصلی دفتر مرکزی"
COL_WEBSITE  = "نشانی وبسایت*"
COL_POST     = "آدرس پستی"
COL_CONTACT  = "ایمیل سازمانی یا لینک تماس* "   # trailing space
COL_PHONE    = "تلفن"
COL_MANIFEST = "لینک اساسنامه، مرامنانه، مانیفست، *"
COL_MEMBERS  = "تعداد اعضا"
COL_ORIENT   = "گرایش"
COL_TELEGRAM = "نشانی تلگرام"
COL_FACEBOOK = "نشانی فیسبوک"
COL_TWITTER  = "   نشانی توییتر  (X.com)"          # leading/trailing spaces
COL_YOUTUBE  = "نشانی یوتیوب"
COL_INSTAGRAM= "نشانی اینستاگرام"
COL_BLUESKY  = "نشانی بلواسکای"
COL_LINKEDIN = "نشانی لینکدین"
COL_TIKTOK   = "نشانی تیک تاک"
COL_ABOUT    = "درباره - فقط لینک"
COL_NAME_LOCAL = "نام محلی"

DEFAULT_HEADER_BG = "background-image: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%);"


def c(row, col):
    """Get and clean a value from a CSV row, tolerating missing columns.
    Treats '-', '.', 'n.a', 'n/a', 'unknown' as empty (common placeholders in the CSV).
    """
    v = row.get(col, "") or ""
    v = v.strip().replace("\r", " ").replace("\n", " ")
    if v.lower() in ("-", ".", "n.a", "n/a", "unknown", "unknown "):
        return ""
    return v


def logo_exists(entry_id):
    return os.path.exists(os.path.join(LOGOS_DIR, f"{entry_id}.png"))


def make_title(name_fa, name_en, name_short):
    title = (name_fa or name_en or name_short or "").strip()
    # Replace spaces and any characters that are unsafe in filenames
    title = title.replace(" ", "-").replace("/", "-")
    return title


def load_existing():
    """Load existing data.json; return lookup dicts and next available int ID."""
    try:
        with open(DATA_JSON_PATH, encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}, {}, 1

    by_name_fa = {}
    by_name_en = {}
    max_id = 0

    for entry in data:
        try:
            iid = int(entry.get("id", 0))
            if iid > max_id:
                max_id = iid
        except (ValueError, TypeError):
            pass

        nfa = (entry.get("name_fa") or "").strip()
        nen = (entry.get("name_en") or "").strip()
        if nfa:
            by_name_fa[nfa] = entry
        if nen:
            by_name_en[nen] = entry

    return by_name_fa, by_name_en, max_id + 1


def find_existing(row, by_name_fa, by_name_en):
    name_fa = c(row, COL_NAME_FA)
    name_en = c(row, COL_NAME_EN)
    if name_fa and name_fa in by_name_fa:
        return by_name_fa[name_fa]
    if name_en and name_en in by_name_en:
        return by_name_en[name_en]
    return None


def convert_row(row, existing, next_id):
    name_fa    = c(row, COL_NAME_FA)
    name_en    = c(row, COL_NAME_EN)
    name_short = c(row, COL_NAME_SHORT)
    title      = make_title(name_fa, name_en, name_short)
    page_link  = f"/op/{title}"

    if existing:
        entry_id = existing.get("id", str(next_id))
        logo     = existing.get("logo", "")
        # Preserve fields that come from manual editing, not the CSV
        expertise = existing.get("expertise", "")
        history   = existing.get("history", "")
        coc       = existing.get("coc", "")
        mark_edit = existing.get("markForEdit", "")
        header_bg = existing.get("headerBg", DEFAULT_HEADER_BG)
    else:
        entry_id  = str(next_id)
        logo      = f"logos/{entry_id}.png" if logo_exists(entry_id) else ""
        expertise = ""
        history   = ""
        coc       = ""
        mark_edit = ""
        header_bg = DEFAULT_HEADER_BG

    return {
        "title":                title,
        "id":                   entry_id,
        "org_type":             c(row, COL_ORG_TYPE),
        "pageLink":             page_link,
        "logo":                 logo,
        "name_fa":              name_fa,
        "name_en":              name_en,
        "name_short":           name_short,
        "name_local":           c(row, COL_NAME_LOCAL),
        "location":             c(row, COL_LOCATION),
        "post_location":        c(row, COL_POST),
        "internetAddress":      c(row, COL_WEBSITE),
        "contact":              c(row, COL_CONTACT),
        "phone":                c(row, COL_PHONE),
        "about":                c(row, COL_ABOUT),
        "expertise":            expertise,
        "history":              history,
        "manifest":             c(row, COL_MANIFEST),
        "coc":                  coc,
        "estimation_of_members": c(row, COL_MEMBERS),
        "political_orientation": c(row, COL_ORIENT),
        "markForEdit":          mark_edit,
        "social_telegram":      c(row, COL_TELEGRAM),
        "social_facebook":      c(row, COL_FACEBOOK),
        "social_youtube":       c(row, COL_YOUTUBE),
        "social_x":             c(row, COL_TWITTER),
        "social_instagram":     c(row, COL_INSTAGRAM),
        "social_bluesky":       c(row, COL_BLUESKY),
        "social_linkedin":      c(row, COL_LINKEDIN),
        "social_tiktok":        c(row, COL_TIKTOK),
        "created_at":           c(row, COL_FOUNDED),
        "updated_at":           c(row, COL_UPDATED),
        "mark_for_delete":      "",
        "delete_reason":        "",
        "deleted_at":           "",
        "headerBg":             header_bg,
    }


def main():
    by_name_fa, by_name_en, next_id = load_existing()

    results = []
    matched = 0
    new_count = 0

    with open(CSV_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (row.get(COL_STATUS) or "").strip() != "Done":
                continue

            existing = find_existing(row, by_name_fa, by_name_en)

            if existing:
                matched += 1
                entry = convert_row(row, existing, next_id)
            else:
                entry = convert_row(row, None, next_id)
                next_id += 1
                new_count += 1

            results.append(entry)

    with open(DATA_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    political = [e for e in results if e.get("org_type") in POLITICAL_ORG_TYPES]
    with open(PARTIES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(political, f, ensure_ascii=False, indent=4)

    print(f"Written {len(results)} entries to {DATA_JSON_PATH}")
    print(f"Written {len(political)} political entries to {PARTIES_JSON_PATH}")
    print(f"  Matched existing (ID/logo preserved): {matched}")
    print(f"  New entries (new IDs assigned):        {new_count}")


if __name__ == "__main__":
    main()
