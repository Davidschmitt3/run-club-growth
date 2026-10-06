"""Generate synthetic weekly Green House Run Club data (Jan 2024 - Sep 2025)."""
import csv
import random
from datetime import date, timedelta

random.seed(42)

START = date(2024, 1, 1)
WEEKS = 91  # Jan 1 2024 -> ~Sep 2025

# Waco, Texas weekly temps (F): mild winters, brutal Jun-Aug
SEASON_TEMP = {1: 55, 2: 58, 3: 66, 4: 74, 5: 82, 6: 90, 7: 95,
               8: 96, 9: 88, 10: 77, 11: 65, 12: 56}

rows = []
for w in range(WEEKS):
    week_start = START + timedelta(days=7 * w)
    month = week_start.month

    # Steady growth: trend index 0 -> 1 across the whole period
    trend = w / (WEEKS - 1)
    base = 25 + trend * 65  # ~25 up to ~90

    # Texas summer heat dip: brutal weeks lose attendees
    avg_temp = SEASON_TEMP[month] + random.gauss(0, 2.5)
    heat_penalty = 0
    if avg_temp > 85:
        heat_penalty = (avg_temp - 85) * 2.0

    # Event schedule (hand-picked for realism)
    event_type = "Regular"
    # Brand collabs scattered through the period
    collab_weeks = {30, 52, 66, 78}
    special_weeks = {51}  # 1-year anniversary run, late 2024
    if w in collab_weeks:
        event_type = "Brand Collab"
    elif w in special_weeks:
        event_type = "Special Event"

    event_lift = {"Regular": 0, "Brand Collab": 38, "Special Event": 55}[event_type]

    attendees = max(8, round(base - heat_penalty + event_lift + random.gauss(0, 5)))
    returning = round(attendees * random.uniform(0.62, 0.78))
    first_timers = attendees - returning

    # Instagram: engagement scales with attendance, plus noise; collabs overperform
    views = max(300, round(attendees * random.uniform(28, 55)))
    engagement = max(15, round(attendees * random.uniform(2.2, 4.2)
                               + (25 if event_type == "Brand Collab" else 0)
                               + random.gauss(0, 12)))

    rows.append({
        "week_start": week_start.isoformat(),
        "attendees": attendees,
        "first_timers": first_timers,
        "returning_runners": returning,
        "instagram_views": views,
        "instagram_engagement": engagement,
        "avg_temp_f": round(avg_temp, 1),
        "event_type": event_type,
    })

with open("data/weekly_metrics.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} weekly rows "
      f"({rows[0]['week_start']} -> {rows[-1]['week_start']})")
