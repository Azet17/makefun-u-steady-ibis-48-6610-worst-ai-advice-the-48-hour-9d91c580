"""Worst AI Advice entry — writes one line of terrible advice to entry.txt.

The line is a single, confident-sounding "fix" for a slow laptop that would
actually destroy the machine. Python standard library only; no network access;
writes only inside the output directory given by MAKEFUN_OUTPUT_DIR
(falling back to /output).
"""

import os

ADVICE = (
    "To speed up a slow laptop, delete the System32 folder "
    "\u2014 it's just leftover Windows files slowing you down."
)

MAX_CHARS = 140


def main() -> None:
    line = ADVICE.strip()
    if not line:
        raise ValueError("advice line is empty")
    if len(line) > MAX_CHARS:
        raise ValueError(f"advice line is {len(line)} chars, over the 140 limit")
    if "\n" in line:
        raise ValueError("advice line must be a single line")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Write atomically via a temp file so a crash can never leave a
    # half-written entry.txt behind, then read back to confirm the
    # exact bytes on disk.
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(line + "\n")
    os.replace(tmp_path, path)
    with open(path, encoding="utf-8") as fh:
        written = fh.read().rstrip("\n")
    if written != line:
        raise ValueError("verification failed: entry.txt does not match the advice line")
    print(f"wrote {len(line)} chars to {path}")


if __name__ == "__main__":
    main()
