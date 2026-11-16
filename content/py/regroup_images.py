#!/usr/bin/env python3
"""List all .rst files in or beneath a starting directory."""

import argparse
import sys
from pathlib import Path
import os
from slugify import slugify
import unicodedata
import re
from pprint import pprint


def year(rst):
    m = re.search(r":date:\s*(\d{4})", rst.read_text(encoding="utf-8"))
    year = m.group(1) if m else None
    return year

src_root = Path("/home/systemuser/Documents/code/web_resume/tailcd13e6.ts.net/content/working/pictures")
tgt_root = src_root / Path("..") / 'working'
tgt_root = tgt_root.resolve()
tgt_root.mkdir(exist_ok=True)

img_folder = src_root / 'img'
src_files = sorted(p for p in src_root.rglob("*.rst") if p.is_file())
src_stems = [rst.stem for rst in src_files];
assert len(src_stems) == len(src_files)

years = [year(s) for s in src_files]
assert len(years) == len(src_files)

titles = [rst.read_text(encoding="utf-8").splitlines()[1] for rst in src_files]
assert len(titles) == len(src_files)

replacements = [("Anderson Cancer Center", "ACC"), ("Mississippi School for Mathematics and Science", "MSMS"), ("SN371", "")]
dst_stems = [slugify(s, replacements=replacements, regex_pattern=r"[^a-z]+") for s in titles]; #print(dst_stems)
assert len(dst_stems) == len(src_files)

slugs = [years[i] + "_" + dst_stems[i] for i in range (len(dst_stems))]; #pprint(slugs)
assert len(slugs) == len(src_files)

svg_template = Path('/home/systemuser/Desktop/TEMPLATES/IMAGES/_/working/template.cover.svg')

for i, rst in enumerate(src_files):
    lines = rst.read_text(encoding="utf-8").splitlines()
    title = lines[1]
    title = unicodedata.normalize("NFKD", title)

    src_stem = rst.stem
    src_image = img_folder / f"{src_stem}.jpg"
    
    tgt_stem = slugs[i]
    tgt_folder = tgt_root / tgt_stem 
    tgt_folder.mkdir(exist_ok=True)
    tgt_cover = tgt_folder / f"cover.jpg"
    src_image.copy(tgt_cover)

    tgt_working = tgt_folder / 'working' 
    tgt_working.mkdir(exist_ok=True)

    tgt_image = tgt_working / f"{src_stem}.jpg"
    src_image.rename(tgt_image)
    
    en_copy = tgt_folder / f"en.rst";
    rst.copy(en_copy)
    
    rst_target = tgt_working / f"{src_stem}.rst"
    # rst_target.mkdir(exist_ok=True)
    rst.rename(rst_target)
    svg_template.copy(tgt_working / f"{src_stem}.svg")


exit()

def find_rst_files(start_dir: str) -> list[Path]:
    root = Path(start_dir).resolve()
    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {start_dir}")
    return sorted(p for p in root.rglob("*.rst") if p.is_file())

def is_valid_header(path: Path) -> bool:
    """True if the file opens with an RST-style title:
       line 1: '=' underline, line 2: title, line 3: matching '=' overline."""
    lines = path.read_text(encoding="utf-8").splitlines()

    if len(lines) < 3:
        return False

    first, title, third = lines[:3]
    return (
        first and set(first) == {"="}      # non-empty, '=' only
        and third == first                  # overline matches underline
        and len(first) == len(title)        # length matches the title
    )

def missing_item(path: Path, item: str) -> bool:
    """True if item not in metadata"""
    lines = path.read_text(encoding="utf-8")
    if (":" + item + ":") not in lines:
        return True
    return False

# =======================

def main() -> int:
    parser = argparse.ArgumentParser(description="Find all .rst files under a directory.")
    parser.add_argument("directory", nargs="?", default="./content", help="Starting directory (default: current)")
    args = parser.parse_args()

    try:
        files = find_rst_files(args.directory)
    except NotADirectoryError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    # validate headers
    for path in files:
        if not is_valid_header(path):
            print(f"Bad header: {path}")

    # find missing metadata items
    items = ('date', 'modified', 'author', 
             'category', 'summary', 'description', 
             'slug', 'lang')
    for item in items:
        for path in files:
            if missing_item(path, item):
                print(f"No {item}: {path}")

    # print rst working files 
    for path in files:
        # print(path)
        if 'working' in str(path):
            print(path)
    # return 0
    
    return 0            

# if __name__ == "__main__":
#     sys.exit(main())
    