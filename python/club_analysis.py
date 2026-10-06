"""Analysis of Green House Run Club weekly metrics."""
import pandas as pd

df = pd.read_csv("data/weekly_metrics.csv", parse_dates=["week_start"])
df["month"] = df["week_start"].dt.month
df["year_month"] = df["week_start"].dt.to_period("M")

print("=" * 56)
print("GREEN HOUSE RUN CLUB - GROWTH ANALYSIS")
print(f"{df['week_start'].min().date()} -> {df['week_start'].max().date()} "
      f"({len(df)} weeks)")
print("=" * 56)

# 1. Overall growth: first 13 weeks vs last 13 weeks
first13 = df.iloc[:13]["attendees"].mean()
last13 = df.iloc[-13:]["attendees"].mean()
growth_pct = (last13 - first13) / first13 * 100
print("\n[1] OVERALL GROWTH")
print(f"    First 13 weeks avg attendance: {first13:.1f}")
print(f"    Last 13 weeks avg attendance:  {last13:.1f}")
print(f"    Growth: {growth_pct:+.1f}%")

# 2. Seasonality by month
print("\n[2] SEASONALITY (avg attendance by month)")
monthly = df.groupby("month").agg(
    avg_attendance=("attendees", "mean"),
    avg_temp=("avg_temp_f", "mean"),
    weeks=("attendees", "count"),
).round(1)
print(monthly.to_string())
best = monthly["avg_attendance"].idxmax()
worst = monthly["avg_attendance"].idxmin()
print(f"    Best month: {best} ({monthly.loc[best, 'avg_attendance']:.0f} avg) | "
      f"Toughest month: {worst} ({monthly.loc[worst, 'avg_attendance']:.0f} avg)")

# 2b. Heat buckets
def heat_bucket(t):
    if t < 70:
        return "Mild (<70F)"
    if t < 85:
        return "Warm (70-85F)"
    return "Hot (85F+)"
df["heat"] = df["avg_temp_f"].apply(heat_bucket)
print("\n    By heat bucket (trend-adjusted residuals):")
# The club grew a lot over 91 weeks, so strip out the linear trend first:
# otherwise late-2025 hot weeks look fine only because the base is bigger.
df["week_idx"] = range(len(df))
df["resid"] = df["attendees"] - df["attendees"].mean() - (
    df["attendees"].cov(df["week_idx"]) / df["week_idx"].var()
) * (df["week_idx"] - df["week_idx"].mean())
heat_r = df.groupby("heat")["resid"].mean().reindex(
    ["Mild (<70F)", "Warm (70-85F)", "Hot (85F+)"]).round(1)
print(heat_r.to_string())
print(f"    Trend-adjusted: hot weeks run {heat_r['Hot (85F+)'] - heat_r['Mild (<70F)']:+.1f} "
      f"runners vs mild weeks.")

# 3. First-timer share + retention proxy
print("\n[3] FIRST-TIMERS AND RETENTION")
df["first_timer_share"] = df["first_timers"] / df["attendees"]
share_first_half = df.iloc[:45]["first_timer_share"].mean()
share_second_half = df.iloc[45:]["first_timer_share"].mean()
print(f"    Avg first-timer share, first half:  {share_first_half:.1%}")
print(f"    Avg first-timer share, second half: {share_second_half:.1%}")
# Retention proxy: do first_timers this week predict returning_runners next week?
ft = df["first_timers"].to_numpy()
ret = df["returning_runners"].to_numpy()
corr_ret = pd.Series(ft[:-1]).corr(pd.Series(ret[1:]))
print(f"    Correlation: first_timers (week N) vs returning_runners (week N+1): "
      f"{corr_ret:.2f}")

# 4. Instagram engagement -> next week attendance
print("\n[4] INSTAGRAM EFFECT")
eng = df["instagram_engagement"].to_numpy()
att = df["attendees"].to_numpy()
corr_ig_same = pd.Series(eng).corr(pd.Series(att))
corr_ig = pd.Series(eng[:-1]).corr(pd.Series(att[1:]))
print(f"    Same-week engagement vs attendance:      {corr_ig_same:.2f}")
print(f"    Engagement (week N) vs attendance (N+1): {corr_ig:.2f}")

# 5. Brand collab lift
print("\n[5] BRAND COLLAB LIFT")
by_event = df.groupby("event_type").agg(
    avg_attendance=("attendees", "mean"),
    weeks=("attendees", "count"),
).round(1)
print(by_event.to_string())
regular = by_event.loc["Regular", "avg_attendance"]
collab = by_event.loc["Brand Collab", "avg_attendance"]
special = by_event.loc["Special Event", "avg_attendance"]
print(f"    Brand Collab lift vs Regular: {collab - regular:+.1f} runners "
      f"({(collab / regular - 1) * 100:+.1f}%)")
print(f"    Anniversary run vs Regular:   {special - regular:+.1f} runners "
      f"({(special / regular - 1) * 100:+.1f}%)")

print("\n" + "=" * 56)
