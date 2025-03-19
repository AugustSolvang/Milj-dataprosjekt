import pandas as pd
from pandasql import sqldf

# Eksempeldata
data = {'Navn': ['Alice', 'Bob', None, 'David'],
        'Alder': [25, None, 30, 22],
        'By': ['Oslo', 'Bergen', 'Trondheim', None]}

df = pd.DataFrame(data)

# Identifisere manglende verdier
print(df.isnull().sum())

# Håndtere manglende verdier
df['Navn'].fillna('Ukjent', inplace=True)  # Fyller manglende navn med 'Ukjent'
df['Alder'].fillna(df['Alder'].mean(), inplace=True)  # Fyller med gjennomsnittsalder
df.dropna(subset=['By'], inplace=True)  # Fjerner rader hvor 'By' mangler

df['Aldersgruppe'] = ['Ung' if alder < 30 else 'Voksen' for alder in df['Alder']]

query = "SELECT * FROM df WHERE Alder > 25"
df_filtrert = sqldf(query, globals())

print(df)

print(df_filtrert)
