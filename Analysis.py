import pandas as pd

# -------------------------
# STEP 1: LOAD DATA
# -------------------------
df1 = pd.read_csv("/home/harshitmathur/Downloads/merged_output.csv", low_memory=False)
df2 = pd.read_csv("/home/harshitmathur/Downloads/4145880_2026_06_19.csv", low_memory=False)

# -------------------------
# STEP 2: CLEAN COLUMN NAMES
# -------------------------
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

# -------------------------
# STEP 3: STANDARDIZE KEYS
# -------------------------
df1["sz_loan_account_no"] = df1["sz_loan_account_no"].astype(str).str.strip()
df2["loan_account_no"] = df2["loan_account_no"].astype(str).str.strip()

# -------------------------
# STEP 4: MERGE (CORRECT JOIN)
# -------------------------
final = pd.merge(
    df1,
    df2,
    left_on="sz_loan_account_no",
    right_on="loan_account_no",
    how="left"
)

# -------------------------
# STEP 5: BASIC SANITY CHECKS
# -------------------------
print("Final shape:", final.shape)
print("Match rate (non-null rows from df2):", final["loan_account_no"].notna().mean())
print("Unique loans in df1:", df1["sz_loan_account_no"].nunique())
print("Unique loans in df2:", df2["loan_account_no"].nunique())
print("Unique loans in final:", final["sz_loan_account_no"].nunique())

# -------------------------
# STEP 6: SAVE OUTPUT
# -------------------------
final.to_csv("/home/harshitmathur/Downloads/final_merged_output.csv", index=False)