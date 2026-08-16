# GitHub Pages Rubric

Use this rubric when building or publishing a static website on GitHub Pages.

## Official Sources

Prefer current GitHub documentation when checking behavior:

- Creating a GitHub Pages site: https://docs.github.com/articles/creating-project-pages-manually
- Configuring a publishing source: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- GitHub Pages limits: https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits

## Hosting Fit

| Check | PASS | REVISE | BLOCK |
| --- | --- | --- | --- |
| Static architecture | HTML/CSS/JS/static assets only | Static build exists but needs cleanup | Requires backend runtime, database, server auth, or secrets |
| Public suitability | Public content and public repo are acceptable | Content needs redaction before publishing | Contains private, regulated, or secret data |
| Size and build limits | Small static site with compressed assets | Heavy media should be optimized | Published site is likely over GitHub Pages limits |
| Maintenance | Simple stack and documented commands | Stack works but is more complex than needed | Site cannot be rebuilt or deployed from repo state |

## Deployment Modes

### Branch deploy

Use when the site source is already the final static output.

Required state:

- `index.html` at repository root or `/docs`.
- GitHub Pages source configured to `main` and the selected folder.
- Empty `.nojekyll` at the publishing root when Jekyll processing may break static assets.

Good for:

- Plain HTML/CSS/JS sites.
- Small portfolios, landing pages, resource hubs, documentation written directly as static files.

### GitHub Actions deploy

Use when the site must be built before publishing.

Required state:

- Workflow uses official Pages actions where possible:
  - `actions/configure-pages`
  - `actions/upload-pages-artifact`
  - `actions/deploy-pages`
- Workflow has `pages: write` and `id-token: write` permissions.
- Artifact contains `index.html` at the artifact root.
- Pages source is set to GitHub Actions.

Good for:

- Vite, Astro, Next static export, Hugo, Eleventy, MkDocs, or other generated static output.

## Site Quality Checks

Run these before publishing:

- Local build succeeds.
- Local static server returns `200` for key routes.
- Home page has title, H1, meta description, canonical when public, Open Graph title/description/image if relevant.
- Responsive layout works on mobile and desktop.
- All internal links resolve.
- Images load and have meaningful alt text when informative.
- Forms either use static-compatible services or are clearly mailto/link-based.
- No secrets are present in committed files.
- Project-page asset paths work under `/<repo>/`.

## Live Verification

After publishing, verify:

- GitHub Actions or Pages deployment completed successfully.
- Live URL returns HTTP `200`.
- The expected H1 or unique visible text is present.
- CSS and primary images are not 404.
- Navigation links work from the deployed URL.

## Known Limits

GitHub Pages is suitable for free static publishing, not general application hosting. Official limits can change, so check the current GitHub Pages limits page when the site is large or high traffic. As of the referenced documentation, published sites may be no larger than 1 GB, deployments time out after 10 minutes, and GitHub Pages has soft limits for bandwidth and branch-triggered builds.
