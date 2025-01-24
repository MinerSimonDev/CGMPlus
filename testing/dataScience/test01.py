import pandas as pd
import json
from datetime import datetime

# JSON-Daten laden
with open(r'D:\Windowsordner\Desktop\CGMPlus\dataCollection\mergedData\combined_entries.json', 'r') as f:
    data = json.load(f)

# JSON in DataFrame umwandeln
df = pd.DataFrame(data)

# Datum konvertieren
df['date'] = pd.to_datetime(df['date'], unit='ms')
df['hour'] = df['date'].dt.hour
df['weekday'] = df['date'].dt.day_name()

# Relevante Spalten behalten
df = df[['date', 'sgv', 'direction', 'hour', 'weekday', 'device']]
print(df.head())

# Differenz zwischen aufeinanderfolgenden Werten berechnen
df['delta'] = df['sgv'].diff()

# Starke Anstiege/Abfälle markieren
df['warning'] = (df['delta'] > 30) | (df['delta'] < -30)

# Warnungen anzeigen
print(df[df['warning']])

# Wiederholte Ereignisse zählen
df['double_up_count'] = (df['direction'] == 'DoubleUp').rolling(window=3).sum()

# Warnung, wenn "DoubleUp" dreimal in Folge auftritt
df['trend_warning'] = df['double_up_count'] >= 3

# Warnungen anzeigen
print(df[df['trend_warning']])

# Durchschnittlicher Blutzucker pro Stunde
hourly_avg = df.groupby('hour')['sgv'].mean()
print(hourly_avg)

# Plotten der Ergebnisse
import matplotlib.pyplot as plt

hourly_avg.plot(kind='bar', title='Durchschnittlicher Blutzucker pro Stunde')
plt.xlabel('Stunde')
plt.ylabel('Blutzucker (sgv)')
plt.show()

# Warnung für kritische Richtungen
df['critical_direction'] = df['direction'].isin(['DoubleUp', 'DoubleDown'])

# Kritische Werte anzeigen
print(df[df['critical_direction']])

import seaborn as sns

# Blutzuckerwerte über Zeit
plt.figure(figsize=(12, 6))
sns.lineplot(x='date', y='sgv', data=df, marker='.')
plt.title('Blutzuckerwerte über Zeit')
plt.xlabel('Zeit')
plt.ylabel('Blutzucker (sgv)')
plt.xticks(rotation=45)
plt.show()
