-- 1. Monthly attendance trend
SELECT substr(week_start, 1, 7) AS month,
       ROUND(AVG(attendees), 1) AS avg_attendance,
       SUM(attendees) AS total_attendance,
       COUNT(*) AS weeks
FROM weekly_metrics
GROUP BY month
ORDER BY month;

-- 2. Event type comparison
SELECT event_type,
       ROUND(AVG(attendees), 1) AS avg_attendance,
       ROUND(AVG(first_timers * 1.0 / attendees), 3) AS avg_first_timer_share,
       COUNT(*) AS weeks
FROM weekly_metrics
GROUP BY event_type
ORDER BY avg_attendance DESC;

-- 3. First-timer share over time (quarterly)
SELECT CASE
           WHEN week_start < '2024-07-01' THEN '2024 H1'
           WHEN week_start < '2025-01-01' THEN '2024 H2'
           WHEN week_start < '2025-07-01' THEN '2025 H1'
           ELSE '2025 H2'
       END AS period,
       ROUND(AVG(first_timers * 1.0 / attendees), 3) AS avg_first_timer_share,
       ROUND(AVG(attendees), 1) AS avg_attendance
FROM weekly_metrics
GROUP BY period
ORDER BY period;

-- 4. Instagram engagement vs attendance (lagged one week)
SELECT ROUND(
    (COUNT(*) * SUM(a.instagram_engagement * b.attendees)
     - SUM(a.instagram_engagement) * SUM(b.attendees))
    / (SQRT(COUNT(*) * SUM(a.instagram_engagement * a.instagram_engagement)
            - SUM(a.instagram_engagement) * SUM(a.instagram_engagement))
       * SQRT(COUNT(*) * SUM(b.attendees * b.attendees)
              - SUM(b.attendees) * SUM(b.attendees))), 3
       ) AS engagement_to_next_week_corr
FROM weekly_metrics a
JOIN weekly_metrics b
  ON b.week_start = date(a.week_start, '+7 days');

-- 5. Hottest vs coolest week buckets
SELECT CASE
           WHEN avg_temp_f >= 85 THEN 'Hot (85F+)'
           WHEN avg_temp_f >= 70 THEN 'Warm (70-85F)'
           ELSE 'Mild (<70F)'
       END AS heat_bucket,
       ROUND(AVG(attendees), 1) AS avg_attendance,
       ROUND(AVG(avg_temp_f), 1) AS avg_temp,
       COUNT(*) AS weeks
FROM weekly_metrics
GROUP BY heat_bucket
ORDER BY avg_temp;

-- 6. Brand collab lift vs regular weeks
SELECT ROUND(
       (SELECT AVG(attendees) FROM weekly_metrics WHERE event_type = 'Brand Collab')
       - (SELECT AVG(attendees) FROM weekly_metrics WHERE event_type = 'Regular')
       , 1) AS collab_lift_runners,
       ROUND(
       (SELECT AVG(attendees) FROM weekly_metrics WHERE event_type = 'Brand Collab')
       / (SELECT AVG(attendees) FROM weekly_metrics WHERE event_type = 'Regular')
       - 1, 3) AS collab_lift_pct;
