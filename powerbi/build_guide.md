# Power BI Build Guide: Green House Run Club Dashboard

Source file: `data/weekly_metrics.csv`. Total build time: about an hour.

## 1. Load the data

1. Home > Get Data > Text/CSV > select `weekly_metrics.csv` > Transform Data.
2. In Power Query, set types: `week_start` = Date, counts = Whole Number, `avg_temp_f` = Decimal Number, `event_type` = Text.
3. Add columns (Add Column > Custom Column):
   - `MonthName` = `Date.ToText([week_start], "MMM")`
   - `MonthNum` = `Date.Month([week_start])` (sort MonthName by this later)
   - `HeatBucket` = `if [avg_temp_f] >= 76 then "Hot (76F+)" else if [avg_temp_f] >= 68 then "Warm (68-76F)" else "Mild (<68F)"`
4. Close & Apply. In Model view, sort `MonthName` by `MonthNum`.

## 2. Measures (Modeling > New Measure)

```dax
Avg Attendance = AVERAGE(weekly_metrics[attendees])

First Timer Share = DIVIDE(SUM(weekly_metrics[first_timers]), SUM(weekly_metrics[attendees]))

Collab Lift Pct =
DIVIDE(
    CALCULATE(AVERAGE(weekly_metrics[attendees]), weekly_metrics[event_type] = "Brand Collab"),
    CALCULATE(AVERAGE(weekly_metrics[attendees]), weekly_metrics[event_type] = "Regular")
) - 1

Growth First13 vs Last13 =
VAR First13 = CALCULATE(AVERAGE(weekly_metrics[attendees]), TOPN(13, weekly_metrics, weekly_metrics[week_start], ASC))
VAR Last13  = CALCULATE(AVERAGE(weekly_metrics[attendees]), TOPN(13, weekly_metrics, weekly_metrics[week_start], DESC))
RETURN DIVIDE(Last13 - First13, First13)
```

## 3. Report pages

### Page 1: Growth overview
- **Card visuals (x3):** `Avg Attendance` (title: "Avg runners / week"), `Growth First13 vs Last13` formatted as % ("Growth, first 13 vs last 13 weeks"), `Collab Lift Pct` formatted as % ("Brand collab lift").
- **Line chart:** Axis = `week_start`, Values = `Avg Attendance`. Legend = `event_type`. Turn on data labels only for max points if needed. Title: "Weekly attendance, Jan 2024 - Sep 2025".
- **Clustered bar chart:** Y-axis = `event_type`, X-axis = `Avg Attendance`. Data labels on. Title: "Brand collabs double turnout".

### Page 2: Seasonality and social
- **Clustered column chart:** X-axis = `MonthName`, Y-axis = `Avg Attendance`. Sort by MonthNum. Title: "Attendance by month".
- **Scatter chart:** X = `instagram_engagement` (Values), Y = `attendees` (Values), Legend = `event_type`. Turn on the trend line under Analytics. Title: "Instagram engagement vs attendance".
- **Area chart:** X-axis = `week_start`, Y-axis = `First Timer Share` (format %). Title: "First-timer share holds near 30%".
- **Donut chart:** Legend = `HeatBucket`, Values = count of weeks. Title: "Weeks by heat bucket".

### Slicers (put on both pages, synced)
- `event_type` as a multi-select slicer (vertical list).
- `week_start` as a "Between" date slicer.

## 4. Polish and interactivity

- Format > Page > 16:9 canvas. Dark header bar with the club name as a text box.
- Select the scatter chart > Format > Edit interactions: set it to filter the other visuals on click.
- Turn off "Include in tooltip" clutter: keep tooltips to week, attendees, event type, engagement.
- Rename every visual title to plain English. No default "Sum of attendees" titles left anywhere.
- File > Publish > Publish to Power BI Service when done; paste the link in the README.
