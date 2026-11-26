#!/usr/bin/env python3
"""List all .rst files in or beneath a starting directory."""

import argparse
import sys
from pathlib import Path
import os
import re
from datetime import date
from pprint import pprint

# short version of a file Path
succinct = lambda loc: str(loc).split('/books/')[-1]

host = r"https://raspberrypi.tailcd13e6.ts.net"

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

def get_field_value(rst_text: Path, fld_name: str) -> str | None:
    """Get field value from rst file."""
    # rst_text = rst_file.read_text(encoding="utf-8")
    key_pattern = rf":{re.escape(fld_name)}:\s"
    key_exists = re.search(key_pattern, rst_text)
    if not key_exists:
        return False
    val_pattern = key_pattern + r"([^\n]*)"
    val = re.search(val_pattern, rst_text).group(1).strip()
    if not val:
        return False
    return val

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

    categories = ('page', 'book', 'snap', 'writing', 'post', 'picture', 
                  'musing', 'meme', 'document', 'comic', 'film',
                'illustrations', 'Illustrations')

    valid_tags = {"blackwood", 
                  "auth:lovecraft","auth:blackwood",
                  "format:epub", "format:kobo", "format:kindle", "format:pdf",
                "fiction", "nonfiction", "creative",  
                "esperanto", "lang:eo", 
                "group-photo", "portrait",
                "icon",
                "illustration", 
                "medical-physics", "how-to", 
                "politics", 
                "quote", "review", "scan", "transcription",
                "pub:internet-archive", "pub:standard-ebooks", 
                
                }
    used_tags = set()
    no_ext_link = {'goodreads': [], 'hardcover': [], 'bookwyrm': []}

    def get_tags(path):
        try:
            tags = get_field_value(rst_text, 'tags')
            tags = tags.replace(" ", "").split(",")
            if len(set(tags)) != len(tags):
                print(f"Duplicate tags: {succinct(path)}")
        except:
            tags = []
        return tags

    # for path in rst_paths[179:180]:
    for path in rst_paths:
        rst_text = path.read_text(encoding="utf-8")
        status_not_set = not get_field_value(rst_text, 'status')
        status_hidden = get_field_value(rst_text, 'status') == 'hidden'
        status_working = '/working/' in str(path)
        visible = ((status_not_set) or (not status_hidden)) and (not status_working)
        is_page = "/pages/" in str(path)
        is_article = not is_page
        slug = get_field_value(rst_text, 'slug')
        author = get_field_value(rst_text, 'author')
        lang = get_field_value(rst_text, 'lang')
        rst_name = path.stem
        created = get_field_value(rst_text, 'date')
        modified = get_field_value(rst_text, 'modified')
        category = get_field_value(rst_text, 'category')
        description = get_field_value(rst_text, 'description')
        working = '/working/' in str(path)
        tags = get_tags(path)
        
        # header
        lines = rst_text.splitlines()
        valid_header = lines[0] == lines[2] == "="*len(lines[1])
        if not valid_header:
            print(f"Bad header: {succinct(path)}")

        # author 
        if author != "pairko":
            print(f"Bad author: {succinct(path)}")

        # lang
        try:
            assert lang in ('en', 'eo')
        except:
            print(f"Valid lang not specified: {succinct(path)}")
        if (lang == 'eo') and ("lang:eo" not in tags):
            print(f"lang:eo tag missing: {succinct(path)}")

        # social image
        if visible:
            if is_article:
                try:
                    og_image = get_field_value(rst_text, 'og_image')
                    pattern = rf"{host}.+(social|social-en|social-eo)\.(jpg|png)"
                    assert re.fullmatch(pattern, og_image)
                except:
                    print(f"Bad og_image: {succinct(path)}")

        # translation
        if rst_name in ("en", "eo"):
            try:
                assert rst_name == lang
            except:
                print(f"Filename lang mismatch: {succinct(path)}")
                # exit()

        # date
        try:
            assert is_good_date(created)
            assert is_good_date(modified)
        except:
            print(f"Bad date: {succinct(path)}")

        try:
            created = date.fromisoformat(created)
            modified = date.fromisoformat(modified)
        except:
            print(f"Bad date format: {succinct(path)}")
        try:
            assert modified >= created
        except:
            print(f"Modified before created: {succinct(path)}")

    # slug
        if '/working/' not in str(path):
            bad_slug = False
            if is_page:
                if not re.fullmatch(r"[a-z0-9-]+", slug):
                    bad_slug = path
            else:
                match category:
                    case "comic":
                        if not re.fullmatch(r"[a-z0-9-]+", slug):
                            bad_slug = path
                    case "book":
                        if not re.fullmatch(r"[a-z-]+_[a-z0-9-]+", slug):
                            bad_slug = path                        
                    case "snap":
                        if not re.fullmatch(r"\d\d\d\d-\d\d-\d\d_[a-z0-9-]+", slug):
                            bad_slug = path                        
                    case "film" | "picture":
                        if not re.fullmatch(r"\d\d\d\d_[a-z0-9-]+", slug):
                            bad_slug = path                        
                    case "writing" | "post" | "musing" | "meme":                    
                        if slug != "blackwood" and not re.fullmatch(r"\d\d\d\d-\d\d-\d\d_[a-z0-9-]+", slug):
                            bad_slug = path                        
                    case "document":
                        if not re.fullmatch(r"\d\d\d\d(-\d\d-\d\d)?_[a-z0-9-]+", slug):
                            bad_slug = path                        
                    case "illustrations":
                        if not re.fullmatch(r"[a-z0-9-]+", slug):
                            bad_slug = path                        
        if bad_slug:
            print(f"Malformed slug: {bad_slug}")
        
    # category
        if is_page:
            assert not category
        if is_article:
            try:
                assert category in categories
            except:
                print(f"Bad category: {succinct(path)}")

    # description
        if '/working/' not in str(succinct(path)):
            if is_article:
                try:
                    assert len(description) > 1
                except:
                    pass

    # tags
        if is_page:
            pass
        if is_article:
            # Look for invalid tags
            for tag in tags:
                used_tags.add(tag)
                if tag not in valid_tags:
                    print(f"Bad tag: {tag}, {succinct(path)}")
                
            # Look for missing tags
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
            # look for inconsistent en-eo tags -- pelican requires they be the same
            if rst_name == 'eo':
                en_path = path.parent/'en.rst'
                if en_path.exists():
                    en_tags = get_tags(en_path)
                    if set(tags) != set(en_tags):
                        if len(set(tags) - set(en_tags)) == 1:
                            missing_tag = list(set(tags) - set(en_tags))[0]
                            if missing_tag in valid_tags:
                                print(rf"add {missing_tag} to: {en_path}")
                        else:
                            print(rf"mismatched translation tags: {succinct(path)}")
                            print(rf" Tags: {tags}")
                            print(rf"   Path: {succinct(path)}")
                            print(rf" Tags: {en_tags}")
                            print(rf"   Path: {en_path}")

            # Book Reviews - validate platform links
            good_links = True 
            if category == "book":
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
                print(rf"platform links not correct: {succinct(path)}")

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
                "azw3": ("format:kindle", 
                              ("")),
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
                                print(f"Add {tag_words[word][0]} tag?: {succinct(path)}")

    # Unused valid post tags
    REPORT_UNUSED_TAGS = True
    if REPORT_UNUSED_TAGS:
        if len(valid_tags - used_tags) != 0:
            print(rf"Unused tags: {[u for u in (valid_tags - used_tags) ]}")
    
    # Book Reviews Not Posted to Platforms
    COUNT_REVIEWS_NOT_POSTED_ON_PLATFORMS = False
    if COUNT_REVIEWS_NOT_POSTED_ON_PLATFORMS:
        print(rf"Book reviews not posted ⸺  Goodreads {len(no_ext_link["goodreads"])}, Hardcover {len(no_ext_link["hardcover"])}, Bookwyrm {len(no_ext_link["bookwyrm"])}")
    LIST_REVIEWS_NOT_POSTED_ON_PLATFORMS = False
    if LIST_REVIEWS_NOT_POSTED_ON_PLATFORMS: # LIST REVIEWS NOT POSTED ON PLATFORMS
        
        print("Reviews not posted externally:")
        for n in no_ext_link:
            print(n.capitalize())
            for p in no_ext_link[n]:
                print(rf"  {succinct(p)}")

    return 0            

if __name__ == "__main__":
    sys.exit(main())
    