SITENAME = 'PAIRKO'
SITESUBTITLE = 'A garden, not a platform.🌱'
SITEURL = "https://raspberrypi.tailcd13e6.ts.net"
AUTHOR = 'PAIRKO'

DELETE_OUTPUT_DIRECTORY = True

DEFAULT_LANG = 'en'
OG_LOCALE = 'en_US'
LOCALE = ('en_US', 'eo_EO')
TIMEZONE = 'America/Chicago'
DEFAULT_DATE_FORMAT = '%b %d, %Y'  # e.g., "Feb 04, 2026"

MARKUP = ('md', 'rst') 
RST_IGNORE_COMMENTS = ['exportable-section', 'end-exportable-section']

THEME = 'themes/flex'
PATH = "content"
PAGE_PATHS = ['pages']
# ARTICLE_PATHS = ['articles']
DIRECT_TEMPLATES = ['index', 'tags', 'categories', 'archives', 'search']

INDEX_SAVE_AS = 'index.html'
PATH_METADATA = r'(?P<path_no_ext>.*)..*'
# PAGE_URL = PAGE_SAVE_AS = '{path_no_ext}.html'
ARTICLE_URL = ARTICLE_SAVE_AS = PAGE_URL = PAGE_SAVE_AS = '{slug}.html'

PLUGINS = ['tipue_search', 
           'seo',
           'sitemap'
        #    'pelican-plugins/i18n_subsites'  # dual-language plugin for later
           ]

EXTRA_PATH_METADATA = {
    # "extra/robots.txt": {"path": "robots.txt"},
    "extra/favicon.ico": {"path": "favicon.ico"},
    "extra/custom.css": {'path': "static/css/custom.css"},
}

CUSTOM_CSS = "static/css/custom.css"

DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = False
DISPLAY_TAGS_ON_SIDEBAR = False

SITELOGO = "/extra/avatar.jpg"
# SITELOGO = "/pages/images/landing/social_small.png"
DEFAULT_SOCIAL_IMAGE = '/extra/social_large.jpg'

LINKS = (
    ('Home', '/'),
    ('📄 posts', '/category/post.html'),    
    ('writings', '/category/writing.html'),      
    ('memes', '/category/meme.html'),      
    ('musings', '/category/musing.html'),  
    ('documents', '/category/document.html'),  
    ('📘 books', '/category/book.html'),
    ('blackwood', '/blackwood.html'),
    ('☢️ medphys', '/tag/medical-physics.html'),
    ('🎬 film', '/category/film.html'),
    ('🖼️ pictures', '/category/picture.html'),  
    ('📸 snaps', '/category/snap.html'),    
    ('illustrations', '/category/illustrations.html'),
    ('💬 comics', '/category/comic.html'),      
    ('🗃️ Archive', '/archives.html'),
    ('😉 About', '/about.html'),
    ('🏷️ Tags', '/tags.html'),
    ('🟩 Esperanto', '/tag/esperanto-lingva.html'),    
    ('📶 RSS', '/feeds/all.rss.xml'),
    ('⚡ Atom', '/feeds/all.atom.xml'),
)

FEED_ALL_RSS = "feeds/all.rss.xml" 
FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_RSS = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
RSS_FEED_SUMMARY_ONLY = True
SUMMARY_MAX_LENGTH = 200

GITHUB_URL = "https://github.com/kingrpaul/"

ANALYTICS = r"""
<script type="text/javascript">
        (function (f, b) { if (!b.__SV) { var e, g, i, h; window.mixpanel = b; b._i = []; b.init = function (e, f, c) { function g(a, d) { var b = d.split("."); 2 == b.length && ((a = a[b[0]]), (d = b[1])); a[d] = function () { a.push([d].concat(Array.prototype.slice.call(arguments, 0))); }; } var a = b; "undefined" !== typeof c ? (a = b[c] = []) : (c = "mixpanel"); a.people = a.people || []; a.toString = function (a) { var d = "mixpanel"; "mixpanel" !== c && (d += "." + c); a || (d += " (stub)"); return d; }; a.people.toString = function () { return a.toString(1) + ".people (stub)"; }; i = "disable time_event track track_pageview track_links track_forms track_with_groups add_group set_group remove_group register register_once alias unregister identify name_tag set_config reset opt_in_tracking opt_out_tracking has_opted_in_tracking has_opted_out_tracking clear_opt_in_out_tracking start_batch_senders people.set people.set_once people.unset people.increment people.append people.union people.track_charge people.clear_charges people.delete_user people.remove".split( " "); for (h = 0; h < i.length; h++) g(a, i[h]); var j = "set set_once union unset remove delete".split(" "); a.get_group = function () { function b(c) { d[c] = function () { call2_args = arguments; call2 = [c].concat(Array.prototype.slice.call(call2_args, 0)); a.push([e, call2]); }; } for ( var d = {}, e = ["get_group"].concat( Array.prototype.slice.call(arguments, 0)), c = 0; c < j.length; c++) b(j[c]); return d; }; b._i.push([e, f, c]); }; b.__SV = 1.2; e = f.createElement("script"); e.type = "text/javascript"; e.async = !0; e.src = "undefined" !== typeof MIXPANEL_CUSTOM_LIB_URL ? MIXPANEL_CUSTOM_LIB_URL : "file:" === f.location.protocol && "//cdn.mxpnl.com/libs/mixpanel-2-latest.min.js".match(/^\/\//) ? "https://cdn.mxpnl.com/libs/mixpanel-2-latest.min.js" : "//cdn.mxpnl.com/libs/mixpanel-2-latest.min.js"; g = f.getElementsByTagName("script")[0]; g.parentNode.insertBefore(e, g); } })(document, window.mixpanel || []);
</script>
<script type="text/javascript">
        mixpanel.init("81e4cf01632c3345fc9cd44185211e60", {debug: true});
        mixpanel.track("Page Viewed");
</script>
"""

# OG_IMAGE = '/pages/images/landing/wave.png'  # Fallback image
# DEFAULT_TWITTER_IMAGE = '/pages/images/landing/wave.png'

# TWITTER_CARDS = True
TWITTER_USERNAME = "pairko49393"

DEFAULT_METADATA = {
    'og_image': 'https://raspberrypi.tailcd13e6.ts.net/extra/social_large.jpg',
    'og_image_type': 'image/jpeg',
    'og_type': 'website',  # Default type (use 'article' for blog posts)
    'twitter_card': 'summary_large_image',
    'twitter_creator': "@pairko49393",  # Add this to attribute the author    
}

SOCIAL = (
    ("github", "https://github.com/kingrpaul"),
    ("mastodon", "https://mastodon.social/@pairko"),
    ("telegram", "https://web.telegram.org/k/#@pairko_en"),
    ("discord", "https://discord.com/channels/@oncobot"),
    ("orcid", "https://orcid.org/my-orcid?orcid=0000-0001-6748-4538"),
)

DEFAULT_PAGINATION = 100
RELATIVE_URLS = True  # when developing
DISPLAY_PAGES_INDEX = True
SUMMARY_MAX_LENGTH = 50

IGNORE_FILES = ['working', 'drafts', 'py']

STATIC_PATHS = [
                'posts',
                'comic',
                'books',
                'film',                
                'memes',
                'snaps',                
                'writings',
                'musings',
                'documents',
                "extra",
                'icons',
                'illustrations',
                'pages',
                "pictures",
                "py",
                ]


# --- SEO plugin (pelican-seo) ---
SEO_REPORT = False
SEO_ENHANCER = True
SEO_ENHANCER_OPEN_GRAPH = True
SEO_ENHANCER_SITEMAP_URL = "https://raspberrypi.tailcd13e6.ts.net/sitemap.xml"
LOGO = "https://raspberrypi.tailcd13e6.ts.net/extra/avatar.jpg"

# ===========

REL_CANONICAL = False

ROBOTS = "index, follow"