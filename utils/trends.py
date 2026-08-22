"""Deterministic trend and anomaly detection for longitudinal health logs."""
from __future__ import annotations
import pandas as pd

def analyze_trends(rows: list[dict]) -> list[dict]:
    if not rows: return []
    df = pd.DataFrame(rows).sort_values("logged_on")
    insights: list[dict] = []
    rules = {"glucose": (140, "High glucose reading"), "systolic": (140, "High systolic blood pressure"), "diastolic": (90, "High diastolic blood pressure"), "heart_rate": (100, "Elevated resting heart rate")}
    for column, (limit, label) in rules.items():
        if column in df and df[column].notna().any() and float(df[column].dropna().iloc[-1]) >= limit:
            insights.append({"severity": "warning", "metric": column, "message": f"{label}: latest value is {df[column].dropna().iloc[-1]:g}."})
    for column in ("weight", "glucose", "sleep", "water", "steps"):
        values = df[column].dropna() if column in df else pd.Series(dtype=float)
        if len(values) >= 4:
            recent, earlier = float(values.tail(2).mean()), float(values.iloc[:-2].tail(3).mean())
            delta = recent - earlier
            if abs(delta) >= max(abs(earlier) * .1, .5):
                direction = "increased" if delta > 0 else "decreased"
                insights.append({"severity": "info", "metric": column, "message": f"{column.replace('_',' ').title()} has {direction} by {abs(delta):.1f} versus the previous baseline."})
    return insights
