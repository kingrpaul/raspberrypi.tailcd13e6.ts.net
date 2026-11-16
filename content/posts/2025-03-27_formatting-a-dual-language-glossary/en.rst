===================================
Formatting a Dual-Language Glossary
===================================
:date: 2025-03-27
:modified: 2026-10-08
:author: pairko
:category: post
:summary: How to format a dual-language glossary for use with Standard Ebooks tools.
:description: How to format a dual-language glossary for use with Standard Ebooks tools.
:tags: esperanto, how-to
:slug: 2025-03-27_formatting-a-dual-language-glossary
:lang: en
:og_image: https://raspberrypi.tailcd13e6.ts.net/posts/2025-03-27_formatting-a-dual-language-glossary/social.jpg

**Esperanto-English Using Standard Ebooks Tools**

An e-book glossary entry ordinarily consists of three parts:

1. Term to be defined: stored as the dt-term in a dl-description-list, contained in glossary.txt.
2. Definition: stored as the dd-description in a dl-description-list.
3. Synonyms and variations of each term, connecting them to that term: stored as a search-key-map in glossary-search-key-map.xml.

In practice, a glossary is used by a user looking up a word in the text, when this word is encountered. Also, it is significant that the glossary-search-key-map is not well-supported by existing readers and the glossary is intended to work around this limitation, providing good function, while also functioning properly when the support is widely available. These goals are accomplished by using the following formats.

text/glossary.xhtml
===================

The glossary file contains a description list with one dt-dd pair per term, in alphabetical order. Using the example, for each entry, make the following replacements.
    
1. Within the term:
        
  * Replace *Abdul Alhazred* with the *English* term being described.
  * Replace *abdul-alhazred* as the id with the lower-case, dash-separated, no-diacritics version of this term.
        
2. Within the description:
        
  * Replace *Abdul-Alhazredo* inside the <strong> element with the Esperanto transation of the term.
  * After the <strong>, colon, and space; provide a brief, simple, and consistently arranged Esperanto definition of the term. Do not include any links.
  * In the second paragraph, after the <strong> list all words, separated by comma, in either language which correspond to this definition. Exclude the two words already given. Include variations in tense, number, possessive, etc. that appear in the work and consider include alternate spellings found in Wikipedia. Do not tag these words to indicate their language.

.. code-block:: html

    <?xml version="1.0" encoding="utf-8"?>
    <html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" epub:prefix="z3998: http://www.daisy.org/z3998/2012/vocab/structure/, se: https://standardebooks.org/vocab/1.0" xml:lang="eo">
        <head>
            <title>Glosaro</title>
            <link href="../css/core.css" rel="stylesheet" type="text/css"/>
            <link href="../css/local.css" rel="stylesheet" type="text/css"/>
        </head>
        <body epub:type="backmatter">
            <section id="glossary" epub:type="glossary">
                <h2 epub:type="title">Glosaro</h2>
                <dl>
                    <dt id="abdul-alhazred" epub:type="glossterm" xml:lang="en-US">
                        <dfn>Abdul Alhazred</dfn>
                    </dt>
                    <dd epub:type="glossdef">
                        <p><strong>Abdul-Alhazredo</strong>: Verkisto de la Nekronomiko.</p>
                        <p><span xml:lang="en-US">Also:</span> Alhazred.</p>
                    </dd>
                </dl>
            </section>
        </body>
    </html>
    
epub/glossary-search-key-map.xml
================================

For each term, the key-map contains a single element that provides a describes the relationship between the main glossary term
and all other words mapped to that term.

    
1. Within each search-key-group:
        
 * Replace *abdul-alhazred* with the corresponding id from the glossary file.
 * Copy one <match> item for each synonym. There will be at least two. The original English and
                original Esperanto will be the first two and the list will include all of the "Also" elements from the
                corresponding glossary item.
        
2. Within match:
        
 * For the title, replace *Abdul Alhazred* with the English from the definition term. All these will
                be the same.
 * For the values, enter all of the available synonyms from the glossary.
        
    

.. code-block:: html

        <?xml version="1.0" encoding="utf-8"?>
        <search-key-map xmlns="http://www.idpf.org/2007/ops" xml:lang="en">
            <search-key-group href="text/glossary.xhtml#abdul-alhazred">
                <match title="Abdul Alhazred" value="Abdul Alhazred"/>
                <match title="Abdul Alhazred" value="Abdul-Alhazredo"/>
                <match title="Abdul Alhazred" value="Alhazred"/>
            </search-key-group>
        </search-key-map>        

Note that the key-map is not yet well supported by ebook readers. The "Also" line in the glossary is intended as
a workaround. These items are intended to be hidden, though the reading device may present them anyway. But by listing here, the reader should bring up the glossary item during search.

css/local.css
=============

The first three items here are SE styles, meant to show the glossary items in a good way. The remaining items
are meant to make the English and Esperanto words easy to distinguish during search and in the final document. It is meant to hide the extra
synonyms but present them well in a a helpful way if the reader-device does display them.

.. code-block:: html

    # SE Part
    dl{
        margin: 1em 0;
    }
    
    dd{
        margin-left: 40px;
    }

    dd + dt{
        margin-top: 1em;
    }

    # Dual-Language Part
    dl dd p:nth-of-type(odd) strong{
        font-weight: bold;
    }
            
    dl dd p:nth-of-type(2){
        display: none;
        font-size: smaller;
        font-style: italic;
        font-variant: small-caps;
        text-indent: 0;
    }
    
    dl dd p:nth-of-type(even) span:first-of-type{
        font-size: 1em;
        margin-right: 1em;
    }
    

