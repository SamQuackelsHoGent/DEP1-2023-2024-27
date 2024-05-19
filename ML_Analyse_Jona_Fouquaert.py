# Jona Fouquaert
# G27
# Analyse 2


import pyodbc
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# Connection parameters
server = '127.0.0.1,1500'  # server name and port
database = 'G27'  # name of your database
username = 'sa' # username
password = 'G27SimonJonaSam' # password

# Create a connection string
conn_str = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Establish connection
conn = pyodbc.connect(conn_str)

# Create a cursor object
cursor = conn.cursor()

# load tables
query = "SELECT * FROM klassement"
klassement = pd.read_sql(query, conn)

query = "SELECT * FROM doelpunten"
doelpunten = pd.read_sql(query, conn)

query = "SELECT * FROM dimWedstrijden"
dimWedstrijden = pd.read_sql(query, conn)

query = "SELECT * FROM dimDatum"
dimDatum = pd.read_sql(query, conn)

query = "SELECT * FROM dimPloeg"
dimPloeg = pd.read_sql(query, conn)

query = "SELECT * FROM DimTime"
DimTime = pd.read_sql(query, conn)

query = "SELECT * FROM weddenschapSource"
weddenschapSource = pd.read_sql(query, conn)

query = "SELECT * FROM weddenschapTarget"
weddenschapTarget = pd.read_sql(query, conn)


# Close the connection
conn.close()

# Function to test the data
def testDataframes(df):
    print(df.head())

testDataframes(klassement)

# Analyse 2
y = klassement['driePunten']
X = klassement.drop(['seizoen', 'speeldag', 'stand', 'stamnummer', 'roepnaam', 
                     'aantalGespeelde', 'doelpuntenVoor', 'doelpuntenTegen', 
                     'doelpuntenSaldo', 'tweePuntenLinks', 'tweePuntenRechts', 'driePunten'], axis=1)

# Split the dataset
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Check the shapes of the datasets
print("shape trainingset: ", X_train.shape, X_test.shape)
print("shape testset: ", y_train.shape, y_test.shape)

# Classification pr Regression?
# Because we are predicting a namuber value -> Regression problem (There are 87 unique values -> a little to much for classification)

# Select model
# Decision Tree -> Because the dataset is non-linear ideal for Dicision Tree + Efficient compared to a random forest regressor
from sklearn.tree import DecisionTreeRegressor
Dtree = DecisionTreeRegressor(random_state=42)
Dtree.fit(X_train, y_train)
y_pred = Dtree.predict(X_test)

# Evaluate the model
# We use the mean squared error and mean absolute error te evaluate the accuracy of the model
from sklearn.metrics import mean_squared_error, mean_absolute_error
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
print("Mean Squared Error:", mse)
print("Mean Absolute Error:", mae)