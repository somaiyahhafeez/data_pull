# Data Release Watcher

Checks a list of recurring datasets every day and pushes an alert to your
phone the moment new data is posted -- so you're never finding out about a
release two days late by accident.

## How it works

1. **Live-polled series** (`config.py` -> `TRACKED_SERIES`): pulled from the
   [FRED API](https://fred.stlouisfed.org/), which mirrors most BLS/Census
   economic series (CPI, wages, unemployment, housing, state-level data)
   behind one consistent, free API. The script remembers the last date it
   saw for each series; if a newer date appears, it's a new release and you
   get pinged.
2. **Calendar reminders** (`config.py` -> `CALENDAR_REMINDERS`): datasets that
   don't have a clean polling API (school report cards, FBI crime stats,
   agency-specific portals). You maintain a list of expected release dates
   and the script reminds you 2 days out and on the day.

Alerts go out as a single daily email via SMTP (works with Gmail, Outlook,
or any provider that supports app passwords).

## One-time setup (about 15 minutes)

### 1. Get a free FRED API key
Sign up at https://fred.stlouisfed.org/docs/api/api_key.html (instant,
no approval wait). This lets the script poll for new data.

### 2. Set up email sending
The simplest option is a Gmail account with an **app password** (a Google
account setting, not your normal password -- required because Gmail blocks
plain-password SMTP logins from scripts):

1. Go to https://myaccount.google.com/apppasswords (requires 2-Step
   Verification to be turned on for the account).
2. Create an app password for "Mail" / "Other (custom name)" -- call it
   something like "data-watcher".
3. Copy the 16-character password it gives you.

If you use Outlook, Yahoo, or another provider, the same idea applies --
search "[your provider] app password SMTP" for their exact steps, and note
their SMTP host/port (set via `SMTP_HOST`/`SMTP_PORT` env vars if not Gmail;
Gmail's defaults are already built in).

Then in `config.py`, set `EMAIL_TO` to whatever address you want alerts
delivered to (can be the same account or a different one).

### 3. Put this project on GitHub
Create a new **private** repo and push these files to it.

### 4. Add secrets to GitHub
In your repo: Settings -> Secrets and variables -> Actions -> New repository
secret. Add three:

| Secret name | Value |
|---|---|
| `FRED_API_KEY` | your key from step 1 |
| `SMTP_USER` | the sending email address (e.g. your Gmail address) |
| `SMTP_PASSWORD` | the app password from step 2 (NOT your real password) |

### 5. Enable GitHub Actions
The workflow in `.github/workflows/watch.yml` runs automatically once it's
pushed, on the schedule set there (default: daily at 13:00 UTC). You can
also trigger it manually any time from the "Actions" tab -> "Data release
watcher" -> "Run workflow" -- useful for testing.

## Running it locally (optional, for testing)

```bash
pip install -r requirements.txt
export FRED_API_KEY=your_key_here
export SMTP_USER=you@gmail.com
export SMTP_PASSWORD=your_app_password
python3 data_watcher.py
```

The first run will alert on *everything* tracked, since there's no prior
cache yet -- that's expected. After that, you'll only hear about genuinely
new data.

## Adding a new dataset to track

Open `config.py`:

- **For a FRED-covered series**: search the dataset name on
  https://fred.stlouisfed.org/, copy the series ID from the URL
  (e.g. `fred.stlouisfed.org/series/CPIAUCSL` -> `CPIAUCSL`), and add it to
  `TRACKED_SERIES` with a readable label.
- **For anything without a clean API** (state education dept, local FOIA
  tracker, agency-specific data): add an entry to `CALENDAR_REMINDERS` with
  the expected date. Update this manually as agencies confirm real dates.

## Extending this later

- **Auto-pull and rank**: once an alert fires for something like state
  unemployment, you could extend `data_watcher.py` to also pull all 50
  states' values and write a ranked CSV automatically -- turning the alert
  into a ready-made story starting point. Ask if you want this built out.
- **Slack instead of email**: swap the `send_email_digest()` function to post
  to a Slack webhook instead if that fits your workflow better.
- **FOIA tracker**: a similar cache-and-compare pattern works well for
  tracking FOIA request statuses/due dates -- happy to build that as a
  companion script.

## Files in this project

| File | Purpose |
|---|---|
| `config.py` | List of tracked series + calendar reminders + ntfy topic |
| `data_watcher.py` | Main script: polls FRED, checks calendar, sends alerts |
| `last_seen.json` | Auto-generated cache of the last-seen date per series |
| `requirements.txt` | Python dependencies |
| `.github/workflows/watch.yml` | Runs the script daily via GitHub Actions |
