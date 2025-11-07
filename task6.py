import pandas as pd
import plotly.graph_objects as go

data = pd.read_csv("data/cleaned_playstore.csv")

def generate_task6_chart(data):
  
    # Cleaning columns
    data["Last Updated"] = pd.to_datetime(data["Last Updated"], errors="coerce")
    data["Installs"] = data["Installs"].astype(str).str.replace(",", "").str.replace("+", "")
    data["Installs"] = pd.to_numeric(data["Installs"], errors="coerce").fillna(0)

    # Applying filters
    data = data[
        (pd.to_numeric(data["Rating"], errors="coerce") >= 4.2)
        & (~data["App"].astype(str).str.contains(r"\d"))
        & (data["Category"].str.upper().str.startswith(("T", "P")))
        & (pd.to_numeric(data["Reviews"], errors="coerce") > 1000)
        & (pd.to_numeric(data["Size_MB"], errors="coerce").between(20, 80))
    ].copy()

    # Translations for legend
    data["Category"] = data["Category"].replace({
        "TRAVEL_AND_LOCAL": "Voyage & Local (FR)",  #French
        "PRODUCTIVITY": "Productividad (ES)",     #Spanish
        "PHOTOGRAPHY": "写真 (JP)"                 #Japanese
    })

    # Grouping by month and category
    data["Month"] = data["Last Updated"].dt.to_period("M")
    monthly = data.groupby(["Month", "Category"], as_index=False)["Installs"].sum()
    monthly["Month"] = monthly["Month"].dt.to_timestamp()

    # Pivot for stacked chart
    pivot = monthly.pivot(index="Month", columns="Category", values="Installs").fillna(0)
    pivot = pivot.sort_index()

    # Find months with >25 % growth
    growth = pivot.pct_change() * 100
    highlight_months = growth.index[(growth > 25).any(axis=1)]

    # Stack chart
    fig = go.Figure()
    for cat in pivot.columns:
        fig.add_trace(go.Scatter(
            x=pivot.index.astype(str),
            y=pivot[cat].cumsum(),
            mode="lines",
            stackgroup="one",
            name=cat
        ))

    # Highlight growth months
    for m in highlight_months:
        fig.add_shape(
            type="rect", xref="x", yref="paper",
            x0=str(m), x1=str(m + pd.offsets.MonthBegin(1)),
            y0=0, y1=1, fillcolor="rgba(255,165,0,0.2)", line_width=0
        )

    fig.update_layout(
        title="Cumulative App Installs Over Time by Category",
        xaxis_title="Month",
        yaxis_title="Cumulative Installs",
        legend_title="App Category",
        template="plotly_white"
    )
    return fig