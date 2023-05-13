import os
import pandas as pd
from src.utils.projekt_utils import get_project_root
import re
from sklearn.preprocessing import StandardScaler



def get_data_by_state():
    education_data = pd.read_csv(os.path.join(get_project_root(), 'data/processed/education_data.csv'), sep=';')
    GDP_data = pd.read_csv(os.path.join(get_project_root(), 'data/processed/GDP_data.csv'), sep=';')
    health_data = pd.read_csv(os.path.join(get_project_root(), 'data/processed/health_data.csv'), sep=';')
    HPI_data = pd.read_csv(os.path.join(get_project_root(), 'data/processed/HPI_data.csv'), sep=';')
    income_data = pd.read_csv(os.path.join(get_project_root(), 'data/processed/income_data.csv'), sep=';')
    unemployment_data = pd.read_csv(os.path.join(get_project_root(), 'data/processed/unemployment_data.csv'), sep=';')
    population = pd.read_csv(os.path.join(get_project_root(), 'data/processed/population_20-22_data.csv'), sep=';')[['FIPS code', 'NPOPCHG2022']]

    part1=pd.merge(education_data, GDP_data, on='FIPS code', suffixes=('','_y'))
    part2=pd.merge(part1, health_data, on='FIPS code', suffixes=('','_y'))
    part3=pd.merge(part2, HPI_data, on='FIPS code', suffixes=('','_y'))
    part4=pd.merge(part3, income_data, on='FIPS code', suffixes=('','_y'))
    part5=pd.merge(part4, population, on='FIPS code', suffixes=('','_y'))
    part6=pd.merge(part5, unemployment_data, on='FIPS code', suffixes=('','_y'))

    # part5=pd.merge(part4, MigrationData, on='FIPS code', suffixes=('','_y'))

    part6.drop(part6.filter(regex='_y$').columns, axis=1, inplace=True)

    years = ['1970','1980','1990','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022']
    columns = part6.columns.tolist()

    def extract_year(col):
        match = re.search(r"\d{4}", col)
        if match:
            return int(match.group())
        else:
            return -1

    columns = part6.columns.tolist()
    columns.sort(key=extract_year)
    part6 = part6[columns]

    data = part6.drop(part6.iloc[:, 3:32], axis=1)
    data = data.rename(columns={'Area name': 'County'}) 

    data = data.ffill()
    data = data.bfill()

    all_states = list(set(list(data['State'])))
    all_states = sorted(all_states)



    for state in all_states:
        tmp = data[data["State"] == state]
        tmp = tmp.drop(columns=['FIPS code', 'State', 'County'], axis=1)
        tmp = tmp.iloc[:, -10:]
        scaler = StandardScaler()
        array = scaler.fit_transform(tmp)
        scaled_data = pd.DataFrame(data=array, columns=tmp.columns)
        tmp.to_csv(f'../data/states_data/{state}.csv', sep=';', index=False)