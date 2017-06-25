# Pull feeds and save new articles to DB

import feedparser
import sqlite3
# import pocket

from rssfeeds import my_feeds
from keywords import my_keywords
from secrets import *
from pocket import Pocket

keywords = my_keywords

# Review feeds, score and add to DB

# Review feeds
for feeds in my_feeds:
    feed = feedparser.parse(feeds)
    for entry in feed['entries']:
        t = entry["title"]
        l = entry["link"]
        ident = entry["id"]
        su = entry["summary"]
# Score feed elements based on keywords
        entry_score = 0
        for keyword in keywords:
            entry_score += entry['summary'].count(keyword)
        sc = entry_score
# Connect to DB and add unique items to the list
        conn = sqlite3.Connection("Pocket.db")
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS results(
                    ID UNIQUE, Title TEXT, Link TEXT, Summary TEXT, Score INTEGER, Pocket INTEGER)
                 ''')
        c.execute('''INSERT OR IGNORE INTO results VALUES (?, ?, ?, ?, ?, 0);
                ''', (ident, t, l, su, sc))
        conn.commit()
        conn.close()
# Check score and add high scores to Pocket
p = Pocket(
    consumer_key=p_c_key,
    access_token=p_a_token
)
conn = sqlite3.Connection("Pocket.db")
c = conn.cursor()
c.execute('SELECT Link FROM results WHERE Score > 2 AND Pocket = 0 LIMIT 1')
all_rows = c.fetchall()
try:
    add = all_rows[0][0]
    p.add(add, tags="Amber")
except IndexError:
    print("No new articles meet the threshold")
c.execute('UPDATE results SET Pocket = 1 WHERE (Score > 2 AND Pocket = 0) LIMIT 1')
conn.commit()
conn.close
