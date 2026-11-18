#!/usr/bin/env python3
"""Entry program for make.fun competition news-image-20261118.

"Sum up 18 November 2026's world news in one image."

Copies the pre-built entry image stored in this repository
(assets/day.png) to /output/entry.png. No network access, no
randomness, no timestamps: repeated runs write byte-identical output.
"""

import shutil
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "assets" / "day.png"
DEST_DIR = Path("/output")
DEST = DEST_DIR / "entry.png"


def main() -> None:
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, DEST)


if __name__ == "__main__":
    main()
