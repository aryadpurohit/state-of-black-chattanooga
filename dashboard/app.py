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

tab_overview, tab_economics, tab_health, tab_education, tab_population, tab_work, tab_justice, tab_explore, tab_method = st.tabs([
    "2026 Overview", "Economics & Wealth", "Health", "Education", "Population",
    "Work & Industry", "Social Justice", "Explore the Data", "Sources & Methodology"
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

with tab_health:
    st.markdown('<div class="eyebrow">04 / HEALTH & WELLBEING</div>', unsafe_allow_html=True)
    st.header("Health is the strongest index pillar—but progress is uneven")
    st.write("Health accounts for 25% of the overall Equality Index. The 2026 health score reached 67%, up from 64% in 2022 and 66% in 2024. The report cautions that a modest overall gain can hide worsening outcomes in specific areas.")
    health_components = pd.DataFrame([
        {"Health component": "Health Insurance", "Weight in health index (%)": 10, "2026 parity score (%)": 99},
        {"Health component": "Contagious disease", "Weight in health index (%)": 25, "2026 parity score (%)": 36},
        {"Health component": "Chronic disease and cancer", "Weight in health index (%)": 30, "2026 parity score (%)": 76},
        {"Health component": "Accidental and non-accidental death", "Weight in health index (%)": 15, "2026 parity score (%)": 77},
        {"Health component": "Maternal and infant health issues", "Weight in health index (%)": 20, "2026 parity score (%)": 69},
    ])
    fig, ax = plt.subplots(figsize=(9, 4.4))
    hp = health_components.sort_values("2026 parity score (%)")
    bars = ax.barh(hp["Health component"], hp["2026 parity score (%)"], color=RED, height=.58)
    ax.set_title("2026 health component parity scores", loc="left", fontsize=16, fontweight="bold", color=WHITE, pad=16)
    ax.set_xlabel("Parity score (100 = full parity)"); ax.set_xlim(0, 110)
    for bar, value in zip(bars, hp["2026 parity score (%)"]):
        ax.text(value+1.5, bar.get_y()+bar.get_height()/2, f"{value}%", va="center", color=WHITE, fontweight="bold")
    style_axis(ax); ax.grid(axis="x", color=GRID, linewidth=.7); ax.grid(axis="y", visible=False); chart_theme(fig, ax)
    st.caption("Weights and scores transcribed from the 2026 report, page 9. Component scores are parity scores, not raw rates.")
    h1, h2 = st.columns(2)
    h1.metric("Highest component", "Insurance · 99%")
    h2.metric("Lowest component", "Contagious disease · 36%")
    st.subheader("What the report highlights")
    st.markdown("""
    - **Maternal and infant health:** premature-birth and low-birthweight rates for Black mothers declined; maternal tobacco use among births fell from 6.9% to 2.7%. The report says Black mothers still lag on nearly every indicator in this category.
    - **Chronic disease:** heart-disease mortality, diabetes mortality, and prostate-cancer mortality increased for Black residents; heart-disease and stroke gaps widened.
    - **Insurance:** the share of Black residents without insurance declined from 9.1% to 7.3%.
    - **Communicable disease:** HIV/AIDS, gonorrhea, and chlamydia rates declined for Black residents, while the report says the syphilis rate increased nearly fivefold amid a broader 2023 outbreak.
    - **Deaths and accidents:** the report flags motor-vehicle and other accidental deaths as areas where outcomes moved away from parity.
    """)
    with st.expander("Health measures tracked in the report"):
        st.markdown("**Maternal and infant health:** prenatal care; premature births; low birthweight; teen pregnancies; infant mortality; smoking during pregnancy; live births when mother is unmarried.\n\n**Accidental and non-accidental death:** life expectancy; total mortality; years of potential life lost before 75; motor-vehicle mortality; accident mortality; suicide mortality; homicide.\n\n**Chronic disease and cancer:** Alzheimer’s; chronic lower respiratory disease; heart disease; stroke; diabetes; hypertension; kidney disease; cancer mortality and incidence (including lung, prostate, colon, breast, and pancreatic cancer); chronic-disease survey measures.\n\n**Contagious disease:** HIV/AIDS, gonorrhea, chlamydia, syphilis, influenza/pneumonia, and COVID-related measures.\n\n**Health insurance:** uninsured population, uninsured children under 6, private insurance, and public insurance.")

with tab_population:
    st.markdown('<div class="eyebrow">05 / POPULATION</div>', unsafe_allow_html=True)
    st.header("Population trends provide important context")
    st.write("The report includes Hamilton County population trends by race alongside the Equality Index. These counts and growth rates are context—not an additional Equality Index pillar.")
    pop = pd.DataFrame([
        {"Population measure": "Average annual growth, 2019–2024", "Group": "White (one race)", "Rate (%)": -0.21},
        {"Population measure": "Average annual growth, 2019–2024", "Group": "Black or African American (one race)", "Rate (%)": -1.62},
        {"Population measure": "Compound annual growth, 2018–2024", "Group": "White alone or in combination (ACOMR)", "Rate (%)": 0.88},
        {"Population measure": "Compound annual growth, 2018–2024", "Group": "Black alone or in combination (ACOMR)", "Rate (%)": -0.10},
        {"Population measure": "Compound annual growth, 2018–2024", "Group": "White alone, not Hispanic or Latino (NHL)", "Rate (%)": 0.26},
        {"Population measure": "Compound annual growth, 2018–2024", "Group": "Black alone, not Hispanic or Latino (NHL)", "Rate (%)": -1.19},
    ])
    fig, ax = plt.subplots(figsize=(9, 4.1))
    colors = [RED if v < 0 else "#B7B7B7" for v in pop["Rate (%)"]]
    bars = ax.barh(pop["Group"], pop["Rate (%)"], color=colors, height=.62)
    ax.axvline(0, color="#DDDDDD", linewidth=.8)
    ax.set_title("Population growth rates reported by S&P Global", loc="left", fontsize=15, fontweight="bold", color=WHITE, pad=14)
    ax.set_xlabel("Annual growth rate (%)")
    for bar, value in zip(bars, pop["Rate (%)"]):
        ax.text(value + (0.06 if value >= 0 else -0.06), bar.get_y()+bar.get_height()/2, f"{value:.2f}%", va="center", ha="left" if value >= 0 else "right", color=WHITE)
    style_axis(ax); ax.grid(axis="x", color=GRID, linewidth=.7); ax.grid(axis="y", visible=False); chart_theme(fig, ax)
    st.dataframe(pop, hide_index=True, use_container_width=True)
    st.markdown("""
    <div class="insight"><b>Report takeaway</b><br>
    From 2019 to 2024, the report estimates average annual population growth of −0.21% for White residents (one race) and −1.62% for Black residents (one race). It also notes that the White population rebounded more strongly after 2021, while the Black population's trend remained downward overall.</div>
    """, unsafe_allow_html=True)
    st.caption("ACOMR means alone or in combination with one or more races; NHL means not Hispanic or Latino. These are the report's stated growth rates, not independently recalculated estimates.")

with tab_work:
    st.markdown('<div class="eyebrow">06 / WORK, OCCUPATIONS & INDUSTRY</div>', unsafe_allow_html=True)
    st.header("Employment parity does not tell the whole labor-market story")
    st.write("The report pairs an 83% employment parity score with a discussion of differences in occupation and projected industry mix. It suggests these patterns are useful context when examining why employment parity is stronger than income and poverty parity.")
    st.subheader("Occupations differ by race (2023)")
    occ = pd.DataFrame([
        {"Occupation group": "Management, business, and financial", "Report describes White share as higher": True},
        {"Occupation group": "Computer, engineering, and science", "Report describes White share as higher": True},
        {"Occupation group": "Education, legal, community service, arts, and media", "Report describes White share as higher": True},
        {"Occupation group": "Healthcare", "Report describes White share as higher": True},
        {"Occupation group": "Natural resources, construction, and maintenance", "Report describes White share as higher": True},
        {"Occupation group": "Service occupations", "Report describes White share as higher": False},
        {"Occupation group": "Sales and office", "Report describes White share as higher": False},
        {"Occupation group": "Production, transportation, and material moving", "Report describes White share as higher": False},
    ])
    occ["Pattern described in report"] = occ["Report describes White share as higher"].map({True:"White residents more likely",False:"Black residents more likely"})
    st.dataframe(occ[["Occupation group", "Pattern described in report"]], hide_index=True, use_container_width=True)
    st.subheader("Projected industry mix")
    st.markdown("The report's Chattanooga, TN–GA forecast says transportation, trade, and utilities are projected to decline from 18% of employment in 2025 to 16% in 2036. Retail/trade is projected to decline by about one percentage point, leisure and hospitality to increase by about one point, and financial activities to decline by about one point as shares of total employment.")
    with st.expander("Economic measures listed in the report glossary"):
        st.markdown("**Income:** median household income; median male weekly earnings; median female weekly earnings; median family income.\n\n**Poverty:** residents below the poverty line; below 50% and 125% of poverty; below poverty among children under 18, adults 18–64, and adults 65+; SNAP/food-stamp benefits; cash public assistance income.\n\n**Employment:** unemployment rate; labor-force participation; employment-to-population ratio; not in labor force; salaried employment.\n\n**Housing and wealth:** median home value; public transportation to work; employer businesses per adult population; overcrowding in owner- and renter-occupied units; average household size; owner-occupied and renter-occupied housing.")
    st.caption("The occupation page provides charted comparisons, but this dashboard only states directional findings from the report narrative rather than inventing exact bar values.")

with tab_justice:
    st.markdown('<div class="eyebrow">07 / SOCIAL JUSTICE</div>', unsafe_allow_html=True)
    st.header("The report examines arrests and policing data")
    st.write("The Social Justice section includes the Black share of Black-and-White arrests by offense for 2024–2026, plus a per-capita comparison for 2024. These measures describe arrest data; they do not, by themselves, establish the causes of differences or the prevalence of offending.")
    st.metric("2024 arrest rate per capita", "≈2×", "Black residents vs. White residents")
    st.caption("The report's page 20 chart lists 1.6% for Black residents and 0.8% for White residents. Data compiled July 31, 2026; sources: FBI Crime Data and ACS.")
    st.subheader("Selected arrest-share trends shown in the report")
    arrest_rows = [
        {"Offense": "Aggravated assault", "2024": 48, "2025": 50, "2026": 37},
        {"Offense": "All other larceny", "2024": 15, "2025": 16, "2026": 28},
        {"Offense": "Counterfeiting/forgery", "2024": 19, "2025": 22, "2026": 12},
        {"Offense": "Credit card / ATM fraud", "2024": 36, "2025": 14, "2026": 25},
        {"Offense": "Criminal sexual crime", "2024": 61, "2025": 49, "2026": 36},
        {"Offense": "Drug equipment violations", "2024": 18, "2025": 19, "2026": 16},
        {"Offense": "Drug narcotic violations", "2024": 28, "2025": 30, "2026": 32},
        {"Offense": "False pretenses / swindle", "2024": 35, "2025": 17, "2026": 9},
        {"Offense": "Impersonation", "2024": 37, "2025": 29, "2026": 17},
        {"Offense": "Intimidation", "2024": 40, "2025": 51, "2026": 46},
        {"Offense": "Larceny-theft", "2024": 29, "2025": 16, "2026": 15},
        {"Offense": "Motor vehicle theft", "2024": 44, "2025": 17, "2026": 13},
        {"Offense": "Simple assault", "2024": 40, "2025": 44, "2026": 51},
        {"Offense": "Weapon law violations", "2024": 57, "2025": 60, "2026": 40},
    ]
    arrest_df = pd.DataFrame(arrest_rows)
    offense = st.selectbox("Choose an offense", arrest_df["Offense"].tolist())
    chosen = arrest_df[arrest_df["Offense"] == offense].iloc[0]
    fig, ax = plt.subplots(figsize=(7, 3.3))
    vals = [chosen["2024"], chosen["2025"], chosen["2026"]]
    bars = ax.bar(["2024", "2025", "2026"], vals, color=["#777777", "#999999", RED], width=.55)
    ax.set_title(f"Black arrests as a share of Black + White arrests: {offense}", loc="left", fontsize=13, fontweight="bold", color=WHITE, pad=14)
    ax.set_ylabel("Share of arrests (%)"); ax.set_ylim(0, 110)
    for bar, value in zip(bars, vals): ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+2, f"{value}%", ha="center", color=WHITE, fontweight="bold")
    style_axis(ax); chart_theme(fig, ax)
    st.dataframe(arrest_df, hide_index=True, use_container_width=True)
    st.download_button("Download selected arrest-share table (CSV)", arrest_df.to_csv(index=False).encode("utf-8"), "social_justice_arrest_shares.csv", "text/csv")
    st.caption("Dashes in the source table mean no percentage was displayed for that offense/year; only a subset of the report's offenses is transcribed here. The report's source is S&P Global Market Intelligence calculations based on FBI.gov data.")
    with st.expander("Other Social Justice data included in the report"):
        st.write("The appendix identifies biased-based policing overview data and public CPD arrest charges data from the Chattanooga Open Data Portal's Policing and Racial Equity resources.")

with tab_explore:
    st.markdown('<div class="eyebrow">04 / EXPLORE THE DATA</div>', unsafe_allow_html=True)
    st.header("Find a measure and explore the evidence")
    st.write(
        "Filter the available indicators by topic, search for a measure, compare the reported "
        "Black and White values where available, and download the filtered results."
    )

    # Keep the indicator inventory explicit so users can see what is and is not available.
    explore_rows = [
        {"Topic": "Health", "Indicator": "Health Insurance parity score", "Year": 2026, "Black value": None, "White value": None, "Unit": "Parity index score", "Value / score": 99, "Source note": "Health component score, report p. 9"},
        {"Topic": "Health", "Indicator": "Contagious disease parity score", "Year": 2026, "Black value": None, "White value": None, "Unit": "Parity index score", "Value / score": 36, "Source note": "Health component score, report p. 9"},
        {"Topic": "Health", "Indicator": "Chronic disease and cancer parity score", "Year": 2026, "Black value": None, "White value": None, "Unit": "Parity index score", "Value / score": 76, "Source note": "Health component score, report p. 9"},
        {"Topic": "Health", "Indicator": "Accidental and non-accidental death parity score", "Year": 2026, "Black value": None, "White value": None, "Unit": "Parity index score", "Value / score": 77, "Source note": "Health component score, report p. 9"},
        {"Topic": "Health", "Indicator": "Maternal and infant health parity score", "Year": 2026, "Black value": None, "White value": None, "Unit": "Parity index score", "Value / score": 69, "Source note": "Health component score, report p. 9"},
        {"Topic": "Population", "Indicator": "Average annual population growth, White (one race), 2019–2024", "Year": 2026, "Black value": None, "White value": None, "Unit": "% per year", "Value / score": -0.21, "Source note": "Report p. 13"},
        {"Topic": "Population", "Indicator": "Average annual population growth, Black (one race), 2019–2024", "Year": 2026, "Black value": None, "White value": None, "Unit": "% per year", "Value / score": -1.62, "Source note": "Report p. 13"},
        {"Topic": "Social Justice", "Indicator": "Arrests per capita, Black residents, 2024", "Year": 2024, "Black value": 1.6, "White value": 0.8, "Unit": "%", "Value / score": None, "Source note": "Report p. 20; approximate 2x comparison"},
        {"Topic": "Economics", "Indicator": "Employment Issues parity score", "Year": 2026,
         "Black value": None, "White value": None, "Unit": "Parity index score",
         "Value / score": 83, "Source note": "2026 report economic component score"},
        {"Topic": "Economics", "Indicator": "Income parity score", "Year": 2026,
         "Black value": None, "White value": None, "Unit": "Parity index score",
         "Value / score": 63, "Source note": "2026 report economic component score"},
        {"Topic": "Economics", "Indicator": "Housing & Wealth parity score", "Year": 2026,
         "Black value": None, "White value": None, "Unit": "Parity index score",
         "Value / score": 54, "Source note": "2026 report economic component score"},
        {"Topic": "Economics", "Indicator": "Poverty parity score", "Year": 2026,
         "Black value": None, "White value": None, "Unit": "Parity index score",
         "Value / score": 31, "Source note": "2026 report economic component score"},
        {"Topic": "Education", "Indicator": "Preschool / nursery enrollment", "Year": 2026,
         "Black value": 15, "White value": 29, "Unit": "%", "Value / score": None,
         "Source note": "Report chart; underlying data year should be checked against report notes"},
        {"Topic": "Education", "Indicator": "College / graduate enrollment, ages 18–29", "Year": 2026,
         "Black value": 40, "White value": 41, "Unit": "%", "Value / score": None,
         "Source note": "2026 report summary; verify exact source note before publication"},
        {"Topic": "Education", "Indicator": "Bachelor's degree attainment", "Year": 2026,
         "Black value": 10, "White value": 28, "Unit": "%", "Value / score": None,
         "Source note": "2026 report summary"},
        {"Topic": "Education", "Indicator": "TNReady on-grade-level performance", "Year": 2026,
         "Black value": 23, "White value": 60, "Unit": "%", "Value / score": None,
         "Source note": "2026 report summary"},
        {"Topic": "Education", "Indicator": "Ready Graduate rate", "Year": 2026,
         "Black value": 47, "White value": 73, "Unit": "%", "Value / score": None,
         "Source note": "2026 report summary"},
    ]
    explorer_df = pd.DataFrame(explore_rows)

    f1, f2 = st.columns([1, 2])
    with f1:
        topic_filter = st.multiselect(
            "Topic", options=sorted(explorer_df["Topic"].unique()),
            default=sorted(explorer_df["Topic"].unique())
        )
    with f2:
        search_term = st.text_input(
            "Search indicators", placeholder="Try ‘degree’, ‘poverty’, or ‘enrollment’"
        )

    filtered = explorer_df[explorer_df["Topic"].isin(topic_filter)].copy()
    if search_term.strip():
        filtered = filtered[
            filtered["Indicator"].str.contains(search_term.strip(), case=False, na=False)
        ]

    st.caption(f"{len(filtered)} indicator(s) match your filters.")
    display_cols = ["Topic", "Indicator", "Year", "Black value", "White value",
                    "Unit", "Value / score", "Source note"]
    st.dataframe(filtered[display_cols], hide_index=True, use_container_width=True)

    if not filtered.empty:
        comparable = filtered.dropna(subset=["Black value", "White value"]).copy()
        choices = comparable["Indicator"].tolist()
        if choices:
            st.subheader("Compare a specific outcome")
            selected_compare = st.selectbox("Choose an indicator to compare", choices)
            chosen = comparable[comparable["Indicator"] == selected_compare].iloc[0]
            black_val, white_val = float(chosen["Black value"]), float(chosen["White value"])
            m1, m2, m3 = st.columns(3)
            m1.metric("Black", f"{black_val:g}{chosen['Unit']}")
            m2.metric("White", f"{white_val:g}{chosen['Unit']}")
            m3.metric("Difference", f"{white_val-black_val:g} percentage points")
            fig, ax = plt.subplots(figsize=(7.5, 3.4))
            bars = ax.bar(["Black", "White"], [black_val, white_val],
                          color=[RED, "#A6A6A6"], width=0.52)
            ax.set_title(selected_compare, loc="left", fontsize=15, fontweight="bold",
                         color=WHITE, pad=14)
            ax.set_ylabel("Share (%)")
            ax.set_ylim(0, max(white_val, black_val) * 1.25 + 2)
            for bar, value in zip(bars, [black_val, white_val]):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.7,
                        f"{value:g}%", ha="center", color=WHITE, fontweight="bold")
            style_axis(ax)
            chart_theme(fig, ax)
            st.caption("A difference in percentage points is a descriptive comparison, not an explanation of cause.")
        else:
            st.info("The selected results are parity index scores. These are not raw Black and White percentages, so they cannot be plotted as a demographic comparison.")

    st.download_button(
        "Download filtered data (CSV)",
        filtered.to_csv(index=False).encode("utf-8"),
        "state_of_black_chattanooga_filtered_data.csv",
        "text/csv",
        disabled=filtered.empty,
    )
    with st.expander("How to read these indicators"):
        st.markdown("""
        - **Parity index scores** summarize relative parity; they are not raw population percentages.
        - **Black and White values** are shown only for indicators with reported group-specific values.
        - A difference in percentage points describes a gap but does not explain its cause.
        - Report year and underlying observation year may differ. Confirm each source note before making direct year-to-year comparisons.
        - This explorer includes selected measures, not every indicator in the report.
        """)

with tab_method:
    st.markdown('<div class="eyebrow">05 / SOURCES & METHODOLOGY</div>', unsafe_allow_html=True)
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
    st.subheader("Coverage of the full report")
    st.write("The report covers three Equality Index pillars—Economics, Health, and Education—and also presents population, occupations/industry, and social justice analyses. Some detailed charts are summarized qualitatively where the report's graphic does not provide an accessible exact value for every bar.")
    with st.expander("Full indicator inventory from the report appendix"):
        inventory = pd.DataFrame([
            {"Sector": "Economics", "Category": "Income", "Measures listed": "Median household income; median male weekly earnings; median female weekly earnings; median family income"},
            {"Sector": "Economics", "Category": "Poverty", "Measures listed": "Below poverty; below 50% and 125% of poverty; poverty by age (under 18, 18–64, 65+); SNAP benefits; cash public assistance"},
            {"Sector": "Economics", "Category": "Employment", "Measures listed": "Unemployment; labor-force participation; employment-to-population ratio; not in labor force; salaried employment"},
            {"Sector": "Economics", "Category": "Housing & Wealth", "Measures listed": "Median home value; public transportation to work; employer businesses per adult population; overcrowding; household size; owner-occupied and renter-occupied units"},
            {"Sector": "Health", "Category": "Maternal & Infant Health", "Measures listed": "Prenatal care; premature births; low birthweight; teen pregnancies; infant mortality; smoking during pregnancy; births when mother unmarried"},
            {"Sector": "Health", "Category": "Death & Injury", "Measures listed": "Life expectancy; total mortality; years of potential life lost; motor-vehicle mortality; accident mortality; suicide; homicide"},
            {"Sector": "Health", "Category": "Chronic Disease & Cancer", "Measures listed": "Alzheimer’s; chronic lower respiratory disease; heart disease; stroke; diabetes; hypertension; kidney disease; cancer mortality/incidence; survey measures"},
            {"Sector": "Health", "Category": "Contagious Disease", "Measures listed": "HIV/AIDS; gonorrhea; chlamydia; syphilis; influenza/pneumonia; COVID-related measures"},
            {"Sector": "Health", "Category": "Insurance", "Measures listed": "Uninsured population; uninsured children under 6; private insurance; public insurance"},
            {"Sector": "Education", "Category": "Quality", "Measures listed": "Four-year graduation; Ready Graduate; TCAP participation/valid score; per-pupil spending; teacher credentials/experience; student-teacher ratio; TNReady proficiency; TVAAS"},
            {"Sector": "Education", "Category": "Scores", "Measures listed": "End-of-course tests; MSAA; TNReady; ELA and math success rates"},
            {"Sector": "Education", "Category": "Post-secondary Attainment", "Measures listed": "Less than high school; high school graduate; some college/associate degree; bachelor’s degree; graduate/professional degree"},
            {"Sector": "Education", "Category": "Student Risk Factors", "Measures listed": "Zero-tolerance offenses; suspension; alternative school; expulsion; dropout; chronic absenteeism"},
            {"Sector": "Population", "Category": "Population trends", "Measures listed": "Population size and growth by race; alone or in combination; Hispanic/non-Hispanic groupings"},
            {"Sector": "Work & Industry", "Category": "Occupations / Industry", "Measures listed": "Employment by occupation; employment share by industry; industry forecasts"},
            {"Sector": "Social Justice", "Category": "Policing & Arrests", "Measures listed": "Arrest shares by offense and year; per-capita arrests; biased-based policing overview; public CPD arrest charges"},
        ])
        st.dataframe(inventory, hide_index=True, use_container_width=True)
        st.download_button("Download full report indicator inventory (CSV)", inventory.to_csv(index=False).encode("utf-8"), "state_of_black_chattanooga_indicator_inventory.csv", "text/csv")

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
