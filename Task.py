
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
