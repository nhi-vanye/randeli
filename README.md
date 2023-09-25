Randeli
=======

Augment PDFs to help make them easier to read and understand for
people with ADD/ADHD.

This is primarily targeted at processing academic papers and patents.

Randeli is currently using the commercial Apryse PDF SDK, a license
key is required. A free demo license is available at https://dev.apryse.com


Terminology
-----------

"Bionic Reading" is a trademark of Bionic Reading AG aka bionic-reading.com

`randeli` is has been developed independently of any bionic-reading.com
products or non-public informatin and any patents that "Bionic
Reading" hold are not applicable where this code was developed (UK,
USA). The patents that bionic-reading.com filed in the UK and USA
were withdrawn.

To avoid trademark infringement, randeli will use the term "augmented".


A PDF can be augmented using alternate "styles"

The original "Bionic Reading" approach use bold fonts - in randeli
terminology "strong-text".

For OCR parsed PDFs (and also as a personal preference for well formed
PDFs), `randeli` also supports a "strong-box" style that draws a
colored box over the initial letters of a word.


Roadmap
-------

Initially randeli is being developed as a python-based CLI. But a
web-based UI is on the short term roadmap.

Earlier versions were developed in Go and C++, but those have been
postponed to get the first release out.

As are usability features to help users find the best "augmentation" styles for them.

I think there is also scope to add audible augmentation as well.




Augmenting Patents
------------------

PDFs downloaded from http://patents.google.com may have alreay been
regnerated compared to the original national patent office (i.e.
USPTO).

More success has been obtained using PDFs downloaded idirectly from USPTO
and using `randeli's` built-in OCR.


PDF Background
==============

PDF is an unstructured format that is a stream of binary (optionally
compressed) elements. An element can be an image, text etc.

Text can be a single character, word or line.

Some PDFs are the result of scanning a paper or other PDF - so any
text has been rendered into an image.

Well formed PDFs
----------------

If the PDF was created from LaTeX or other document processor (i.e.
Word) then reasonable results should be obtained using

    `randeli augment --read=PDF --write-into=DIR`

(LaTeX and Word both create well structured PDF and typically use
standard fonts which makes it easy to enbolden automatically.

PDFs generated from XeLaTeX are still a WIP as they use a different
font format in the PDF (UTF-8 vs UTF-32).

If the input document uses custom fonts that are not installed on
the system running `randeli` then the font used to strongify the
characters will use a fallback font and it may be too distracting
when compared to the rest of the document. In this case you may
want either load the fonts onto the system and re-run `randeli map-fonts`
or use `randeli augment --override 'policy.use_strong_text=False'
--override 'policy.use_strong_box=True'`.

Scanned PDFs
------------

Scanned PDFs have no information to order to markup the text (no
font information) so we need to use OCR to extract text from images
and then add highlighted boxes at the appropriate position on the
page using

    `randeli augment --read=PDF --write-to=DIR --ocr`

The default OCR assumes that the whole document has been scanned
so performs OCR on the full page. If pages contain a mix of well-formed
text and (in-line) images to be be be OCR'ed, then use `--ocr-mode
element` (rather than the default `--ocr-mode page`).

Font Map
--------

In order to bolden the text in the output PDF using the same fonts
as the rest of the PDF we need to know what fonts are available on
the system. 

If you are expecting to read TeX/LaTeX generated PDFs, you probably
want to load the CMU fonts into your Font Library. The license for
the LaTeX standard Compuer Modern fonts requires changing the name
when the format (Type1 (TTF) vs TeX) is changed. We want the
Type1 version as PDF supports that type natively.

https://www.fontsquirrel.com/fonts/computer-modern

Another good set is the "Latin Modern Roman" fonts.


Getting Started
===============


1) Create the inital configuration file and download required Apryse libraries

```
randeli bootstrap --download
```

2) Configure the Apryse token - this is required to use the PDF
parsing library. Visit https://dev.apryse.com/ to get a key

```
randeli config set --key apryse.token --value "demo:1684698886167:....."
```

3) (optional) Set your preferred fallback font.

A lot of my papers are from LaTeX so prefer to use the Computer Modern font as a fallback.

```
randeli config set --key policy.fallback-font --value "CMU Serif"
```

4) (one off) Index all the fonts on your system - required before augment any PDFs (technically only required before using font-based augmentation,  but do it now before you forget)

``` 
randeli map-fonts --update-config
```


Randeli Usage
=============


```
 ] randeli
Usage: randeli [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

COMMANDS:
     augment - Write an augmented PDF
   bootstrap - Initialize randeli configuration
      config - Read and Write configuration values
     inspect - Read a PDF and report on its structure
   map-fonts - Create fonts.map from installed fonts

For additional help on a command use

    `randeli <CMD> --help`
or
    `randeli <CMD> --hints`
```


```
 ] randeli --help
Usage: randeli [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --verbose INTEGER     Set system-wide verbosity
  --devel                   Run in development mode (additional logging)
  --cfg PATH                Path to configuration file
  --backend [apryse]        Select backend PDF library
  --apryse-token TOKEN      API Token for Apryse backend
  --font-map-file FILE      Load font map from FILE
  --log-level LOGGER=LEVEL  Override logging level for given logger
  --help                    Show this message and exit.
```


```
 ] randeli bootstrap --help
Usage: randeli bootstrap [OPTIONS]

  Initialize randeli configuration

Options:
  --download  Download 3rd party components
  --help      Show this message and exit.
```


