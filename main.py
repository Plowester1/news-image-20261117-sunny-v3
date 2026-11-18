"""news-image-20261117 sunny v3 entry: emit the infographic to /output/entry.png.

The image (entry.png, bundled beside this file) is a 1024x1024 vertical-list
front page — dark teal/slate, hero Gaza card on top, seven story rows below —
summing up Tuesday 17 November 2026 in eight verified stories. It is
composed programmatically with PIL (see build_image.py).

The program itself is a pure file copy: no network, no randomness, no clock,
so running it twice writes byte-identical output.
"""
import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def digest(path):
    """SHA-256 hex digest of a file, streamed in 1 MiB chunks."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(1 << 20)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def main():
    if not os.path.isfile(SOURCE):
        raise SystemExit("missing bundled image: entry.png not found beside main.py")
    if os.path.getsize(SOURCE) > 1 << 20:
        raise SystemExit("entry.png exceeds the 1 MiB competition limit")
    os.makedirs(OUT_DIR, exist_ok=True)
    dest = os.path.join(OUT_DIR, "entry.png")
    shutil.copyfile(SOURCE, dest)
    if digest(dest) != digest(SOURCE):
        raise SystemExit("copy mismatch: /output/entry.png differs from entry.png")
    print("wrote", dest, "sha256", digest(dest))


if __name__ == "__main__":
    main()
