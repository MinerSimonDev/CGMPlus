from datetime import datetime, timezone

# Liste der Datensätze
data = [
    "1711411106096,281",
    "1711410804983,281",
    "1711410503901,276",
    "1711410203795,267",
    "1711409724267,261",
    "1711409422811,254",
    "1711409122507,249",
    "1711408821052,242",
    "1711408520750,237",
    "1711408220833,234",
    "1711407919798,227",
    "1711407620228,214",
    "1711407318225,204",
    "1711406958412,192",
    "1711406656572,180",
    "1711406356942,168",
    "1711405995593,155",
    "1711405635932,144",
    "1711405334091,132",
    "1711405033820,125",
    "1711404613752,119",
    "1711404312055,113"
]

# Liste für die konvertierten Ergebnisse
converted_data = []

# Iteration über alle Datensätze
for entry in data:
    # Splitten des Datensatzes in Zeitstempel und extra Zahl
    timestamp_str, extra_number_str = entry.split(',')
    timestamp_ms = int(timestamp_str)
    extra_number = int(extra_number_str)
    
    # Unix-Zeitstempel in Sekunden umwandeln
    timestamp_sec = timestamp_ms / 1000
    
    # Erstellen eines UTC-datetime-Objekts mit timezone
    date_str = datetime.fromtimestamp(timestamp_sec, timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
    
    # Hinzufügen der konvertierten Daten zur Liste
    converted_data.append((date_str, extra_number))

# Ergebnis anzeigen
print(converted_data)
