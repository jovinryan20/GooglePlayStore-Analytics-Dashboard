import pandas as pd
import plotly.graph_objects as go

# Loading the dataset
data = pd.read_csv("data/cleaned_playstore.csv")

def generate_task4_chart(data):

    # Converting the date column to datetime
    data["Last Updated"] = pd.to_datetime(data["Last Updated"], errors="coerce")

    # Filtering the data
    data = data[
        (~data["App"].str.lower().str.startswith(("x", "y", "z")))
        & (data["Category"].str.upper().str.startswith(("E", "C", "B", "D"))) # Adding the letter 'D' because it's asked in Dating as German 
        & (data["Reviews"] > 500)
        & (~data["App"].str.contains("S", case=False, na=False))
    ]

    # Translating category names
    data["Category"] = data["Category"].replace(
        {
            "BEAUTY": "सौंदर्य",  # Hindi
            "BUSINESS": "வணிகம்",  # Tamil
            "DATING": "Verabredung",  # German
        }
    )

    # Extracting month from the date
    data["Month"] = data["Last Updated"].dt.to_period("M")

    # Grouping total installs by month and category
    trend = data.groupby(["Month", "Category"])["Installs"].sum().reset_index()

    # Calculating month-over-month growth
    trend["Prev"] = trend.groupby("Category")["Installs"].shift(1)
    trend["Growth_%"] = ((trend["Installs"] - trend["Prev"]) / trend["Prev"]) * 100

    # Creating the time-series line chart
    fig = go.Figure()

    for cat in trend["Category"].unique():
        sub = trend[trend["Category"] == cat]

        # Normal line for installs
        fig.add_trace(
            go.Scatter(
                x=sub["Month"].astype(str),
                y=sub["Installs"],
                mode="lines+markers",
                name=cat,
            )
        )

        # Highlight months where growth > 20%
        high = sub[sub["Growth_%"] > 20]
        if not high.empty:
            fig.add_trace(
                go.Scatter(
                    x=high["Month"].astype(str),
                    y=high["Installs"],
                    fill="tozeroy",
                    mode="none",
                    fillcolor="rgba(255,165,0,0.3)",
                    name=f"{cat} Growth > 20%",
                )
            )

    fig.update_layout(
        title="Trend of Total Installs Over Time",
        xaxis_title="Month",
        yaxis_title="Total Installs",
        legend_title="App Categories",
        template="plotly_white",
    )
    return fig
