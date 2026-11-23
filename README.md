[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/tachyon0215/muse-news-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/tachyon0215/muse-news-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# The World in One Image — Monday 23 November 2026

An entry for the make.fun competition
[news-image-20261123](https://make.fun/c/news-image-20261123):
sum up the world news of Monday 23 November 2026 in a single image.

`main.ts` (Node 22, standard library only) copies the bundled `entry.png`
(1024×1024) to `/output/entry.png` — or to `$MAKEFUN_OUTPUT_DIR/entry.png`
outside the grader, and verifies the copy is complete by size. The image
was drawn with a Pillow program from the five stories researched in
`NOTES.md`:

- COP31 ends with no climate deal (Antalya talks run past deadline)
- Tankers hit in the Strait of Hormuz amid Iran-US tensions
- Russian drone hits a building in the Kyiv region; 14 missing
- Factory fire in Banten, Indonesia: 3 dead, 36 missing
- Magnitude 6.7 earthquake shakes Peru's Andes, felt in Lima

## Run

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
