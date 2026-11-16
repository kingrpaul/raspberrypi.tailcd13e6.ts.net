import os
import xml.etree.ElementTree as ET
import platform
from datetime import datetime, date
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import json
from pprint import pprint
import os
import sys
from PIL import Image
from slugify import slugify
import shutil
from datetime import datetime
import numpy as np
from pathlib import Path
from os.path import exists as exists
from os.path import join as join
import datetime

def make_slug(data):
    slug_result = ""
    if data['date']:
        slug_result += data['date']
    if data['date'] and data['title-en']:
        slug_result += "_"
    if data['title-en']:
        slug_result += slugify(data['title-en'].replace("'", ""))
    return slug_result

def f_root(filename):
    return os.path.splitext(filename)[0]

def extract_date(str):
    try:
        date = str.split('_')[0]
        y,m,d = date[0:4], date[4:6], date[6:8]
        assert int(date) < 25000000        
        assert int(y) > 1900
        assert int(m) < 13
        assert int(d) < 32
        return('-'.join([y,m,d]))
    except:
        return False


# print("make-post \n   --begin")

####### FOLDERS ####### 
PROJECT_ROOT = join(os.getcwd(), 'content', 'py', 'make-post')
SOURCE = join(PROJECT_ROOT, 'SOURCE')
SOURCE_IMAGES = join(SOURCE, 'IMAGES')
SOURCE_JSON = join(SOURCE, 'JSON')
DEST = join(PROJECT_ROOT, 'DEST')
DEST_IMAGES = join(DEST, 'IMAGES')
DEST_PAGES = join(DEST, 'PAGES')

####### FILES ####### 
src_files = []
for _, _, files in os.walk(SOURCE):
    for file in files:
        src_files.append(file)
json_files = [d for d in os.listdir(SOURCE_JSON)]
image_files = [d for d in os.listdir(SOURCE_IMAGES)]
json_roots = [j.split('.')[0] for j in json_files]
image_roots = [i.split('.')[0] for i in image_files]

####### IF NO SOURCE FILES, DO NOTHING ####### 
if not src_files:
    print("no source files \n   --end")
    exit()

####### IF ONLY SOURCE FILES, CREATE JSON FILES ####### 
if image_files and not json_files:
    for r in image_roots:
        json_source = join(PROJECT_ROOT, 'TEMPLATE.json')
        json_dest = join(SOURCE_JSON, f_root(r) + '.json')
        shutil.copyfile(json_source, json_dest)
        ### IF FILENAME STARTS WITH DATE, ADD DATE TO JSON
        d = extract_date(r)
        if d: 
            with open(json_dest) as file:
                contents = file.read()
                contents = contents.replace('"date": "', '"date": "' + str(d),)
            with open(json_dest, "w") as file:
                file.write(contents)
    exit()


# DEST ##################################################

def clear_dest_folders():
    oldpath = \
        [join(DEST_IMAGES, d) for d in os.listdir(DEST_IMAGES)] + \
        [join(DEST_PAGES, d) for d in os.listdir(DEST_PAGES)]
    for o in oldpath:
        assert exists(o)
        shutil.rmtree(o)
    return
##################################################

def rst_en(data):
    result = "="*len(data["title-en"]) + '\n'
    result += data["title-en"] + '\n'
    result += "="*len(data["title-en"]) + '\n'
    result += ':date: ' + data['date']  + '\n'
    result += ':modified: ' + datetime.date.today().strftime('%Y-%m-%d')  + '\n'
    result += ':author: pairko'  + '\n' 
    result += ':category: blog'  + '\n' 
    result += ':summary: ' +  data['summary-en'] + '\n'         
    result += ':description: ' +  data['description-en'] + '\n'                 
    result += ':tags: du-lingva'  + '\n' 
    result += ':slug: ' +  slug + '\n'                 
    result += ':lang: en'  + '\n' 
    result += ':og_image: /images/' + slug + '/social.jpg' + '\n' 
    result += '\n'
    result += '.. image:: /images/' + slug + '/cover.jpg' + '\n' 
    result += '   :alt: ' +  data['description-en'] + '\n'
    result += '\n'
    result += data['summary-en'] + '\n'         
    return result

def rst_eo(data):
    result = "="*len(data["title-eo"]) + '\n'
    result += data["title-eo"] + '\n'
    result += "="*len(data["title-eo"]) + '\n'
    result += ':date: ' + data['date']  + '\n'
    result += ':modified: ' + datetime.date.today().strftime('%Y-%m-%d')  + '\n'
    result += ':author: pairko'  + '\n' 
    result += ':category: blog'  + '\n' 
    result += ':summary: ' +  data['summary-eo'] + '\n'         
    result += ':description: ' +  data['description-eo'] + '\n'                 
    result += ':tags: esperanto-lingva'  + '\n' 
    result += ':slug: ' +  slug + '\n'                 
    result += ':lang: eo'  + '\n' 
    result += ':og_image: /images/' + slug + '/social.jpg' + '\n' 
    result += ':translation: true'  + '\n' 
    result += ':article-translation-id: ' +  slug + '\n'                 
    result += '\n'
    result += '.. image:: /images/' + slug + '/cover.jpg' + '\n' 
    result += '   :alt: ' +  data['description-eo'] + '\n'
    result += '\n'
    result += data['summary-eo'] + '\n'         
    return result


clear_dest_folders()

# exit()
# ************


for i, j in enumerate(json_roots):

    json_file = join(SOURCE_JSON, j+'.json')

    with open(json_file) as file:
        data = json.load(file)

        # IGNORE UNTITLED JSON FILES
        if not data['title-en'] and not data['title-eo']:
            continue

        slug = make_slug(data)

        # CREATE DESTINATION SUB-FOLDER
        for p in [join(DEST_IMAGES, slug), 
                    join(DEST_PAGES, slug),
                    join(DEST_IMAGES, slug, 'working')]:
            if not exists(p):
                os.makedirs(p)

        # COPY SVG TEMPLATE TO DESTINATION
        svg_source = join(PROJECT_ROOT, 'template.cover.svg') 
        assert exists(svg_source)
        svg_dest = join(DEST_IMAGES, slug, 'working', slug) + '.svg'
        if not exists(svg_dest):
            shutil.copyfile(svg_source, svg_dest)

        # COPY DISPLAY IMAGE TO DESTINATION
        img_source = join(SOURCE_IMAGES, image_files[i])
        img_dest = join(DEST_IMAGES, slug, 'working', image_files[i])
        if not exists(img_dest):
            shutil.copyfile(img_source, img_dest)

        # COPY JSON FILE TO DESTINATION
        json_source = join(SOURCE_JSON, json_files[i])
        json_dest = join(DEST_IMAGES, slug, 'working', json_files[i])
        if not exists(json_dest):
            shutil.copyfile(json_source, json_dest)

        # CREATE EN RST
        if data["title-en"]:
            rst_en_text = rst_en(data)
            rst_en_dest = join(DEST_PAGES, slug, 'en.rst')
            with open(rst_en_dest, 'w') as r:
                for line in rst_en_text:
                    r.write(line)

        # CREATE EO RST
        if data["title-eo"]:
            rst_eo_text = rst_eo(data)
            rst_eo_dest = join(DEST_PAGES, slug, 'eo.rst')
            with open(rst_eo_dest, 'w') as r:
                for line in rst_eo_text:
                    r.write(line)                
                
print("   --end")

