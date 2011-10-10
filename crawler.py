#!/usr/bin/env python

"""
A simple web crawler

Ruaridh Thomson
s0786036

Practical 1 for Text Technologies
(code uses tabs instead of double-space)
"""

import re
import math
import time

import robotparser
import urllib2
import urlparse
import heapq

from BeautifulSoup import BeautifulSoup
#from cgi import escape

AGENT     = "TTS"
ROOT_URL  = "http://ir.inf.ed.ac.uk/tts/0786036/0786036.html"  

# Fetch a url and parse it for more urls.
class Parser(object):
	def __init__(self, url):
		self.url          = url
		self.links        = []  # To store the found urls
		self.opener       = urllib2.build_opener()
		self.numProcessed = 0
		self.numDupes     = 0
		
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
	
	def parse(self, seenLinks):
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
		    print "%s : %s" % (error, error.url)
		    return 0
		  
		  for tag in tags:
		    href = tag.get("href")
		    if href is not None:
		      #url = urlparse.urljoin(self.url, escape(href))
		      url = urlparse.urljoin(self.url, href)
		      self.numProcessed += 1
		      if (url in seenLinks):
		        self.numDupes += 1
		      
		      if (url not in self.links) and (url not in seenLinks):
		        self.links.append(url)
		  return 1
		
# The crawler, managing urls found.
class Crawler(object):
  def __init__(self, url):
    self.url       = url
    self.urlNetloc = urlparse.urlparse(url)[1]
    self.visited   = []
    self.seen      = []
    self.errors    = []
    
    self.police    = robotparser.RobotFileParser()
    self.police.set_url("http://" + self.urlNetloc + "/robots.txt")
    
    self.totalProcessed = 0
    self.numPoliced     = 0
    self.numOutDomain   = 0
    self.totalDupes     = 0
    
  def crawl(self):
    self.police.read()
    frontier = []
    heapq.heappush(frontier,self.url)
    self.seen.append(self.url) # Avoids us visiting the ROOT_URL, should it appear again.
    
    startTime = time.time()
    timeMult = 1
    
    while len(frontier) > 0:
      # The heap maintains the smallest at index 0.  Practical requirements
      # outline the page with the largest number has priority.  Fortunately,
      # heapq does most of the work here.
      seed = frontier[len(frontier)-1]
      frontier.remove(seed)
      
      try:
        # By passing the seen URLs we significantly reduce our processing time.
        parse = Parser(seed)
        if not(parse.parse(self.seen)): #self.police
          continue
        
        self.totalProcessed += parse.numProcessed
        self.totalDupes     += parse.numDupes
        self.visited.append(seed)
        
        # Obviously, the number of links in the frontier is (num links seen)-(num visited)
        #print "Seed: %s" % seed
        #print "Frontier length %i" % len(frontier)
        #print "Seen length: %i" % len(self.seen)
        #print "Visited: %i" % len(self.visited)
        
        for link in parse.links:
          linkNetloc = urlparse.urlparse(link)[1]
          
          # If we've seen the link we discard it.
          # If we are not allowed to fetch the link (via robots.txt) we discard it.
          # If the root of the link is outside the ROOT_URL domain we discard it.
          # If we've already visited it we can discard it.  This is not strictly necessary
          #   as the link will have been seen if we visited it.
          if not (self.police.can_fetch(AGENT,link)):
            #print "Banned by robots.txt: %s" % link
            self.numPoliced += 1
          
          if not (linkNetloc == self.urlNetloc):
            #print "Link points out of domain: %s" % link
            self.numOutDomain += 1
          
          if ((link not in self.seen) and (self.police.can_fetch(AGENT,link)) and (linkNetloc == self.urlNetloc) and (link not in self.visited)):
            heapq.heappush(frontier,link)
            self.seen.append(link)
      except Exception, e:
        print "Can't crawl '%s' (%s)" % (seed, e)
        
      spotTime = time.time()
      elapsedTime = spotTime-startTime
      if (elapsedTime>(timeMult*2)):
        print "Time: %i" % elapsedTime
        print "Dupes: %i" % self.totalDupes
        timeMult += 1

def main():
    crawl = Crawler(ROOT_URL)
    crawl.crawl()
    
    print "Total processed: %i" % crawl.totalProcessed
    print "Total policed: %i" % crawl.numPoliced
    print "Num out of domain: %i" % crawl.numOutDomain
    print "Num of duplicates: %i" % crawl.totalDupes
    
    print "Goodbye."

if __name__ == "__main__":
    main()
