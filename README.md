# shorts-packager

**Your Shorts title has 100 characters. Not 101.** YouTube truncates long titles in feeds, and hashtags shoved into a title either push it over the limit or get silently wasted. shorts-packager fits your title + hashtags into the 100-character cap *without changing your title's wording*: hashtags that fit (in your order) stay in the title, the rest move to a ready-to-paste description — hook line, hashtags, and a credits placeholder included.

Built for faceless and small creators who upload in batches. 100% local: no accounts, no logins, no tracking, nothing leaves your machine.

## Run it

```bash
python3 src/shorts_packager.py --title "Cats React to Cucumbers" --hashtags "#shorts #cats #funny"
```

## Real run (verbatim)

```
$ python3 src/shorts_packager.py --title "Cats React to Cucumbers" --hashtags "#shorts #cats #funny"
Title (44/100): Cats React to Cucumbers #shorts #cats #funny
Verdict: PASS
Hashtags in title: 3 (#shorts #cats #funny)
Hashtags overflow to description: 0

Description:
---
Cats React to Cucumbers

#shorts #cats #funny

Credits: [add your sources / credits here]
---
```

Hashtags that don't fit overflow to the description — in order, never reordered, never dropped:

```
$ python3 src/shorts_packager.py --title "This Goalkeeper Made The Most Impossible Save You Will Ever See In Football History" --hashtags "#shorts #football #goalkeeper #viral #amazing"
Title (91/100): This Goalkeeper Made The Most Impossible Save You Will Ever See In Football History #shorts
Verdict: PASS_WITH_OVERFLOW
Hashtags in title: 1 (#shorts)
Hashtags overflow to description: 4 (#football #goalkeeper #viral #amazing)

Description:
---
This Goalkeeper Made The Most Impossible Save You Will Ever See In Football History

#football #goalkeeper #viral #amazing

Credits: [add your sources / credits here]
---
```

## The rules it enforces

- **100-char cap** on the title line (title + hashtags placed in it).
- **Exact title wording** — the tool never rewrites your title to squeeze a hashtag in.
- **Order preserved** — hashtags fill the title in the order you gave them; once one doesn't fit, it and the rest go to the description.
- **Over-long title = loud warning, not a silent cut.** If the title alone is already over 100 chars, it is truncated only at a word boundary and the output says `Verdict: TRUNCATED` with a warning telling you to edit the wording yourself. A word is never cut in half silently.
- Hashtags work with or without the `#`, comma- or space-separated; duplicates are removed.

Optional: `--hook "Your first description line"` to set the description's hook line (defaults to the title).

Verdicts: `PASS` · `PASS_WITH_OVERFLOW` (some hashtags moved to the description) · `TRUNCATED` (title itself was too long).

## Tests

```bash
python3 -m unittest discover -s tests -v
# 6 tests: short title all fits, long title overflow to description,
# over-long title flagged + word-boundary check, truncate helper,
# custom hook / bare hashtags, no-hashtags case
```

## Privacy

What it touches: only the title/hashtags you type on the command line. What it stores: nothing. What it sends: nothing — there is no network code in this tool.

## Why it's free / sponsor

I build free, local-first tools for small and faceless creators from measured failure data on real channels. GitHub Sponsors is live: **https://github.com/sponsors/jasveerai88** — sponsors keep the tools free and fund the next ones.

## Internal use

This is the title/description packager used before uploads on three real YouTube channels (news + story formats) — the 100-char rule and the overflow-to-description split come straight from that workflow.

MIT licensed. Python 3 stdlib only.
