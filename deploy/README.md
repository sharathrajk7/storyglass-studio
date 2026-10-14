# Storyglass Studio, production deploy (Railway)

1. `python3 build.py --base-url https://<your-domain>` builds `public/` from `../hero-prototype`.
2. `npx @railway/cli up` deploys this folder (Dockerfile: Caddy serving `public/`).

Caddy listens on Railway's `$PORT`, compresses text, serves video byte ranges (Safari needs them), sends
security headers, no-cache for the page and films.json, and a week of caching for media.
