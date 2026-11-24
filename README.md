# THE WORLD TODAY — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b122-front-page-dense/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b122-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image summing up 23 November 2026's world news: the AI rout in Asia (Kospi −3.3%),
Guterres urging AI regulation in Bridgetown, and the US lead over China at a record low —
plus 10 more stories, 18 also-mentioned, a world map with numbered pins, and a DATE CHECK
box listing what did NOT happen on 23 November.

## How it is built

- `draw.py` (PIL) renders `entry.png` — 1024×1024, under 1 MiB.
- `main.py` (stdlib only) validates the PNG and copies it to `$MAKEFUN_OUTPUT_DIR/entry.png`.

## Run

```sh
python3 draw.py
MAKEFUN_OUTPUT_DIR=out python3 -P -s main.py
```
