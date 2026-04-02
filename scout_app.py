import streamlit as st
import pandas as pd

st.title("⚽ FIFA 21 Scout System")
st.markdown("Find undervalued players before the market notices them.")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("fifa_cleaned.csv", low_memory=False)
    df["growth_potential"] = df["POT"] - df["↓OVA"]
    df["scout_score"] = (
        (df["growth_potential"] * 2)
        + df["↓OVA"]
        - (df["Age"] * 0.5)
        - (df["value_eur"] / 1_000_000)
    )
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Scout Filters")

max_age = st.sidebar.slider("Maximum Age", 16, 35, 26)
min_ova = st.sidebar.slider("Minimum OVA", 50, 90, 65)
max_value = st.sidebar.slider("Maximum Value (€M)", 1, 100, 20)
position = st.sidebar.selectbox(
    "Position",
    ["All"] + sorted(df["primary_position"].dropna().unique().tolist())
)

# Apply filters
filtered = df[
    (df["Age"] <= max_age) &
    (df["↓OVA"] >= min_ova) &
    (df["value_eur"] <= max_value * 1_000_000)
].copy()

if position != "All":
    filtered = filtered[filtered["primary_position"] == position]

# Sort by scout score
filtered = filtered.sort_values("scout_score", ascending=False)

# Show results
st.subheader(f"🎯 Top Scout Recommendations ({len(filtered)} players found)")

st.dataframe(
    filtered[[
        "Name", "Age", "Nationality", "Club",
        "primary_position", "↓OVA", "POT",
        "growth_potential", "value_eur", "scout_score"
    ]].head(20).reset_index(drop=True)
)