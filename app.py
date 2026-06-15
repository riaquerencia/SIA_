import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Support Integrity Auditor",
    layout="wide"
)

st.title("🛡️ Support Integrity Auditor (SIA)")
st.write("Detecting priority mismatches in customer support tickets")

# -------------------------
# CSV Upload
# -------------------------

uploaded_file = st.file_uploader(
    "Upload Ticket Dataset",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.success(f"Loaded {len(df)} tickets")

    # -------------------------
    # Ticket Selection
    # -------------------------

    st.subheader("🎫 Ticket Selection")

    selected_ticket = st.selectbox(
        "Select Ticket ID",
        df["Ticket_ID"]
    )

    row = df[df["Ticket_ID"] == selected_ticket].iloc[0]

    # -------------------------
    # Evidence Dossier
    # -------------------------

    st.subheader("📋 Evidence Dossier")

    dossier = {
        "ticket_id": row["Ticket_ID"],
        "assigned_priority": row["assigned_priority"],
        "inferred_severity": row["inferred_severity"],
        "mismatch_type": row["mismatch_type"],
        "resolution_time_hours": float(row["Resolution_Time_Hours"])
    }

    st.json(dossier)

    # -------------------------
    # Mismatch Detection
    # -------------------------

    st.subheader("🚨 Mismatch Detection")

    assigned = str(row["assigned_priority"])
    inferred = str(row["inferred_severity"])
    mismatch_type = str(row["mismatch_type"])

    if mismatch_type == "Consistent":
        st.success("✅ Priority Consistent")
    else:
        st.error(f"🚨 {mismatch_type}")

    st.write("**Assigned Priority:**", assigned)
    st.write("**Inferred Severity:**", inferred)
    st.write("**Mismatch Type:**", mismatch_type)

    # -------------------------
    # Dashboard
    # -------------------------

    st.subheader("📊 Priority Mismatch Dashboard")

    st.bar_chart(
        df["mismatch_type"].value_counts()
    )

    # -------------------------
    # Mismatch Rate
    # -------------------------

    mismatch_rate = (
        df["pseudo_label"].sum() /
        len(df)
    ) * 100

    st.metric(
        "Mismatch Rate",
        f"{mismatch_rate:.2f}%"
    )

    # -------------------------
    # Top Signals
    # -------------------------

    st.subheader("📈 Top Contributing Signals")

    signal_df = pd.DataFrame({
        "Signal": [
            "Keyword Severity",
            "Resolution Severity"
        ],
        "Count": [
            (df["keyword_severity"] > 0).sum(),
            (df["resolution_severity"] > 0).sum()
        ]
    })

    st.bar_chart(
        signal_df.set_index("Signal")
    )

    # -------------------------
    # Heatmap
    # -------------------------

    st.subheader("🔥 Severity Heatmap")

    heatmap_data = pd.crosstab(
        df["Issue_Category"],
        df["mismatch_type"]
    )

    fig, ax = plt.subplots(figsize=(8, 4))

    sns.heatmap(
        heatmap_data,
        annot=True,
        cmap="YlOrRd",
        ax=ax
    )

    st.pyplot(fig)

else:
    st.info("Please upload a CSV file to begin.")