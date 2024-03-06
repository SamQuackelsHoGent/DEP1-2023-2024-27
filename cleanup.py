import pandas as pd

# wedstrijden_df = pd.read_csv('voetbalData_Deel1.csv')
# klassementen_df = pd.read_csv('voetbalData_Deel2.csv')
# doelpunten_df = pd.read_csv('voetbalData_Deel3.csv')

def convert(row):
    startuur = row[4]
    uur, minuut = map(int, row[8].split(':'))
    start_uur, start_minuut = map(int, startuur.split(':'))

    if uur < start_uur:
        absolute_minuten = (60 - start_minuut) + (uur + 1 - start_uur) * 60 + minuut
    else:
        absolute_minuten = (uur - start_uur) * 60 + minuut - start_minuut
    
    return absolute_minuten

voorbeeld_rij = [4009206,'64/65',6,'18/10/1964','15:00','Lierse SK','Standard Luik','Lierse SK','16:17',7,0]

minuten_na_start = convert(voorbeeld_rij)
print(f"Aantal minuten na starttijd van de wedstrijd: {minuten_na_start}")