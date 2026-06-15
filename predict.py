%%writefile predict.py

import pandas as pd
import json

df = pd.read_csv("pseudo_labeled_tickets.csv")

results = []

for _, row in df.iterrows():

    dossier = {
        "ticket_id": str(row["Ticket_ID"]),
        "assigned_priority": row["assigned_priority"],
        "inferred_severity": row["inferred_severity"],
        "mismatch_type": row["mismatch_type"],
        "confidence": round(
            float(row["severity_score"]),
            2
        )
    }

    results.append(dossier)

with open(
    "evidence_dossiers.json",
    "w"
) as f:
    json.dump(results, f, indent=4)

print("Evidence dossiers generated.")