# GitHub Pages landing page and real UI screenshots

User request: add README screenshots and a GitHub Pages landing page. Work directly in
this repository; GitHub Pages is the explicit host, so no separate Sites-hosted project.

Design: a readable, light-paper project site anchored by the real navy BASIC editor.
Palette: paper #f6f4ed, ink #17171f, BASIC blue #1010a8, night #080836,
cyan #6be5ef, yellow #ffe27a. Headings: bold system sans; body: system sans;
code, shortcuts and labels: terminal monospace. Avoid external font/CDN dependencies.
Signature: the actual blue terminal and small ASCII ghost, with editorial line-number
markers used only for the real Write/Run/Learn progression.

Page structure: project navigation; concise hero and screenshot tabs; concrete features;
example programs and their expected output; cross-platform installation with copy controls;
compatibility boundaries; documentation/GitHub links and MIT footer. Responsive to 360px,
keyboard navigation, visible focus, useful without JavaScript, reduced-motion support.

- [x] Capture editor, examples and keyword-help screens from the running app; verify images.
- [x] Embed screenshots in README and add proper public installation instructions.
- [x] Build a dependency-free static site in site/ with relative links for /GBASIC/ hosting.
- [x] Add the official GitHub Actions Pages deployment workflow, restricted to site artifacts.
- [x] Check links/assets, JS interactions, mobile/desktop layout and accessibility basics.
- [x] Verify the whole project, inspect GitHub permissions, and publish if authorized access
      permits; otherwise deliver reviewable files and state the exact external blocker.

No claims of full legacy compatibility, unimplemented graphics, a browser interpreter,
PyPI publication, or native installers. The site must present the current 0.3 feature set.
