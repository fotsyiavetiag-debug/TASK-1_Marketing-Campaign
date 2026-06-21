
# ── 1. Rename columns (lowercase, uniform) ───────────────────────────────────
df.columns = [c.lower() for c in df.columns]
# ── 0. Load ──────────────────────────────────────────────────────────────────

df = pd.read_csv("marketing_campaign.csv", sep="\t")
print(f"Raw shape : {df.shape}") 


# ── 1. Rename columns (lowercase, uniform) ───────────────────────────────────
df.columns = [c.lower() for c in df.columns]

# ── 2. Missing values ────────────────────────────────────────────────────────
# Only `income` has 24 nulls → fill with median (robust to outliers)
print(f"Missing before : {df.isnull().sum().sum()}")   
df["income"] = df["income"].fillna(df["income"].median())
print(f"Missing after  : {df.isnull().sum().sum()}")

# ── 3. Duplicates ─────────────────────────────────────────────────────────────
print(f"Duplicate rows : {df.duplicated().sum()}")     # 0
# df.drop_duplicates(inplace=True)  # uncomment if duplicates exist

# ── 4. Standardise Marital_Status ────────────────────────────────────────────
# 'Alone' is semantically identical to 'Single'
# 'Absurd' and 'YOLO' are invalid entries → grouped as 'Other'
df["marital_status"] = df["marital_status"].replace(
    {"Alone": "Single", "Absurd": "Other", "YOLO": "Other"}
)
print("Marital_Status unique:", sorted(df["marital_status"].unique()))

# ── 5. Convert date column ───────────────────────────────────────────────────
df["dt_customer"] = pd.to_datetime(df["dt_customer"], format="%d-%m-%Y")

# ── 6. Derived column: Age ───────────────────────────────────────────────────
df["age"] = 2024 - df["year_birth"]

# ── 7. Outlier treatment ─────────────────────────────────────────────────────
# Income: one extreme value 666 666 → clear data-entry error
df = df[df["income"] <= 200_000]

# Age: three records born before 1924 (age > 100) → invalid year_birth
df = df[df["age"] <= 100].reset_index(drop=True)

print(f"After outlier removal : {df.shape}")           # (2236, 28)

# ── 8. Drop constant / useless columns ───────────────────────────────────────
# z_costcontact and z_revenue contain a single unique value each → no info
df.drop(columns=["z_costcontact", "z_revenue"], inplace=True)

# ── 9. Data types check ──────────────────────────────────────────────────────
# age should be int
df["age"] = df["age"].astype(int)
# Binary campaign flags already int64 ✓

print("\nFinal dtypes :")
print(df.dtypes)
print(f"\nFinal shape : {df.shape}")    # (2236, 26)

# ── 10. Save ─────────────────────────────────────────────────────────────────
df.to_csv("marketing_campaign_clean.csv", index=False)
print("\n✅  Cleaned dataset saved to marketing_campaign_clean.csv")
