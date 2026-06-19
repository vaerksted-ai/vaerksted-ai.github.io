# Værksted — static site

The full deployable static site for [vaerksted.ai](https://vaerksted.ai).
Single-page landing, no build step, no JavaScript framework.
Drop the folder on any static host and you're live.

## Files

| File | Purpose |
|---|---|
| `index.html` | Landing page. Full content. |
| `404.html` | Error page (same aesthetic). |
| `favicon.svg` | Modern browser favicon (the Æ in the Bifröst rainbow gradient). |
| `favicon.ico` | Legacy fallback (16, 32, 48, 64 px embedded). |
| `apple-touch-icon.png` | iOS home-screen icon (180×180). |
| `icon-192.png` / `icon-512.png` | PWA / Android home-screen. |
| `og-image.png` | Social preview (1200×630) — shown on X, LinkedIn, iMessage, Slack, etc. |
| `og-image.svg` | Editable source for the OG image. |
| `manifest.webmanifest` | PWA manifest (theme color, icons). |
| `robots.txt` | Allow all crawlers, point at sitemap. |
| `sitemap.xml` | One-URL sitemap. Update when you add pages. |
| `CNAME` | Custom-domain mapping for GitHub Pages only. Delete elsewhere. |

All assets are referenced by absolute paths (`/favicon.svg` etc.), so the site must be served from the **root** of the domain, not a subpath.

## Deployment

### Cloudflare Pages (recommended for `.ai` domains)

1. Push this folder to a new GitHub repo.
2. Cloudflare Dashboard → Workers & Pages → Create → connect the repo.
3. Build command: leave empty. Build output: `/`.
4. Custom domains tab → add `vaerksted.ai` and `www.vaerksted.ai`.
5. Cloudflare auto-provisions SSL. Done.

### Netlify

1. Drag-and-drop the folder onto [app.netlify.com/drop](https://app.netlify.com/drop).
2. Domain settings → add custom domain → follow DNS instructions.

### Vercel

1. `npm i -g vercel && vercel` from inside the folder.
2. Add custom domain in the Vercel dashboard.

### GitHub Pages

1. Push to a repo named `vaerksted.github.io` (or any repo with Pages enabled).
2. Settings → Pages → source: `main` branch, `/` (root).
3. Keep the `CNAME` file. It tells Pages to serve at `vaerksted.ai`.
4. Add an `A` record at your DNS pointing at GitHub's IPs.

### Plain S3 / Cloudfront

1. Upload all files to an S3 bucket configured for static website hosting.
2. Point a CloudFront distribution at the bucket. Set custom error response: 404 → `/404.html`.

## DNS

Two domains, both should land in the same place:

- `vaerksted.ai` → primary
- `vaerksted.org` → 301 redirect to `vaerksted.ai`

Most hosts (Cloudflare, Netlify, Vercel) handle the redirect with a single rule in their dashboard.

## Editing

Everything is one HTML file plus assets. To change copy or principles, edit `index.html` directly — the styles are inline, the content is inline, no build step needed.

To regenerate the OG image after editing the wordmark or tagline:
- Edit `og-image.svg` for source-of-truth changes, or
- Edit and re-run the Python script (see `render_og.py` if included).

The Æ in the wordmark is a styled `<span class="ae">æ</span>` painted with the `--bifrost` gradient. Each app carries its own hue from the Bifröst (the rainbow bridge Heimdal guards): the per-app colours live in the `--c-*` CSS variables, applied per card via an inline `--accent`. Maskin is blue, the house colour (`--signal`).

## Performance

- Single HTML file, ~22KB
- Two webfonts loaded from Google Fonts (Space Grotesk, JetBrains Mono)
- No JavaScript, no analytics by default
- Lighthouse should score ≥98 across the board out of the box

If you want to self-host the fonts (faster + GDPR-friendlier), grab the woff2 files from [Google Fonts](https://fonts.google.com/specimen/Space+Grotesk) and [JetBrains](https://www.jetbrains.com/lp/mono/), drop them in a `/fonts` folder, and replace the `<link>` to fonts.googleapis.com with a local `@font-face` block.
