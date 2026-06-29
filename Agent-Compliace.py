import pandas as pd

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv("/home/harshitmathur/Downloads/final_merged_output.csv", low_memory=False)

# -------------------------
# CLEAN COLUMN NAMES
# -------------------------
df.columns = df.columns.str.strip()

print("\nColumns loaded:", len(df.columns))

# -------------------------
# FIND REAL STRATEGY COLUMN (IGNORE DERIVED METRICS)
# -------------------------
strategy_cols = [
    c for c in df.columns
    if "strategy" in c.lower()
    and "follow" not in c.lower()
]

if not strategy_cols:
    raise Exception("No valid strategy column found")

strategy_col = strategy_cols[0]
print("Using strategy column:", strategy_col)

df[strategy_col] = df[strategy_col].astype(str).str.upper()

# -------------------------
# FIND REAL TARGET COLUMN (LOOSE MATCH)
# -------------------------
target_cols = [
    c for c in df.columns
    if "sloppy" in c.lower()
    and "target" in c.lower()
]

if not target_cols:
    raise Exception("No valid target column found")

target_col = target_cols[0]
print("Using target column:", target_col)

# -------------------------
# ENSURE ACTION COLUMNS EXIST
# -------------------------
for col in ["field_visits", "tele_calls", "sms_sent", "whatsapp_sent"]:
    if col not in df.columns:
        df[col] = 0

# -------------------------
# DOMINANT ACTION
# -------------------------
def get_dominant_action(row):
    actions = {
        "FIELD": row["field_visits"],
        "CALL": row["tele_calls"],
        "SMS": row["sms_sent"],
        "WHATSAPP": row["whatsapp_sent"]
    }
    return max(actions, key=actions.get)

df["dominant_action"] = df.apply(get_dominant_action, axis=1)

# -------------------------
# COMPLIANCE LOGIC
# -------------------------
def is_compliant(row):
    strat = row[strategy_col]
    actual = row["dominant_action"]

    if "FIELD" in strat and actual == "FIELD":
        return True
    if ("CALL" in strat or "TELE") and actual == "CALL":
        return True
    if "SMS" in strat and actual == "SMS":
        return True
    if "WHATSAPP" in strat and actual == "WHATSAPP":
        return True

    return False

df["strategy_followed"] = df.apply(is_compliant, axis=1)

# -------------------------
# METRICS
# -------------------------
print("\n=== COMPLIANCE RATE ===")
print(df["strategy_followed"].mean())

print("\n=== OUTCOME BY COMPLIANCE ===")
print(df.groupby("strategy_followed")[target_col].mean())

# -------------------------
# SAVE OUTPUT
# -------------------------
output_file = "/home/harshitmathur/Downloads/final_compliance_fixed.csv"
df.to_csv(output_file, index=False)

print("\nSaved file at:", output_file)
