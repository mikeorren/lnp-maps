# Lancaster Deals

A searchable, sortable board of this week's store deals across Lancaster County, with a build-your-own grocery list grouped by store and department. A project of Always Lancaster / LNP | LancasterOnline.

Live at: `/deals/` (served from the lnp-maps Netlify site).

## What's here

```
deals/index.html      The app (single file: search, sort, filter, add-to-list, printable list)
deals/deals.json      The deal data (one lean record per offer) — regenerated weekly
deals/meta.json       Generated timestamp, store + department lists, counts
deals/build_deals.py  Reusable generator that fetches fresh deals and rewrites the two JSON files
```

## Where the data comes from

The LancasterOnline Circulars page is powered by Flipp/Wishabi. `build_deals.py` calls Flipp's
public flyer API (`backflipp.wishabi.com`) for Lancaster ZIP 17603, pulls every flyer's item-level
deals, classifies each into a shopping department, and writes `deals.json` + `meta.json`. No API key
is required; Flipp is credited in the app footer.

## How it refreshes

Flyers update Wednesday mornings. The **Lancaster Deals Weekly Refresh** routine (in Town) runs every
Wednesday ~7:00 AM ET: it runs `build_deals.py` in a sandbox, then commits the updated `deals.json`
and `meta.json` back to this folder, which triggers a Netlify redeploy. To refresh by hand, run
`python build_deals.py` (writes into `deals/`) and commit the two JSON files.

## Notes

- Only offers with a machine-readable price are included; flyer logos/section headers are skipped.
- Data is point-in-time for one ZIP. Prices and dates should always be confirmed in-store.
- The grocery list is saved in the browser (localStorage) — it stays on the reader's own device.
