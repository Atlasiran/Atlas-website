# Atlas Website — Copilot Instructions

## Project Overview

**Atlas** (اطلس جامعه مدنی ایران) is a SvelteKit website that maps Iranian civil-society organizations. It is bilingual (Persian / English) with RTL-first layout. Pages are pre-rendered from Markdown/MDX frontmatter files.

## Tech Stack

| Layer | Tool |
|---|---|
| Framework | SvelteKit 2 (Svelte 4) |
| Styling | Tailwind CSS 3 — utility-first, no custom CSS unless unavoidable |
| Icons | `lucide-svelte` |
| Content | MDsveX — `.md` / `.svx` files in `src/content/org-pages/` |
| Backend | Supabase (`@supabase/supabase-js`) |
| Deployment | Cloudflare (default) or static adapter (`ADAPTER=static`) |
| Build | `npm run dev` (dev server) · `npm run build` (runs `md_to_json.py` then Vite) |
| Package manager | npm (lockfile: `bun.lockb` — but use `npm` for commands) |

## Directory Structure

```
src/
  routes/
    op/[page]/      ← individual org pages (ALL orgs — civil and political)
    p/[page]/       ← static content pages (about, roadmap, etc.)
    parties/        ← political orgs listing (reads political_parties.json)
    groups/         ← civil society listing, menu label "نهادها" (reads data.json)
    graph/          ← network graph view
    blog/           ← blog posts
    api/            ← JSON API endpoints
  lib/
    components/     ← shared Svelte components
    components/layout/ ← Header, Footer, OrgPageLayout
    icons/
    stores/
  content/
    org-pages/      ← one .md file per organization (frontmatter = all data)
    pages/          ← static content pages
    posts/          ← blog posts
static/
  data/data.json              ← ALL orgs (226 entries); source for org-pages generation
  data/political_parties.json ← filtered subset: political org types only (for /parties/)
  logos/            ← org logos (filename = {id}.png)
  og/op/            ← pre-generated OG images per org
deploy/
  csv_to_json.py    ← converts CSV → data.json AND political_parties.json
  update_org_pages.py ← syncs data.json → src/content/org-pages/*.md
  md_to_json.py     ← run at build time: re-reads org-pages frontmatter → data.json
  gen_org_og_images.py ← generates OG images
  update_db.py      ← Supabase sync script
data/
  *.csv             ← source-of-truth CSV exported from the Atlas database
```

## Org-Page Data Model

Each `src/content/org-pages/*.md` file has YAML frontmatter with these fields:

```yaml
id, org_type, pageLink, logo
name_fa, name_en, name_short, name_local   # name_local = Kurdish/Balochi/Arabic etc.
location, post_location
contact, phone                             # contact = email or other contact info
about, expertise, history
manifest, coc                              # coc = code of conduct / مرام‌نامه
estimation_of_members, political_orientation
social_telegram, social_facebook, social_youtube, social_x, social_instagram
social_bluesky, social_linkedin, social_tiktok
internetAddress
created_at, updated_at
markForEdit, mark_for_delete, delete_reason, deleted_at
headerBg
```

## Data Pipeline

The source of truth is a CSV file in `data/`. When new data arrives:

1. **`python3 deploy/csv_to_json.py`** — reads the CSV, matches rows to existing entries by `name_fa`/`name_en` to preserve IDs and logos, and writes two files:
   - `static/data/data.json` — ALL orgs (civil + political), used by `update_org_pages.py`
   - `static/data/political_parties.json` — filtered subset of political orgs only (used by `/parties/` listing page)

2. **`python3 deploy/update_org_pages.py`** — reads `data.json`, creates/updates/renames `.md` files in `src/content/org-pages/`. Also rewrites `data.json` with updated `pageLink` values.

3. **Build** (`npm run build`) — runs `md_to_json.py` which re-reads all frontmatter back into `data.json` for prerendering.

### Org-type split: نهادها vs احزاب

The following `org_type` values are **political** and appear in `political_parties.json` (shown at `/parties/`):
- `حزب`
- `سازمان سیاسی`
- `شورا / کنگره / ائتلاف`

All other types are **civil society** and shown at `/groups/` (menu label: **نهادها**). The groups page filters out political types client-side. All individual org pages — regardless of type — live at `/op/[page]/`.

This constant is defined in `deploy/csv_to_json.py` as `POLITICAL_ORG_TYPES` and duplicated inline in `src/routes/groups/+page.svelte`. Keep them in sync when adding new types.

### Adding a new org_type to the political section
1. Add the value to `POLITICAL_ORG_TYPES` in `deploy/csv_to_json.py`
2. Add the same value to the `POLITICAL_TYPES` Set in `src/routes/groups/+page.svelte`
3. Re-run `python3 deploy/csv_to_json.py` to regenerate both JSON files

## Coding Conventions

- **Tailwind only** — no scoped `<style>` blocks unless unavoidable. Use arbitrary values like `text-[#1E3A6B]` and `bg-[rgba(30,58,107,0.07)]` to stay on-brand.
- **Brand colors**: primary blue `#1E3A6B`, accent cream `#EDE3C7`, muted `rgba(30,58,107,0.72)`.
- **RTL-aware**: the site is `dir="auto"` or `dir="rtl"`. Use `flex-row-reverse` for RTL sidebars. Wrap Latin text in `<bdi>`.
- **`defined(v)` helper** already exists in `op/[page]/+page.svelte` — use it to guard against `""`, `"None"`, and whitespace-only values.
- **Social URLs**: use the existing `socialUrl()` helper in the org page to normalise handles → full URLs.
- **No TypeScript** — the project uses plain JS with JSDoc (jsconfig.json).
- **Prerendering**: all org/party/blog routes are `prerender = true`. Keep `load` functions pure and side-effect-free.
- **Imports**: use the `@/` alias for `src/lib/` (configured in `jsconfig.json` / `vite.config.js`).

## Org Page Layout (src/routes/op/[page]/+page.svelte)

Current section order (top → bottom):
1. Header (logo + org name)
2. Info grid (2-col): نوع نهاد, نام فارسی, نام لاتین, نام کوتاه, نام محلی, مکان, نشانی پستی, تعداد تخمینی اعضا, گرایش سیاسی *(با یادداشت «این برداشت ماست»)*, ایمیل یا راه تماس, تلفن, بروزرسانی
3. Main content + پیوندها sidebar (flex-row-reverse → sidebar on left):
   - Main: تخصص‌ها → مرامنامه یا مانیفست → درباره → تاریخچه → Markdown body → درخواست ویرایش button
   - Sidebar: sticky card showing active social links only

## Report/Edit Flow

The "درخواست ویرایش اطلاعات" button uses a `mailto:` link:
- **To**: `hi@AtlasIran.org`
- **Subject**: `درخواست ویرایش نهاد {orgName}`
- **Body**: includes the page URL automatically

## Common Tasks

**Import new CSV data**:
1. Place the new CSV in `data/`.
2. `python3 deploy/csv_to_json.py` → regenerates `data.json` + `political_parties.json`.
3. `python3 deploy/update_org_pages.py` → syncs `src/content/org-pages/*.md`.
4. Verify: `python3 -c "import json,os; d=json.load(open('static/data/data.json')); md=set(os.listdir('src/content/org-pages')); print(len(d), len(md), [e['title'] for e in d if e['title']+'.md' not in md])"`

**Add a new field to org pages**:
1. Add the frontmatter key to `src/content/org-pages/*.md` files (via `update_org_pages.py` or manually).
2. Display it in the info grid or a new section in `op/[page]/+page.svelte`.

**Add a new social platform**:
1. Add `social_<platform>: ""` to the frontmatter schema.
2. Add a `socialUrl(m.social_<platform>, 'https://platform.com/')` entry to the `links` object.
3. Add an `{#if links.<platform>}` block in the sidebar.

**Run dev server**: `npm run dev` → http://localhost:5173/
**Build**: `npm run build` (also regenerates `data.json`)
**Preview build**: `npm run preview`
