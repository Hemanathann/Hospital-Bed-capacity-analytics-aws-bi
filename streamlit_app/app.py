import streamlit as st
import pandas as pd
import altair as alt

# -------------------------------------------------------------
# Page config
# -------------------------------------------------------------
st.set_page_config(
    page_title="Healthcare Service Capacity Dashboard",
    layout="wide",
    page_icon="🩺",
)

# -------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------
def style_chart(chart: alt.Chart) -> alt.Chart:
    """Apply a consistent dark-theme style to Altair charts."""
    return (
        chart
        .configure_axis(
            labelColor="#e0e0e0",
            titleColor="#e0e0e0",
            gridColor="#444444",
            labelFontSize=11,
            titleFontSize=13,
        )
        .configure_legend(
            labelColor="#e0e0e0",
            titleColor="#e0e0e0",
            labelFontSize=11,
            titleFontSize=12,
        )
        .configure_view(strokeOpacity=0)
    )


@st.cache_data
def load_data(path: str = "service_capacity_staff.csv") -> pd.DataFrame:
    df = pd.read_csv(path)

    # Derived measures
    df["bed_shortage"] = (df["patients_request"] - df["available_beds"]).clip(lower=0)
    df["spare_capacity"] = (df["available_beds"] - df["patients_request"]).clip(lower=0)
    df["utilisation_rate"] = df["patients_admitted"] / df["available_beds"] * 100
    df["refusal_rate"] = df["patients_refused"] / df["patients_request"] * 100
    return df


df = load_data()

# -------------------------------------------------------------
# Sidebar filters (slicer-style)
# -------------------------------------------------------------
st.sidebar.header("Filters")

# --- Service slicer (checkbox style, like Power BI) ---
st.sidebar.subheader("Select services")

service_options = sorted(df["service"].unique())

select_all = st.sidebar.checkbox("Select all services", value=True)

if select_all:
    selected_services = service_options
else:
    selected_services = [
        s for s in service_options
        if st.sidebar.checkbox(s, value=True, key=f"srv_{s}")
    ]

# Safety: if user unchecks everything, fall back to all
if not selected_services:
    selected_services = service_options

# --- Week slicer ---
min_week, max_week = int(df["week"].min()), int(df["week"].max())
week_range = st.sidebar.slider(
    "Week range",
    min_value=min_week,
    max_value=max_week,
    value=(min_week, max_week),
)

# Apply filters
df_filtered = df[
    df["service"].isin(selected_services)
    & df["week"].between(week_range[0], week_range[1])
].copy()

# -------------------------------------------------------------
# Dashboard header & tabs
# -------------------------------------------------------------
st.title("Healthcare Service Capacity Dashboard")

tab1, tab2 = st.tabs(["Capacity vs Demand Overview", "Service & Staff Experience"])

# -------------------------------------------------------------
# TAB 1 – Capacity vs Demand Overview
# -------------------------------------------------------------
with tab1:
    st.subheader("Capacity vs Demand Overview")

    # KPI calculations
    total_bed_shortage = int(df_filtered["bed_shortage"].sum())
    total_spare_capacity = int(df_filtered["spare_capacity"].sum())
    avg_utilisation = df_filtered["utilisation_rate"].mean()

    total_refused = df_filtered["patients_refused"].sum()
    total_requested = df_filtered["patients_request"].sum()
    avg_refusal_rate = (total_refused / total_requested * 100) if total_requested > 0 else 0.0

    avg_satisfaction = df_filtered["patient_satisfaction"].mean()
    avg_morale = df_filtered["staff_morale"].mean()

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    kpi1.metric("Total Bed Shortage (patients)", f"{total_bed_shortage:,.0f}")
    kpi2.metric("Spare Bed Capacity (beds)", f"{total_spare_capacity:,.0f}")
    kpi3.metric("Average Bed Utilisation", f"{avg_utilisation:.2f}%")
    kpi4.metric("Average Staff Morale", f"{avg_morale:.2f}")
    kpi5.metric("Average Refusal Rate", f"{avg_refusal_rate:.2f}%")

    st.markdown("---")

    # ===== Weekly demand vs admissions (line chart) =====
    st.markdown("### Weekly Demand vs Capacity vs Admissions")

    weekly = (
        df_filtered.groupby("week", as_index=False)[
            ["patients_request", "patients_admitted", "available_beds"]
        ]
        .sum()
        .sort_values("week")
    )

    weekly_long = weekly.melt(
        id_vars="week",
        value_vars=["patients_request", "patients_admitted", "available_beds"],
        var_name="metric",
        value_name="value",
    )

    color_scale = alt.Scale(
        domain=["patients_request", "patients_admitted", "available_beds"],
        range=["#ff6b6b", "#4dabf7", "#20c997"],
    )

    line_chart = (
        alt.Chart(weekly_long)
        .mark_line(point=True, strokeWidth=3)
        .encode(
            x=alt.X("week:O", title="Week"),
            y=alt.Y("value:Q", title="Number of patients / beds"),
            color=alt.Color("metric:N", title="Series", scale=color_scale),
            tooltip=[
                alt.Tooltip("week:O", title="Week"),
                alt.Tooltip("metric:N", title="Series"),
                alt.Tooltip("value:Q", title="Value", format=","),
            ],
        )
        .properties(height=260)
    )

    st.altair_chart(style_chart(line_chart), width="stretch")

    # ===== Distribution chart =====
    st.markdown("### Distribution of Demand, Admissions & Capacity by Week")

    base = alt.Chart(weekly).encode(x=alt.X("week:O", title="Week"))

    bars = base.mark_bar(opacity=0.7, color="#4c6ef5").encode(
        y=alt.Y("patients_request:Q", title="Patient volume")
    )

    admitted_line = base.mark_line(point=True, strokeWidth=3, color="#51cf66").encode(
        y=alt.Y(
            "patients_admitted:Q",
            title="Patients admitted",
            axis=alt.Axis(titleColor="#51cf66"),
        )
    )

    beds_line = base.mark_line(point=True, strokeWidth=3, color="#ffd43b").encode(
        y=alt.Y(
            "available_beds:Q",
            title="Available beds",
            axis=alt.Axis(titleColor="#ffd43b"),
        )
    )

    dist_chart = alt.layer(bars, admitted_line, beds_line).resolve_scale(y="independent")

    st.altair_chart(style_chart(dist_chart), width="stretch")

    # ===== Text insights =====
    st.markdown("### Key Insights – Capacity vs Demand")

    if not weekly.empty:
        peak_week = weekly.loc[weekly["patients_request"].idxmax(), "week"]
        peak_value = int(weekly["patients_request"].max())
        tight_week = weekly.loc[weekly["available_beds"].idxmin(), "week"]
        tight_beds = int(weekly["available_beds"].min())

        st.markdown(
            f"""
            - **Peak demand** occurs in **week {peak_week}**, with around **{peak_value:,} patient requests**.
            - **Tightest capacity** is in **week {tight_week}**, where only **{tight_beds} beds** were available.
            - Across the selected period, the system runs at an average utilisation of **{avg_utilisation:.1f}%**,  
              leaving approximately **{total_spare_capacity:,} spare bed-days** unused.
            - At the same time, bed shortages accumulate to **{total_bed_shortage:,} patients**, indicating
              demand spikes concentrated in particular weeks or services.
            """
        )
    else:
        st.info("No data in the selected filter range.")

# -------------------------------------------------------------
# TAB 2 – Service & Staff Experience
# -------------------------------------------------------------
with tab2:
    st.subheader("Service & Staff Experience")

    # Aggregations by service
    service_summary = (
        df_filtered.groupby("service", as_index=False)
        .agg(
            utilisation_pct=("utilisation_rate", "mean"),
            total_refused=("patients_refused", "sum"),
            total_requested=("patients_request", "sum"),
            avg_satisfaction=("patient_satisfaction", "mean"),
            avg_morale=("staff_morale", "mean"),
            bed_shortage=("bed_shortage", "sum"),
            spare_capacity=("spare_capacity", "sum"),
        )
    )
    service_summary["refusal_pct"] = (
        service_summary["total_refused"] / service_summary["total_requested"] * 100
    )

    # High-level KPIs
    overall_util = service_summary["utilisation_pct"].mean()
    overall_refusal = (
        service_summary["total_refused"].sum()
        / service_summary["total_requested"].sum()
        * 100
        if service_summary["total_requested"].sum() > 0
        else 0.0
    )
    overstretched_services = service_summary[
        (service_summary["utilisation_pct"] >= 95)
        & (service_summary["bed_shortage"] > 0)
    ]["service"].nunique()
    high_satisfaction_services = service_summary[
        service_summary["avg_satisfaction"] >= 80
    ]["service"].nunique()

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Avg Utilisation (all services)", f"{overall_util:.2f}%")
    k2.metric("Avg Refusal Rate (all services)", f"{overall_refusal:.2f}%")
    k3.metric("Overstretched Services (≥95% util & shortage)", f"{overstretched_services}")
    k4.metric("High Satisfaction Services (score ≥ 80)", f"{high_satisfaction_services}")

    st.markdown("---")

    # Average refusal rate by service
    st.markdown("### Average Refusal Rate by Service (%)")

    bar_refusal = (
        alt.Chart(service_summary)
        .mark_bar()
        .encode(
            x=alt.X("refusal_pct:Q", title="Refusal rate (%)"),
            y=alt.Y("service:N", sort="-x", title="Service"),
            color=alt.value("#4dabf7"),
            tooltip=[
                alt.Tooltip("service:N", title="Service"),
                alt.Tooltip("refusal_pct:Q", title="Refusal %", format=".2f"),
            ],
        )
        .properties(height=200)
    )

    st.altair_chart(style_chart(bar_refusal), width="stretch")

    # ---------------------------------------------------------
    # Staff morale vs patient satisfaction (IMPROVED bubble chart)
    # ---------------------------------------------------------
    st.markdown("### Staff Morale vs Patient Satisfaction (bubble size = bed shortage)")

    if not service_summary.empty:
        # Build nice, tight domains around the data (like Power BI)
        x_min = service_summary["avg_morale"].min()
        x_max = service_summary["avg_morale"].max()
        x_margin = max(0.5, (x_max - x_min) * 0.3)
        x_domain = [x_min - x_margin, x_max + x_margin]

        y_min = service_summary["avg_satisfaction"].min()
        y_max = service_summary["avg_satisfaction"].max()
        y_margin = max(0.5, (y_max - y_min) * 0.3)
        y_domain = [y_min - y_margin, y_max + y_margin]

        base_bubble = alt.Chart(service_summary).encode(
            x=alt.X(
                "avg_morale:Q",
                title="Average staff morale",
                scale=alt.Scale(domain=x_domain),
                axis=alt.Axis(format=".1f"),
            ),
            y=alt.Y(
                "avg_satisfaction:Q",
                title="Average patient satisfaction",
                scale=alt.Scale(domain=y_domain),
                axis=alt.Axis(format=".1f"),
            ),
        )

        circles = (
            base_bubble.mark_circle(opacity=0.9, stroke="white", strokeWidth=1)
            .encode(
                size=alt.Size(
                    "bed_shortage:Q",
                    title="Bed shortage (patients)",
                    scale=alt.Scale(range=[150, 1200]),
                    legend=alt.Legend(format=",.0f"),
                ),
                color=alt.Color("service:N", title="Service"),
                tooltip=[
                    alt.Tooltip("service:N", title="Service"),
                    alt.Tooltip("avg_morale:Q", title="Avg morale", format=".2f"),
                    alt.Tooltip(
                        "avg_satisfaction:Q", title="Avg satisfaction", format=".2f"
                    ),
                    alt.Tooltip("bed_shortage:Q", title="Bed shortage", format=","),
                ],
            )
        )

        labels = (
            base_bubble.mark_text(
                align="center",
                baseline="bottom",
                dy=-8,
                fontSize=11,
                color="#ffffff",
            )
            .encode(text="service:N")
        )

        bubble_chart = circles + labels

        st.altair_chart(style_chart(bubble_chart), width="stretch")
    else:
        st.info("No data in the selected filter range.")

    # Detailed table
    st.markdown("### Service Pressure & Experience Summary")

    display_cols = [
        "service",
        "utilisation_pct",
        "refusal_pct",
        "avg_satisfaction",
        "avg_morale",
        "bed_shortage",
        "spare_capacity",
    ]

    table = service_summary[display_cols].rename(
        columns={
            "service": "Service",
            "utilisation_pct": "Utilisation %",
            "refusal_pct": "Refusal %",
            "avg_satisfaction": "Avg Satisfaction",
            "avg_morale": "Avg Morale",
            "bed_shortage": "Bed Shortage",
            "spare_capacity": "Spare Bed Capacity",
        }
    )

    st.dataframe(
        table.style.format(
            {
                "Utilisation %": "{:.2f}",
                "Refusal %": "{:.2f}",
                "Avg Satisfaction": "{:.2f}",
                "Avg Morale": "{:.2f}",
                "Bed Shortage": "{:,.0f}",
                "Spare Bed Capacity": "{:,.0f}",
            }
        ),
        width="stretch",
        hide_index=True,
    )

    # Narrative insights
    st.markdown("### Key Insights – Service & Staff Experience")

    if not service_summary.empty:
        highest_refusal_row = service_summary.loc[service_summary["refusal_pct"].idxmax()]
        lowest_refusal_row = service_summary.loc[service_summary["refusal_pct"].idxmin()]
        highest_satisfaction_row = service_summary.loc[
            service_summary["avg_satisfaction"].idxmax()
        ]
        most_shortage_row = service_summary.loc[service_summary["bed_shortage"].idxmax()]

        st.markdown(
            f"""
            - **{highest_refusal_row['service']}** has the highest refusal rate at **{highest_refusal_row['refusal_pct']:.1f}%**
              and contributes the most to overall bed shortages (**{int(highest_refusal_row['bed_shortage']):,} patients**).
            - **{lowest_refusal_row['service']}** shows the **lowest refusal rate** at just **{lowest_refusal_row['refusal_pct']:.1f}%**,  
              indicating better matching between demand and capacity.
            - **{most_shortage_row['service']}** accounts for **{int(most_shortage_row['bed_shortage']):,} patients** of bed shortage  
              over the selected period, highlighting where relief or reallocation would have the biggest impact.
            - **{highest_satisfaction_row['service']}** achieves the **highest patient satisfaction** with an average score of  
              **{highest_satisfaction_row['avg_satisfaction']:.1f}**, suggesting practices here could be replicated elsewhere.
            """
        )
    else:
        st.info("No data in the selected filter range.")
