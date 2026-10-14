# Cloudflare Worker for storyglass.studio

storyglass.studio is served by a Cloudflare Worker (`worker.js`, `wrangler.jsonc`).

- **Primary:** the static copy bundled with the Worker (`dist/`, built by `./scripts/build-cf.sh`).
  HTTP range requests are handled in the Worker (Safari needs 206 for video).
- **Secondary:** Hostinger (`SECONDARY_ORIGIN` in `wrangler.jsonc`), used only for paths the bundle does not have.
  A 429/403/408 or non-JSON 5xx from Hostinger counts as "down".
- Responses carry `x-served-by: cloudflare` or `x-served-by: hostinger`.

Why Cloudflare is primary: Hostinger's CDN answered 429 to requests originating from Workers.

Deploy (needs `wrangler login`):

    ./scripts/build-cf.sh
    npx wrangler@4 deploy

`cloudflare/_headers` mirrors the Caddyfile (security headers, no-cache page, 7-day media cache).
