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
	  
	def _cropContent(self, content):
	  startIndex = content.find('<!-- CONTENT -->')
	  stopIndex = content.find('<!-- /CONTENT -->')
	  return content[startIndex:stopIndex]
	
	def parse(self, seenLinks, police, rootNetloc):
		request = self._createURLRequest()
		tags = []
		
		if self.opener:
		  try:
		    returnData = self.opener.open(request)
		    url        = returnData.geturl()
		    content    = unicode(returnData.read(), "utf-8", errors="replace")
		    # Crop the content (as outlined in the practical requirements)
		    # Note: This significantly reduces the number of URLs we process.
		    content    = self._cropContent(content)
		    soup       = BeautifulSoup(content)
		    tags       = soup('a') # Get only the a href links
		  except urllib2.HTTPError, error:
		    if error.code == 404:
		      print "%s : %s" % (error, error.url)
		    else:
		      print "%s" % error
		  except urllib2.URLError, error:
		    print "%s" % error
		  
		  for tag in tags:
		    href = tag.get("href")
		    if href is not None:
		      #url = urlparse.urljoin(self.url, escape(href))
		      url = urlparse.urljoin(self.url, href)
		      urlNetloc = urlparse.urlparse(url)[1]
		      if (url not in self.links) and (url not in seenLinks) and (urlNetloc==rootNetloc) and (police.can_fetch(AGENT, url)):
		        self.links.append(url)
		
# The crawler, managing urls found.
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
    frontier = []
    heapq.heappush(frontier,self.url)
    self.seen.append(self.url) # Avoids us visiting the ROOT_URL, should it appear again.
    
    while len(frontier) > 0:
      #seed = heapq.heappop(frontier)
      
      # The heap maintains the smallest at index 0.  Practical requirements
      # outline the page with the largest number has priority.  Fortunately,
      # heapq does most of the work here.
      seed = frontier[len(frontier)-1]
      frontier.remove(seed)
      
      try:
        self.visited.append(seed)
        
        # By passing the seen URLs we significantly reduce our processing time.
        parse = Parser(seed)
        parse.parse(self.seen) #, self.police, self.urlNetloc)
        
        """
        # Obviously, the number of links in the frontier is (num links seen)-(num visited)
        print "Seed: %s" % seed
        print "Frontier length %i" % len(frontier)
        print "Seen length: %i" % len(self.seen)
        print "Visited: %i" % len(self.visited)
        """
        for link in parse.links:
          linkNetloc = urlparse.urlparse(link)[1]
          
          # If we've seen the link we discard it.
          # If we are not allowed to fetch the link (via robots.txt) we discard it.
          # If the root of the link is outside the ROOT_URL domain we discard it.
          # If we've already visited it we can discard it.  This is not strictly necessary
          #   as the link will have been seen if we visited it.
          if ((link not in self.seen) and (self.police.can_fetch(AGENT,link)) and (linkNetloc == self.urlNetloc) and (link not in self.visited)):
            heapq.heappush(frontier,link)
            self.seen.append(link)
      except Exception, e:
        print "Can't crawl url '%s' (%s)" % (seed, e)
        
    
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
