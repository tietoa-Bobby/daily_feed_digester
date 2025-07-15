# RSS aggregation using feedparser
import feedparser


def fetch_rss_posts(cfg):
    """Fetch top posts from configured RSS feeds using feedparser for Daily Feed Digester."""
    feeds = cfg.get('feeds', [])
    post_limit = cfg.get('post_limit', 5)
    posts = []
    for feed_url in feeds:
        try:
            d = feedparser.parse(feed_url)
            count = 0
            for entry in d.entries:
                if count >= post_limit:
                    break
                title = entry.get('title', 'No Title')
                url = entry.get('link', '')
                summary = entry.get('summary', '') or entry.get('description', '')
                posts.append({
                    'source': feed_url,
                    'title': title,
                    'url': url,
                    'summary': summary[:200].replace('\n', ' ')
                })
                count += 1
        except Exception as e:
            posts.append({
                'source': feed_url,
                'title': 'Error fetching feed',
                'url': '',
                'summary': str(e)
            })
    return posts 