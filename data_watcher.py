#!/usr/bin/env python3
"""
data_watcher.py

Checks tracked datasets for new releases and sends a push alert when
something new shows up. Designed to run once a day via cron or
GitHub Actions.

Requires:
    pip install requests
    A free FRED API key: https://fred.stlouisfed.org/docs/api/api_key.html
    Set it as an environment variable: FRED_API_KEY

Usage:
    FRED_API_KEY=xxxx python3 data_watcher.py
"""

import json
import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional

import requests

from config import TRACKED_SERIES, CALENDAR_REMINDERS, NTFY_TOPIC

CACHE_FILE = Path(__file__).parent / "last_seen.json"
FRED_API_KEY = os.environ.get("FRED_API_KEY", "")
FRED_URL = "https://api.stlouisfed.org/fred/series/observations"


def load_cache() -> dict:
    if CACHE_FILE.exists():
        return json.loads(CACHE_FILE.read_text())
    return {}


def save_cache(cache: dict) -> None:
    CACHE_FILE.write_text(json.dumps(cache, indent=2))


def get_latest_observation(series_id: str) -> Optional[dict]:
    """Return the most recent observation for a FRED series, or None on failure."""
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 1,
    }
    try:
        resp = requests.get(FRED_URL, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        obs = data.get("observations", [])
        return obs[0] if obs else None
    except requests.RequestException as e:
        print(f"  [error] fetching {series_id}: {e}", file=sys.stderr)
        return None


def send_alert(message: str) -> None:
    """Send a push notification via ntfy.sh. Also prints to stdout as a fallback."""
    print(f"[ALERT] {message}")
    if not NTFY_TOPIC or "CHANGE-ME" in NTFY_TOPIC:
        print("  (ntfy topic not configured -- skipping push notification)")
        return
    try:
        requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=message.encode("utf-8"),
            headers={"Title": "New dataset released"},
            timeout=10,
        )
    except requests.RequestException as e:
        print(f"  [error] sending push notification: {e}", file=sys.stderr)


def check_tracked_series() -> None:
    if not FRED_API_KEY:
        print("FRED_API_KEY not set -- skipping live series checks.", file=sys.stderr)
        return

    cache = load_cache()
    changed = False

    for label, series_id in TRACKED_SERIES.items():
        print(f"Checking: {label} ({series_id})")
        latest = get_latest_observation(series_id)
        if latest is None:
            continue

        latest_date = latest.get("date")
        latest_value = latest.get("value")
        previous_date = cache.get(series_id, {}).get("date")

        if latest_date != previous_date:
            send_alert(
                f"{label}: new data for {latest_date} (value: {latest_value}). "
                f"https://fred.stlouisfed.org/series/{series_id}"
            )
            cache[series_id] = {"date": latest_date, "value": latest_value}
            changed = True

    if changed:
        save_cache(cache)
    else:
        print("No new data since last check.")


def check_calendar_reminders() -> None:
    today = date.today()
    lookahead = today + timedelta(days=2)  # heads-up 2 days before

    for item in CALENDAR_REMINDERS:
        release_date = datetime.strptime(item["date"], "%Y-%m-%d").date()
        if today <= release_date <= lookahead:
            days_out = (release_date - today).days
            when = "today" if days_out == 0 else f"in {days_out} day(s)"
            send_alert(
                f"Reminder: {item['label']} is scheduled {when} "
                f"({item['date']}). {item['note']} {item['url']}"
            )


def main() -> None:
    print(f"=== Data watcher run: {datetime.now().isoformat()} ===")
    check_tracked_series()
    check_calendar_reminders()


if __name__ == "__main__":
    main()
