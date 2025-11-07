import pandas as pd
from datetime import datetime
import pytz

# Importing all task chart functions
from task1 import generate_task1_chart
from task2 import generate_task2_chart
from task3 import generate_task3_chart
from task4 import generate_task4_chart
from task5 import generate_task5_chart
from task6 import generate_task6_chart

# Loading the dataset
data = pd.read_csv("data/cleaned_playstore.csv")

# IST time
ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)

# List to hold chart titles and figures
charts = []

# Task 1: 3PM-5PM IST
if 15 <= now.hour < 17:
    charts.append(("Task 1: Average Rating & Reviews", generate_task1_chart(data)))
else:
    charts.append(("Task 1: Average Rating & Reviews", None))

# Task 2: 6PM-8PM IST
if 18 <= now.hour < 20:
    charts.append(("Task 2: Global Installs Choropleth", generate_task2_chart(data)))
else:
    charts.append(("Task 2: Global Installs Choropleth", None))

# Task 3: 1PM-2PM IST
if 13 <= now.hour < 14:
    charts.append(("Task 3: Free vs Paid Apps Dual-Axis", generate_task3_chart(data)))
else:
    charts.append(("Task 3: Free vs Paid Apps Dual-Axis", None))

# Task 4: 6PM-9PM IST
if 18 <= now.hour < 21:
    charts.append(("Task 4: Installs Trend by Category Time Series Line", generate_task4_chart(data)))
else:
    charts.append(("Task 4: Installs Trend by Category Time Series Line", None))

# Task 5: 5PM-7PM IST
if 17 <= now.hour < 19:
    charts.append(("Task 5: Bubble Chart - Size vs Rating", generate_task5_chart(data)))
else:
    charts.append(("Task 5: Bubble Chart - Size vs Rating", None))

# Task 6: 4PM-6PM IST
if 16 <= now.hour < 18:
    charts.append(("Task 6: Stacked Area - Cumulative Installs", generate_task6_chart(data)))
else:
    charts.append(("Task 6: Stacked Area - Cumulative Installs", None))

# Build HTML dashboard
html = """
<html>
<head>
<title>Google Play Store Dashboard</title>
<style>
body { 
    font-family: Arial; 
    background: #121212; 
    margin: 0; 
    padding: 0; 
}
header { 
    text-align: center; 
    background: #3c4042; 
    color: white; 
    padding: 15px; 
    font-size: 24px; 
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
}
header img {
    height: 40px; 
}
section { 
    margin: 20px auto; 
    padding: 20px; 
    max-width: 1200px; 
    background: white; 
    border-radius: 10px; 
    box-shadow: 0 3px 10px rgba(0,0,0,0.1); 
}
h2 { 
    color: #343a40; 
    text-align: center; 
}
p { 
    text-align: center; 
    color: red; 
    font-weight: bold; 
}
</style>
</head>
<body>
<header>Google Play Store Dashboard
<img src="images/playstore_icon.png" alt="Play Store" style="height:60px; margin-left:10px;">
</header>
"""

# Adding each chart to the dashboard
for title, fig in charts:
    html += "<section>"
    html += f"<h2>{title}</h2>"
    
    # I added a special message for chart 2
    if title == "Task 2: Choropleth Map":
        html += "<p style='text-align:center; color:#007bff; font-weight:normal;'>Note: If the chart appears empty, there is no 'Country' column in the dataset.</p>"
    
    # Inserting chart and the placeholder message
    if fig:
        html += fig.to_html(full_html=False, include_plotlyjs='cdn')
    else:
        html += "<p>Chart not available in this time window</p>"
    html += "</section>"

html += "</body></html>"

# Saving the final dashboard
with open("dashboard.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Dashboard generated as: dashboard.html")