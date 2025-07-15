# Notifier for Daily Feed Digestor
import os
import sys


def send_digest(summary, config):
    """Send digest to CLI, optionally as Markdown file, and as Windows toast if enabled and on Windows. UK English."""
    notif_cfg = config.get('notification', {})
    if notif_cfg.get('enable_cli_output', True):
        print("\n[Daily Feed Digester] Today's Digest:\n" + "=" * 40)
        print(summary)
        print("\n" + "=" * 40)
    if notif_cfg.get('enable_windows_toast', False) and sys.platform.startswith('win'):
        try:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(
                "Daily Feed Digester",
                "Tech digest ready!",
                duration=10
            )
        except ImportError:
            print("[Daily Feed Digester] win10toast not installed or not supported on this platform.")
    if notif_cfg.get('save_markdown', False):
        out_path = notif_cfg.get('markdown_path', 'daily_digest.md')
        try:
            # Always overwrite the file with the latest digest
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(f"{summary}\n")
                f.flush()
            print(f"[Daily Feed Digester] Digest saved to {os.path.abspath(out_path)}")
        except Exception as e:
            print(f"[Daily Feed Digester] Error saving digest: {e}") 