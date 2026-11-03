#!/usr/bin/env python3
"""shorts-packager — fit a YouTube Shorts title into 100 characters.

Rule (standing): a Shorts title line (title + any hashtags placed in it)
must be <= 100 characters. The title's own wording is never altered to
make hashtags fit — hashtags that do not fit move to the description.
If the title alone is already >100 chars, it is truncated only at a
word boundary and a warning is emitted; a word is never cut in half
silently.

Stdlib only. No network, no files written, no data leaves the machine.
"""
from __future__ import annotations

import argparse
import sys

LIMIT = 100
CREDITS_PLACEHOLDER = "Credits: [add your sources / credits here]"


def _normalize_hashtags(raw) -> list[str]:
    """Accept a string ('#a #b' or '#a,#b') or a list; return ['#a', '#b']."""
    if raw is None:
        return []
    if isinstance(raw, str):
        parts = raw.replace(",", " ").split()
    else:
        parts = []
        for item in raw:
            parts.extend(str(item).replace(",", " ").split())
    tags: list[str] = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if not p.startswith("#"):
            p = "#" + p
        if p not in tags:
            tags.append(p)
    return tags


def truncate_at_word_boundary(text: str, limit: int = LIMIT) -> tuple[str, bool]:
    """Return (truncated, was_truncated). Never cuts mid-word if avoidable."""
    if len(text) <= limit:
        return text, False
    cut = text[:limit]
    # If the next char is a space or we are exactly at a boundary, fine.
    if text[limit:limit + 1] == " " or cut.endswith(" "):
        return cut.rstrip(), True
    # Back off to the last space inside the limit.
    idx = cut.rfind(" ")
    if idx > 0:
        return cut[:idx].rstrip(), True
    # Single word longer than the limit: hard cut is unavoidable, flag it.
    return cut, True


def pack(title: str, hashtags=None, hook: str | None = None) -> dict:
    title = (title or "").strip()
    tags = _normalize_hashtags(hashtags)
    warnings: list[str] = []
    verdict = "PASS"

    original_title = title
    was_truncated = False
    if len(title) > LIMIT:
        title, was_truncated = truncate_at_word_boundary(title, LIMIT)
        warnings.append(
            f"Title alone is {len(original_title)} chars (> {LIMIT}) even without hashtags: "
            f"truncated at a word boundary to {len(title)} chars. Edit the title wording yourself for a better fit."
        )
        verdict = "TRUNCATED"

    in_title: list[str] = []
    overflow: list[str] = []
    current = title
    # Preserve hashtag order: fill the title in order; once one does not
    # fit, it and every later hashtag go to the description (no reordering).
    filling = True
    for tag in tags:
        candidate = f"{current} {tag}" if current else tag
        if filling and len(candidate) <= LIMIT:
            in_title.append(tag)
            current = candidate
        else:
            filling = False
            overflow.append(tag)

    if overflow and verdict == "PASS":
        verdict = "PASS_WITH_OVERFLOW"

    hook_line = (hook or "").strip() or title
    desc_lines = [hook_line, ""]
    # Description carries overflow hashtags; if none overflowed, repeat all
    # hashtags there too so the description is still discoverable.
    desc_tags = overflow if overflow else tags
    if desc_tags:
        desc_lines.append(" ".join(desc_tags))
        desc_lines.append("")
    desc_lines.append(CREDITS_PLACEHOLDER)
    description = "\n".join(desc_lines)

    return {
        "title": current,
        "title_length": len(current),
        "limit": LIMIT,
        "base_title": title,
        "original_title": original_title,
        "truncated": was_truncated,
        "hashtags_in_title": in_title,
        "hashtags_overflow": overflow,
        "description": description,
        "hook": hook_line,
        "warnings": warnings,
        "verdict": verdict,
    }


def format_result(r: dict) -> str:
    lines = []
    lines.append(f"Title ({r['title_length']}/{r['limit']}): {r['title']}")
    lines.append(f"Verdict: {r['verdict']}")
    lines.append(
        f"Hashtags in title: {len(r['hashtags_in_title'])}"
        + (f" ({' '.join(r['hashtags_in_title'])})" if r["hashtags_in_title"] else "")
    )
    lines.append(
        f"Hashtags overflow to description: {len(r['hashtags_overflow'])}"
        + (f" ({' '.join(r['hashtags_overflow'])})" if r["hashtags_overflow"] else "")
    )
    for w in r["warnings"]:
        lines.append(f"WARNING: {w}")
    lines.append("")
    lines.append("Description:")
    lines.append("---")
    lines.append(r["description"])
    lines.append("---")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Fit a YouTube Shorts title into 100 characters.")
    ap.add_argument("--title", required=True, help="Video title (exact wording is preserved)")
    ap.add_argument("--hashtags", default="", help='Hashtags, e.g. "#shorts #viral" or "#shorts,#viral"')
    ap.add_argument("--hook", default=None, help="Optional first line for the description")
    args = ap.parse_args(argv)
    result = pack(args.title, args.hashtags, hook=args.hook)
    print(format_result(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
