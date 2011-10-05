# TTS Practical #
Ruaridh Thomson

## Specification ##
"Using Python, implement a web crawler with the agent name TTS. The general algorithm was outlined in lecture 2 and is covered in chapter 3 of the textbook. Your crawler should only fetch local links that occur in the body of the webpage after the <!-- CONTENT --> tag and before the <!-- /CONTENT --> tag. As a quick reminder, your implementation should involve the following steps:
* Find out which areas on the server are accessible to crawlers, and what restrictions are in place.
* Fetch web pages from the server using the HTTP 1.0/1.1 protocol.
* Extract a set of outgoing hyperlinks that occur between <!-- CONTENT --> and <!-- /CONTENT -->
* Discard the links that point to external locations.
* Detect which of the extracted URLs have already been processed.
* Assign priorities to the URLs and insert them into the frontier queue. In this case, document names are numeric, and you should give priority to high numbers."

## Notes ##
The following regular expression may be useful for matching tags: <[^>]*>
You should only follow anchor tags of the form: <a ...> ... </a>
You should not follow any links pointing outside of the Informatics network.

## Q&A ##
Q: As we are fetching all the pages from the same server is it important how do we assign the priorities in priority queue? 
A: Please set the priority to the numeric value of the page name.

Q: I'd like to know if the BeautifulSoup (python) qualifies as generic. 
A: Using BeautifulSoup as an HTML parser is fine. Please don't use extensions that combine it with URL fetching / link traversal.

Q: Is it possible to have an archive zip or rar, because it is faster to parse web pages in local? 
A: No. The whole point of the assessment is to work in a live environment. You should parse the pages as you crawl.

Q:Will you disclose the expected statistical details (number of links etc.)about the example pages so that we can test our crawlers against those. 
A: Uncertainty is a big part of this assessment, so no, we can't disclose the stats.

Q: Could you please give me some idea how many web pages should be fetched? 
A: No. Part of the assessment is working with an unknown target.

Q: Is python's htmllib allowed to use? 
A: Yes as long as no link-traversal extensions are used. Please keep in mind: if htmllib fails to parse a page, you should attempt to extract links from that page by other means.

Q: Should we follow the links that have the attribute "rel=nofollow"? 
A: Yes. The attribute is a not intended to prevent crawlers from gathering the content.