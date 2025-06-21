import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# --- PAGE CONFIG ---
st.set_page_config(page_title="COVID-19 Dashboard", layout="wide")

# --- CUSTOM CSS ---
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- IMAGE BANNER ---
image = Image.open("covid_image.png")  # Replace with your banner image
st.image(image, use_container_width=True)

# --- LOAD DATA ---
df = pd.read_csv("cleaned_covid_data.csv", parse_dates=["DATE"])

# --- SIDEBAR FILTERS ---
st.sidebar.title("Filter Data")

countries = st.sidebar.multiselect(
    "Select Countries",
    options=df["COUNTRY"].unique(),
    default=df["COUNTRY"].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df["DATE"].min(), df["DATE"].max()],
    min_value=df["DATE"].min(),
    max_value=df["DATE"].max()
)

show_data = st.sidebar.checkbox("Show Raw Data")

# Sidebar footer
st.sidebar.markdown("""
---
Created with by [Ezekiel Mbaya](https:www.linkedin.com/in/ezekiel-ibrahim-866a1915b/)
""")

# --- FILTER DATAFRAME ---
filtered_df = df[
    (df["COUNTRY"].isin(countries)) &
    (df["DATE"] >= pd.to_datetime(date_range[0])) &
    (df["DATE"] <= pd.to_datetime(date_range[1]))
]

# --- KPI CALCULATIONS ---
total_cases = int(filtered_df["NEW_CASES"].sum())
total_deaths = int(filtered_df["NEW_DEATHS"].sum())
total_vaccinated = int(filtered_df["VACCINATED"].sum())

# --- TITLE ---
st.title("COVID-19 Dashboard")
st.markdown("#### Data Source: Cleaned Dataset | Visualizing Trends & Vaccination Progress")

# --- KPI DISPLAY ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="metric-box total-cases">
            <h2>Total Cases</h2>
            <p>{total_cases:,}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-box total-deaths">
            <h2>☠️ Total Deaths</h2>
            <p>{total_deaths:,}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-box total-vaccinated">
            <h2>Total Vaccinated</h2>
            <p>{total_vaccinated:,}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- RAW DATA ---
if show_data:
    st.subheader("Raw Data Preview")
    st.dataframe(filtered_df)

# --- VISUALIZATIONS ---
st.subheader("New COVID-19 Cases Over Time")
fig1 = px.line(filtered_df, x="DATE", y="NEW_CASES", color="COUNTRY", markers=True)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Vaccinations Over Time")
fig2 = px.line(filtered_df, x="DATE", y="VACCINATED", color="COUNTRY", markers=True)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Daily Total New Cases (All Countries Combined)")
daily_cases = filtered_df.groupby("DATE")["NEW_CASES"].sum().reset_index()
fig3 = px.bar(daily_cases, x="DATE", y="NEW_CASES", title="Total Daily Cases")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Total Deaths by Country")
death_by_country = filtered_df.groupby("COUNTRY")["NEW_DEATHS"].sum().sort_values(ascending=False).reset_index()
fig4 = px.bar(death_by_country, x="COUNTRY", y="NEW_DEATHS", title="Total Deaths by Country")
st.plotly_chart(fig4, use_container_width=True)

st.subheader("Top 5 Countries by Total Vaccinations")
vax_top = filtered_df.groupby("COUNTRY")["VACCINATED"].sum().nlargest(5).reset_index()
fig5 = px.bar(vax_top, x="COUNTRY", y="VACCINATED", title="Top 5 Vaccinated Countries", color="VACCINATED")
st.plotly_chart(fig5, use_container_width=True)

st.subheader("Vaccination Share by Country")
vax_total = filtered_df.groupby("COUNTRY")["VACCINATED"].sum().reset_index()
fig6 = px.pie(vax_total, values="VACCINATED", names="COUNTRY", title="Vaccination Distribution")
st.plotly_chart(fig6, use_container_width=True)
