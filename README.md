# Storyglass Studio site

Source for storyglass.studio.

- `hero-prototype/`: the page source and media tooling
- `deploy/`: production build (`build.py` produces `deploy/public/`)
- `mockups/`, `docs/`: design mockups and the site spec

## Hosting

The `hostinger` branch holds only the built site (the contents of `deploy/public/` plus an
`.htaccess`) and is what Hostinger deploys on every push. Refresh it with `deploy/publish-hostinger.sh`.
