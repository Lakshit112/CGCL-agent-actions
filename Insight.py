import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# LOAD FINAL CLEAN FILE
# -------------------------
df = pd.read_csv(
    "/home/harshitmathur/Downloads/final_compliance_fixed.csv",
    low_memory=False
)

df.columns = df.columns.str.strip()

# -------------------------
# IDENTIFY KEY COLUMNS SAFELY
# -------------------------
strategy_col = "collection_business_strategy"
target_col = [c for c in df.columns if "sloppy" in c.lower() and "target" in c.lower()][0]

# -------------------------
# CLEAN STRATEGY
# -------------------------
df[strategy_col] = df[strategy_col].astype(str).str.upper()

# -------------------------
# KPI 1: OVERALL SUMMARY
# -------------------------
overall = pd.DataFrame([{
    "Total Loans": len(df),
    "Compliance Rate": df["strategy_followed"].mean(),
    "Overall Outcome Rate": df[target_col].mean()
}])

# -------------------------
# KPI 2: STRATEGY PERFORMANCE
# -------------------------
strategy_perf = df.groupby(strategy_col).agg(
    total_loans=("strategy_followed", "count"),
    compliance_rate=("strategy_followed", "mean"),
    outcome_rate=(target_col, "mean")
).reset_index()

# -------------------------
# KPI 3: ACTION PERFORMANCE
# -------------------------
action_perf = df.groupby("dominant_action").agg(
    count=("dominant_action", "count"),
    outcome_rate=(target_col, "mean")
).reset_index()

# -------------------------
# CHART 1: STRATEGY OUTCOME
# -------------------------
plt.figure()
strategy_perf.sort_values("outcome_rate", ascending=False).head(10).plot(
    x=strategy_col,
    y="outcome_rate",
    kind="bar",
    title="Top Strategies by Outcome Rate"
)
plt.tight_layout()
plt.savefig("/home/harshitmathur/Downloads/v2_strategy_chart.png")

# -------------------------
# CHART 2: ACTION IMPACT
# -------------------------
plt.figure()
action_perf.plot(
    x="dominant_action",
    y="outcome_rate",
    kind="bar",
    title="Action Type vs Outcome Rate"
)
plt.tight_layout()
plt.savefig("/home/harshitmathur/Downloads/v2_action_chart.png")

# -------------------------
# EXPORT EXCEL (FINAL V2 REPORT)
# -------------------------
output_path = "/home/harshitmathur/Downloads/collection_report_v2.xlsx"

with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
    overall.to_excel(writer, sheet_name="Overall", index=False)
    strategy_perf.to_excel(writer, sheet_name="Strategy_Performance", index=False)
    action_perf.to_excel(writer, sheet_name="Action_Performance", index=False)

print("V2 REPORT CREATED:", output_path)
