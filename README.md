# lnp-maps

Interactive roundup maps for **LNP | LancasterOnline**, built from published articles and served as static pages on Netlify.

## What's here

```
index.html                        Landing page listing published maps + the request form
request/index.html                Reporter-facing "request a map" form (Netlify Forms)
maps/<slug>/index.html            One published interactive map per roundup
_template/map-template.html       Reusable data-injectable map template (not a public page)
```

## How a map gets made

1. A reporter opens `/request/` and pastes a link to their published roundup.
2. Netlify Forms captures the submission and emails it in.
3. The **Article-to-Map Builder** routine (in Town) reads the submission, fetches the article, extracts each location (name, dates, address, photo, must-see events), geocodes it, fills `_template/map-template.html`, and commits the result to `maps/<slug>/index.html`.
4. Netlify auto-deploys the new page.
5. The routine drafts a reply to the reporter with the live link and embed code (the reporter's editor reviews and sends).

## The template data model

`_template/map-template.html` renders from a single `POINTS` array. Each item:

- `n`, `name`, `lat`, `lng` (required)
- `start`, `end` (`YYYY-MM-DD`, optional — include only for date-bound events; drives the "open today / upcoming / ended" logic)
- `img`, `cap`, `cred` (optional photo + caption + credit)
- `loc` (optional address), `blurb` (optional description)
- `rows: [{label, html}]` (optional extra detail rows — Hours, Cost, Menu, etc.)
- `isnew` (optional "what's new" callout)
- `events: [{d:"YYYY-MM-DD", t}]` (optional dated highlights; a match on the current date lights up)
- `url`, `info`, `phone` (optional links)

Preview any date with `?today=YYYY-MM-DD`.

## Adding a map by hand

Copy `_template/map-template.html` to `maps/<slug>/index.html`, replace the `__DATA__`, `__PAGE_TITLE__`, `__HEADER_TITLE__`, `__HEADER_INTRO__`, `__FOOTER_HTML__`, and `__OG_*__` placeholders, and commit.
