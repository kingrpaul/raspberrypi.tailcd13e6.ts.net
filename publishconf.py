# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
import subprocess

sys.path.append(os.curdir)
from pelicanconf import *

DELETE_OUTPUT_DIRECTORY = True

SITEURL = "https://raspberrypi.tailcd13e6.ts.net"
RELATIVE_URLS = False

# --- SEO plugin (pelican-seo) ---
SEO_REPORT = False
SEO_ENHANCER = True
SEO_ENHANCER_OPEN_GRAPH = True
SEO_ENHANCER_SITEMAP_URL = "https://raspberrypi.tailcd13e6.ts.net/sitemap.xml"
LOGO = "https://raspberrypi.tailcd13e6.ts.net/extra/avatar.jpg"