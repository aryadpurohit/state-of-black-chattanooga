import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# -----------------------------------
# Page setup
# -----------------------------------

st.set_page_config(
    page_title="State of Black Chattanooga",
    page_icon="📊",
    layout="wide"
)


# -----------------------------------
# Title
# -----------------------------------

st.title("Economics")
st.subheader("How has economic parity changed from 2022 to 2026?")


st.write(
    "The Economics Index compares economic outcomes for Black and White "
    "residents. A score of 100% represents full parity."
)


# -----------------------------------
# Load data
# -----------------------------------

economics_url = (
    "https://raw.githubusercontent.com/"
    "aryadpurohit/state-of-black-chattanooga/"
    "main/data/processed/economics_index.csv"
)

components_url = (
    "https://raw.githubusercontent.com/"
    "aryadpurohit/state-of-black-chattanooga/"
    "main/data/processed/economics_components.csv"
)


economics = pd.read_csv(economics_url)
components = pd.read_csv(components_url)


# -----------------------------------
# Economics Index
# -----------------------------------

st.header("Economics Index")


col1, col2, col3 = st.columns(3)

col1.metric(
    "2022",
    f"{economics.loc[economics['year'] == 2022, 'economics_index'].iloc[0]}%"
)

col2.metric(
    "2024",
    f"{economics.loc[economics['year'] == 2024, 'economics_index'].iloc[0]}%"
)

col3.metric(
    "2026",
    f"{economics.loc[economics['year'] == 2026, 'economics_index'].iloc[0]}%"
)


# -----------------------------------
# Economics Index trend
# -----------------------------------

st.subheader("Economics Index Trend")

fig, ax = plt.subplots()

ax.plot(
    economics["year"],
    economics["economics_index"],
    marker="o"
)

ax.set_xlabel("Year")
ax.set_ylabel("Economics Index (%)")
ax.set_title("Economics Index, 2022–2026")

ax.set_xticks(economics["year"])

st.pyplot(fig)


# -----------------------------------
# Economic Components
# -----------------------------------

st.header("Economic Components")

st.write(
    "The Economics Index is represented by four components: "
    "Income, Poverty, Employment, and Housing & Wealth."
)


# Get 2026 values

income_2026 = components[
    (components["year"] == 2026) &
    (components["indicator"] == "Income")
]["value"].iloc[0]

poverty_2026 = components[
    (components["year"] == 2026) &
    (components["indicator"] == "Poverty")
]["value"].iloc[0]

employment_2026 = components[
    (components["year"] == 2026) &
    (components["indicator"] == "Employment")
]["value"].iloc[0]

housing_2026 = components[
    (components["year"] == 2026) &
    (components["indicator"] == "Housing & Wealth")
]["value"].iloc[0]


col1, col2, col3, col4 = st.columns(4)

col1.metric("Income", f"{income_2026}%")
col2.metric("Poverty", f"{poverty_2026}%")
col3.metric("Employment", f"{employment_2026}%")
col4.metric("Housing & Wealth", f"{housing_2026}%")


# -----------------------------------
# Component trends
# -----------------------------------

st.subheader("Economic Component Trends")


fig, ax = plt.subplots()

for indicator in components["indicator"].unique():

    data = components[
        components["indicator"] == indicator
    ]

    ax.plot(
        data["year"],
        data["value"],
        marker="o",
        label=indicator
    )


ax.set_xlabel("Year")
ax.set_ylabel("Parity Index (%)")
ax.set_title("Economic Component Trends, 2022–2026")
ax.set_xticks([2022, 2024, 2026])

ax.legend()

st.pyplot(fig)


# -----------------------------------
# Change from 2022 to 2026
# -----------------------------------

st.header("Change from 2022 to 2026")


component_change = components.pivot(
    index="indicator",
    columns="year",
    values="value"
)


component_change["change_2022_2026"] = (
    component_change[2026] -
    component_change[2022]
)


st.dataframe(
    component_change[
        [2022, 2024, 2026, "change_2022_2026"]
    ]
)


# -----------------------------------
# Key findings
# -----------------------------------

st.header("Key Findings")


largest_improvement = component_change[
    "change_2022_2026"
].idxmax()

largest_decline = component_change[
    "change_2022_2026"
].idxmin()


improvement_value = component_change.loc[
    largest_improvement,
    "change_2022_2026"
]

decline_value = component_change.loc[
    largest_decline,
    "change_2022_2026"
]


col1, col2 = st.columns(2)

col1.metric(
    "Largest Improvement",
    largest_improvement,
    f"+{improvement_value} percentage points"
)

col2.metric(
    "Largest Decline",
    largest_decline,
    f"{decline_value} percentage points"
)


# -----------------------------------
# Research questions
# -----------------------------------

st.header("Questions for Further Analysis")

st.write(
    "• Why did employment parity improve while poverty parity declined?"
)

st.write(
    "• What explains the difference between employment, income, and poverty outcomes?"
)

st.write(
    "• Which economic indicators show the largest disparities?"
)

st.write(
    "• How do these economic patterns vary across neighborhoods?"
)
