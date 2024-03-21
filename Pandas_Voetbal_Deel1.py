# Library's importeren
import pandas as pd
import numpy as np

# Kolommen van wedstrijden.csv ophalen
columns = ["seizoen","speeldag","datum","tijdstip","id","thuisploeg","uitploeg","thuisstand","uitstand"]
df = pd.read_csv('wedstrijden.csv', encoding='latin1',
names=columns, sep=";")

# Invalide waardes weghalen
df = df[df.speeldag.notnull()]

# Floats omzetten naar int64
df.speeldag = df.speeldag.astype('int64')
df.thuisstand = df.thuisstand.astype('int64')
df.uitstand = df.uitstand.astype('int64')

# Kolommen voor doelpunten 
df_doelpunten = pd.read_csv("doelpunten.csv", encoding='latin1',
names=['seizoen', 'speeldag', 'datum', 'tijd', 'id', 'thuisploeg', 'uitploeg',
'minuten', 'tijdgoal', 'goalploeg', 'thuisstand', 'uitstand'], sep=";")
df_doelpunten.head()

# Invalide waardes weghalen
df_doelpunten = df_doelpunten[df_doelpunten.speeldag.notnull()]

# Floats omzetten naar int64
df_doelpunten.thuisstand = df_doelpunten.thuisstand.astype('int64')
df_doelpunten.uitstand = df_doelpunten.uitstand.astype('int64')

# Lijst maken van alle matches zonder goals
df_geenGoals = df.loc[(df['thuisstand'] == 0) & (df['uitstand'] == 0)]
df_geenGoals.count()

# Lijst maken van alle ID's van wedstrijden zonder goals
df_doelpunten.id = df_doelpunten.id.astype('str')
lst = list(df_geenGoals.id)

# Alle doelpunten die verbonden zijn met een match die "eindigde" zonder goals
df_goals = df_doelpunten[df_doelpunten.id.isin(lst)]


# IDS Toevoegen


# Kolommen voor ID's voor de thuisploegen van alle wedstrijden
columns = ["club_id", "thuisploeg", "huisstamnummer", "huisroepnaam"]
id_df = pd.read_csv("stamnummers.csv", sep=";", header=None)
id_df.columns = columns

# Drop duplicate ploegen
id_df.drop(index=115, inplace=True)
id_df.drop(index=24, inplace=True)
id_df.drop(index=48, inplace=True)
id_df.drop(index=131, inplace=True)

# Merge de twee dataframes on de ploeg kolom
df = pd.merge(df, id_df, on="thuisploeg", how="left")

# Kolommen voor ID's voor de uitploegen van alle wedstrijden
columns = ["club_id", "uitploeg", "uitstamnummer", "uitroepnaam"]
id_df.columns = columns
df = pd.merge(df, id_df, on="uitploeg", how="left")

# Drop overbodige kolommen
df = df.drop(columns="club_id_y")
df = df.drop(columns="thuisploeg")
df = df.drop(columns="uitploeg")
df = df.drop(columns="club_id_x")

# Herangschik alle kolommen
desired_order = ["seizoen", "speeldag", "datum", "tijdstip", "id", "huisstamnummer", "huisroepnaam",
                 "uitstamnummer", "uitroepnaam", "thuisstand", "uitstand"]
df = df[desired_order]

# Een csv file aanmaken
df.to_csv('wedstrijden_final.csv', index=False, header=None)