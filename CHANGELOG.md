# Changelog

## v0.1.0 — 2026-11-03
- Initial release: YouTube Shorts title fitter (100-char cap, exact title wording preserved).
- Hashtags that fit stay in the title; overflow hashtags move to the description.
- Full description builder: hook line + hashtags + credits placeholder.
- Over-long titles (>100 chars before hashtags) get a word-boundary truncation warning — never a silent mid-word cut.
