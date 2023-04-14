import pandas as pd
import sqlite3

df_edu = pd.read_csv('../../data/processed/education_data.csv', delimiter=';')
df_gdp = pd.read_csv('../../data/processed/GDP_data.csv', delimiter=';')
df_hea = pd.read_csv('../../data/processed/health_data.csv', delimiter=';')
df_hpi = pd.read_csv('../../data/processed/HPI_data.csv', delimiter=';')
df_inc = pd.read_csv('../../data/processed/income_data.csv', delimiter=';')
# df_mig = pd.read_csv('nazwa_pliku.csv')
df_pop = pd.read_csv('../../data/processed/population_20-22_data.csv', delimiter=';')
df_une = pd.read_csv('../../data/processed/unemployment_data.csv', delimiter=';')


conn = sqlite3.connect('../../data/baza_projekt.db')

df_edu.to_sql('education', conn, index=False, if_exists='replace', dtype={'FIPS code': 'INTEGER PRIMARY KEY'})
df_gdp.to_sql('gdp', conn, index=False, if_exists='replace', dtype={'FIPS code': 'INTEGER PRIMARY KEY'})
df_hea.to_sql('health', conn, index=False, if_exists='replace', dtype={'FIPS code': 'INTEGER PRIMARY KEY'})
df_hpi.to_sql('hpi', conn, index=False, if_exists='replace', dtype={'FIPS code': 'INTEGER PRIMARY KEY'})
df_inc.to_sql('income', conn, index=False, if_exists='replace', dtype={'FIPS code': 'INTEGER PRIMARY KEY'})
df_pop.to_sql('population', conn, index=False, if_exists='replace', dtype={'FIPS code': 'INTEGER PRIMARY KEY'})
df_une.to_sql('unemployment', conn, index=False, if_exists='replace', dtype={'FIPS code': 'INTEGER PRIMARY KEY'})

conn.close()


