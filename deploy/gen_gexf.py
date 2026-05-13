#!/usr/bin/env python3
"""
Generate static/test.gexf from static/data/data.json.

Org nodes are labelled "Organization" or "Political Party" depending on org_type.
Country nodes (one per unique normalised location) are labelled "Country".
Each org gets a "BASED IN" edge pointing to its country node.
Run from the repo root:
    python3 deploy/gen_gexf.py
"""

import json
import math
import random
import uuid
import xml.sax.saxutils as saxutils
from pathlib import Path

# ── Configuration ────────────────────────────────────────────────────────────

DATA_JSON = Path("static/data/data.json")
OUT_GEXF = Path("static/test.gexf")

POLITICAL_ORG_TYPES = {"حزب", "سازمان سیاسی", "شورا / کنگره / ائتلاف"}

# Map raw/variant location strings → canonical country label
LOCATION_NORMALISE = {
    # typos / alternate spellings
    "امریکا": "آمریکا",
    "انگستان": "انگلستان",
    "بریتانیا": "انگلستان",
    # cities that imply a country
    "برلین": "آلمان",
    "فرانکفورت آلمان": "آلمان",
    "کلن آلمان": "آلمان",
    "تبریز": "ایران",
    "وین": "اتریش",
    "مللمو، سوئد": "سوئد",
    "زندان\u200cهای ایران": "ایران",
}

# ── Helpers ──────────────────────────────────────────────────────────────────

def esc(value: str) -> str:
    """Escape a string for use as an XML attribute value."""
    if not value:
        return ""
    return saxutils.escape(str(value), {'"': "&quot;"})


def normalise_location(raw: str) -> str:
    """Return a canonical country/region label from a raw location string."""
    if not raw:
        return "نامشخص"

    # Strip invisible / directional Unicode characters
    raw = raw.strip().strip("\u202a\u202b\u200c\u200d\u200f\u200e").strip()

    # Check explicit override map first
    if raw in LOCATION_NORMALISE:
        return LOCATION_NORMALISE[raw]

    # Take the primary part before ، (Arabic comma), , or /
    for sep in ["،", ",", "/"]:
        if sep in raw:
            primary = raw.split(sep)[0].strip().strip("\u202a\u202b\u200c\u200d").strip()
            if primary in LOCATION_NORMALISE:
                return LOCATION_NORMALISE[primary]
            return primary

    return raw


def stable_id(namespace_str: str, name: str) -> str:
    """Generate a stable UUID5 from a namespace string + name."""
    ns = uuid.UUID(bytes=bytes.fromhex(
        hashlib.md5(namespace_str.encode()).hexdigest()
    ))
    return str(uuid.uuid5(ns, name))


def circular_position(index: int, total: int, radius: float = 300.0):
    angle = 2 * math.pi * index / max(total, 1)
    return radius * math.cos(angle), radius * math.sin(angle)


# ── Main ─────────────────────────────────────────────────────────────────────

import hashlib  # noqa: E402 (placed after helpers for readability)


def main():
    data = json.loads(DATA_JSON.read_text(encoding="utf-8"))

    # ── 1. Collect unique locations ──────────────────────────────────────────
    country_labels: set[str] = set()
    for org in data:
        loc = normalise_location(org.get("location", ""))
        country_labels.add(loc)

    # Assign stable IDs to countries
    country_ids: dict[str, str] = {
        label: stable_id("atlas-country", label)
        for label in country_labels
    }

    # Assign stable IDs to orgs (use their numeric id field)
    org_ids: dict[int, str] = {
        org["id"]: stable_id("atlas-org", str(org["id"]))
        for org in data
    }

    # ── 2. Build XML ─────────────────────────────────────────────────────────
    lines = []

    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf version="1.2" xmlns="http://www.gexf.net/1.2draft" xmlns:viz="http:///www.gexf.net/1.1draft/viz">')
    lines.append("  <meta/>")
    lines.append('  <graph defaultedgetype="directed">')

    # Node attribute schema
    lines.append('    <attributes class="node">')
    for attr_id, title in [
        ("name",                        "name"),
        ("@id",                         "@id"),
        ("@typeId",                     "@typeId"),
        ("@labels",                     "@labels"),
        ("English Name",                "English Name"),
        ("Full name",                   "Full name"),
        ("Contact",                     "Contact"),
        ("Location(s)",                 "Location(s)"),
        ("About",                       "About"),
        ("activities",                  "activities"),
        ("assets &amp; specialties",    "assets &amp; specialties"),
        ("History",                     "History"),
        ("مرامنامه و باورها و منشور",   "مرامنامه و باورها و منشور"),
        ("estimation of Nb of members", "estimation of Nb of members"),
        ("reference",                   "reference"),
        ("image",                       "image"),
        ("pageLink",                    "pageLink"),
    ]:
        lines.append(f'      <attribute id="{attr_id}" title="{title}" type="string"/>')
    lines.append("    </attributes>")

    # Edge attribute schema
    lines.append('    <attributes class="edge">')
    for attr_id, title in [("@id", "@id"), ("@typeId", "@typeId"), ("@type", "@type")]:
        lines.append(f'      <attribute id="{attr_id}" title="{title}" type="string"/>')
    lines.append("    </attributes>")

    # ── Nodes ────────────────────────────────────────────────────────────────
    lines.append("    <nodes>")

    # Country nodes – arranged in a circle
    country_list = sorted(country_labels)
    for i, label in enumerate(country_list):
        node_id = country_ids[label]
        x, y = circular_position(i, len(country_list), radius=500)
        lines.append(f'      <node id="{node_id}" label="{esc(label)}">')
        lines.append("        <attvalues>")
        lines.append(f'          <attvalue for="name" value="{esc(label)}"/>')
        lines.append(f'          <attvalue for="@id" value="{node_id}"/>')
        lines.append(f'          <attvalue for="@typeId" value="country-type"/>')
        lines.append(f'          <attvalue for="@labels" value="Country"/>')
        lines.append("        </attvalues>")
        lines.append(f'        <viz:color r="217" g="50" b="246"/>')
        lines.append(f'        <viz:size value="1"/>')
        lines.append(f'        <viz:position x="{x:.4f}" y="{y:.4f}"/>')
        lines.append("      </node>")

    # Org nodes – random positions near centre
    random.seed(42)
    for org in data:
        org_id = org_ids[org["id"]]
        gexf_label = org.get("name_fa") or org.get("name_en") or f"org-{org['id']}"
        is_political = org.get("org_type", "") in POLITICAL_ORG_TYPES
        node_label = "Political Party" if is_political else "Organization"

        x = random.uniform(-200, 200)
        y = random.uniform(-200, 200)

        # Build attvalues
        av = {
            "name":                        gexf_label,
            "@id":                         org_id,
            "@typeId":                     "org-type",
            "@labels":                     node_label,
            "English Name":                org.get("name_en", ""),
            "Full name":                   org.get("name_fa", ""),
            "Contact":                     org.get("contact", ""),
            "Location(s)":                 org.get("location", ""),
            "About":                       org.get("about", ""),
            "activities":                  org.get("expertise", ""),
            "History":                     org.get("history", ""),
            "مرامنامه و باورها و منشور":   org.get("manifest", "") or org.get("coc", ""),
            "estimation of Nb of members": str(org.get("estimation_of_members", "")),
            "reference":                   org.get("internetAddress", ""),
            "pageLink":                    org.get("pageLink", ""),
        }
        # logo image URL
        if org.get("logo"):
            av["image"] = f"/{org['logo']}"
        elif org.get("id"):
            av["image"] = f"/logos/{org['id']}.png"

        lines.append(f'      <node id="{org_id}" label="{esc(gexf_label)}">')
        lines.append("        <attvalues>")
        for k, v in av.items():
            if v:
                lines.append(f'          <attvalue for="{k}" value="{esc(str(v))}"/>')
        lines.append("        </attvalues>")
        lines.append(f'        <viz:color r="240" g="41" b="219"/>')
        lines.append(f'        <viz:size value="1"/>')
        lines.append(f'        <viz:position x="{x:.4f}" y="{y:.4f}"/>')
        lines.append("      </node>")

    lines.append("    </nodes>")

    # ── Edges ────────────────────────────────────────────────────────────────
    lines.append("    <edges>")
    edge_type_id = stable_id("atlas-edge-type", "BASED IN")

    for org in data:
        org_id = org_ids[org["id"]]
        country_label = normalise_location(org.get("location", ""))
        country_id = country_ids[country_label]
        edge_id = stable_id("atlas-edge", f"{org_id}->{country_id}")

        lines.append(f'      <edge id="{edge_id}" source="{org_id}" target="{country_id}" weight="1" label="BASED IN (1)">')
        lines.append("        <attvalues>")
        lines.append(f'          <attvalue for="@id" value="{edge_id}"/>')
        lines.append(f'          <attvalue for="@typeId" value="{edge_type_id}"/>')
        lines.append(f'          <attvalue for="@type" value="BASED IN"/>')
        lines.append("        </attvalues>")
        lines.append("      </edge>")

    lines.append("    </edges>")
    lines.append("  </graph>")
    lines.append("</gexf>")

    OUT_GEXF.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Written {OUT_GEXF}  ({len(data)} orgs, {len(country_labels)} countries)")


if __name__ == "__main__":
    main()
