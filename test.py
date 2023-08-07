# %%
#Importing libraries
import pandas as pd
from datetime import date, timedelta
import matplotlib.pyplot as plt
import numpy as np
import sdt.changepoint as c
import math

# %%
# create a dataframe from the csv file
dataframe = pd.read_csv('data.csv')

# filter data from 2021-07-16 to 2021-08-15
dataframe = dataframe[(dataframe['date'] >= '2021-07-16') & (dataframe['date'] <= '2021-08-15')]

# %%
'''# partiziona il dataframe con soltanto gli iso_code che iniziano con "OWID_" e salvali in un nuovo dataframe
df_owid = dataframe[dataframe['iso_code'].str.startswith('OWID_')]
# per ogni iso_code all'interno del nuovo dataframe crea un plot con y positive_rate e x date
for iso_code in df_owid['iso_code'].unique():
    if df_owid[df_owid['iso_code'] == iso_code]['new_cases'].isnull().all():
        continue
    plt.plot(df_owid[df_owid['iso_code'] == iso_code]['date'], df_owid[df_owid['iso_code'] == iso_code]['new_cases'])
    plt.title("Positive rate - " + df_owid[df_owid['iso_code'] == iso_code]['location'].unique()[0])
    plt.ylabel("new_cases")
    plt.xlabel("Date")
    plt.xticks(rotation=90)
    plt.show()'''

# %%
#filter by iso_cod that not contain "OWID" prefix
dataframe = dataframe[~dataframe['iso_code'].str.contains("OWID")]

# aggragate by iso_code and date and sum total_cases, total_deaths, population, total_vaccinations, new_cases, mind positive_rate, max positive_rate,KEEP LOCATION 
dataframe = dataframe.groupby(['iso_code', 'date']).agg({'total_cases': 'sum', 'total_deaths': 'sum', 'total_vaccinations': 'sum', 'new_cases': 'sum', 'positive_rate': 'max','population': 'sum', 'location': 'max'})

# save dataframe in csv file
#dataframe.to_csv('dataframe.csv')

#iso_codes_europe = [ "ITA", "FRA", "DEU", "ESP", "GBR", "CHE", "NLD", "BEL", "AUT", "SWE", "NOR", "FIN", "GRC", "PRT", "DNK", "POL", "CZE", "HUN", "ROU", "BGR", "HRV", "SVK", "SVN", "IRL", "LUX", "EST", "LVA", "LTU", "MLT", "CYP", "ISL", "LIE", "AND", "MCO", "SMR", "VAT"]
# rimuovo da iso_cedes_europe tutti i codici che non sono presenti nel dataframe
#iso_codes_europe = [iso_code for iso_code in iso_codes_europe if iso_code in dataframe.index.get_level_values('iso_code').unique()]

# per ogni iso_code stampa il plot di positive_rate
'''for iso_code in iso_codes_europe:
    plt.plot(dataframe.loc[iso_code]['new_cases'])
    plt.title("New cases - " + dataframe.loc[iso_code]['location'].unique()[0])
    plt.ylabel("new cases")
    plt.xlabel("Date")
    plt.xticks(rotation=90)
    plt.show()'''


# %%
def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier

# %%
#Change point detection with Bayesian Offline

BayesOffline = c.BayesOffline()
media_changepoint = 0.0
count_changepoint = 0.0
min_changepoint = (999,"error")
max_changepoint = (-1,"error")
save_me = []
tabella = pd.DataFrame(columns=['State','FirstSlope','SecondSlope','when'])

iso_codes = dataframe.index.get_level_values('iso_code').unique()

for code in iso_codes:
    # Out is a list of possible changepoint "indices"
    values = dataframe[code]['new_cases'].values
    print("CHE CE DENTRO? ", values)

    prob = 0.9
    out = []
    plot_out = []
    
    while len(out) == 0:
        prob = prob * 0.9
        out = BayesOffline.find_changepoints(values, prob_threshold=prob)
    
    print("OUT", out)
    # Crea un plot con i punti di cambio colorati
    plt.figure(figsize=(10, 6))
    plt.plot(iso_data['date'], iso_data['new_cases'], label='Nuovi casi')
    plt.scatter(iso_data['date'].iloc[change_points], iso_data['new_cases'].iloc[change_points], color='red', label='Punto di cambio')
    plt.title(f"Punti di cambio per {code}")
    plt.xlabel('Data')
    plt.ylabel('Nuovi casi')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# %%



