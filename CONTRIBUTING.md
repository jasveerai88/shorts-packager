# Contributing

Thanks for helping improve shorts-packager!

## Rules
- Python 3 stdlib only — no new dependencies.
- Keep the 100-character rule exact: never cut a word in half, never silently drop a hashtag.
- Add a test for every behaviour change.

## Dev
```bash
python3 -m unittest discover -s tests -v
python3 src/shorts_packager.py --title "My Title" --hashtags "#shorts #viral"
```

Open an issue or PR with a real example (title + hashtags + expected output).
