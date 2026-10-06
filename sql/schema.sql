CREATE TABLE weekly_metrics (
    week_start TEXT NOT NULL,
    attendees INTEGER NOT NULL,
    first_timers INTEGER NOT NULL,
    returning_runners INTEGER NOT NULL,
    instagram_views INTEGER NOT NULL,
    instagram_engagement INTEGER NOT NULL,
    avg_temp_f REAL NOT NULL,
    event_type TEXT NOT NULL
);
