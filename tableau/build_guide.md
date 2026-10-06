# Tableau Build Guide: Green House Run Club Dashboard

Source file: `data/weekly_metrics.csv`. Total build time: about an hour.

## 1. Connect the data

1. Open Tableau Desktop > Connect > Text File > select `weekly_metrics.csv`.
2. In the Data Source tab, confirm types: `week_start` = Date, `attendees` / `first_timers` / `returning_runners` / `instagram_views` / `instagram_engagement` = Number (whole), `avg_temp_f` = Number (decimal), `event_type` = String.
3. Add two calculated fields:
   - `First Timer Share` = `[first_timers] / [attendees]`
   - `Heat Bucket` =
     ```
     IF [avg_temp_f] >= 76 THEN "Hot (76F+)"
     ELSEIF [avg_temp_f] >= 68 THEN "Warm (68-76F)"
     ELSE "Mild (<68F)"
     END
     ```

## 2. Sheets

### Sheet A: Weekly attendance trend (line)
- Columns: `WEEK(week_start)` (continuous, exact date)
- Rows: `AVG(attendees)`
- Color: `event_type`
- Add a trend line (Analytics pane > Trend Line > Linear) and turn on Mark Labels for Brand Collab and Special Event points only.
- Format: line thickness 2, show gridlines off.

### Sheet B: Seasonality by month (bar)
- Columns: `MONTH(week_start)` as discrete (Jan, Feb...)
- Rows: `AVG(attendees)`
- Color: `AVG(avg_temp_f)` (orange sequential palette, reversed so hotter = darker)
- Sort: by month order, not by value.
- Tooltip: add `AVG(avg_temp_f)` and record count.

### Sheet C: Event type comparison (bar)
- Rows: `event_type`
- Columns: `AVG(attendees)`
- Label: show mark labels with one decimal.
- Sort descending. This is the "Red Bull / Prime weeks double turnout" chart.

### Sheet D: Instagram vs attendance (scatter)
- Columns: `instagram_engagement`
- Rows: `attendees`
- Detail: `event_type` (also put it on Shape so collab weeks stand out)
- Analytics pane > Trend Line. Check "Show R-Squared" in the trend line tooltip options.
- Tooltip: `week_start`, `instagram_views`, `event_type`.

### Sheet E: First-timer share over time (area)
- Columns: `WEEK(week_start)`
- Rows: `First Timer Share` (format as %)
- Area chart, light fill. Add a constant reference line at 0.30.

## 3. Dashboard: "Green House Run Club Growth"

Layout (1600 x 900, tiled):
- Top row: title + three KPI text boxes (Insert > Text, big numbers):
  - Last 13 weeks avg: 82.2 runners
  - Growth vs first 13 weeks: +180.6%
  - Brand collab lift: +82.3%
- Middle row: Sheet A (wide, spans 2/3) + Sheet C (1/3)
- Bottom row: Sheet B + Sheet D + Sheet E, equal thirds.

## 4. Filters and interactivity

- Add `event_type` as a multi-select filter (applies to all sheets using the data source: right-click filter > Apply to Worksheets > All Using This Data Source).
- Add `week_start` as a range-of-dates slider filter, same apply-to setting.
- Dashboard > Actions > Add Filter Action: selecting points in Sheet D filters the whole dashboard to those weeks.
- Rename all sheet titles to plain English ("Weekly attendance", not "Sheet A").
- Publish to Tableau Public when done; paste the link in the README.
