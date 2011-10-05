#!/usr/bin/env python

"""
A simple web crawler

Ruaridh Thomson
s0786036

Practical 1 for Text Technologies
(code uses tabs instead of double-space)
"""

import re
import sys
import time
import math

import robotparser
import urllib2
import urlparse

from BeautifulSoup import BeautifulSoup

__version__   = "0.1"
__copyright__ = "Copyright (C) 2011 Ruaridh Thomson"
__license__   = "MIT"
__author__    = "Ruaridh Thomson"

USAGE     = "%prog [options] <url>"
VERSION   = "%prog v" + __version__
AGENT     = "TTS"
ROOT_URL  = "http://ir.inf.ed.ac.uk/tts/0786036/0786036.html"

class Parser(object):
	def __init__(self, url):
		self.url = url
		self.links = []
	
	def parse():
		

# Give ourselves the option of watching as it crawls.
def options():
    parser = optparse.OptionParser(usage=USAGE, version=VERSION)
    parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose", help="Print parsing information")

    opts, args = parser.parse_args()
    return opts

def main():    
    opts = options()
    
    parse = Parser(ROOT_URL)
    
    print "Goodbye."

if __name__ == "__main__":
    main()
