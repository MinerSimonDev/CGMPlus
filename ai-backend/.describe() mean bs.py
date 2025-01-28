import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Pfad zur JSON-Datei
file_path = r'..\dataCollection\mergedData\combined_entries.json'

try:
    # Laden der JSON-Datei
    with open(file_path, 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Die Datei unter {file_path} wurde nicht gefunden.")
    raise

# Konvertiere die JSON-Daten in ein pandas DataFrame
df = pd.json_normalize(data)

# Überprüfen der Spaltennamen
print("Spaltennamen im DataFrame:", df.columns)

# Auswahl der relevanten Spalten: 'dateString' und 'sgv'
glucose = df[['dateString', 'sgv']]

# Umwandlung der 'dateString' Spalte in datetime (mit .loc, um die Warnung zu vermeiden)
glucose.loc[:, 'timestamp'] = pd.to_datetime(glucose['dateString'], errors='coerce')

# Entfernen der 'dateString' Spalte
glucose = glucose.drop(columns=['dateString'])

# Entfernen der Zeilen mit den Indizes 1 bis 12
glucose = glucose.drop([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

# Index zurücksetzen
glucose.reset_index(drop=True, inplace=True)

# Überprüfen der ersten Zeilen des DataFrames
print(glucose.head())

# count | mean | std | min | 25% | 50% | 75% | max
print(glucose.describe().transpose())

# box and whisker plot / quartile vs. ausreißer
plt.figure(figsize=(10,4))
sns.boxplot(x=glucose['sgv'])
plt.title('Blood Glucose Interquartile Range, mu=144')
plt.show()

# verteilung auf die wochentage

glucose['Day'] = glucose['timestamp'].dt.date  # Extrahiere das Datum
glucose = glucose.rename(columns={'sgv': 'Glucose Value (mg/dl)'})  # Umbenennen der 'sgv'-Spalte

# Erstellen des Boxplots mit Plotly
fig = px.box(glucose, x="Day", y="Glucose Value (mg/dl)", points="all", color='Day')

# Anzeigen des Plots
fig.show()
