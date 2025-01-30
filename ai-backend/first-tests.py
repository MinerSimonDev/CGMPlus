import pandas as pd

# Versuchen, die CSV-Datei zu laden und Fehler zu behandeln
file_path = r'..\dataCollection\raw_data.csv'

try:
    # Beim Laden des CSVs das Semikolon als Trennzeichen angeben
    df = pd.read_csv(file_path, sep=';')
except FileNotFoundError:
    print(f"Die Datei unter {file_path} wurde nicht gefunden.")
    raise

# Überprüfen der Spaltennamen
print("Spaltennamen im DataFrame:", df.columns)

# Bereinigen der Spaltennamen (entfernen von führenden und folgenden Leerzeichen)
df.columns = df.columns.str.strip()

# Überprüfen der ersten Zeilen des DataFrames
print(df.head())

# Auswahl der relevanten Spalten
glucose = df[['timestamp', 'svg']]

# Entfernen der Zeilen mit den Indizes 1 bis 12
glucose = glucose.drop([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

# Index zurücksetzen
glucose.reset_index(drop=True, inplace=True)

# Umwandlung der 'timestamp' Spalte in datetime
glucose['timestamp'] = pd.to_datetime(glucose['timestamp'], errors='coerce')

# Überprüfen der ersten Zeilen des DataFrames
print(glucose.head())

# count | mean | std | min | 25% | 50% | 75% | max
print(glucose.describe().transpose())
