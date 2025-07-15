# Daily Feed Digester

[![MIT Licence](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)

A Python tool that aggregates top daily tech news from Reddit, Hacker News, and tech RSS feeds, summarises them, and delivers a daily digest via command line and Markdown file. Highly configurable, cross-platform, and easy to use.

## Features
- Aggregates tech news from:
  - Reddit tech subreddits (via PRAW)
  - Hacker News (API)
  - Tech RSS feeds (via feedparser)
- Summarises top daily posts as Markdown bullet points, grouped and numbered by source
- Delivers digest via command line and optional Markdown file
- Runs automatically at a fixed daily time (APScheduler)
- Configurable feeds, schedule, and notification options via YAML config file
- No history stored; fresh digest daily
- Minimal UI: config via file or CLI, output as Markdown
- Cross-platform (Windows, macOS, Linux)

## Setup
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy and edit the example config file:
   ```bash
   cp config.example.yaml config.yaml
   # Edit config.yaml as needed (add your Reddit API credentials)
   ```

## Usage
Run manually:
```bash
python main.py --config config.yaml
```

### Immediate Test Run
To run the digest immediately (for testing), use:
```bash
python main.py --config config.yaml --run-now
```

## Configuration
Edit `config.yaml` to set up feeds, schedule, and notification settings. See `config.example.yaml` for details.

Example notification section:
```yaml
notification:
  enable_cli_output: true
  save_markdown: true
  markdown_path: daily_digest.md
```

## Output Format
- Posts are grouped by source (Reddit, Hacker News, each RSS feed)
- Each group is numbered and clearly separated
- Errors (e.g., Reddit authentication) are shown in a separate section

## Troubleshooting
- **Reddit 401 Error:** Check your Reddit API credentials in `config.yaml`. Ensure your Reddit app is set up for "script" use and the credentials are correct. You may need to reauthorise your app or check for typos.
- **Missing config.yaml:** Copy `config.example.yaml` to `config.yaml` and edit as needed.
- **No output:** Ensure your feeds are correct and you have internet access.

## Scheduling
- Uses APScheduler to run daily at the configured time.
- To run at system startup or on a schedule outside Python, use your OS's task scheduler to call `python main.py --config config.yaml --run-now`.

## Licence
MIT 