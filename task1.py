import pandas as pd
import plotly.graph_objects as go

# Loading cleaned dataset
data = pd.read_csv("data/cleaned_playstore.csv")

def generate_task1_chart(data):

    # Filtering for January month, avg rating >= 4.0 & avg size >= 10MB
    data = data[pd.to_datetime(data["Last Updated"]).dt.month == 1]

    grouped = (
        data.groupby("Category")
        .agg(
            avg_rating=("Rating", "mean"),
            total_reviews=("Reviews", "sum"),
            total_installs=("Installs", "sum"),
            avg_size=("Size_MB", "mean"),
        )
        .reset_index()
    )

    filtered = grouped[(grouped["avg_rating"] >= 4.0) & (grouped["avg_size"] >= 10)]

    # Picking top 10 apps by installs

    top10 = filtered.sort_values("total_installs", ascending=False).head(10)
    print(top10)

    # Creating Grouped Bar Chart

    fig = go.Figure()

    fig.add_trace(
        go.Bar(x=top10["Category"], y=top10["avg_rating"], name="Average Rating")
    )
    fig.add_trace(
        go.Bar(x=top10["Category"], y=top10["total_reviews"], name="Total Reviews")
    )
    fig.update_layout(
        barmode="group",
        title="Top 10 App Categories (Jan Updates, ≥4.0 Avg Rating, ≥10MB Avg Size)",
        xaxis_title="Category",
        yaxis_title="Values",
        legend_title="Metrics",
    )
    return fig
