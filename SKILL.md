---
name: shorts-packager
description: Fit a YouTube Shorts title plus hashtags into the 100-visible-character cap without changing the title's wording — use before uploading a Short whenever the title and hashtags together might exceed 100 characters.
---

# shorts-packager — agent skill

## Purpose

Packages a YouTube Shorts upload title: it fits the title + hashtags
into YouTube's 100-character title line, preserving the title's exact
wording. Hashtags that fit (in the caller's order) stay in the title;
the rest move, in order, into a ready-to-paste description (hook line,
hashtags, credits placeholder). Characters are counted as grapheme
clusters — one visible character = 1 (a flag emoji, a ZWJ family emoji,
a skin-tone emoji, or a letter with a combining accent each count as 1,
not as their raw Unicode code points).

## When to use / not use

Use when:
- You are preparing a Shorts upload and need the final title string and
  description text.
- You need to know whether a title alone already exceeds 100 visible
  characters.

Do not use when:
- The video is a long-form YouTube upload (the 100-char Shorts title
  rule and the overflow-to-description split are Shorts packaging).
- You want the title rewritten — this tool never rewrites wording; it
  only truncates an over-long title (with a loud warning) and places
  hashtags.

## Commands

```bash
# human-readable report
python3 src/shorts_packager.py --title "Cats React to Cucumbers" --hashtags "#shorts #cats #funny"

# machine-readable (agents): one JSON object on stdout
python3 src/shorts_packager.py --title "Cats React to Cucumbers" --hashtags "#shorts #cats #funny" --json

# optional: custom first line for the description
python3 src/shorts_packager.py --title "..." --hashtags "#a #b" --hook "Your hook line" --json
```

Arguments: `--title` (required), `--hashtags` (space- or
comma-separated, with or without `#`), `--hook` (optional), `--json`.

## Output JSON schema

On success, stdout is exactly one JSON object:

- `tool` — `"shorts-packager"`
- `version` — tool version string
- `verdict` — `"PASS"` · `"PASS_WITH_OVERFLOW"` · `"TRUNCATED"`
- `title` — the final title line to paste into YouTube (≤ `limit`)
- `title_length` — visible-character (grapheme) length of `title`
- `limit` — `100`
- `original_title` — the title as supplied (after control-char cleanup)
- `base_title` — the title after any truncation, before hashtags
- `truncated` — bool: the title alone exceeded the limit and was cut
- `mid_word_cut` — bool: the cut had to happen mid-word (no boundary)
- `hashtags_in_title` — list of hashtags placed in the title, in order
- `hashtags_overflow` — list of hashtags moved to the description
- `hashtags_rejected` — invalid hashtag tokens that were ignored
- `hook` — the description's first line
- `description` — the full ready-to-paste description text
- `checks` — list of `{name, status, message, ...numbers}` mirroring
  the human report (Title length, Hashtag placement)
- `warnings` — list of warning strings (same text a human sees)

On error, stdout is one JSON object `{"error": "<message>"}` and the
exit code is 2 — never plain text, never a traceback.

## Exit codes

- `0` — packaged (any verdict: PASS, PASS_WITH_OVERFLOW, TRUNCATED)
- `2` — error: empty/blank title, hashtags alone as the title, or a
  usage error. In `--json` mode the error is the JSON object above.

## Limits & honesty rules

- `TRUNCATED` means the supplied title itself was too long and was
  cut. Report that to the user and suggest they edit the wording — do
  not present a truncated title as the user's exact title.
- The tool never rewrites title wording to make hashtags fit; if you
  need a different title, change it yourself and re-run.
- `PASS_WITH_OVERFLOW` means some hashtags exist only in the
  description, not the title — say so if it matters.
- A hashtag-only string is not a title: it errors (exit 2), in both
  modes. There is no mode in which an empty title passes.
- Counting is visible characters, not bytes and not Unicode code
  points; `title_length` is the number a viewer would count.
