import praw
import json
from bs4 import BeautifulSoup
import os

#reddit scraping
reddit = praw.Reddit(
    client_id="l6-y4jUaYas_7w6R-7iISA",
    client_secret="NRGoShclae_uxg9OranycIro2udeTw",
    user_agent="collegeAppHelper"
)

subreddit_name = "ApplyingToCollege"
search_query = {"senior year timeline", "when to submit early decision", "last minute application tips", "how many schools to apply to"}
limit = 20

data = []

if(os.path.exists("../data.json")):
    with open(".venv/data.json", "r") as f:
        data = json.load(f)
else:
    data = []

for query in search_query:
    for post in reddit.subreddit(subreddit_name).search(search_query, limit=limit):
        post_data = {
            "title": post.title,
            "url": post.url,
            "score": post.score,
            "comments": []
        }

        post.comments.replace_more(limit=0) # remove placeholder comments
        for comment in post.comments[:10]:
            post_data["comments"].append(comment.body)

        data.append(post_data)

    with open(".venv/data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("finished " + query)


#blog scraping using beautiful soup

print("data saved to json file")
