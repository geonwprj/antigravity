# Example: Clarification Message

This is a real example of an efficient clarification message from the Scrape Tools project. Instead of asking questions one-by-one across 5+ round-trips, all independent questions were batched into a single message.

---

## The Message

> Before I draft the implementation plan, I have a few clarifying questions:
>
> 1. **Port mapping** — What host port would you like for this service? (Must be >20000 per homelab rules, e.g. `28010:8000`)
> 2. **WebUI framework** — Would you prefer:
>    - **(a) Next.js** (separate frontend, richer interactivity for the dashboard/profile editor) — aligns with your existing stack
>    - **(b) Jinja2 templates served by FastAPI** (single-service, simpler deployment)
>    - **(c) Static SPA (vanilla HTML/JS)** served by FastAPI (lightweight, no Node dependency)
> 3. **Profile storage** — For the scraping profiles (the JSON you showed), would you prefer:
>    - **(a) SQLite** (consistent with other projects, queryable)
>    - **(b) JSON files on disk** in `./data/profiles/` (simpler, human-editable directly)
> 4. **Scraping engine** — Any preference between:
>    - **(a) BeautifulSoup + httpx** (lightweight, async HTTP + DOM parsing)
>    - **(b) Playwright/Selenium** (if target sites require JavaScript rendering)
> 5. **Preview feature** — For the profile page's "preview section for setting the rules," should this be:
>    - **(a) Live scrape** — Actually fetch the page and show results against the current selectors in real-time
>    - **(b) Cached preview** — User provides sample HTML, selectors are tested against it locally

## Why This Works

- **5 questions in 1 message** = 1 round-trip instead of 5+
- **Multiple-choice** = user can answer in a few words (e.g. "next, sqlite, bs4, live")
- **Every option has context** = user makes informed decisions, not guesses
- **Independent questions only** = no question depends on another's answer
- **Research-backed** = checked existing codebase patterns before proposing options
