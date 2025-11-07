import pandas as pd
import plotly.express as px

#Loading cleaned dataset
data = pd.read_csv("data/cleaned_playstore.csv")

def generate_task5_chart(data):

    data = data.copy()
    #Applying all filters
    data = data[
        (data["Rating"] > 3.5)
        & (data["Reviews"] > 500)
        & (data["Installs"] > 50000)
        & (~data["App"].str.contains("S", case=False, na=False))
        & (data["Sentiment_Subjectivity"] > 0.5)
        & (data["Category"].str.lower().isin(
            ["game", "beauty", "business", "comics", "communication",
             "dating", "entertainment", "social", "events"]
        ))
    ].copy()
 
    #Translating categories
 
    data["Category"] = data["Category"].str.title()
    translations = {
        "Beauty": "सौंदर्य",  #Hindi
        "Business": "வணிகம்", #Tamil
        "Dating": "Verabredung" #German
    }
    data["Category"] = data["Category"].replace(translations)

    #Highlight Game category in pink
    data["Color"] = data["Category"].apply(
        lambda x: "pink" if x.lower() == "game" else "lightblue"
    )

    #Ploting bubble chart
    fig = px.scatter(
        data,
        x="Size_MB",
        y="Rating",
        size="Installs",
        color="Color",
        hover_name="App",
        title="App Size vs Rating (Bubble Size = Installs)",
        labels={"Size_MB": "App Size (MB)", "Rating": "Average Rating"},
        size_max=40,
    )

    fig.update_layout(
        showlegend=False,
        template="plotly_white",
    )
    return fig
