# Cleaning up the doelpunten.csv file
import pandas as pd

# Creating doelpunten dataframe
df = pd.read_csv("doelpunten.csv", encoding='latin1', 
names=['Match_ID', 'Seizoen', 'Speeldag', 'Datum', 'Startuur', 'Thuisploeg', 'Uitploeg', 
'Scorende ploeg', 'Tijdstip goal', 'Score thuisploeg', 'Score Uitploeg'])

# Adding column for minute goal
def convert(row):
    uur, minuut = row['Tijdstip goal'].split(":")
    start_uur, start_minuut = row['Startuur'].split(":")
    
    uur = int(uur)
    minuut = int(minuut)
    start_uur = int(start_uur)
    start_minuut = int(start_minuut)

    if uur < start_uur:
        absolute_minuten = (60 - start_minuut) + (uur + 1 - start_uur) * 60 + minuut
    else:
        absolute_minuten = (uur - start_uur) * 60 + minuut - start_minuut
    
    return absolute_minuten

df['Minuut goal'] = df.apply(convert, axis=1)

controle_binnen_tijd = df[df['Minuut goal'] > 120]
print(len(controle_binnen_tijd))

# Creating matches dataframe
wedstrijden_df = pd.read_csv('wedstrijden.csv', encoding='latin1',
names=['Match_ID', 'Seizoen', 'Speeldag', 'Datum', 'Startuur', 'Thuisploeg', 
'Score thuisploeg', 'Score Uitploeg', 'Uitploeg'])

# Merge dataframes
df_unique = df.drop_duplicates(subset=['Match_ID'], keep='last')
# wedstrijden_df_unique = wedstrijden_df.drop_duplicates(subset=['Match_ID'], keep='last')

df_unique['Match_ID'] = df_unique['Match_ID'].astype(str)
wedstrijden_df.Match_ID = wedstrijden_df.Match_ID.astype(str)

merged_df = pd.merge(df_unique, wedstrijden_df, on="Match_ID", how="inner")

# Vergelijjken datums
merged_df['Datums_gelijk'] = merged_df['Datum_x'] == merged_df['Datum_y']

merged_df["Datums_gelijk"].value_counts()

# Controleren of uiteindelijke resultaat overeenkomt met doelpunten
fouten = merged_df[(merged_df['Score thuisploeg_x'] != merged_df['Score thuisploeg_y']) | 
                        (merged_df['Score Uitploeg_x'] != merged_df['Score Uitploeg_y'])]

if len(fouten) == 0:
    print("Geen fouten")
else:
    print(fouten.index)