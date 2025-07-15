# Aggregator module for Daily Feed Digestor
from .reddit import fetch_reddit_posts
from .hackernews import fetch_hackernews_posts
from .rss import fetch_rss_posts


def aggregate_all_sources(config):
    """Aggregate posts from Reddit, Hacker News, and RSS feeds."""
    posts = []
    posts += fetch_reddit_posts(config.get('reddit', {}))
    posts += fetch_hackernews_posts(config.get('hackernews', {}))
    posts += fetch_rss_posts(config.get('rss', {}))
    return posts 