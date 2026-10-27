# GitHub Pages landing page

The static site is in `site/`. It includes real captures of Ghost BASIC's editor,
examples picker, keyword help and startup splash, with tabbed screenshots, BASIC examples,
platform-specific installation and copy controls. It uses no framework, build service,
external fonts, analytics or runtime API. The screenshot gallery is a showcase; BASIC runs
in the installed Python app, not in the browser.

## Preview locally

From the repository root:

```sh
python3 -m http.server 5510 --directory site
```

Visit `http://localhost:5510/`. The site uses relative asset URLs so it also works beneath
the `/GBASIC/` GitHub project path. With JavaScript disabled, all screenshot/instruction
panels remain available; links and installation text work without the controls.

## Publish on GitHub Pages

The configured repository is `https://github.com/tusharv/GBASIC`, branch `main`.
The workflow is `.github/workflows/pages.yml`; it uploads **only `site/`**, excluding
program files, development environments and other repository content.

A repository owner/administrator must enable Pages once:

1. Open [repository Pages settings](https://github.com/tusharv/GBASIC/settings/pages).
2. Under **Build and deployment → Source**, select **GitHub Actions**.
3. Open **Actions → Deploy landing page → Run workflow** on `main` (or rerun the initial
   attempt if it ran before Pages was enabled).
4. Use the successful deployment's URL. The intended project address is
   `https://tusharv.github.io/GBASIC/`; do not describe it as live until deployment succeeds.

Later pushes to `site/` or the Pages workflow deploy automatically. Deployment uses the
`github-pages` environment with `pages: write` and `id-token: write`, following GitHub's
[custom-workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
Enabling Pages is an administration step separate from pushing source; a read-only API
connection cannot enable it. No personal access token is stored in the repository.

## Refresh the real app screenshots

The committed PNGs are browser-independent rasterizations of the running app's native
Textual SVG screen captures, using an installed monospace font. They show genuine source,
execution output, picker and help state, not hand-built product mockups. The SVGs remove
the exporter's optional external font declarations. The splash capture shows one animation
frame; the local app animates for five seconds.

```sh
python -m pip install -e '.[screenshots]'
python tools/capture_screenshots.py
```

CairoSVG needs the OS Cairo library. On macOS with Homebrew Cairo and Menlo:

```sh
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib python tools/capture_screenshots.py --font Menlo
```

Screenshots are shared by the README and site in `site/assets/screenshots/`; refresh them
there rather than duplicating images. The app itself does not depend on CairoSVG or Cairo.

## Verification

```sh
python -m pytest
ruff check src tests tools
ruff format --check src tests tools
mypy
node --check site/main.js
```

Static checks validate local links, anchors, accessible image attributes, screenshot sizes,
Pages configuration and the executable BASIC examples on the page. Browser QA covers desktop
and 390-pixel mobile layouts, image loading, screenshot tabs (including Splash), keyboard
navigation and copying Windows instructions. Reduced-motion CSS disables the small decorative
website ghost's animation. Full program compatibility remains described in COMPATIBILITY.md.
