import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="State of Black Chattanooga", page_icon="📊", layout="wide")

RED = "#E12B32"
WHITE = "#F5F5F5"
MUTED = "#B7B7B7"
PANEL = "#1C1C1C"
GRID = "#424242"

st.markdown("""
<style>
.stApp { background: #101010; }
.block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1450px; }
h1,h2,h3 { letter-spacing: -0.025em; }
div[data-testid="stMetric"] { background:#1C1C1C; border-left:3px solid #E12B32; padding:14px 16px; border-radius:5px; }
div[data-testid="stMetricLabel"] { color:#B7B7B7; }
.eyebrow { color:#E12B32; letter-spacing:2px; font-size:11px; font-weight:800; }
.hero { background:linear-gradient(115deg,#252525,#111111); border-left:6px solid #E12B32; padding:26px 30px; margin-bottom:14px; border-radius:3px; }
.hero h1 { color:#F5F5F5; font-size:36px; margin:7px 0 9px 0; }
.hero p { color:#D0D0D0; font-size:16px; line-height:1.55; margin-bottom:0; }
.insight { background:#1C1C1C; border-left:4px solid #E12B32; padding:14px 17px; margin:8px 0 15px 0; line-height:1.6; }
.muted { color:#B7B7B7; font-size:13px; }
</style>
""", unsafe_allow_html=True)

# Data transcribed from the State of Black Chattanooga 2026 report's summary charts.
index_trend = pd.DataFrame({
    "Report year": [2022, 2024, 2026],
    "Overall Equality Index": [61, 61, 60],
    "Economics Index": [60, 58, 59],
    "Education Index": [60, 60, 55],
})

housing_score = 54  # 2026 Housing & Wealth component parity score
housing_weights = pd.DataFrame({
    "Measure": ["Income", "Poverty", "Employment Issues", "Housing & Wealth"],
    "Weight within economics index (%)": [40, 20, 20, 20],
    "2026 parity score (%)": [63, 31, 83, 54],
})

education = pd.DataFrame([
    {"Indicator": "Preschool / nursery enrollment (children under 5)", "Black": 15, "White": 29, "Year": 2024, "Theme": "Early learning", "Type": "Enrollment"},
    {"Indicator": "College / graduate enrollment (ages 18–29)", "Black": 40, "White": 41, "Year": 2024, "Theme": "Postsecondary", "Type": "Enrollment"},
    {"Indicator": "Bachelor's degree attainment", "Black": 10, "White": 28, "Year": "2026 report summary", "Theme": "Postsecondary", "Type": "Attainment"},
    {"Indicator": "TNReady on-grade-level performance", "Black": 23, "White": 60, "Year": "2026 report summary", "Theme": "School outcomes", "Type": "Achievement"},
    {"Indicator": "Ready Graduate rate", "Black": 47, "White": 73, "Year": "2026 report summary", "Theme": "School outcomes", "Type": "Readiness"},
])
education_trend = pd.DataFrame({"Report year": [2022, 2024, 2026], "Education Index": [60, 60, 55]})

# Glossary inventory for the housing/wealth topic. Items without report values are deliberately not plotted as numbers.
housing_measures = pd.DataFrame([
    {"Measure": "Median home value", "What it helps examine": "Differences in the value of homes by race.", "Value included in this dashboard?": "No — not transcribed as a group value"},
    {"Measure": "Owner-occupied housing", "What it helps examine": "The share of residents living in homes they own.", "Value included in this dashboard?": "No — not transcribed as a group value"},
    {"Measure": "Renter-occupied housing", "What it helps examine": "The share of residents living in rented homes.", "Value included in this dashboard?": "No — not transcribed as a group value"},
    {"Measure": "Crowding in owner-occupied homes", "What it helps examine": "Housing conditions where more than one person occupies a room.", "Value included in this dashboard?": "No — not transcribed as a group value"},
    {"Measure": "Crowding in renter-occupied homes", "What it helps examine": "Housing conditions in renter-occupied homes.", "Value included in this dashboard?": "No — not transcribed as a group value"},
    {"Measure": "Employer business ownership", "What it helps examine": "Business ownership as one potential store of wealth.", "Value included in this dashboard?": "No — report notes this data was not updated"},
])

# Plotly theme helpers: charts retain hover, zoom, and legend interaction.
def polish(fig, height=390):
    fig.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=WHITE, family="Arial"), height=height,
        margin=dict(l=20, r=25, t=65, b=30), title=dict(x=0, xanchor="left", font=dict(size=18)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        hoverlabel=dict(bgcolor="#222222", font_color=WHITE),
    )
    fig.update_xaxes(gridcolor=GRID, zerolinecolor=GRID)
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=GRID)
    return fig

st.markdown("""
<div class="hero">
  <div class="eyebrow">COMMUNITY DATA • 2026 REPORT</div>
  <h1>STATE OF BLACK CHATTANOOGA</h1>
  <p>Explore two connected parts of opportunity in Hamilton County: housing and wealth, and education. Interactive visuals make the reported gaps easier to inspect without repeating the same chart on every page.</p>
</div>
""", unsafe_allow_html=True)
st.caption("Source: State of Black Chattanooga 2026, S&P Global Market Intelligence. The report's 2026 update uses 2024 Census data for many measures; underlying years vary by indicator.")

with st.sidebar:
    st.markdown('<div class="eyebrow">DASHBOARD CONTROLS</div>', unsafe_allow_html=True)
    st.write("Use these controls to change the education comparison and display style.")
    chosen_theme = st.multiselect("Education themes", education["Theme"].unique().tolist(), default=education["Theme"].unique().tolist())
    chart_style = st.radio("Education comparison style", ["Dumbbell comparison", "Grouped bars", "Gap ranking"], index=0)
    st.markdown("---")
    st.caption("Housing & wealth figures are limited in the report summary. Missing group-level values are not estimated.")

tab_overview, tab_housing, tab_education, tab_explore, tab_method = st.tabs([
    "Overview", "Housing & Wealth", "Education", "Explore Data", "Sources & Methodology"
])

with tab_overview:
    st.markdown('<div class="eyebrow">01 / THE STORY SO FAR</div>', unsafe_allow_html=True)
    st.header("The headline: progress is uneven")
    m1, m2, m3 = st.columns(3)
    m1.metric("Overall Equality Index", "60%", "−1 point vs. 2024")
    m2.metric("Housing & Wealth parity", "54%", "2026 component score")
    m3.metric("Education Index", "55%", "−5 points vs. 2024")

    col1, col2 = st.columns([1.35, 1])
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=index_trend["Report year"], y=index_trend["Education Index"], mode="lines+markers+text",
            text=["60%", "60%", "55%"], textposition="top center", name="Education", line=dict(color=RED, width=4), marker=dict(size=10)))
        fig.add_trace(go.Scatter(x=[2026], y=[housing_score], mode="markers+text", text=["54%"], textposition="bottom center",
            name="Housing & Wealth (2026 only)", marker=dict(color="#F2B66D", size=13, symbol="diamond")))
        fig.update_layout(title="Education over time vs. housing & wealth in 2026", xaxis_title="Report year", yaxis_title="Parity score (100 = full parity)")
        fig.update_xaxes(tickmode="array", tickvals=[2022, 2024, 2026])
        fig.update_yaxes(range=[0, 100], ticksuffix="%")
        st.plotly_chart(polish(fig, 390), use_container_width=True, config={"displaylogo": False})
        st.caption("Housing & Wealth is shown only for 2026 because this dashboard does not yet contain a validated historical series for that component.")
    with col2:
        fig = go.Figure(go.Indicator(mode="gauge+number", value=60, number={"suffix": "%", "font": {"color": WHITE, "size": 34}},
            title={"text": "Overall parity index", "font": {"color": WHITE, "size": 17}},
            gauge={"axis": {"range": [0, 100], "tickcolor": WHITE}, "bar": {"color": RED}, "bgcolor": PANEL,
                   "steps": [{"range": [0, 50], "color": "#292929"}, {"range": [50, 100], "color": "#3A3A3A"}],
                   "threshold": {"line": {"color": "#F2B66D", "width": 3}, "thickness": 0.8, "value": 100}}))
        st.plotly_chart(polish(fig, 390), use_container_width=True, config={"displaylogo": False})
        st.caption("100% represents full parity with White residents. Index scores are not raw rates.")
    st.markdown("""
    <div class="insight"><b>Why focus on these two areas?</b><br>
    The 2026 report highlights a 54% parity score for Housing & Wealth and a 55% Education Index. These scores summarize different underlying indicators; they should not be interpreted as the percentage of residents who own a home, graduate, or experience a specific outcome.</div>
    """, unsafe_allow_html=True)

with tab_housing:
    st.markdown('<div class="eyebrow">02 / HOUSING & WEALTH</div>', unsafe_allow_html=True)
    st.header("Housing is about stability and the ability to build wealth")
    st.write("The report assigns Housing & Wealth 20% of the economics sub-index. It includes home values, homeownership, crowding, transportation, household characteristics, and employer-business ownership.")
    left, right = st.columns([1, 1.2])
    with left:
        fig = go.Figure(go.Indicator(mode="gauge+number", value=housing_score, number={"suffix": "%", "font": {"size": 40, "color": WHITE}},
            title={"text": "Housing & Wealth parity score", "font": {"size": 18, "color": WHITE}},
            gauge={"axis": {"range": [0, 100], "tickcolor": WHITE}, "bar": {"color": RED}, "bgcolor": PANEL,
                   "steps": [{"range": [0, 50], "color": "#292929"}, {"range": [50, 100], "color": "#3A3A3A"}],
                   "threshold": {"line": {"color": "#F2B66D", "width": 3}, "thickness": 0.8, "value": 100}}))
        st.plotly_chart(polish(fig, 330), use_container_width=True, config={"displaylogo": False})
        st.caption("2026 report component score. 100% = full parity; this is not a homeownership rate.")
    with right:
        st.subheader("How the economic index is weighted")
        st.write("Select a component to see its share of the economics score and its 2026 parity score.")
        component = st.selectbox("Economic component", housing_weights["Measure"].tolist(), index=3)
        selected = housing_weights[housing_weights["Measure"] == component].iloc[0]
        x, y = st.columns(2)
        x.metric("Weight in economics", f"{selected['Weight within economics index (%)']}%")
        y.metric("2026 parity score", f"{selected['2026 parity score (%)']}%")
        fig = px.treemap(housing_weights, path=["Measure"], values="Weight within economics index (%)",
            color="2026 parity score (%)", color_continuous_scale=[[0, "#4B1B1E"], [0.55, RED], [1, "#E9B7A0"]],
            hover_data={"Weight within economics index (%)": True, "2026 parity score (%)": True})
        fig.update_layout(title="Economic index composition", coloraxis_colorbar_title="Parity score")
        st.plotly_chart(polish(fig, 330), use_container_width=True, config={"displaylogo": False})
    st.markdown("### Housing and wealth measures covered in the report")
    st.caption("The glossary lists these measures, but the current dashboard does not yet have validated race-specific values for every one. They are shown as a research inventory, not as measured results.")
    selected_measure = st.selectbox("Choose a measure to learn about", housing_measures["Measure"].tolist())
    detail = housing_measures[housing_measures["Measure"] == selected_measure].iloc[0]
    st.markdown(f'<div class="insight"><b>{detail["Measure"]}</b><br>{detail["What it helps examine"]}<br><span class="muted">{detail["Value included in this dashboard?"]}</span></div>', unsafe_allow_html=True)
    with st.expander("View all housing and wealth measures"):
        st.dataframe(housing_measures, hide_index=True, use_container_width=True)
        st.download_button("Download housing measures inventory", housing_measures.to_csv(index=False).encode("utf-8"), "housing_wealth_measures.csv", "text/csv")

with tab_education:
    st.markdown('<div class="eyebrow">03 / EDUCATION</div>', unsafe_allow_html=True)
    st.header("The education index declined in 2026")
    st.write("The report's Education Index moved from 60% in 2022 and 2024 to 55% in 2026. Use the controls to focus on early learning, postsecondary access, or school outcomes.")
    filtered_edu = education[education["Theme"].isin(chosen_theme)].copy()
    k1, k2, k3 = st.columns(3)
    k1.metric("2026 Education Index", "55%", "−5 points vs. 2024")
    k2.metric("Indicators in view", str(len(filtered_edu)))
    k3.metric("Largest shown gap", f"{(filtered_edu['White']-filtered_edu['Black']).max():.0f} pts" if not filtered_edu.empty else "—")

    left, right = st.columns([1.15, 1])
    with left:
        trend_fig = px.area(education_trend, x="Report year", y="Education Index", markers=True,
            title="Education index trend", line_shape="linear")
        trend_fig.update_traces(line_color=RED, fillcolor="rgba(225,43,50,0.18)", marker=dict(size=10))
        trend_fig.update_xaxes(tickmode="array", tickvals=[2022, 2024, 2026])
        trend_fig.update_yaxes(range=[0, 100], ticksuffix="%", title="Parity score")
        st.plotly_chart(polish(trend_fig, 350), use_container_width=True, config={"displaylogo": False})
    with right:
        if filtered_edu.empty:
            st.info("Select at least one education theme in the sidebar to display comparisons.")
        elif chart_style == "Dumbbell comparison":
            fig = go.Figure()
            for _, r in filtered_edu.iterrows():
                fig.add_shape(type="line", x0=r["Black"], x1=r["White"], y0=r["Indicator"], y1=r["Indicator"], line=dict(color="#777777", width=3))
            fig.add_trace(go.Scatter(x=filtered_edu["Black"], y=filtered_edu["Indicator"], mode="markers", name="Black", marker=dict(color=RED, size=11), customdata=filtered_edu[["Year"]], hovertemplate="Black: %{x}%<br>%{y}<br>Year: %{customdata[0]}<extra></extra>"))
            fig.add_trace(go.Scatter(x=filtered_edu["White"], y=filtered_edu["Indicator"], mode="markers", name="White", marker=dict(color="#D9D9D9", size=11), customdata=filtered_edu[["Year"]], hovertemplate="White: %{x}%<br>%{y}<br>Year: %{customdata[0]}<extra></extra>"))
            fig.update_layout(title="Black–White outcome comparison", xaxis_title="Share (%)", yaxis_title="", showlegend=True)
            fig.update_xaxes(range=[0, 100])
            st.plotly_chart(polish(fig, 430), use_container_width=True, config={"displaylogo": False})
        elif chart_style == "Grouped bars":
            long = filtered_edu.melt(id_vars=["Indicator", "Year", "Theme"], value_vars=["Black", "White"], var_name="Group", value_name="Share")
            fig = px.bar(long, x="Share", y="Indicator", color="Group", barmode="group", orientation="h", text="Share", title="Reported outcomes by group", color_discrete_map={"Black": RED, "White": "#BDBDBD"}, hover_data=["Year", "Theme"])
            fig.update_traces(texttemplate="%{text}%", textposition="outside", cliponaxis=False)
            fig.update_xaxes(range=[0, 110], title="Share (%)")
            st.plotly_chart(polish(fig, 430), use_container_width=True, config={"displaylogo": False})
        else:
            gap = filtered_edu.assign(Gap=filtered_edu["White"] - filtered_edu["Black"]).sort_values("Gap")
            fig = px.bar(gap, x="Gap", y="Indicator", orientation="h", text="Gap", title="Difference in percentage points", color="Gap", color_continuous_scale=[[0, "#6B6B6B"], [1, RED]], hover_data=["Black", "White", "Year"])
            fig.update_traces(texttemplate="%{text:.0f} pts", textposition="outside", cliponaxis=False)
            fig.update_xaxes(range=[0, max(10, float(gap["Gap"].max()) * 1.25)], title="White minus Black (percentage points)")
            st.plotly_chart(polish(fig, 430), use_container_width=True, config={"displaylogo": False})

    st.subheader("Explore an individual indicator")
    if not filtered_edu.empty:
        chosen_indicator = st.selectbox("Education indicator", filtered_edu["Indicator"].tolist())
        r = filtered_edu[filtered_edu["Indicator"] == chosen_indicator].iloc[0]
        a, b, c = st.columns(3)
        a.metric("Black", f"{r['Black']}%")
        b.metric("White", f"{r['White']}%")
        c.metric("Difference", f"{r['White'] - r['Black']} percentage points")
        st.caption(f"Data-year label in this dashboard: {r['Year']}. The report's chart/source notes should be checked before comparing across years.")
        st.download_button("Download displayed education indicators", filtered_edu.to_csv(index=False).encode("utf-8"), "education_indicators.csv", "text/csv")
    st.markdown("""
    <div class="insight"><b>How to interpret this section</b><br>
    Enrollment, attainment, achievement, and readiness are different kinds of measures. A gap is descriptive; it does not by itself explain why the gap exists.</div>
    """, unsafe_allow_html=True)

with tab_explore:
    st.markdown('<div class="eyebrow">04 / EXPLORE DATA</div>', unsafe_allow_html=True)
    st.header("Search and download the indicators used here")
    all_rows = []
    for _, r in housing_weights.iterrows():
        all_rows.append({"Topic": "Housing & Wealth / Economics context", "Indicator": f"{r['Measure']} parity score", "Value": r["2026 parity score (%)"], "Unit": "Parity score (%)", "Year": 2026, "Data status": "Reported score"})
    for _, r in education.iterrows():
        all_rows.append({"Topic": "Education", "Indicator": r["Indicator"], "Value": None, "Unit": "Black/White comparison available below", "Year": r["Year"], "Data status": "Selected outcome values"})
    for _, r in housing_measures.iterrows():
        all_rows.append({"Topic": "Housing & Wealth", "Indicator": r["Measure"], "Value": None, "Unit": "Not transcribed as a group value", "Year": "—", "Data status": r["Value included in this dashboard?"]})
    df = pd.DataFrame(all_rows)
    f1, f2 = st.columns([1, 2])
    with f1:
        topic = st.multiselect("Filter topics", df["Topic"].unique().tolist(), default=df["Topic"].unique().tolist())
    with f2:
        search = st.text_input("Search indicators", placeholder="Try homeownership, degree, poverty…")
    view = df[df["Topic"].isin(topic)].copy()
    if search.strip():
        view = view[view["Indicator"].str.contains(search.strip(), case=False, na=False)]
    st.caption(f"{len(view)} result(s)")
    st.dataframe(view, hide_index=True, use_container_width=True)
    st.download_button("Download filtered inventory (CSV)", view.to_csv(index=False).encode("utf-8"), "state_of_black_chattanooga_indicator_inventory.csv", "text/csv", disabled=view.empty)

with tab_method:
    st.markdown('<div class="eyebrow">05 / SOURCES & METHODOLOGY</div>', unsafe_allow_html=True)
    st.header("Read the original research")
    st.write("This dashboard summarizes selected findings from the State of Black Chattanooga 2026 report prepared by S&P Global Market Intelligence. The report describes its geography as Hamilton County.")
    st.link_button("Urban League of Greater Chattanooga reports", "https://www.ulchatt.net/reports/", use_container_width=True)
    st.link_button("State of Black Chattanooga 2024 report", "https://www.ulchatt.net/s/state-of-black-chattanooga-2024-BOOK-FINAL-01.pdf", use_container_width=True)
    st.link_button("State of Black Chattanooga 2022 report", "https://www.ulchatt.net/s/UL-State-of-Black-Chattanooga-Booklet-20221.pdf", use_container_width=True)
    st.subheader("Important interpretation notes")
    st.markdown("""
    - **100% means full parity** between Black and White residents for the relevant index measure.
    - The overall 2026 Equality Index combines Economics (45%), Education (30%), and Health (25%); this dashboard's subject focus is Housing & Wealth and Education.
    - Housing & Wealth is one component of the economics index and carries 20% of that sub-index.
    - A parity score is not a raw rate. A Housing & Wealth score of 54% does not mean 54% of residents own homes.
    - The report states that 2026 uses 2024 Census data for many measures; school and health data may be more recent, and underlying years vary.
    - Some education values are presented as selected report summary values. Their precise underlying year should be verified against the original chart before doing historical comparisons.
    - Missing values have not been estimated or filled in.
    - This dashboard is descriptive and does not establish causation.
    """)
    with st.expander("Download the data tables used in this dashboard"):
        st.write("Education indicators")
        st.dataframe(education, hide_index=True, use_container_width=True)
        st.download_button("Download education source table", education.to_csv(index=False).encode("utf-8"), "education_source_table.csv", "text/csv")
        st.write("Housing & Wealth / economics context")
        st.dataframe(housing_weights, hide_index=True, use_container_width=True)
        st.download_button("Download component table", housing_weights.to_csv(index=False).encode("utf-8"), "housing_wealth_context.csv", "text/csv")

st.divider()
st.caption("State of Black Chattanooga • Independent student data project • Source: State of Black Chattanooga 2026, S&P Global Market Intelligence")
