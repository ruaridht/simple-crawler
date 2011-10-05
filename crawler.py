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
import optparse
import heapq

from BeautifulSoup import BeautifulSoup
from cgi import escape

__version__   = "0.1"
__copyright__ = "Copyright (C) 2011 Ruaridh Thomson"
__license__   = "MIT"
__author__    = "Ruaridh Thomson"

USAGE     = "%prog [options] <url>"
VERSION   = "%prog v" + __version__
AGENT     = "TTS"
ROOT_URL  = "http://ir.inf.ed.ac.uk/tts/0786036/0786036.html"

# The crawler
class Crawler(object):
  def __init__(self, url):
    self.url       = url
    self.urlNetloc = urlparse.urlparse(url)[1]
    self.visited   = []
    self.seen      = []
    
    self.police    = robotparser.RobotFileParser()
    self.police.set_url("http://" + self.urlNetloc + "/robots.txt")
    
  def crawl(self):
    self.police.read()
    frontier   = []
    heapq.heappush(frontier,self.url)
    numCrawled = 0
    
    while len(frontier) > 0:
      seed = heapq.heappop(frontier)
      numCrawled += 1
      
      try:
        self.visited.append(seed)
        parse = Parser(seed)
        parse.parse()
        
        print "Seed: %s" % seed
        
        for link in parse.links:
          linkNetloc = urlparse.urlparse(link)[1]
          if (link not in self.seen) and (self.police.can_fetch(AGENT,link) and (linkNetloc == self.urlNetloc)):
            heapq.heappush(frontier,link)
            self.seen.append(link)
            print "Adding: %s" % link
      except Exception, e:
        print "ERROR: Can't process url '%s' (%s)" % (seed, e)
      
      print numCrawled
          

# Fetch a url and parse it for more urls.
class Parser(object):
	def __init__(self, url):
		self.url    = url
		self.links  = []  # To store the found urls
		self.opener = urllib2.build_opener()
		
	def _createURLRequest(self):
	  seed = self.url
	  try:
	    request = urllib2.Request(seed)
	    request.add_header("User-Agent", AGENT)
	  except IOError:
	    return None
	  return request
	
	def parse(self):
		request = self._createURLRequest()
		tags = []
		
		if self.opener:
		  try:
		    returnData = self.opener.open(request)
		    url        = returnData.geturl()
		    content    = unicode(returnData.read(), "utf-8", errors="replace")
		    soup       = BeautifulSoup(content)
		    tags       = soup('a')
		  except urllib2.HTTPError, error:
		    if error.code == 404:
		      print "ERROR: %s -> %s" % (error, error.url)
		    else:
		      print "ERROR: %s" % error
		  except urllib2.URLError, error:
		    print "ERROR: %s" % error
		  
		  for tag in tags:
		    href = tag.get("href")
		    if href is not None:
		      url = urlparse.urljoin(self.url, escape(href))
		      if url not in self.links:
		        self.links.append(url)
		
# Give ourselves the option of watching as it crawls.
def options():
    parser = optparse.OptionParser(usage=USAGE, version=VERSION)
    parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose", help="Print parsing information")

    opts, args = parser.parse_args()
    return opts

def main():    
    opts = options()
    
    #parse = Parser(ROOT_URL)
    #parse.parse()
    
    crawl = Crawler(ROOT_URL)
    crawl.crawl()
    
    if opts.verbose:
      for i, url in enumerate(parse.links):
        print "%d. %s" % (i, url)
    
    print "Goodbye."

if __name__ == "__main__":
    main()
