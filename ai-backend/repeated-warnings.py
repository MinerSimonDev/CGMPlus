import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import timedelta

file_path = r'..\dataCollection\mergedData\combined_entries.json'

try:
    with open(file_path, 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Die Datei unter {file_path} wurde nicht gefunden.")
    raise

# Daten laden und vorbereiten
df = pd.json_normalize(data)
glucose = df[['dateString', 'sgv']]
glucose.loc[:, 'timestamp'] = pd.to_datetime(glucose['dateString'], errors='coerce')
glucose = glucose.drop(columns=['dateString'])
glucose = glucose.drop([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])  # falls fehlerhafte Daten vorhanden sind
glucose.reset_index(drop=True, inplace=True)

# Aggregierte Werte für normale und abnormale Glukosewerte
glucose['Aggregate'] = [180 if glucose_val >= 180 else 70 if glucose_val <= 70 else 110 for glucose_val in glucose['sgv']]

# Interaktive Plotly-Grafik
fig = px.line(glucose, 
              x="timestamp", 
              y=["sgv", "Aggregate"], 
              title="Glucose Value Vs. Time", 
              labels={"sgv": "Glucose Fluctuation", 
                      "Aggregate": "Aggregate Blood Glucose"})

fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([dict(count=1, label="1d", step="day", stepmode="backward"),
                      dict(count=1, label="1m", step="month", stepmode="backward"),
                      dict(count=1, label="YTD", step="year", stepmode="todate"),
                      dict(count=1, label="1y", step="year", stepmode="backward"),
                      dict(step="all")])
    )
)

fig.update_layout(xaxis_title="Time", yaxis_title="Glucose Value (mg/dL)")
fig.show()

# Daten für die letzten 7 Tage extrahieren
glucose['timestamp'] = glucose['timestamp'].dt.tz_localize(None)
last_week = pd.to_datetime("today") - timedelta(days=7)
last_week = last_week.replace(tzinfo=None)

last_week_glucose = glucose[glucose['timestamp'] >= last_week]

# Werte, die außerhalb des normalen Bereichs sind
out_of_range_last_week = last_week_glucose[(last_week_glucose['sgv'] < 70) | (last_week_glucose['sgv'] > 180)]

# Zeilen nach Zeitstempel sortieren
out_of_range_last_week = out_of_range_last_week.sort_values('timestamp')

# Berechnung der Zeitdifferenz zwischen den Zeitstempeln
out_of_range_last_week['time_diff'] = out_of_range_last_week['timestamp'].diff().fillna(pd.Timedelta(seconds=0))

# Gruppierung der Daten: Wenn die Zeitdifferenz mehr als 10 Minuten beträgt, wird eine neue Gruppe gestartet
out_of_range_last_week['group'] = (out_of_range_last_week['time_diff'] > pd.Timedelta(minutes=10)).cumsum()

# Gruppieren und Aggregieren
grouped = out_of_range_last_week.groupby('group').agg(
    start_time=('timestamp', 'first'),
    end_time=('timestamp', 'last'),
    glucose_range=('sgv', 'mean')
).reset_index()

# Gruppen filtern, um nur relevante Zeiträume zu behalten
filtered_groups = []
for i, row in grouped.iterrows():
    # Wenn mehr als 10 Minuten zwischen der aktuellen Gruppe und der vorherigen Gruppe liegen, wird die Gruppe beibehalten
    if i == 0 or (row['start_time'] - grouped.iloc[i-1]['end_time'] > pd.Timedelta(minutes=10)):
        filtered_groups.append(row)

# Ausgabe der gefilterten Zeiträume
for row in filtered_groups:
    print(f"Zeitraum: {row['start_time']} bis {row['end_time']}, Durchschnittlicher Glukosewert: {row['glucose_range']} mg/dL")
