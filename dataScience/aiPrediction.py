# Datenimport und Vorverarbeitung
import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# Pfad zu den JSON-Daten
data_path = r'C:\Users\simon\Desktop\CGM+\dataCollection\mergedData\combined_entries.json'

# Lade die JSON-Daten
with open(data_path, 'r') as file:
    data = json.load(file)

# Umwandeln der JSON-Daten in einen DataFrame
df = pd.json_normalize(data)

# Zeitstempel in Datetime umwandeln
df['date'] = pd.to_datetime(df['date'], unit='ms')

# Zusätzliche zeitliche Features erstellen
df['hour'] = df['date'].dt.hour
df['day_of_week'] = df['date'].dt.weekday
df['month'] = df['date'].dt.month
df['is_weekend'] = df['day_of_week'].isin([5, 6])  # Samstag und Sonntag
df['season_Spring'] = (df['month'] >= 3) & (df['month'] <= 5)
df['season_Summer'] = (df['month'] >= 6) & (df['month'] <= 8)
df['season_Fall'] = (df['month'] >= 9) & (df['month'] <= 11)
df['season_Winter'] = (df['month'] == 12) | (df['month'] <= 2)

# Zielvariable und Features definieren
features = ['hour', 'day_of_week', 'month', 'is_weekend',
            'season_Spring', 'season_Summer', 'season_Fall', 'season_Winter']

# Entferne Zeilen mit fehlenden Werten in den Features oder der Zielvariable
df = df.dropna(subset=features + ['sgv'])

# Zielvariable: Blutzucker (sgv)
X = df[features]  # Features
y = df['sgv']  # Zielvariable

# Aufteilen der Daten in Trainings- und Testset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modell erstellen und trainieren
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Vorhersagen machen
y_pred = model.predict(X_test)

# Modell evaluieren
mae = mean_absolute_error(y_test, y_pred)
print(f'Mean Absolute Error: {mae}')

# Vorhersage für 20 Uhr
sample_data = pd.DataFrame({
    'hour': [17],             # 20 Uhr
    'day_of_week': [4],       # Freitag (z. B. ändern für andere Tage)
    'month': [1],             # Januar
    'is_weekend': [0],        # Kein Wochenende
    'season_Spring': [0],     # Nicht Frühling
    'season_Summer': [0],     # Nicht Sommer
    'season_Fall': [0],       # Nicht Herbst
    'season_Winter': [1]      # Winter
})

# Vorhersage durchführen
prediction = model.predict(sample_data)
print(f'Vorhersage für 20 Uhr: {prediction[0]}')
