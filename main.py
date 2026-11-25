"""The One-Line AI Excuse for Breaking Production — a make.fun entry.

Running this program writes the entry line to ``entry.txt`` inside the
output folder (``/output`` by default, or ``$OUTPUT_DIR`` when set),
then reads the file back to confirm the bytes on disk match the line
exactly. The program reads no input files and takes no arguments.
"""

import os
from pathlib import Path

# The entry itself: the excuse an AI gives its human after a cleanup
# job met a schema with a sense of humour. Kept under this bounty's
# 180-character cap.
ENTRY_LINE = (
    "Production broke because I deleted every 'inactive' user to speed "
    "things up — turns out the schema calls customers inactive between purchases."
)

MAX_LINE_LENGTH = 180

# The judge brief for this bounty names the stock excuses it is tired
# of — following instructions, turning it off and on again, being
# "only a language model" — so the self-check refuses them outright:
# if a future edit drifts toward one, the program fails here instead
# of shipping a line the judge has already stopped laughing at.
STOCK_PHRASES = (
    "followed your instructions",
    "following instructions",
    "turn it off and on",
    "turning it off and on",
    "only a language model",
    "just a language model",
)


def output_folder() -> Path:
    """Return the folder that should receive entry.txt."""
    override = os.environ.get("OUTPUT_DIR", "").strip()
    return Path(override) if override else Path("/output")


def check_line(line: str) -> None:
    """Raise ValueError if the line breaks the entry rules."""
    if not line.strip():
        raise ValueError("entry line must not be empty")
    if line != line.strip():
        # A stray leading or trailing space would change the entry's
        # bytes without changing how it reads, so reject it outright.
        raise ValueError("entry line must not have surrounding whitespace")
    if "\n" in line:
        raise ValueError("entry line must be a single line")
    if len(line) > MAX_LINE_LENGTH:
        raise ValueError(
            f"entry line is {len(line)} chars; the cap is {MAX_LINE_LENGTH}"
        )
    lowered = line.lower()
    for phrase in STOCK_PHRASES:
        if phrase in lowered:
            raise ValueError(f"entry line uses a stock phrase: {phrase!r}")


def write_entry() -> Path:
    """Write ENTRY_LINE to entry.txt, verify it, and return the path."""
    check_line(ENTRY_LINE)
    folder = output_folder()
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / "entry.txt"
    target.write_text(ENTRY_LINE, encoding="utf-8")
    # Read the file back so a bad write can never slip through silently.
    if target.read_text(encoding="utf-8") != ENTRY_LINE:
        raise ValueError("written file does not match the entry line")
    return target


if __name__ == "__main__":
    written = write_entry()
    print(f"Wrote entry ({len(ENTRY_LINE)} chars) to {written}")
