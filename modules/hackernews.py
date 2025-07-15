# Hacker News aggregation
import requests

HACKERNEWS_TOP_URL = 'https://hacker-news.firebaseio.com/v0/topstories.json'
HACKERNEWS_ITEM_URL = 'https://hacker-news.firebaseio.com/v0/item/{}.json'


def fetch_hackernews_posts(cfg):
    """Fetch top posts from Hacker News using the official API for Daily Feed Digester."""
    post_limit = cfg.get('post_limit', 5)
    try:
        top_ids = requests.get(HACKERNEWS_TOP_URL, timeout=10).json()
    except Exception as e:
        return [{
            'source': 'HackerNews',
            'title': 'Error fetching top stories',
            'url': '',
            'summary': str(e)
        }]
    posts = []
    count = 0
    for story_id in top_ids:
        if count >= post_limit:
            break
        try:
            item = requests.get(
                HACKERNEWS_ITEM_URL.format(story_id), timeout=10
            ).json()
            if not item or item.get('type') != 'story':
                continue
            title = item.get('title', 'No Title')
            url = item.get('url', f'https://news.ycombinator.com/item?id={story_id}')
            summary = item.get('title', '')
            posts.append({
                'source': 'HackerNews',
                'title': title,
                'url': url,
                'summary': summary
            })
            count += 1
        except Exception as e:
            posts.append({
                'source': 'HackerNews',
                'title': f'Error fetching story {story_id}',
                'url': '',
                'summary': str(e)
            })
    return posts 