
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
# Colors
# -----------------------------------

RED = "#E12B32"
WHITE = "#F5F5F5"
MUTED = "#B7B7B7"
PANEL = "#1C1C1C"
GRID = "#424242"

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
        "The data could not be loaded. Check that the "
        "CSV files exist in data/processed/ on GitHub."
    )
    st.exception(error)
    st.stop()


# -----------------------------------
# Clean and Validate Data
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

economics = (
    economics
    .dropna(subset=["year", "economics_index"])
    .sort_values("year")
)

components = (
    components
    .dropna(subset=["year", "indicator", "value"])
    .sort_values(["indicator", "year"])
)

if economics.empty or components.empty:
    st.error("The CSV files do not contain usable data.")
    st.stop()


# -----------------------------------
# Reusable Chart Styling
# -----------------------------------

def style_axis(ax):
    ax.set_facecolor(PANEL)
    ax.figure.set_facecolor(PANEL)

    ax.tick_params(colors=WHITE, labelsize=10)
    ax.xaxis.label.set_color(MUTED)
    ax.yaxis.label.set_color(MUTED)
    ax.title.set_color(WHITE)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)

    ax.grid(
        axis="y",
        color=GRID,
        linestyle="--",
        linewidth=0.7,
        alpha=0.7
    )

    ax.set_axisbelow(True)


# -----------------------------------
# Story Header
# -----------------------------------

st.markdown(
    f"""
    <div style="
        background: linear-gradient(120deg, #202020, #101010);
        border-left: 6px solid {RED};
        padding: 30px 30px 26px 30px;
        margin-bottom: 20px;
    ">
        <div style="
            color: {RED};
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 3px;
            margin-bottom: 14px;
        ">
            COMMUNITY DATA • ECONOMIC EQUITY
        </div>
        <div style="
            color: {WHITE};
            font-size: 38px;
            font-weight: 800;
            line-height: 1.12;
        ">
            STATE OF BLACK<br>CHATTANOOGA
        </div>
        <div style="
            color: #D0D0D0;
            font-size: 17px;
            margin-top: 16px;
            line-height: 1.6;
        ">
            Tracking economic parity. Understanding change.
            Identifying the questions that matter next.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    This project examines economic parity across the 2022,
    2024, and 2026 State of Black Chattanooga reports.
    Rather than looking at each number in isolation, the
    dashboard follows the overall trend, explores the
    components behind it, and identifies areas for deeper
    research.
    """
)

st.caption(
    "HOW TO READ THE DATA: These figures are parity index "
    "scores, not raw poverty, income, or employment rates. "
    "A score of 100 represents full Black–White parity. "
    "Report years may reflect different underlying data "
    "years or methodologies."
)

st.divider()


# -----------------------------------
# CHAPTER 1: The Big Picture
# -----------------------------------

st.markdown("### 01 / THE BIG PICTURE")
st.header("Has economic parity moved forward?")

first_row = economics.iloc[0]
latest_row = economics.iloc[-1]

starting_score = float(first_row["economics_index"])
latest_score = float(latest_row["economics_index"])
overall_change = latest_score - starting_score

first_year = int(first_row["year"])
latest_year = int(latest_row["year"])

if overall_change > 0:
    headline = "The overall index increased."
elif overall_change < 0:
    headline = "The overall index remains below its starting point."
else:
    headline = "The overall index is unchanged."

st.markdown(
    f"""
    <div style="
        background: {PANEL};
        border-top: 3px solid {RED};
        padding: 22px;
        margin-bottom: 16px;
    ">
        <div style="
            font-size: 12px;
            letter-spacing: 2px;
            color: {MUTED};
            font-weight: 700;
        ">
            THE CENTRAL FINDING
        </div>
        <div style="
            color: {WHITE};
            font-size: 25px;
            font-weight: 700;
            margin-top: 8px;
        ">
            {headline}
        </div>
        <div style="
            color: {MUTED};
            margin-top: 8px;
            line-height: 1.6;
        ">
            The Economics Index moved from {starting_score:.0f}
            in {first_year} to {latest_score:.0f} in {latest_year}.
            The overall change was {overall_change:+.0f} points.
            The component scores help show why looking at the
            overall index alone does not tell the whole story.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        f"Economics Index · {first_year}",
        f"{starting_score:.0f}"
    )

with col2:
    st.metric(
        f"Economics Index · {latest_year}",
        f"{latest_score:.0f}",
        delta=f"{overall_change:+.0f} points"
    )

with col3:
    st.metric(
        "Report Years Compared",
        f"{economics['year'].nunique()}"
    )

st.subheader("The overall trend")

fig, ax = plt.subplots(figsize=(10, 4.2))

ax.plot(
    economics["year"],
    economics["economics_index"],
    color=RED,
    marker="o",
    linewidth=3,
    markersize=9
)

for _, row in economics.iterrows():
    ax.annotate(
        f"{row['economics_index']:.0f}",
        (row["year"], row["economics_index"]),
        xytext=(0, 12),
        textcoords="offset points",
        color=WHITE,
        ha="center",
        fontweight="bold"
    )

ax.set_title(
    "Economics Index Across Report Years",
    loc="left",
    fontsize=15,
    fontweight="bold",
    pad=18
)

ax.set_xlabel("Report Year")
ax.set_ylabel("Parity Index Score")
ax.set_xticks(economics["year"].astype(int))
ax.set_ylim(0, 100)

style_axis(ax)
fig.tight_layout()

st.pyplot(fig)
plt.close(fig)

st.caption(
    "The index summarizes the overall economic parity measure. "
    "Changes in the score alone do not establish the reasons "
    "behind the trend."
)

st.divider()


# -----------------------------------
# CHAPTER 2: The Components Tell
# a More Complicated Story
# -----------------------------------

st.markdown("### 02 / BEHIND THE INDEX")
st.header("Four indicators. Different directions.")

st.write(
    """
    The overall index can conceal important differences.
    Income, poverty, employment, and housing and wealth
    do not necessarily move together. Comparing them helps
    identify where progress appears in the scores and where
    further investigation is warranted.
    """
)

preferred_order = [
    "Income",
    "Poverty",
    "Employment",
    "Housing & Wealth"
]

indicators = components["indicator"].unique().tolist()

indicators = [
    name for name in preferred_order if name in indicators
] + [
    name for name in indicators if name not in preferred_order
]

changes = []

for indicator in indicators:
    data = components[
        components["indicator"] == indicator
    ].sort_values("year")

    if len(data) >= 2:
        changes.append({
            "Component": indicator,
            "Starting score": float(data.iloc[0]["value"]),
            "Latest score": float(data.iloc[-1]["value"]),
            "Change": float(
                data.iloc[-1]["value"] - data.iloc[0]["value"]
            ),
            "Starting year": int(data.iloc[0]["year"]),
            "Latest year": int(data.iloc[-1]["year"])
        })

changes_df = pd.DataFrame(changes)

for start in range(0, len(changes_df), 2):
    cols = st.columns(2)

    for offset, (_, row) in enumerate(
        changes_df.iloc[start:start + 2].iterrows()
    ):
        with cols[offset]:
            direction = (
                "increase in score"
                if row["Change"] > 0
                else "decrease in score"
                if row["Change"] < 0
                else "no change in score"
            )

            st.markdown(
                f"""
                <div style="
                    background: {PANEL};
                    border-left: 4px solid {RED};
                    padding: 18px;
                    margin-bottom: 12px;
                    min-height: 155px;
                ">
                    <div style="
                        color: {MUTED};
                        font-size: 12px;
                        letter-spacing: 1.5px;
                        text-transform: uppercase;
                    ">
                        {row['Component']}
                    </div>
                    <div style="
                        color: {WHITE};
                        font-size: 31px;
                        font-weight: 750;
                        margin: 8px 0;
                    ">
                        {row['Latest score']:.0f}
                        <span style="
                            color: {MUTED};
                            font-size: 15px;
                            font-weight: 400;
                        "> / 100</span>
                    </div>
                    <div style="
                        color: {RED if row['Change'] < 0 else WHITE};
                        font-size: 14px;
                        font-weight: 600;
                    ">
                        {row['Change']:+.0f} points
                        <span style="
                            color: {MUTED};
                            font-weight: 400;
                        "> since {row['Starting year']}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

st.subheader("Comparing the four components")

pivot = components.pivot_table(
    index="year",
    columns="indicator",
    values="value",
    aggfunc="mean"
).sort_index()

fig, ax = plt.subplots(figsize=(10, 5))

for indicator in indicators:
    if indicator in pivot.columns:
        ax.plot(
            pivot.index,
            pivot[indicator],
            marker="o",
            linewidth=2.5,
            markersize=6,
            label=indicator
        )

ax.set_title(
    "Parity Scores by Economic Component",
    loc="left",
    fontsize=15,
    fontweight="bold",
    pad=18
)

ax.set_xlabel("Report Year")
ax.set_ylabel("Parity Index Score")
ax.set_xticks(pivot.index.astype(int))
ax.set_ylim(0, 100)

style_axis(ax)

legend = ax.legend(
    frameon=False,
    ncol=2,
    labelcolor=WHITE
)

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.markdown(
    """
    **What stands out?**

    The component trends move in different directions.
    Housing & Wealth and Employment show higher scores in
    the latest report than in the earliest report, while
    Poverty shows a lower parity score. Income also ends
    below its starting score.

    These are descriptive findings. They do not, by
    themselves, explain what caused the changes.
    """
)

st.divider()


# -----------------------------------
# CHAPTER 3: Explore the Evidence
# -----------------------------------

st.markdown("### 03 / EXPLORE THE EVIDENCE")
st.header("Take a closer look")

st.write(
    """
    Choose an indicator to follow its score across the
    available report years. Use this section to examine
    the numbers behind the overall findings.
    """
)

selected_indicator = st.selectbox(
    "Select an economic component",
    indicators
)

selected_data = components[
    components["indicator"] == selected_indicator
].sort_values("year")

first_component = selected_data.iloc[0]
latest_component = selected_data.iloc[-1]

component_change = (
    float(latest_component["value"])
    - float(first_component["value"])
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Latest score",
        f"{latest_component['value']:.0f}"
    )

with col2:
    st.metric(
        "Change across available years",
        f"{component_change:+.0f} points"
    )

with col3:
    st.metric(
        "First score",
        f"{first_component['value']:.0f}"
    )

fig, ax = plt.subplots(figsize=(10, 4))

ax.plot(
    selected_data["year"],
    selected_data["value"],
    color=RED,
    marker="o",
    linewidth=3,
    markersize=9
)

for _, row in selected_data.iterrows():
    ax.annotate(
        f"{row['value']:.0f}",
        (row["year"], row["value"]),
        xytext=(0, 10),
        textcoords="offset points",
        color=WHITE,
        ha="center",
        fontweight="bold"
    )

ax.set_title(
    f"{selected_indicator}: Score Over Time",
    loc="left",
    fontsize=15,
    fontweight="bold",
    pad=18
)

ax.set_xlabel("Report Year")
ax.set_ylabel("Parity Index Score")
ax.set_xticks(selected_data["year"].astype(int))
ax.set_ylim(0, 100)

style_axis(ax)
fig.tight_layout()

st.pyplot(fig)
plt.close(fig)

display_data = selected_data[
    ["year", "indicator", "value"]
].rename(
    columns={
        "year": "Report Year",
        "indicator": "Component",
        "value": "Parity Score"
    }
)

display_data["Report Year"] = (
    display_data["Report Year"].astype(int)
)

st.dataframe(
    display_data,
    hide_index=True,
    use_container_width=True
)

st.download_button(
    "Download this component's data",
    data=display_data.to_csv(index=False).encode("utf-8"),
    file_name=(
        selected_indicator.lower()
        .replace(" ", "_")
        .replace("&", "and")
        + "_trend.csv"
    ),
    mime="text/csv"
)

st.divider()


# -----------------------------------
# CHAPTER 4: What Needs More Attention?
# -----------------------------------

st.markdown("### 04 / WHAT COMES NEXT")
st.header("The numbers raise new questions")

if not changes_df.empty:
    largest_increase = changes_df.loc[
        changes_df["Change"].idxmax()
    ]

    largest_decrease = changes_df.loc[
        changes_df["Change"].idxmin()
    ]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div style="
                background: {PANEL};
                padding: 20px;
                border-top: 3px solid {RED};
                min-height: 190px;
            ">
                <div style="
                    color: {MUTED};
                    font-size: 12px;
                    letter-spacing: 1.5px;
                ">
                    LARGEST INCREASE IN SCORE
                </div>
                <div style="
                    color: {WHITE};
                    font-size: 26px;
                    font-weight: 700;
                    margin-top: 12px;
                ">
                    {largest_increase['Component']}
                </div>
                <div style="
                    color: {WHITE};
                    font-size: 19px;
                    margin-top: 5px;
                ">
                    +{largest_increase['Change']:.0f} points
                </div>
                <div style="
                    color: {MUTED};
                    font-size: 13px;
                    margin-top: 10px;
                ">
                    This component recorded the largest
                    score increase across the available years.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style="
                background: {PANEL};
                padding: 20px;
                border-top: 3px solid {RED};
                min-height: 190px;
            ">
                <div style="
                    color: {MUTED};
                    font-size: 12px;
                    letter-spacing: 1.5px;
                ">
                    LARGEST DECREASE IN SCORE
                </div>
                <div style="
                    color: {WHITE};
                    font-size: 26px;
                    font-weight: 700;
                    margin-top: 12px;
                ">
                    {largest_decrease['Component']}
                </div>
                <div style="
                    color: {RED};
                    font-size: 19px;
                    margin-top: 5px;
                ">
                    {largest_decrease['Change']:.0f} points
                </div>
                <div style="
                    color: {MUTED};
                    font-size: 13px;
                    margin-top: 10px;
                ">
                    This component recorded the largest
                    score decrease across the available years.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.write("")

st.subheader("Questions for the next phase of research")

questions = [
    (
        "Data comparability",
        "Do the reports use the same underlying data years, "
        "definitions, and calculation methods?"
    ),
    (
        "Neighborhood differences",
        "Can these trends be examined at a neighborhood level "
        "within Chattanooga or Hamilton County?"
    ),
    (
        "Understanding the changes",
        "What additional data would help explain why individual "
        "parity scores changed?"
    ),
    (
        "Policy and community response",
        "What evidence would be needed to evaluate possible "
        "programs or policy responses?"
    )
]

for title, question in questions:
    with st.expander(title):
        st.write(question)

st.divider()


# -----------------------------------
# REPORTS & PUBLICATIONS
# -----------------------------------

st.markdown("### 05 / GO TO THE SOURCE")
st.header("Reports & Publications")

st.markdown(
    """
    The findings in this dashboard should be read alongside
    the original reports. Explore the publications below to
    learn more about the data, methodology, and community
    conditions discussed in the State of Black Chattanooga
    reports.
    """
)

st.markdown(
    """
    <div style="
        background: linear-gradient(120deg, #242424, #111111);
        border-left: 5px solid #E12B32;
        padding: 24px;
        margin: 12px 0 22px 0;
    ">
        <div style="
            color: #E12B32;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 2px;
        ">
            OFFICIAL PUBLICATIONS
        </div>
        <div style="
            color: #F5F5F5;
            font-size: 23px;
            font-weight: 750;
            margin-top: 8px;
        ">
            Go beyond the dashboard.
        </div>
        <div style="
            color: #B7B7B7;
            font-size: 15px;
            line-height: 1.6;
            margin-top: 8px;
        ">
            Read the original research from the Urban League
            of Greater Chattanooga and explore the context
            behind the data.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### State of Black Chattanooga 2024")
    st.write(
        "The report examines economic, educational, health, "
        "and social outcomes for Black residents in "
        "Chattanooga and Hamilton County."
    )
    st.link_button(
        "Read the 2024 Report",
        "https://www.ulchatt.net/s/state-of-black-chattanooga-2024-BOOK-FINAL-01.pdf",
        use_container_width=True
    )

with col2:
    st.markdown("#### State of Black Chattanooga 2022")
    st.write(
        "Review the earlier report to compare findings "
        "and investigate changes across reporting periods."
    )
    st.link_button(
        "Read the 2022 Report",
        "https://www.ulchatt.net/s/UL-State-of-Black-Chattanooga-Booklet-20221.pdf",
        use_container_width=True
    )

st.markdown("")

st.link_button(
    "Visit the Official Reports & Publications Page",
    "https://www.ulchatt.net/reports/",
    use_container_width=True
)

st.caption(
    "Source: Urban League of Greater Chattanooga. "
    "The dashboard's report-year labels do not necessarily "
    "represent the underlying data collection years."
)

st.divider()

# -----------------------------------
# Methodology and Source Data
# -----------------------------------

st.markdown("### METHODOLOGY & TRANSPARENCY")

st.write(
    """
    This dashboard compares values recorded in the project's
    processed CSV files. The comparisons describe differences
    between reported scores; they do not establish causation.
    Before drawing stronger conclusions, the underlying report
    sources, data years, definitions, and index methodology
    should be checked for comparability.
    """
)

with st.expander("View the underlying datasets"):
    st.subheader("Overall Economics Index")
    st.dataframe(
        economics,
        hide_index=True,
        use_container_width=True
    )

    st.subheader("Economic Components")
    st.dataframe(
        components,
        hide_index=True,
        use_container_width=True
    )

    st.download_button(
        "Download all component data",
        data=components.to_csv(index=False).encode("utf-8"),
        file_name="economics_components.csv",
        mime="text/csv"
    )

st.caption(
    "State of Black Chattanooga | Economic Parity Analysis"
)
