import pandas as pd
import json
import os
import matplotlib.pyplot as plt

# Pfad zu den JSON-Daten
data_path = r'C:\Users\simon\Desktop\CGM+\dataCollection\mergedData\combined_entries.json'

# Lade die JSON-Daten
with open(data_path, 'r') as file:
    data = json.load(file)

# Umwandeln der JSON-Daten in einen DataFrame
df = pd.json_normalize(data)

# Überprüfe die ersten paar Zeilen der Daten
print(df.head())

# Zeitstempel in Datetime umwandeln
df['date'] = pd.to_datetime(df['date'], unit='ms')

# Optional: Erstelle zusätzliche Features wie die Stunde und den Wochentag
df['hour'] = df['date'].dt.hour
df['day'] = df['date'].dt.date
df['day_of_week'] = df['date'].dt.weekday
df['month'] = df['date'].dt.month

# Überprüfe die ersten paar Zeilen
print(df.head())

# Aggregation der Blutzuckerwerte pro Tag
daily_data = df.groupby('day').agg({
    'sgv': ['mean', 'max', 'min'],  # Blutzuckerwerte: Mittelwert, Maximum, Minimum
    'delta': 'mean'                # Durchschnittliche Änderung des Blutzuckers
}).reset_index()

# Überprüfe die aggregierten Daten
print(daily_data.head())

# Blutzucker über die Zeit hinweg visualisieren
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['sgv'], label='Blutzucker')
plt.xlabel('Zeit')
plt.ylabel('Blutzucker (mg/dl)')
plt.title('Blutzuckerspiegel über die Zeit')
plt.xticks(rotation=45)
plt.show()

# Durchschnittlicher Blutzucker pro Wochentag
plt.figure(figsize=(10, 6))
df.groupby('day_of_week')['sgv'].mean().plot(kind='bar')
plt.title('Durchschnittlicher Blutzucker pro Wochentag')
plt.xlabel('Wochentag')
plt.ylabel('Durchschnittlicher Blutzucker')
plt.xticks(rotation=0)
plt.show()
