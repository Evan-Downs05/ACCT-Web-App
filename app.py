
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Financial Analysis Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Financial Analysis Dashboard")
st.write("Analyze and compare publicly traded companies.")

# Sample data (we'll replace this with real data)
data = {
    "Company": ["Apple", "Microsoft", "Nike", "Coca-Cola", "Nvidia"],
    "Sector": ["Technology", "Technology", "Consumer",
               "Consumer", "Technology"],
    "P/E Ratio": [32, 29, 22, 24, 45],
    "ROE (%)": [25, 32, 18, 35, 40],
    "Debt/Equity": [1.5, 0.4, 0.8, 1.6, 0.5]
}

df = pd.DataFrame(data)

st.sidebar.header("Financial Filters")

sector = st.sidebar.selectbox(
    "Select Sector",
    ["All"] + sorted(df["Sector"].unique().tolist())
)

pe_max = st.sidebar.slider(
    "Maximum P/E Ratio", 0, 100, 40
)

roe_min = st.sidebar.slider(
    "Minimum ROE (%)", 0, 100, 10
)

filtered = df[
    (df["P/E Ratio"] <= pe_max) &
    (df["ROE (%)"] >= roe_min)
]

if sector != "All":
    filtered = filtered[filtered["Sector"] == sector]

st.metric("Companies Matching Filters", len(filtered))

st.subheader("Company Screening Results")
st.dataframe(filtered, use_container_width=True)

st.subheader("Return on Equity Comparison")

if not filtered.empty:
    st.bar_chart(
        filtered.set_index("Company")["ROE (%)"]
    )
else:
    st.info("No companies match the selected filters.")
