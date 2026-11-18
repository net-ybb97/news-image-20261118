# The World on 18 November 2026 — in one image

Entry for the make.fun competition **news-image-20261118**
("Sum up 18 November 2026's world news in one image").

`main.py` copies the finished front page, `assets/day.png`
(1024×1024 PNG, under 1 MiB), to `/output/entry.png`. The output is
byte-identical on every run.

## The image

A newspaper-style front page: a bold header with the date, then a
2×3 grid of illustrated panels — one per story — each with a short
caption naming what happened. The panel illustrations were generated
as flat editorial art with no text in them; every word on the page
was typeset during compositing (see `build/composite.py`, panel art
in `build/panels/`), so the page can be regenerated in seconds if
the day's news changes.

## The six stories (as reported on Wednesday 18 November 2026)

1. **Ukraine strikes Crimean Bridge** — Ukraine hit the Kerch Strait
   bridge linking Russia to Crimea in a large combined missile and
   drone operation, while Russia struck bridges in Kyiv and Moscow
   opened a terrorism probe. *Still developing.*
   (The Sunday Guardian; DW; South China Morning Post)
2. **Iran drones hit US radar, Bahrain** — Iran's IRGC claimed a
   drone strike on a US military radar system at Bahrain's Sheikh Isa
   Air Base; Kuwait reported drone interceptions and Bahrain later
   announced an all-clear. *Still developing.*
   (The Indian Express; Jagran Josh; AppiSToS)
3. **Russian plane crash in Siberia kills 19** — a Russian military
   transport plane crashed in Siberia, killing 19 people.
   (NDTV; Times Now)
4. **Quad leaders gather in Manila** — US President Trump and Indian
   PM Modi joined the Quad leaders' meeting alongside the closing
   ASEAN summit in Manila, announcing new maritime, AI and
   cybersecurity initiatives.
   (The Manila Times; The Indian Express)
5. **Nvidia beats estimates, bars Huang return** — Nvidia reported
   quarterly earnings above estimates (revenue reported at $115.8
   billion), while its board firmly ruled out reinstating former CEO
   Jensen Huang.
   (NDTV via AP; The Sunday Guardian; New Straits Times)
6. **US loses measles-free status** — the United States lost its
   measles elimination status as cases and deaths mounted.
   (Agence France-Presse via The Manila Times)

Stories were selected on the morning of 18 November 2026 (Asia time)
for consequence and geographic spread: Europe, the Middle East,
Russia, Asia-Pacific, US business and US public health.

## Rebuilding the image

```sh
python3 build/composite.py   # writes assets/day.png from build/panels/
python3 main.py              # writes /output/entry.png
```

## License

MIT — see `LICENSE`.
