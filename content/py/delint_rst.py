#!/usr/bin/env python3
"""List all .rst files in or beneath a starting directory."""

import argparse
import sys
from pathlib import Path
import os
import re
from datetime import date
from pprint import pprint

def find_rst_files(start_dir: str) -> list[Path]:
    root = Path(start_dir).resolve()
    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {start_dir}")
    return sorted(p for p in root.rglob("*.rst") if p.is_file())

def is_good_date(d: str) -> bool:
    pattern = r"\d\d\d\d-\d\d-\d\d"
    try:
        assert re.fullmatch(pattern, d)
        return True
    except:
        return False

def fld_exists(rst_file: Path, fld_name: str) -> bool:
    """Metadata item present."""
    rst_text = rst_file.read_text(encoding="utf-8")
    if rf":{fld_name}:" in rst_text:
        return True
    return False

def val_exists(rst_file: Path, fld_name: str) -> bool:
    """Metadata item not empty."""
    if fld_exists(rst_file, fld_name):
        rst_text = rst_file.read_text(encoding="utf-8")
        pattern = rf":{re.escape(fld_name)}:\s([^\n]+)\n"
        matching_text = re.search(pattern, rst_text)
        try:
            assert matching_text.group(1)
            return True
        except:
            return False

def field_value(rst_file: Path, fld_name: str) -> str | None:
    """Get field vlue from rst file."""
    if val_exists(rst_file, fld_name):
        rst_text = rst_file.read_text(encoding="utf-8")
        pattern = rf":{re.escape(fld_name)}:\s*\n?"
        matching_text = re.search(pattern + r"([^\n]*)", rst_text)
        fld_val = matching_text.group(1).strip()
        return fld_val         
    return False

def contents(rst_file: Path) -> str | None:
    rst_text = rst_file.read_text(encoding="utf-8")
    return rst_text
    

# =======================

def main() -> int:
    parser = argparse.ArgumentParser(description="Find all .rst files under a directory.")
    parser.add_argument("directory", nargs="?", default="./content", help="Starting directory (default: current)")
    args = parser.parse_args()

    try:
        rst_paths = find_rst_files(args.directory)[:]
    except NotADirectoryError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

#   ==========================
    def good_header(path: Path) -> bool:
        """Has RST-style header."""
        lines = path.read_text(encoding="utf-8").splitlines()
        try: 
            assert lines[0] == lines[2] == "="*len(lines[1])
            return True
        except: 
            return False

    categories = ('page', 'book', 'snap', 'writing', 'post', 'picture', 
                  'musing', 'meme', 'document', 'comic', 'film',
                'illustrations', 'Illustrations')

    valid_tags = {"blackwood", 
                  "auth:lovecraft","auth:blackwood",
                  "format:epub", "format:kobo", "format:pdf",
                "fiction", "nonfiction", "creative",  
                "esperanto", "esperanto-lingva", 
                "group-photo", "portrait", "snap", 
                "icon",
                "illustration", 
                "medical-physics", "how-to", 
                "politics", 
                "quote", "review", "scan", "transcription",
                "pub:internet-archive", "pub:standard-ebooks", 
                
                }
    used_tags = set()
    no_ext_link = {'goodreads': [], 'hardcover': [], 'bookwyrm': []}

    for path in rst_paths:
        # page = "/pages/" in str(path)
        # article = not page

        visible = (not field_value(path, 'status') or field_value(path, 'status') != 'hidden') and '/working/' not in str(path)
        
        is_page = "/pages/" in str(path)
        is_article = not is_page
        slug = field_value(path, 'slug')
        author = field_value(path, 'author')
        lang = field_value(path, 'lang')
        rst_name = path.stem
        created = field_value(path, 'date')
        modified = field_value(path, 'modified')
        category = field_value(path, 'category')
        description = field_value(path, 'description')
        working = '/working/' in str(path)
        try:
            tags = field_value(path, 'tags')
            tags = tags.replace(" ", "").split(",")
        except:
            tags = []
        rst_text = contents(path)
        
        # header
        if not good_header(path):
            print(f"Bad header: {path}")

        # author 
        try: 
            assert author == "pairko"
        except:
            print(f"Bad author: {path}")

        # lang
        try:
            assert lang in ('en', 'eo')
        except:
            print(f"Bad lang: {path}")

        # social image  --- this code is UGLY
        if visible:
            if is_article:
                malformed = False

                og_image = field_value(path, 'og_image')
                if not og_image:
                    malformed = path
                host = r"https://raspberrypi.tailcd13e6.ts.net"

                if not og_image.startswith(host):
                    malformed = path
                else:
                    rel_path = Path(og_image[len(host):])

                stem = str(rel_path.stem)
                if stem not in ("social", "social-en", "social-eo"):
                    malformed = path

                ext = str(rel_path.suffix)
                if ext not in (".jpg", ".png"):
                    malformed = path

                rel_path = rel_path.parent
                expected_rel_path = Path("/".join(str(path).split("/content")[-1].split("/")[:-1]))
                if rel_path != expected_rel_path:
                    malformed = path

                if malformed:
                    print(f"Bad og_image: {path}")
                    # exit()

        # translation
        if rst_name in ("en", "eo"):
            try:
                assert rst_name == lang
            except:
                print(f"Filename lang mismatch: {path}")
                exit()

        # date
        try:
            assert is_good_date(created)
            assert is_good_date(modified)
        except:
            print(f"Bad date: {path}")

        try:
            created = date.fromisoformat(created)
            modified = date.fromisoformat(modified)
        except:
            print(f"Bad date format: {path}")
        try:
            assert modified >= created
        except:
            print(f"Modified before created: {path}")

    # slug
        if '/working/' not in str(path):
            malformed_slug = False
            if is_page:
                if not re.fullmatch(r"[a-z0-9-]+", slug):
                    malformed_slug = path
            else:
                
                match category:
                    case "comic":
                        if not re.fullmatch(r"[a-z0-9-]+", slug):
                            malformed_slug = path
                    case "book":
                        if not re.fullmatch(r"[a-z-]+_[a-z0-9-]+", slug):
                            malformed_slug = path                        
                    case "snap":
                        if not re.fullmatch(r"\d\d\d\d-\d\d-\d\d_[a-z0-9-]+", slug):
                            malformed_slug = path                        
                    case "film" | "picture":
                        if not re.fullmatch(r"\d\d\d\d_[a-z0-9-]+", slug):
                            malformed_slug = path                        
                    case "writing" | "post" | "musing" | "meme":                    
                        if slug != "blackwood" and not re.fullmatch(r"\d\d\d\d-\d\d-\d\d_[a-z0-9-]+", slug):
                            malformed_slug = path                        
                    case "document":
                        if not re.fullmatch(r"\d\d\d\d(-\d\d-\d\d)?_[a-z0-9-]+", slug):
                            malformed_slug = path                        
                    case "illustrations":
                        if not re.fullmatch(r"[a-z0-9-]+", slug):
                            malformed_slug = path                        
        if malformed_slug:
            print(f"Malformed slug: {malformed_slug}")
        
    # category
        if is_page:
            assert not category
        if is_article:
            try:
                assert category in categories
            except:
                print(f"Bad category: {path}")

    # description
        if '/working/' not in str(path):
            if is_article:
                try:
                    assert len(description) > 1
                except:
                    pass
                    # print(f"No description: {path}")

    # tags
        if is_page:
            pass
        if is_article:
            try:
                for tag in tags:
                    used_tags.add(tag)
                    if tag not in valid_tags:
                        print(f"Bad tag: {tag}, {path}")
            except:
                print(f"Bad tag: {path}")
                
            # Look for missed tags
            def is_exception(path, exceptions):
                if any([e in str(path) for e in exceptions]):
                    return True
                else:
                    return False
            def word_in_text(substring, fulltext):
                match = re.search(rf"[^a-z]{substring}[^a-z]", rst_text, re.IGNORECASE)
                if match:
                    return True
                else:
                    return False
            def in_tags(tag, tags):
                if tag in tags:
                    return True
                else:
                    return False

            # Book Reviews
            if category == "book":
                good_links = True 
                if "review" in tags:

                    # GOODREADS 
                    goodreads_pattern = r"\|goodreads\| `Goodreads <https://www\.goodreads\.com/review/show/(\d+)>`\_ \|br\|"
                    goodreads_link = re.findall(goodreads_pattern, rst_text)
                    no_goodreads_link = "🚫 Goodreads |br|" in rst_text
                    if no_goodreads_link: 
                        no_ext_link["goodreads"].extend([path])
                    elif not goodreads_link:
                        good_links = False 

                    # HARDCOVER
                    hardcover_pattern = r"\|hardcover\| `Hardcover <https://hardcover\.app\/books/(.+)>`\_ \|br\|"
                    harcover_link = re.findall(hardcover_pattern, rst_text)
                    no_hardcover_link = "🚫 Hardcover |br|" in rst_text
                    if no_hardcover_link: 
                        no_ext_link["hardcover"].extend([path])
                    elif not harcover_link:
                        good_links = False 

                    # BOOKWYRM
                    bookwyrm_pattern = r"\|bookwyrm\| `Bookwyrm <https://books\.theunseen\.city\/book/(.+)>`\_ \|br\|"
                    bookwyrm_link = re.findall(bookwyrm_pattern, rst_text)
                    no_bookwyrm_link = "🚫 Bookwyrm |br|" in rst_text
                    if no_bookwyrm_link: 
                        no_ext_link["bookwyrm"].extend([path])
                    elif not bookwyrm_link:
                        good_links = False 
            if not good_links:
                        print(path)
                        exit()
            # print(missing_links)

            # Authors
            tag_words = {
                "lovecraft": ("auth:lovecraft", 
                              ("blackwood.rst", "trainspotting", "quantum-field-theory-as-simply-as-possible", "30-coins", "evil-dead-rise", "2026-08-05_nocturne", "2026-08-05_nocturne")),
                "blackwood": ("auth:blackwood", 
                              ("/the-book/en.rst",)),
                "epub": ("format:epub", 
                              ("blackwood.rst", "/icons/icons.rst", "formatting-a-dual-language-glossary")),
                "kobo": ("format:kobo", 
                              ("/icons/icons.rst")),
                "pdf": ("format:pdf", 
                              ("blackwood.rst", "/icons/icons.rst", "quantum-field-theory-as-simply-as-possible", "things-do-indeed-bite-back", "the-shared-philosophy-of-the-scientific-revolution", )),
                "archive.org": ("pub:internet-archive", 
                              ("blackwood.rst", "teago-audrey", "beebe-robert", "quantum-field-theory-as-simply-as-possible", "main-generative-ai", "things-do-indeed-bite-back", "the-shared-philosophy-of-the-scientific-revolution",)),
                "standardebooks": ("pub:standard-ebooks", 
                              ("formatting-a-dual-language-glossary", "wergild")),
            } # 
            
            for word in tag_words:
                if word_in_text(word, rst_text):
                    if not in_tags(tag_words[word][0], tags): 
                        if not is_exception(path, tag_words[word][1]):
                            if not working:
                                print(f"Add {tag_words[word][0]} tag?: {path}")

        # ---------

        # missing meta items
        # field_names = ('summary')
        # for name in field_names:
        #     if not fld_exists(path, name):
        #         print(f"No {name}: {path}")

    # RETURNS THE LINTING RESULTS 

    # Unused valid post tags
    if len(valid_tags - used_tags) > 0:
        print(rf"Unused tags: {[u for u in (valid_tags - used_tags) ]}")
    
    # Book Reviews Not Posted to Platforms
    if False: # COUNT REVIEWS NOT POSTED ON PLATFORMS
        print(rf"Book reviews not posted ⸺ Goodreads {len(no_ext_link["goodreads"])}, Hardcover {len(no_ext_link["hardcover"])}, Bookwyrm {len(no_ext_link["bookwyrm"])}")
    if False: # LIST REVIEWS NOT POSTED ON PLATFORMS
        succinct = lambda loc: str(loc).split('/books/')[-1]
        print("Reviews not posted externally:")
        for n in no_ext_link:
            print(n.capitalize())
            for p in no_ext_link[n]:
                print(rf"  {succinct(p)}")

    return 0            

if __name__ == "__main__":
    sys.exit(main())
    