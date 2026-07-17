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

    # --- Regional CPI (monthly, not seasonally adjusted) ---
    "CPI - Northeast Region": "CUUR0100SA0",
    "CPI - Midwest Region": "CUUR0200SA0",
    "CPI - South Region": "CUUR0300SA0",
    "CPI - West Region": "CUUR0400SA0",

    # --- Wages & earnings ---
    # Note: "Real" (inflation-adjusted) average hourly earnings isn't its own
    # persistent FRED series -- BLS calculates it monthly (nominal wages
    # deflated by CPI-W) in its Real Earnings release. Tracked as a calendar
    # reminder below instead. This series is the nominal (non-inflation-
    # adjusted) figure, which IS a clean live-polled series:
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
        "label": "Real Earnings (BLS) - inflation-adjusted wages",
        "date": "2026-08-12",
        "note": "Monthly. Confirmed next release date from BLS. Covers real "
                "average hourly/weekly earnings, all employees and "
                "production/nonsupervisory.",
        "url": "https://www.bls.gov/news.release/realer.nr0.htm",
    },
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
# Alerts are sent as a single daily email digest via SMTP. The sending
# account's credentials come from environment variables (GitHub Secrets:
# SMTP_USER, SMTP_PASSWORD) -- never put a real password in this file.
# Just set the address you want alerts sent TO:
EMAIL_TO = "sh4625@columbia.edu"  # CHANGE-ME: your real inbox
