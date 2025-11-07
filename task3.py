import pandas as pd
import plotly.graph_objects as go

# Importing the dataset
data = pd.read_csv("data/cleaned_playstore.csv")

def generate_task3_chart(data):
    # Applying filters
    filtered = data[
        (data["Installs"] >= 10000)
        & (data["Revenue"] >= 10000)
        & (pd.to_numeric(data["Android Ver"], errors="coerce") > 4.0)
        & (data["Size_MB"] > 15)
        & (data["Content Rating"] == "Everyone")
        & (data["App"].str.len() <= 30)
    ]
    # Finding Top 3 categories by installs
    category_installs = filtered.groupby("Category")["Installs"].sum().reset_index()
    top3_categories = category_installs.sort_values("Installs", ascending=False).head(
        3
    )["Category"]

    top_data = filtered[filtered["Category"].isin(top3_categories)]

    # Group by Free vs Paid
    grouped = (
        top_data.groupby("Type")
        .agg(avg_installs=("Installs", "mean"), avg_revenue=("Revenue", "mean"))
        .reset_index()
    )

    # Dual-axis chart
    fig = go.Figure()

    # Bar for installs
    fig.add_trace(
        go.Bar(
            x=grouped["Type"],
            y=grouped["avg_installs"],
            name="Average Installs",
            yaxis="y1",
        )
    )

    # Line for revenue
    fig.add_trace(
        go.Scatter(
            x=grouped["Type"],
            y=grouped["avg_revenue"],
            name="Average Revenue",
            yaxis="y2",
            mode="lines+markers",
        )
    )

    fig.update_layout(
        title="Free vs Paid Apps in Top 3 Categories",
        xaxis=dict(title="App Type"),
        yaxis=dict(title="Average Installs", side="left"),
        yaxis2=dict(title="Average Revenue", side="right", overlaying="y"),
        legend_title="Metrics",
    )
    return fig
