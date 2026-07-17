"""
Configuration for the data-release watcher.

TRACKED_SERIES: series polled automatically via the FRED API.
    Each entry: "label" -> "FRED series ID"
    FRED mirrors most BLS/Census series with one consistent API,
    so this is the easiest way to auto-detect "new data just posted."

    To find more series IDs: https://fred.stlouisfed.org/
    Search for a dataset, the series ID is in the URL, e.g.
    https://fred.stlouisfed.org/series/CPIAUCSL -> "CPIAUCSL"

CALENDAR_REMINDERS: releases that don't have a clean polling API
    (school report cards, FBI crime data, state-specific portals, etc.)
    You maintain these as known/expected dates and the script just
    reminds you a release is imminent. Update this list periodically
    from each agency's published release calendar.
"""

TRACKED_SERIES = {
    # --- National inflation & prices ---
    "CPI - All Items (national, SA)": "CPIAUCSL",
    "CPI - All Items Less Food & Energy (core)": "CPILFESL",

    # --- Regional CPI ---
    "CPI - Northeast Region": "CUUS0100SA0",
    "CPI - Midwest Region": "CUUS0200SA0",
    "CPI - South Region": "CUUS0300SA0",
    "CPI - West Region": "CUUS0400SA0",

    # --- Wages & earnings ---
    "Real Average Hourly Earnings (all employees)": "LES1252881600",
    "Average Hourly Earnings (all employees, private)": "CES0500000003",

    # --- Employment / unemployment ---
    "National Unemployment Rate": "UNRATE",
    "Total Nonfarm Payroll Employment": "PAYEMS",

    # --- Housing ---
    "Median Sales Price of Houses Sold (US)": "MSPUS",
    "Housing Starts": "HOUST",

    # --- Example state-level (duplicate this pattern per state you cover) ---
    # Find the right code by searching "unemployment rate [state]" on FRED.
    "Unemployment Rate - California": "CAUR",
    "Unemployment Rate - Texas": "TXUR",
    "Unemployment Rate - New York": "NYUR",
}

# NOTE: verify every series ID above at fred.stlouisfed.org before relying
# on it -- FRED series IDs occasionally get superseded/renamed, and it's
# worth confirming cadence (monthly/quarterly/annual) matches your expectations.

CALENDAR_REMINDERS = [
    {
        "label": "State Employment & Unemployment (BLS)",
        "date": "2026-07-21",
        "note": "Monthly. Good source for a 50-state ranking story.",
        "url": "https://www.bls.gov/schedule/news_release/empsit.htm",
    },
    {
        "label": "Import/Export Price Indexes (BLS)",
        "date": "2026-07-17",
        "note": "Monthly.",
        "url": "https://www.bls.gov/mxp/",
    },
    {
        "label": "CDC Provisional Overdose Death Counts",
        "date": "2026-08-01",  # update monthly - CDC posts on a rolling basis, no fixed day
        "note": "Rolling monthly update, check for revisions too, not just new months.",
        "url": "https://www.cdc.gov/nchs/nvss/vsrr/drug-overdose-data.htm",
    },
    {
        "label": "FBI Crime Data Explorer - quarterly update",
        "date": "2026-09-01",  # placeholder, FBI doesn't publish a fixed public calendar
        "note": "Check FBI CDE for actual cadence; often irregular.",
        "url": "https://cde.ucr.cjis.gov/",
    },
    # Add more as you identify recurring releases relevant to your beat.
]

# --- Alerting ---
# ntfy.sh is a free, no-signup push notification service. Pick any
# hard-to-guess topic name (it's public if someone knows the name) and
# install the ntfy app (iOS/Android) or use a browser, subscribed to
# that same topic, to receive alerts on your phone.
NTFY_TOPIC = "reach-data-watch-CHANGE-ME-1234"
