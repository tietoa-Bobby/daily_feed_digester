# Reddit aggregation using PRAW
import praw


def fetch_reddit_posts(cfg):
    """Fetch top posts from configured subreddits using PRAW for Daily Feed Digester."""
    client_id = cfg.get('client_id')
    client_secret = cfg.get('client_secret')
    user_agent = cfg.get('user_agent', 'daily_feed_digester')
    subreddits = cfg.get('subreddits', [])
    post_limit = cfg.get('post_limit', 5)
    if not (client_id and client_secret and user_agent and subreddits):
        return []
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )
    posts = []
    for subreddit in subreddits:
        try:
            for submission in reddit.subreddit(subreddit).hot(limit=post_limit):
                if submission.stickied:
                    continue
                summary = (
                    submission.selftext[:200].replace('\n', ' ')
                    if submission.selftext else submission.title
                )
                posts.append({
                    'source': f'Reddit/{subreddit}',
                    'title': submission.title,
                    'url': submission.url,
                    'summary': summary
                })
        except Exception as e:
            posts.append({
                'source': f'Reddit/{subreddit}',
                'title': f'Error fetching subreddit: {subreddit}',
                'url': '',
                'summary': str(e)
            })
    return posts 