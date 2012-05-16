# Web Crawler (TTS) #
Ruaridh Thomson

A simple web crawler in python, which works as follows:

* Find out which areas on the server are accessible to crawlers, and what restrictions are in place.
* Fetch web pages from the server using the HTTP 1.0/1.1 protocol.
* Extract a set of outgoing hyperlinks that occur between <!-- CONTENT -- > and <!-- /CONTENT -->
* Discard the links that point to external locations.
* Detect which of the extracted URLs have already been processed.
* Assign priorities to the URLs and insert them into the frontier queue. In this case, document names are numeric, and priority is given to high numbers.