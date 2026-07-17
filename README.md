# Data Release Watcher

Checks a list of recurring datasets every day and pushes an alert to your
phone the moment new data is posted. 

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

Alerts go out via [ntfy.sh](https://ntfy.sh) -- a free push notification
service with no signup required.

## One-time setup 

### 1. Get a free FRED API key
Sign up at https://fred.stlouisfed.org/docs/api/api_key.html (instant,
no approval wait). This lets the script poll for new data.

### 2. Pick an ntfy.sh topic and subscribe to it on your phone
- Install the ntfy app ([iOS](https://apps.apple.com/us/app/ntfy/id1625396347) /
  [Android](https://play.google.com/store/apps/details?id=io.heckel.ntfy)),
  or use ntfy.sh in a browser.
- Pick a hard-to-guess topic name (anyone who knows the exact name can read
  your alerts, since there's no login) and subscribe to it in the app.
- Put that same topic name in `config.py` -> `NTFY_TOPIC`.

### 3. Put this project on GitHub
Create a new **private** repo and push these files to it. Being private
matters mainly so your `config.py` (with your topic name) isn't public --
though the FRED key itself should go in GitHub Secrets, not the code (next
step).

### 4. Add your FRED key as a GitHub Secret
In your repo: Settings -> Secrets and variables -> Actions -> New repository
secret.
- Name: `FRED_API_KEY`
- Value: the key from step 1

### 5. Enable GitHub Actions
The workflow in `.github/workflows/watch.yml` runs automatically once it's
pushed, on the schedule set there (default: daily at 13:00 UTC). You can
also trigger it manually any time from the "Actions" tab -> "Data release
watcher" -> "Run workflow" -- useful for testing.

## Running it locally (optional, for testing)

```bash
pip install -r requirements.txt
export FRED_API_KEY=your_key_here
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
- **Slack instead of phone push**: swap the `send_alert()` function to post
  to a Slack webhook instead of ntfy if that fits your workflow better.
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
