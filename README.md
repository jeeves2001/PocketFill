# PocketFill

This is a _very_ simple Python script that searches specified RSS feeds (held in rssfeeds.py) for new articles and adds them to a SQLite database. 
Each article is then scored on the number of keywords (defined in keywords.py) and the score is added to the database. 
Articles with a score above 2 (currently hard coded, but easy to change) are then added to Pocket one at a time, each time the script is run. The database is then updated to reflect that this has been added to Pocket to prevent duplicates. 

The script has several dependancies: 
- [feedparser](https://pypi.python.org/pypi/feedparser)
- sqlite3
- [Pocket](https://github.com/felipecorrea/python-pocket)

ToDo: 
- [ ] Add a cleanup to remove old low scoring articles 
- [ ] Turn the minimum score into a variable
- [ ] Add tag in Pocket to show were the story came from 
