# Notes site

Ted's personal research notes, published as a public static site. This glossary fixes the names
used for the kinds of pages and material in the repo.

## Language

**Hub**:
The site's landing page, with one section per topic and a card per durable page or topic.
_Avoid_: home page, root index

**Topic**:
A subject Ted writes about, given its own directory once it has two or more pages.
_Avoid_: category, section

**Topic page**:
The list page that is a topic's landing page; the hub card for a topic points to it.
_Avoid_: topic index, overview page

**Content page**:
A page of written notes on a subject. Every content page carries a freshness stamp.
_Avoid_: doc, article, post

**List page**:
A page whose job is to link to other pages, such as the hub, a topic page, or a dated list. List
pages carry no freshness stamp.
_Avoid_: index (except as a filename)

**Dated entry**:
A content page about a point in time, named by date and listed newest first on a list page. It is
expected to go stale.
_Avoid_: log entry, post

**Raw input**:
Unedited source material (a transcript, research output, a screenshot) kept beside the content
page it feeds.
_Avoid_: source dump, attachment

**Freshness stamp**:
The "Contents last updated" date on a content page, bumped on real content changes only.
_Avoid_: last-modified date, timestamp
