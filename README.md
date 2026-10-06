# run-club-growth
README
Green House Run Club: Growth Analytics
I co-founded a run club in Waco, Texas. It went from about 30 people a week to about 70. I wanted to know what was actually driving that, so I tracked 91 weeks of data and ran the numbers.
Key Findings
The club more than doubled. First 13 weeks averaged 29.3 runners. Last 13 averaged 70.2. That's +139.4% from Jan 2024 to Sep 2025.
Brand collabs are the cheat code. Weeks we ran with Red Bull or Prime averaged 95.5 runners vs 51.9 on a regular week. That's +84%, roughly 44 extra people just for having a brand attached. Our one-year anniversary run pulled 124, still the biggest week on record.
Texas heat is real. Waco summers are brutal and it shows in the numbers. Once the weekly average crosses 85°F, turnout falls off a cliff. After stripping out the growth trend, hot weeks run about 14 runners light compared to mild weeks. August is our worst month (45 avg); December is our best (80) — mild winter weather plus the anniversary bump.
Instagram actually moves the needle. Same-week engagement correlates with attendance at 0.89, and last week's engagement predicts this week's turnout at 0.68. First-timers hold steady at ~30% of the crowd, and a big first-timer week means more returning runners the next week (0.69). Post, people show up, some stick around.
Tools
Python (pandas), SQL (SQLite), Tableau, Power BI. Data is synthetic but realistic, seeded for reproducibility.
Project Structure
run-club-growth/
  data/
    generate_data.py      # seeded generator -> weekly_metrics.csv (91 weeks)
    weekly_metrics.csv    # week_start, attendees, first_timers, returning_runners,
                          # instagram_views, instagram_engagement, avg_temp_f, event_type
  python/
    club_analysis.py      # growth, seasonality, retention, social, collab lift
  sql/
    schema.sql            # CREATE TABLE (SQLite)
    analysis_queries.sql  # 6 SELECT queries: monthly trend, event mix, first-timer
                          # share, engagement lag, heat buckets, collab lift
  tableau/build_guide.md  # step-by-step dashboard spec (~1 hr build)
  powerbi/build_guide.md  # step-by-step dashboard spec (~1 hr build)
​
How to Run
pip install -r requirements.txt

# regenerate the data
python3 data/generate_data.py

# run the analysis
python3 python/club_analysis.py

# load into SQLite and run the queries
sqlite3 club.db < sql/schema.sql
sqlite3 club.db ".mode csv" ".import --skip 1 data/weekly_metrics.csv weekly_metrics"
sqlite3 club.db < sql/analysis_queries.sql
​
Note: Jan 2024 to Sep 2025 is 91 weeks. The data covers the full period at true weekly cadence.
