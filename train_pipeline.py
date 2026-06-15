%%writefile train_pipeline.py

import pandas as pd

print("Loading dataset...")

df = pd.read_csv("customer_support_tickets.csv")

priority_map = {
    "Low":1,
    "Medium":2,
    "High":3,
    "Critical":4
}

df["keyword_severity"] = df["Ticket_Description"].str.lower().apply(
    lambda x: 4 if any(k in x for k in [
        "urgent","outage","down","security","fraud"
    ]) else 2
)

df["resolution_severity"] = (
    df["Resolution_Time_Hours"] > 48
).astype(int) * 4

df["severity_score"] = (
    df["keyword_severity"] +
    df["resolution_severity"]
) / 2

def infer(score):
    if score >= 3.5:
        return "Critical"
    elif score >= 3:
        return "High"
    elif score >= 2:
        return "Medium"
    return "Low"

df["inferred_severity"] = df["severity_score"].apply(infer)

df["assigned_priority"] = df["Priority_Level"]

df["pseudo_label"] = (
    df["assigned_priority"] !=
    df["inferred_severity"]
).astype(int)

df["mismatch_type"] = df.apply(
    lambda row:
    "Hidden Crisis"
    if priority_map.get(row["assigned_priority"],0)
       < priority_map.get(row["inferred_severity"],0)
    else "False Alarm",
    axis=1
)

df.to_csv(
    "pseudo_labeled_tickets.csv",
    index=False
)

print("Saved pseudo_labeled_tickets.csv")