import pandas as pd
import plotly.graph_objects as go

# Importing the dataset
data = pd.read_csv("data/cleaned_playstore.csv")

def generate_task2_chart(data):

    # Excluding categories starting with A, C, G, S
    data = data[~data["Category"].str.upper().str.startswith(("A", "C", "G", "S"))]

    # Assigning one country per category since 'Country' column is missing in the csv
    category_country = {
        "Business": "USA",
        "Beauty": "IND",
        "Dating": "GBR",
        "Entertainment": "CAN",
        "Health": "AUS",
        "Productivity": "DEU",
        "Travel & Local": "FRA",
        "Photography": "JPN",
    }
    # Keep only categories present in mapping
    data = data[data["Category"].isin(category_country.keys())]
    # Add Country column
    data["Country"] = data["Category"].map(category_country)

    # Grouping by Category and Country to get total installs
    grouped = data.groupby(["Category", "Country"], as_index=False).agg(
        total_installs=("Installs", "sum")
    )

    # Top 5 categories by global installs
    top_categories = (
        grouped.groupby("Category")["total_installs"].sum().nlargest(5).index
    )
    filtered = grouped[grouped["Category"].isin(top_categories)].copy()

    # Highlight installs > 1 million
    filtered["highlight"] = filtered["total_installs"] > 1_000_000

    # Choropleth chart
    fig = go.Figure()
    for cat in top_categories:
        cat_data = filtered[filtered["Category"] == cat]
        fig.add_trace(
            go.Choropleth(
                locations=cat_data["Country"],
                z=cat_data["total_installs"],
                text=cat_data["Country"],
                colorscale="Viridis",
                name=cat,
                showscale=True,
                locationmode="ISO-3",
            )
        )

    fig.update_layout(
        title="Global App Installs by Category. Note: The map looks empty because it only has data for a few scattered countries.",
        geo=dict(showframe=False, projection_type="natural earth"),
    )

    return fig
