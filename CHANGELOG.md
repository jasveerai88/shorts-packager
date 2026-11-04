# Changelog

## v0.2.0 — 2026-11-03
Agent-ready release (no behaviour change to the existing human output):
- `--json` flag: prints one JSON object to stdout capturing the same verdict, numbers and warnings as the human report (tool, version, verdict, final title, grapheme title_length vs the 100 limit, truncated / mid_word_cut flags, hashtags in title / overflow / rejected, hook, description, per-check entries). Exit codes are unchanged in both modes.
- Error paths in `--json` mode emit `{"error": "<message>"}` as JSON on stdout with the same exit code (2) — never plain text, never a traceback. This covers the empty-title error and argparse usage errors.
- `SKILL.md` added at repo root: an agent-facing brief (purpose, exact commands incl. `--json`, the full JSON schema, exit codes, honesty rules).
- README gained a "Use with AI agents" section pointing at `--json` + `SKILL.md`.
- 5 tests added (22 total, all passing): JSON parses with verdict + key fields, JSON verdict agrees with `pack()`/human mode on the overflow sample, JSON error object + exit 2 for an empty title and for a usage error, and a byte-identical guard on the human output.

## v0.1.2 — 2026-11-03
Mini-fix from the delta re-audit:
- SP-1b: a title consisting ONLY of hashtag tokens (`--title "#cats #dogs"`) now fails with the same clean empty-title error (exit 2) instead of PASSing — hashtags alone are not a title, including when they are typed into the title itself rather than passed via `--hashtags`. v0.1.1 covered the blank-title case; this closes the in-title variant. A real title that merely contains a hashtag is unaffected.
- 1 regression test added (17 total, all passing).

## v0.1.1 — 2026-11-03
Bug-fix release from the adversarial QA audit (owner's bug-free production gate):
- SP-1 (critical): empty or whitespace-only `--title` now fails with a clean error (exit 2, "title is empty") instead of printing `Verdict: PASS` with exit 0. An empty title plus hashtags (a hashtags-only title) errors the same way.
- SP-2: truncation warnings now tell the truth — a single word longer than the limit reports "cut mid-word — no word boundary available"; the "truncated at a word boundary" wording is used only when a boundary cut actually happened.
- SP-3: character counting is now grapheme-cluster aware (pure stdlib): combining marks, variation selectors, ZWJ sequences, regional-indicator flag pairs, and skin-tone modifiers each count as one visible character. The 100-char rule uses visible characters everywhere.
- SP-4: hashtags are validated (letters/digits/underscore, at least one letter or digit), normalised to a single leading `#` (`##double` → `#double`), invalid tokens (`#` alone, `___`) are ignored with a warning, and dedupe is case-insensitive keeping the first form (`#Cats` + `#cats` → `#Cats`).
- SP-5: control characters (newline, tab, etc.) in the title are replaced with spaces and flagged with a warning — a printed title never contains a raw newline. A title made only of control characters is an empty-title error.
- 10 regression tests added (16 total, all passing). README's documented example runs are unchanged — their outputs still match verbatim.

## v0.1.0 — 2026-11-03
- Initial release: YouTube Shorts title fitter (100-char cap, exact title wording preserved).
- Hashtags that fit stay in the title; overflow hashtags move to the description.
- Full description builder: hook line + hashtags + credits placeholder.
- Over-long titles (>100 chars before hashtags) get a word-boundary truncation warning — never a silent mid-word cut.
