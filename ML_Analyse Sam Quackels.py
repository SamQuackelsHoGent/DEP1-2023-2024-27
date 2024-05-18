# Analyse 3
# Sam Quackels - G27

import pyodbc
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# Variabelen om te verbinden met DWH
server = '127.0.0.1,1500'  # Localhost / port forwarding
database = 'G27'  # DB naam
username = 'sa'   # DB username
password = 'G27SimonJonaSam' # DB wachtwoord (niet delen aub)

# String om te verbinden met de DWH
conn_str = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Connectie vastleggen met DWH
conn = pyodbc.connect(conn_str)

# Cursor aanmaken en gebruiken om data in te laden
cursor = conn.cursor()
query = "SELECT * FROM klassement"
klassement = pd.read_sql(query, conn)

# Connectie verbreken met de DWH
conn.close()

# Toon head van de dataframe 'klassement'
print(klassement.head())


x = klassement[['aantalGespeelde', 'doelpuntenVoor', 'doelpuntenTegen']] # Wat we gebruiken
y = klassement['stand'] # Wat we bekomen gebaseerd op x

# Data 80/20 training/testing opsplitsen
x_training, x_testing, y_training, y_testing = train_test_split(x, y, test_size=0.2, random_state=42)

# Aantal records in de sets weergeven
print("Aantal records in de trainingsset:", len(x_training))
print("Aantal records in de testset:", len(x_testing))

# Regressie model aanmaken
# Ik heb regressie gekozen omdat we exacte posities willen voorspellen met continue numerieke gegevens.
# Ik heb RandomForest gekozen omdat het een goed allround algoritme is en een guest 
# speaker bij Machine Learning zei dat je dit moest kiezen als je twijfelde
# Ook gaf dit me het beste resultaat over LinearRegression
model = RandomForestRegressor()

# Train het model gebaseerd op de 80% train data
model.fit(x_training, y_training)

# Voorspel y (stand) gebaseerd op x_testing data
y_predicted = model.predict(x_testing)

# Bereken de accuratie van het model
mse = mean_squared_error(y_testing, y_predicted)
print("Mean Squared Error (Gelimiteerde data):", mse)


###########
## Ik was niet zeker of het de bedoeling was om het te trainen op enkel de aantalGespeelde, doelpuntenVoor en doelpuntenTegen, of ook op stamnummer etc.
## Dus hier is hetzelfde met alle data
###########


x = klassement.drop(['stand', 'roepnaam'], axis=1) # Wat we gebruiken
y = klassement['stand'] # Wat we willen

# Data 80/20 opsplitsen
x_training, x_testing, y_training, y_testing = train_test_split(x, y, test_size=0.2, random_state=42)

# Regressie model aanmaken
model = RandomForestRegressor()

# Train het model op train data
model.fit(x_training, y_training)

# Voorspel stand gebaseerd op test data
y_predicted = model.predict(x_testing)

# Bereken de accuratie van het model
mse = mean_squared_error(y_testing, y_predicted)
print("Mean Squared Error (Alle data):", mse)