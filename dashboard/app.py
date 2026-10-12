
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="State of Black Chattanooga",
    page_icon="📊",
    layout="wide"
)

# -----------------------------------
# Load Data
# -----------------------------------

BASE_URL = (
    "https://raw.githubusercontent.com/"
    "aryadpurohit/state-of-black-chattanooga/main/"
    "data/processed/"
)

@st.cache_data
def load_data():
    economics = pd.read_csv(
        BASE_URL + "economics_index.csv"
    )

    components = pd.read_csv(
        BASE_URL + "economics_components.csv"
    )

    return economics, components


try:
    economics, components = load_data()

except Exception as error:
    st.error(
        "The data could not be loaded. "
        "Check that the CSV files exist in "
        "data/processed/ on GitHub."
    )
    st.exception(error)
    st.stop()


# -----------------------------------
# Data Preparation
# -----------------------------------

economics["year"] = pd.to_numeric(
    economics["year"], errors="coerce"
)

economics["economics_index"] = pd.to_numeric(
    economics["economics_index"], errors="coerce"
)

components["year"] = pd.to_numeric(
    components["year"], errors="coerce"
)

components["value"] = pd.to_numeric(
    components["value"], errors="coerce"
)

economics = economics.dropna(
    subset=["year", "economics_index"]
).sort_values("year")

components = components.dropna(
    subset=["year", "indicator", "value"]
).sort_values(["indicator", "year"])

if economics.empty or components.empty:
    st.error("The data files do not contain usable data.")
    st.stop()


# -----------------------------------
# Dashboard Header
# -----------------------------------

st.markdown("### COMMUNITY DATA • ECONOMIC EQUITY")

st.title("STATE OF BLACK CHATTANOOGA")

st.markdown(
    """
    **Tracking progress. Understanding disparities. Informing action.**
    
    An interactive look at economic parity and changes across
    the 2022, 2024, and 2026 State of Black Chattanooga reports.
    """
)

st.divider()

st.caption(
    "DATA NOTE: Parity index scores are not raw income, "
    "poverty, or employment rates. A score of 100 represents "
    "full Black–White parity. Underlying data years and "
    "methodologies may differ across reports."
)




# -----------------------------------
# Overall Economics Index
# -----------------------------------

st.header("Overall Economics Index")

st.write(
    "Compare the overall Economics Index across report years."
)

economics = economics.sort_values("year")

first_row = economics.iloc[0]
latest_row = economics.iloc[-1]

starting_score = first_row["economics_index"]
latest_score = latest_row["economics_index"]
overall_change = latest_score - starting_score

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Latest Index Score",
        f"{latest_score:.0f}"
    )

with col2:
    st.metric(
        "Change Since First Report",
        f"{overall_change:+.0f} points"
    )

with col3:
    st.metric(
        "First Report Score",
        f"{starting_score:.0f}"
    )

st.subheader("Economics Index Trend")

index_chart = economics.set_index("year")[
    ["economics_index"]
]

st.line_chart(index_chart)

st.dataframe(
    economics.rename(
        columns={
            "year": "Year",
            "economics_index": "Economics Index Score"
        }
    ),
    hide_index=True,
    use_container_width=True
)

st.divider()


# -----------------------------------
# Interactive Economic Component Explorer
# -----------------------------------

st.header("Explore an Economic Component")

st.write(
    """
    Select a component to examine its parity scores over time.
    The metrics, chart, and table will update automatically.
    """
)

indicators = sorted(
    components["indicator"].unique().tolist()
)

preferred_order = [
    "Income",
    "Poverty",
    "Employment",
    "Housing & Wealth"
]

indicators = [
    indicator
    for indicator in preferred_order
    if indicator in indicators
] + [
    indicator
    for indicator in indicators
    if indicator not in preferred_order
]

selected_indicator = st.selectbox(
    "Choose an economic component:",
    indicators
)

selected_data = components[
    components["indicator"] == selected_indicator
].sort_values("year")

first_component = selected_data.iloc[0]
latest_component = selected_data.iloc[-1]

component_start = first_component["value"]
component_latest = latest_component["value"]
component_change = component_latest - component_start

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        f"Latest {int(latest_component['year'])} Score",
        f"{component_latest:.0f}%"
    )

with col2:
    st.metric(
        "Change Across Available Years",
        f"{component_change:+.0f} percentage points"
    )

with col3:
    st.metric(
        f"First {int(first_component['year'])} Score",
        f"{component_start:.0f}%"
    )

st.subheader(
    f"{selected_indicator}: "
    f"{int(selected_data['year'].min())}–"
    f"{int(selected_data['year'].max())}"
)

component_chart = selected_data.set_index("year")[["value"]]

st.line_chart(component_chart)

st.subheader("Score Details")

display_data = selected_data[
    ["year", "value"]
].rename(
    columns={
        "year": "Year",
        "value": "Parity Score (%)"
    }
)

display_data["Year"] = display_data["Year"].astype(int)

st.dataframe(
    display_data,
    hide_index=True,
    use_container_width=True
)

st.divider()


# -----------------------------------
# 2026 Economic Component Cards
# -----------------------------------

st.header("Economic Components in 2026")

latest_year = int(components["year"].max())

latest_components = components[
    components["year"] == latest_year
]

component_values = dict(
    zip(
        latest_components["indicator"],
        latest_components["value"]
    )
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    if "Income" in component_values:
        st.metric(
            "Income",
            f"{component_values['Income']:.0f}%"
        )

with col2:
    if "Poverty" in component_values:
        st.metric(
            "Poverty",
            f"{component_values['Poverty']:.0f}%"
        )

with col3:
    if "Employment" in component_values:
        st.metric(
            "Employment",
            f"{component_values['Employment']:.0f}%"
        )

with col4:
    if "Housing & Wealth" in component_values:
        st.metric(
            "Housing & Wealth",
            f"{component_values['Housing & Wealth']:.0f}%"
        )

st.caption(
    f"Component parity scores for the latest available year ({latest_year})."
)

st.divider()


# -----------------------------------
# Component Trends
# -----------------------------------

st.header("All Economic Components Over Time")

st.write(
    "Compare how the four economic components changed "
    "across the available report years."
)

component_pivot = components.pivot_table(
    index="year",
    columns="indicator",
    values="value",
    aggfunc="mean"
).sort_index()

st.line_chart(component_pivot)

st.divider()


# -----------------------------------
# Change from First to Latest Report
# -----------------------------------

st.header("Economic Changes Across Report Years")

st.write(
    """
    This table shows the difference between the earliest
    and latest available score for each component.
    Positive values indicate an increase in the parity score;
    negative values indicate a decrease.
    """
)

component_changes = []

for indicator in indicators:
    indicator_data = components[
        components["indicator"] == indicator
    ].sort_values("year")

    if len(indicator_data) >= 2:
        first = indicator_data.iloc[0]
        latest = indicator_data.iloc[-1]

        change = latest["value"] - first["value"]

        component_changes.append({
            "Component": indicator,
            "Starting Year": int(first["year"]),
            "Starting Score": first["value"],
            "Latest Year": int(latest["year"]),
            "Latest Score": latest["value"],
            "Change (Percentage Points)": change
        })

changes_df = pd.DataFrame(component_changes)

if not changes_df.empty:
    changes_df["Starting Score"] = (
        changes_df["Starting Score"].round(1)
    )

    changes_df["Latest Score"] = (
        changes_df["Latest Score"].round(1)
    )

    changes_df["Change (Percentage Points)"] = (
        changes_df["Change (Percentage Points)"].round(1)
    )

    st.dataframe(
        changes_df,
        hide_index=True,
        use_container_width=True
    )

st.divider()


# -----------------------------------
# Key Findings
# -----------------------------------

st.header("Key Findings")

if not changes_df.empty:
    largest_improvement = changes_df.loc[
        changes_df["Change (Percentage Points)"].idxmax()
    ]

    largest_decline = changes_df.loc[
        changes_df["Change (Percentage Points)"].idxmin()
    ]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Largest Score Increase")

        st.metric(
            largest_improvement["Component"],
            f"{largest_improvement['Change (Percentage Points)']:+.0f} points"
        )

        st.write(
            "This component had the largest increase in its "
            "parity score across the available years."
        )

    with col2:
        st.subheader("Largest Score Decrease")

        st.metric(
            largest_decline["Component"],
            f"{largest_decline['Change (Percentage Points)']:+.0f} points"
        )

        st.write(
            "This component had the largest decrease in its "
            "parity score across the available years."
        )

st.info(
    """
    These comparisons describe changes in scores. They do not
    establish why the scores changed or prove that a particular
    policy, event, or condition caused the change.
    """
)

st.divider()


# -----------------------------------
# Questions for Further Analysis
# -----------------------------------

st.header("Questions for Further Analysis")

st.write(
    """
    The following questions can guide the next phase of the project:
    """
)

st.markdown(
    """
    - What factors might help explain changes in the Economics Index?
    - Why did the component scores move in different directions?
    - How do the underlying data years and definitions compare
      across the three reports?
    - Are neighborhood-level data available to reveal geographic
      differences within Chattanooga?
    - Which additional indicators could help explain changes in
      income, poverty, employment, and housing and wealth?
    - What further research would be needed before proposing
      policy recommendations?
    """
)

st.divider()


# -----------------------------------
# Data Tables
# -----------------------------------

with st.expander("View the underlying data"):
    st.subheader("Overall Economics Index Data")
    st.dataframe(
        economics,
        hide_index=True,
        use_container_width=True
    )

    st.subheader("Economic Component Data")
    st.dataframe(
        components,
        hide_index=True,
        use_container_width=True
    )

    st.download_button(
        label="Download component data as CSV",
        data=components.to_csv(index=False).encode("utf-8"),
        file_name="economics_components.csv",
        mime="text/csv"
    )


# -----------------------------------
# Footer
# -----------------------------------

st.caption(
    "State of Black Chattanooga | Economic Parity Analysis"
)
