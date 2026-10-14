# Storyglass Studio website: static files served by Caddy (gzip/zstd, byte ranges for video, cache headers)
FROM caddy:2.8.4-alpine
COPY Caddyfile /etc/caddy/Caddyfile
COPY public /srv
