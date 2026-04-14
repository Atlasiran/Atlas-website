
## Run 
1. clone the project
2. `npm install` 
3. `npm run dev`

## Build
1. `npm run build`

## OG Images (social preview images)

OG images for org/party pages are pre-generated locally and committed to `static/og/op/`. They are **not** regenerated during CI — this is intentional, because Cloudflare's Linux build environment produces distorted Persian text due to FreeType rendering differences vs macOS.

**When to regenerate:** whenever you add or update org pages in `src/content/org-pages/`.

**How to regenerate:**
```bash
npm run gen:og              # regenerate all org OG images
npm run gen:og -- Hengaw    # regenerate a single org by slug
```

Then commit the updated images together with your content changes:
```bash
git add static/og/op/ && git commit -m "chore: regenerate OG images"
```

**Requirements:** Python 3 with `Pillow`, `arabic-reshaper`, `python-bidi`, `PyYAML` (the `gen:og` script installs them automatically).

## Licence 
AGPL 3

