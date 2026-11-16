#!/usr/bin/env python3
"""List all .rst files in or beneath a starting directory."""

import argparse
import sys
from pathlib import Path as Filepath
import os
import re
from datetime import date
from pprint import pprint
import xml.etree.ElementTree as ET
from svgelements import *


def find_svg_files(start_dir: str) -> list[Filepath]:
    root = Filepath(start_dir).resolve()
    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {start_dir}")
    svg_files = sorted(p for p in root.rglob("*.svg") if p.is_file())
    for b in ('/working/', '/py/', '/icons/'):
        svg_files = [s for s in svg_files if b not in str(s)]
    return svg_files

# =======================

def main() -> int:

    svg_folder = Filepath("./content")
    try:
        svg_paths = find_svg_files(svg_folder)[:]
    except NotADirectoryError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

#   ==========================
    
    SVG_NS = "http://www.w3.org/2000/svg"
    RDF_NS = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    CC_NS = "http://creativecommons.org/ns#"
    DC_NS = "http://purl.org/dc/elements/1.1/"
    INKSCAPE_NS = "http://www.inkscape.org/namespaces/inkscape"
    SODIPODI_NS = "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
    XLINK_NS = "http://www.w3.org/1999/xlink"
    
    ns = {"svg": SVG_NS, "rdf": RDF_NS, "cc": CC_NS, "dc": DC_NS, }

    ET.register_namespace("", SVG_NS)
    ET.register_namespace("cc", CC_NS)
    ET.register_namespace("dc", DC_NS)
    ET.register_namespace("rdf", RDF_NS)
    ET.register_namespace("inkscape", INKSCAPE_NS)
    ET.register_namespace("sodipodi", SODIPODI_NS)
    ET.register_namespace("xlink", XLINK_NS)

    
    files_parsed = []
    roots_found = []
    svg_titles_found = []
    dc_metadata_found = []
    titles_differ = []
    descriptions_differ = []
    creators_found = []
    licenses_found = []
    sources_found = []
    has_subjects = []
    all_subjects = []

    for s in svg_paths:

        license_tag = { 'cc0': '<cc:license rdf:resource="http://creativecommons.org/publicdomain/zero/1.0/" />'}
        license_tag_cc0 = license_tag['cc0']

        license_uri = { 'cc0': "http://creativecommons.org/publicdomain/zero/1.0/"}
        license_uri_cc0 = license_uri['cc0']
        
        license = license_uri_cc0

        title = None
        description = None
        creator = "pairko"
        subjects = []
        source = ""

        
        # ------------------------------------------
        try:  # PARSE THE SVG
            tree = ET.parse(s)
            files_parsed.extend([s])
        except:
            tree = None
            # print("failed to parse:", s.stem)
        try: # GET THE ROOT
            root = tree.getroot()
            roots_found.extend([s])
        except:
            root = None
            # print("failed to find root:", s.stem)
        # ------------------------------------------
        try: # FIND SVG TITLE
            svg_title = root.find("svg:title", ns).text
            svg_titles_found.extend([s])
            # print(svg_title)
        except AttributeError:
            svg_title = None
            # print("no svg title", s)
        title = svg_title
        # ------------------------------------------
        try: #FIND SVG DESC
            svg_desc = root.find("svg:desc", ns).text
        except AttributeError:
            svg_desc = None
            # print("no svg desc", s)
        description = svg_desc
        # ------------------------------------------
        try: # FIND DC METADATA
            dc_metadata = root.find("svg:metadata", ns).text
            dc_metadata_found.extend([s])
            # --------------------------------------
            try: # FIND DC TITLE
                dc_title = root.find(".//dc:title", ns).text
            except AttributeError:
                dc_title = None
            if svg_title != dc_title:
                titles_differ.extend([s])
            # --------------------------------------
            try: # FIND DC DESCRIPTION
                dc_description = root.find(".//dc:description", ns).text
            except AttributeError:
                dc_description = None
            if svg_desc != dc_description:
                descriptions_differ .extend([s])
            # --------------------------------------
            try: # FIND DC CREATOR
                dc_creator = root.find(".//dc:creator", ns).text
                creator = dc_creator
                creators_found.extend([s])
            except AttributeError:
                dc_creator = None
            # --------------------------------------
            try: # FIND LICENSE
                license = root.find(".//cc:Work/cc:license", ns).get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource")
                licenses_found.extend([s])
            except AttributeError:
                pass
            # --------------------------------------
            try:  # FIND SOURCE
                source = root.find(".//cc:Work/dc:source", ns).text
                if not source: assert False
                sources_found.append(source)
            except:
                pass            
            # --------------------------------------
            try: # FIND DC SUBJECTS
                subjects = root.findall(".//cc:Work/dc:subject/rdf:Bag/rdf:li", ns)
                subjects_list = [d.text for d in subjects]
                subjects = subjects_list
                if subjects == [None]:
                    assert False
                has_subjects.extend([s])
                try:  # UPDATE THE MASTER LIST OF SUBJECTS
                    all_subjects.extend(subjects_list)
                    all_subjects = list(set(all_subjects))
                except:
                    pass
            except:
                pass
        except AttributeError:
            dc_metadata = None

        def q(ns, tag): # {uri}local — the form ET demands
            return f"{{{ns}}}{tag}"

        def build_metadata(title, creator, description, license_uri, subjects, source):

            work = ET.Element(q(CC_NS, "Work"), {q(RDF_NS, "about"): ""})
            ET.SubElement(work, q(DC_NS, "title")).text = title

            agent = ET.SubElement(work, q(DC_NS, "creator"))
            ag = ET.SubElement(agent, q(CC_NS, "Agent"))
            ET.SubElement(ag, q(DC_NS, "title")).text = creator

            ET.SubElement(work, q(DC_NS, "description")).text = description

            ET.SubElement(work, q(DC_NS, "source")).text = source

            if not subjects:
                subjects = [""]                    # empty list → one empty slot
            subject = ET.SubElement(work, q(DC_NS, "subject"))
            bag = ET.SubElement(subject, q(RDF_NS, "Bag"))
            for s in subjects:
                ET.SubElement(bag, q(RDF_NS, "li")).text = s

            ET.SubElement(work, q(CC_NS, "license"),
                        {q(RDF_NS, "resource"): license_uri})

            rdf = ET.Element(q(RDF_NS, "RDF"))
            rdf.append(work)
            meta = ET.Element(q(SVG_NS, "metadata"))
            meta.append(rdf)
            return meta
        
        meta = build_metadata(
            title = title,
            creator = creator,
            description = description,
            license_uri = license,
            subjects = subjects,
            source = source
            )

        old = root.find(q(SVG_NS, "metadata"))
        if old is not None:
            i = list(root).index(old)
            root[i] = meta
        else:
            root.append(meta)                 # none existed — insert

        ET.indent(tree, space="  ")
        dest = '/home/systemuser/Downloads/' + str(s).split('/content/')[-1]
        os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
        tree.write(dest, encoding="utf-8", xml_declaration=True)
        # tree.write(f"/home/systemuser/Downloads/{s.stem}.svg", encoding="utf-8", xml_declaration=True)

    # PRINT THE DIAGNOSTICS
    print(rf"svg_folder: {svg_folder.resolve()}")
    print(rf"svg_paths: {len(svg_paths)}")
    print(rf"files_parsed: {len(files_parsed)}")
    print(rf"roots_found: {len(roots_found)}")
    print(rf"svg_titles_found: {len(svg_titles_found)}")
    print(rf"dc_metadata_found: {len(dc_metadata_found)}")
    print(rf"titles_differ: {len(titles_differ)}")
    print(rf"descriptions_differ: {len(descriptions_differ)}")
    print(rf"creators_found: {len(creators_found)}")
    print(rf"licenses_found: {len(licenses_found)}")
    print(rf"sources_found: {len(sources_found)}")
    print(rf"has_subjects: {len(has_subjects)}")
    print(rf"total subjects: {len(all_subjects)}")
    print(rf"subjects {len((all_subjects))} : {', '.join(all_subjects[1:])}")
    return 0            

if __name__ == "__main__":
    sys.exit(main())
    