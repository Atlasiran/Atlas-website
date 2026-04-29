
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

## Adding or Updating an Organization

Each organization is a single `.md` file in `src/content/org-pages/` with YAML frontmatter:

```yaml
---
id: "123"
org_type: "ORG"          # ORG | H_ORG | NGO | PARTY | رسانه | پروژه | گوناگون
name_fa: "نام فارسی"
name_en: "English Name"
name_short: ""
name_local: ""           # Kurdish / Balochi / Arabic etc.
location: ""
contact: ""              # email or other contact info
about: ""
expertise: ""
history: ""
manifest: ""
coc: ""                  # code of conduct / مرام‌نامه
political_orientation: ""
estimation_of_members: ""
social_telegram: ""
social_instagram: ""
social_x: ""
social_facebook: ""
social_youtube: ""
internetAddress: ""
logo: "logos/{id}.png"
updated_at: ""
---
```

After adding or editing files, run `npm run build` to regenerate `static/data/data.json`.

## OG Images (social preview images)

OG images for org pages are pre-generated locally and committed to `static/og/op/`. They are **not** regenerated during CI — Cloudflare's Linux build environment produces distorted Persian text due to FreeType rendering differences vs macOS.

Regenerate after adding or updating org pages:

```bash
npm run gen:og                  # regenerate all org OG images
npm run gen:og -- Hengaw        # regenerate a single org by slug
git add static/og/op/ && git commit -m "chore: regenerate OG images"
```

Requires Python 3 with `Pillow`, `arabic-reshaper`, `python-bidi`, `PyYAML` (the script installs them automatically).

## Project Structure

```
src/
  routes/
    op/[page]/      ← individual org pages
    p/[page]/       ← political-party pages
    parties/        ← party listing
    groups/         ← groups listing
    graph/          ← network graph view
    blog/           ← blog posts
    api/            ← JSON API endpoints
  lib/
    components/     ← shared Svelte components
  content/
    org-pages/      ← one .md file per organization
    posts/          ← blog posts
static/
  data/data.json    ← generated at build time
  logos/            ← org logos ({id}.png)
  og/op/            ← pre-generated OG images
deploy/
  md_to_json.py         ← frontmatter → data.json
  gen_org_og_images.py  ← generates OG images
  update_db.py          ← Supabase sync script
```

## Licence

AGPL 3

