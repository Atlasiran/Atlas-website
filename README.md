
# اطلس جامعه مدنی ایران — Atlas of Iranian Civil Society

A bilingual (Persian / English) SvelteKit website that maps Iranian civil-society organizations. RTL-first layout, pre-rendered from Markdown frontmatter files.

**Live site:** [atlasiran.org](https://atlasiran.org)

---

## Tech Stack

| Layer | Tool |
|---|---|
| Framework | SvelteKit 2 (Svelte 4) |
| Styling | Tailwind CSS 3 |
| Content | MDsveX (`.md` files in `src/content/org-pages/`) |
| Backend | Supabase |
| Deployment | Cloudflare Pages |

## Getting Started

```bash
git clone https://github.com/Atlasiran/Atlas-website.git
cd Atlas-website
npm install
npm run dev          # → http://localhost:5173
```

## Build

```bash
npm run build        # runs md_to_json.py then Vite build
npm run preview      # preview the production build locally
```

## Data Pipeline

The source of truth is a CSV file in `data/`. When new data arrives:

1. **`python3 deploy/csv_to_json.py`** — reads the CSV and writes:
   - `static/data/data.json` — all 226+ orgs (civil + political)
   - `static/data/political_parties.json` — political orgs only (used by `/parties/`)

2. **`python3 deploy/update_org_pages.py`** — syncs `data.json` → `src/content/org-pages/*.md`

3. **`npm run build`** — runs `deploy/md_to_json.py` (frontmatter → `data.json`) then Vite

### Org-type split: نهادها vs احزاب

The following `org_type` values are political and appear at `/parties/`:
- `حزب`
- `سازمان سیاسی`
- `شورا / کنگره / ائتلاف`

All other types are civil society and appear at `/groups/`.

## Adding or Updating an Organization

Each organization is a single `.md` file in `src/content/org-pages/` with YAML frontmatter:

```yaml
---
id: "123"
org_type: "سازمان غیرانتفاعی"   # e.g. حزب | سازمان سیاسی | سازمان غیرانتفاعی | رسانه | پروژه | ...
pageLink: "/op/slug"
logo: "logos/{id}.png"
name_fa: "نام فارسی"
name_en: "English Name"
name_short: ""
name_local: ""           # Kurdish / Balochi / Arabic etc.
location: ""
post_location: ""
contact: ""              # email or other contact info
phone: ""
about: ""
expertise: ""
history: ""
manifest: ""
coc: ""                  # code of conduct / مرام‌نامه
estimation_of_members: ""
political_orientation: ""
social_telegram: ""
social_instagram: ""
social_x: ""
social_facebook: ""
social_youtube: ""
social_bluesky: ""
social_linkedin: ""
social_tiktok: ""
internetAddress: ""
headerBg: ""
created_at: ""
updated_at: ""
---
```

After editing files manually, run `npm run build` to regenerate `static/data/data.json`.

## OG Images (social preview images)

OG images for org pages are pre-generated locally and committed to `static/og/op/`. They are **not** regenerated during CI — Cloudflare's Linux build environment produces distorted Persian text due to FreeType rendering differences vs macOS.

Regenerate after adding or updating org pages:

```bash
npm run gen:og
git add static/og/op/ && git commit -m "chore: regenerate OG images"
```

Requires Python 3 with `Pillow`, `arabic-reshaper`, `python-bidi`, `PyYAML` (the script installs them automatically via `pip3`).

## Network Graph

The graph at `/graph` reads `static/test.gexf`. Regenerate it after data changes:

```bash
python3 deploy/gen_gexf.py
```

## Project Structure

```
data/
  *.csv                       ← source-of-truth CSV from the Atlas database
src/
  routes/
    op/[page]/                ← individual org pages (civil + political)
    p/[page]/                 ← static content pages (about, contact, etc.)
    parties/                  ← political orgs listing
    groups/                   ← civil society listing (نهادها)
    graph/                    ← network graph view
    blog/                     ← blog posts
    api/                      ← JSON API endpoints
  lib/
    components/               ← shared Svelte components
  content/
    org-pages/                ← one .md file per organization
    pages/                    ← static content pages
    posts/                    ← blog posts
static/
  data/data.json              ← all orgs; regenerated at build time
  data/political_parties.json ← political orgs only; used by /parties/
  logos/                      ← org logos ({id}.png)
  og/op/                      ← pre-generated OG images
deploy/
  csv_to_json.py      ← CSV → data.json + political_parties.json
  update_org_pages.py ← data.json → src/content/org-pages/*.md
  md_to_json.py       ← frontmatter → data.json (run at build time)
  gen_gexf.py         ← data.json → static/test.gexf (network graph)
  gen_org_og_images.py← generates OG images
  update_db.py        ← Supabase sync script
```

## Licence

AGPL 3

