# Summarizer for Daily Feed Digester
from collections import defaultdict


def summarise_posts(posts):
    """Group posts by source, number, and format as Markdown. Show errors separately. UK English. For Daily Feed Digester."""
    grouped = defaultdict(list)
    errors = []
    for p in posts:
        source = p.get('source', '')
        title = p.get('title', 'No Title')
        summary = p.get('summary', '')
        url = p.get('url', '')
        # Error detection: treat as error if title or summary contains 'Error'
        if 'error' in title.lower() or 'error' in summary.lower():
            errors.append(f"- **{title}** _(from {source})_\n  - {summary}")
        else:
            if source.startswith('Reddit/'):
                grouped['Reddit'].append((title, url, summary, source))
            elif source == 'HackerNews':
                grouped['Hacker News'].append((title, url, summary, source))
            else:
                # RSS: use the feed URL as the group name
                grouped[f"RSS: {source}"].append((title, url, summary, source))

    lines = []
    # Only add the heading if not already present
    heading = "# Daily Feed Digester"
    lines.append(heading + "\n")
    for section in ['Reddit', 'Hacker News'] + [k for k in grouped if k.startswith('RSS:')]:
        if section in grouped:
            lines.append(f"## {section}\n")
            for idx, (title, url, summary, source) in enumerate(grouped[section], 1):
                # Truncate summary to 140 chars
                summary = summary.replace('\n', ' ').strip()
                if len(summary) > 140:
                    summary = summary[:137] + '...'
                lines.append(f"{idx}. [{title}]({url})\n   {summary}\n")
    if errors:
        lines.append("## Errors\n")
        lines.extend(errors)
    # Remove duplicate heading if present
    output = '\n'.join(lines)
    while output.count(heading) > 1:
        output = output.replace(heading + "\n", "", 1)
    return output.strip() + "\n" 