import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="State of Black Chattanooga",
    page_icon="📊",
    layout="wide",
)

RED = "#E12B32"
WHITE = "#F5F5F5"
MUTED = "#B7B7B7"
PANEL = "#1C1C1C"
GRID = "#424242"

st.markdown("""
<style>
    .stApp { background: #101010; }
    .block-container { padding-top: 2rem; padding-bottom: 3rem; }
    h1, h2, h3 { letter-spacing: -0.02em; }
    div[data-testid="stMetric"] {
        background: #1C1C1C; border-top: 3px solid #E12B32;
        padding: 16px; border-radius: 4px;
    }
    div[data-testid="stMetricLabel"] { color: #B7B7B7; }
    .eyebrow { color: #E12B32; letter-spacing: 2px; font-size: 12px; font-weight: 800; }
    .hero {
        background: linear-gradient(120deg, #242424, #101010);
        border-left: 6px solid #E12B32; padding: 28px 30px;
        margin-bottom: 20px;
    }
    .hero h1 { color: #F5F5F5; font-size: 38px; margin: 8px 0; }
    .hero p { color: #D0D0D0; font-size: 16px; line-height: 1.6; }
    .insight {
        background: #1C1C1C; border-left: 4px solid #E12B32;
        padding: 16px 18px; margin: 8px 0 16px 0;
    }
    .small-note { color: #B7B7B7; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

def style_axis(ax):
    ax.set_facecolor("#1B1B1B")
    ax.figure.set_facecolor("#1B1B1B")
    ax.tick_params(axis="both", colors="#E6E6E6", labelsize=10)
    ax.xaxis.label.set_color("#D6D6D6")
    ax.yaxis.label.set_color("#D6D6D6")
    ax.grid(axis="y", color=GRID, linewidth=0.7, alpha=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color("#666666")
    ax.spines["bottom"].set_color("#666666")
    ax.title.set_color(WHITE)

def chart_theme(fig, ax):
    style_axis(ax)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

st.markdown("""
<div class="hero">
  <div class="eyebrow">COMMUNITY DATA • 2026 SNAPSHOT</div>
  <h1>STATE OF BLACK CHATTANOOGA</h1>
  <p>What the latest Equality Index reveals about economic opportunity and education in Hamilton County—and where the gaps remain.</p>
</div>
""", unsafe_allow_html=True)

st.caption(
    "Source: State of Black Chattanooga 2026, S&P Global Market Intelligence. "
    "The report's 2026 update uses 2024 Census data for many measures; earlier index "
    "periods use different underlying data years. Report-year comparisons should be read with that limitation in mind."
)

# Data below are transcribed from the 2026 report's summary charts and narrative.
index_trend = pd.DataFrame({
    "Report year": [2022, 2024, 2026],
    "Overall Equality Index": [61, 61, 60],
    "Economics Index": [60, 58, 59],
    "Education Index": [60, 60, 55],
    "Health Index": [64, 66, 67],
})

econ_2026 = pd.DataFrame({
    "Economic component": ["Employment Issues", "Income", "Housing & Wealth", "Poverty"],
    "Parity score": [83, 63, 54, 31],
    "Weight within economics index": [20, 40, 20, 20],
})

education_index_trend = pd.DataFrame({
    "Report year": [2022, 2024, 2026],
    "Education Index": [60, 60, 55],
})

# 2026 report's stated outcomes; underlying observation year is usually 2024.
education_snapshot = pd.DataFrame([
    {"Indicator": "Children under 5 enrolled in preschool/nursery", "Black residents": 15, "White residents": 29, "Unit": "%", "Data year": 2024},
    {"Indicator": "Population ages 18–29 enrolled in college/graduate program", "Black residents": 40, "White residents": 41, "Unit": "%", "Data year": 2024},
    {"Indicator": "Population with a bachelor's degree", "Black residents": 10, "White residents": 28, "Unit": "%", "Data year": "2026 report summary"},
    {"Indicator": "Students performing on grade level on TNReady", "Black residents": 23, "White residents": 60, "Unit": "%", "Data year": "2026 report summary"},
    {"Indicator": "Ready Graduate rate", "Black residents": 47, "White residents": 73, "Unit": "%", "Data year": "2026 report summary"},
])

tab_overview, tab_economics, tab_education, tab_method = st.tabs([
    "2026 Overview", "Economics & Wealth", "Education", "Sources & Methodology"
])

with tab_overview:
    st.markdown('<div class="eyebrow">01 / THE BIG PICTURE</div>', unsafe_allow_html=True)
    st.header("Equality remains below parity")
    st.write(
        "The 2026 report places the overall Greater Chattanooga Equality Index at 60% of full "
        "Black–White parity, down one point from 2024. The headline score hides different patterns "
        "across economics, education, and health."
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Overall Equality Index", "60%", "−1 point vs. 2024")
    c2.metric("Economics Index", "59%", "45% of overall index")
    c3.metric("Education Index", "55%", "−5 points vs. 2024")

    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(index_trend["Report year"], index_trend["Overall Equality Index"], color=WHITE,
            marker="o", linewidth=2.8, markersize=7, label="Overall")
    ax.plot(index_trend["Report year"], index_trend["Economics Index"], color=RED,
            marker="o", linewidth=2.4, markersize=6, label="Economics")
    ax.plot(index_trend["Report year"], index_trend["Education Index"], color="#D9BFA3",
            marker="o", linewidth=2.4, markersize=6, label="Education")
    ax.plot(index_trend["Report year"], index_trend["Health Index"], color="#66B3B0",
            marker="o", linewidth=2.4, markersize=6, label="Health")
    ax.set_title("Three pillars, three different trajectories", loc="left", fontsize=16,
                 fontweight="bold", color=WHITE, pad=16)
    ax.set_xlabel("Report year")
    ax.set_ylabel("Parity index score")
    ax.set_xticks([2022, 2024, 2026])
    ax.set_ylim(45, 72)
    style_axis(ax)
    ax.legend(frameon=False, ncol=4, labelcolor=WHITE)
    chart_theme(fig, ax)

    st.markdown("""
    <div class="insight"><b>What stands out</b><br>
    Health has improved across the three reports, economics has changed only modestly,
    and education has fallen to 55% parity in 2026. The report says the overall index has
    made no net gain since 2022.</div>
    """, unsafe_allow_html=True)
    st.caption("The report labels 2022, 2024, and 2026 as pre-COVID, COVID, and post-COVID comparison periods. Underlying data years differ.")

with tab_economics:
    st.markdown('<div class="eyebrow">02 / ECONOMICS & WEALTH</div>', unsafe_allow_html=True)
    st.header("Employment is comparatively strong; poverty parity is weakest")
    st.write(
        "Rather than repeating the overall index in several charts, this section focuses on the "
        "2026 breakdown and the different economic conditions it points toward."
    )
    fig, ax = plt.subplots(figsize=(9, 4.4))
    plot_data = econ_2026.sort_values("Parity score")
    bars = ax.barh(plot_data["Economic component"], plot_data["Parity score"], color=RED, height=0.58)
    ax.set_title("2026 economic component scores", loc="left", fontsize=16, fontweight="bold",
                 color=WHITE, pad=16)
    ax.set_xlabel("Parity score (100 = full parity)")
    ax.set_xlim(0, 100)
    for bar, value in zip(bars, plot_data["Parity score"]):
        ax.text(value + 1.5, bar.get_y() + bar.get_height()/2, f"{value}%",
                va="center", color=WHITE, fontweight="bold")
    style_axis(ax)
    ax.grid(axis="x", color=GRID, linewidth=0.7, alpha=0.8)
    ax.grid(axis="y", visible=False)
    chart_theme(fig, ax)

    left, right = st.columns(2)
    with left:
        st.metric("Highest component", "Employment · 83%")
        st.write("The report identifies employment as the strongest economic sub-pillar.")
    with right:
        st.metric("Lowest component", "Poverty · 31%")
        st.write("The report identifies poverty as the area with the greatest economic disparity.")
    st.markdown("""
    <div class="insight"><b>Question worth investigating</b><br>
    The report notes that employment parity is relatively stronger than poverty parity.
    This suggests that having employment and achieving economic security are not the same thing.
    The index alone cannot establish the reasons; occupation, wages, hours, and household costs
    would be useful next measures to examine.</div>
    """, unsafe_allow_html=True)

    with st.expander("Historical context: economic index"):
        fig, ax = plt.subplots(figsize=(8, 3.4))
        ax.plot(index_trend["Report year"], index_trend["Economics Index"], color=RED,
                marker="o", linewidth=3, markersize=8)
        for _, row in index_trend.iterrows():
            ax.annotate(f"{row['Economics Index']}%", (row["Report year"], row["Economics Index"]),
                        xytext=(0, 10), textcoords="offset points", color=WHITE, ha="center")
        ax.set_title("Economics index: 2022–2026", loc="left", fontsize=15, fontweight="bold", color=WHITE)
        ax.set_xlabel("Report year")
        ax.set_ylabel("Parity score")
        ax.set_xticks([2022, 2024, 2026])
        ax.set_ylim(45, 70)
        chart_theme(fig, ax)
        st.caption("2022: 60%; 2024: 58%; 2026: 59%, according to the report.")

with tab_education:
    st.markdown('<div class="eyebrow">03 / EDUCATION & OPPORTUNITY</div>', unsafe_allow_html=True)
    st.header("Education is the clearest area of concern in the 2026 index")
    st.write(
        "Education represents 30% of the overall Equality Index. Its parity score fell to 55% in 2026, "
        "reversing the gains shown in 2024. The report breaks education into student risk factors, "
        "post-secondary attainment, scores, and education quality."
    )
    c1, c2, c3 = st.columns(3)
    c1.metric("Education Index", "55%", "−5 points vs. 2024")
    c2.metric("Bachelor's degree", "10% Black", "vs. 28% White")
    c3.metric("TNReady on grade level", "23% Black", "vs. 60% White")

    fig, ax = plt.subplots(figsize=(9, 4.2))
    ax.plot(education_index_trend["Report year"], education_index_trend["Education Index"],
            color=RED, marker="o", linewidth=3, markersize=8)
    for _, row in education_index_trend.iterrows():
        ax.annotate(f"{row['Education Index']}%", (row["Report year"], row["Education Index"]),
                    xytext=(0, 10), textcoords="offset points", color=WHITE, ha="center", fontweight="bold")
    ax.set_title("Education parity has declined in the latest report", loc="left", fontsize=16,
                 fontweight="bold", color=WHITE, pad=16)
    ax.set_xlabel("Report year")
    ax.set_ylabel("Education parity score")
    ax.set_xticks([2022, 2024, 2026])
    ax.set_ylim(40, 70)
    chart_theme(fig, ax)

    st.subheader("A closer look at selected education outcomes")
    st.write("These measures are not the same thing: some describe access, others attainment or school outcomes.")
    selected_edu = st.selectbox("Choose an education indicator", education_snapshot["Indicator"].tolist())
    row = education_snapshot.loc[education_snapshot["Indicator"] == selected_edu].iloc[0]
    a, b, c = st.columns(3)
    a.metric("Black residents/students", f"{row['Black residents']}%")
    b.metric("White residents/students", f"{row['White residents']}%")
    c.metric("Difference", f"{row['White residents'] - row['Black residents']} points")
    fig, ax = plt.subplots(figsize=(7, 3.3))
    labels = ["Black", "White"]
    values = [row["Black residents"], row["White residents"]]
    bars = ax.bar(labels, values, color=[RED, "#B7B7B7"], width=0.52)
    ax.set_title(selected_edu, loc="left", fontsize=14, fontweight="bold", color=WHITE, pad=14)
    ax.set_ylabel("Share (%)")
    ax.set_ylim(0, max(values) * 1.25 + 2)
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.7, f"{value}%",
                ha="center", color=WHITE, fontweight="bold")
    style_axis(ax)
    ax.grid(axis="y", color=GRID, linewidth=0.7, alpha=0.8)
    chart_theme(fig, ax)
    st.caption(f"Source: State of Black Chattanooga 2026. Data-year note: {row['Data year']}.")
    st.markdown("""
    <div class="insight"><b>What the report says</b><br>
    The report describes significant disparities in TNReady proficiency and bachelor's-degree
    attainment. It also reports that Black students are nearly twice as likely to be chronically
    absent and four times as likely to be suspended. These findings point to distinct questions
    about learning outcomes, educational access, and student risk factors.</div>
    """, unsafe_allow_html=True)
    st.caption("The 2026 report's selected outcomes are shown as reported. Do not treat them as a complete measure of school quality or as proof of cause.")

with tab_method:
    st.markdown('<div class="eyebrow">04 / SOURCES & METHODOLOGY</div>', unsafe_allow_html=True)
    st.header("Read the original research")
    st.write(
        "This dashboard summarizes selected findings from the State of Black Chattanooga 2026 report "
        "prepared by S&P Global Market Intelligence. The report describes the geography as Hamilton County."
    )
    st.link_button("Open the Urban League of Greater Chattanooga reports page",
                   "https://www.ulchatt.net/reports/", use_container_width=True)
    st.link_button("Read the State of Black Chattanooga 2024 report",
                   "https://www.ulchatt.net/s/state-of-black-chattanooga-2024-BOOK-FINAL-01.pdf",
                   use_container_width=True)
    st.link_button("Read the State of Black Chattanooga 2022 report",
                   "https://www.ulchatt.net/s/UL-State-of-Black-Chattanooga-Booklet-20221.pdf",
                   use_container_width=True)
    st.subheader("How to interpret the index")
    st.markdown("""
    - **100% means full parity** between Black and White residents for the index measure.
    - The 2026 overall index combines Economics (45%), Education (30%), and Health (25%).
    - The economic component weights are Income (40%), Poverty (20%), Employment Issues (20%), and Housing & Wealth (20%).
    - Index scores are not raw rates. For example, a poverty parity score of 31% does **not** mean 31% of Black residents live in poverty.
    - The report notes that the 2026 update uses 2024 Census data; 2024 and 2022 report periods use earlier underlying data. Comparisons should be interpreted cautiously.
    - The dashboard presents descriptive comparisons and does not establish causation.
    """)
    with st.expander("Data used in the dashboard"):
        st.subheader("Index trend data")
        st.dataframe(index_trend, hide_index=True, use_container_width=True)
        st.download_button("Download index trend CSV", index_trend.to_csv(index=False).encode("utf-8"),
                           "equality_index_trend.csv", "text/csv")
        st.subheader("2026 economic components")
        st.dataframe(econ_2026, hide_index=True, use_container_width=True)
        st.download_button("Download economic components CSV", econ_2026.to_csv(index=False).encode("utf-8"),
                           "economics_2026.csv", "text/csv")
        st.subheader("Selected education indicators")
        st.dataframe(education_snapshot, hide_index=True, use_container_width=True)
        st.download_button("Download education indicators CSV", education_snapshot.to_csv(index=False).encode("utf-8"),
                           "education_2026.csv", "text/csv")

st.divider()
st.caption("State of Black Chattanooga • Independent student data project • Source: State of Black Chattanooga 2026, S&P Global Market Intelligence")
