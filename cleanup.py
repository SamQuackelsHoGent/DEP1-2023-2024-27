import pandas as pd

# wedstrijden_df = pd.read_csv('voetbalData_Deel1.csv')
klassementen_df = pd.read_csv('voetbalData_Deel2.csv', encoding='latin1', header=None)
doelpunten_df = pd.read_csv('voetbalData_Deel3.csv', encoding='latin1', header=None)

def convert(row):
    startuur = row[4]
    uur, minuut = map(int, row[8].split(':'))
    start_uur, start_minuut = map(int, startuur.split(':'))

    if uur < start_uur:
        absolute_minuten = (60 - start_minuut) + (uur + 1 - start_uur) * 60 + minuut
    else:
        absolute_minuten = (uur - start_uur) * 60 + minuut - start_minuut
    
    return absolute_minuten

doelpunten_df['11'] = doelpunten_df.apply(convert, axis=1)

print(doelpunten_df.head(30))