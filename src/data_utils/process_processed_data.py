import pandas as pd
import numpy as np
import os
from src.utils.projekt_utils import get_project_root


def process_education():
    data_path = os.path.join(
        get_project_root(), './data/processed/education_data.csv')
    data = pd.read_csv(data_path, sep=';')

    to_proccess = data.iloc[:, [0, 1, 2, 31, 32, 33, 34,
                                35, 36, 37, 38, -8, -7, -6, -5, -4, -3, -2, -1]]
    for i in range(0, 8):
        to_proccess.iloc[:, 3+i] = to_proccess.iloc[:,
                                                    3+i+8] - to_proccess.iloc[:, 3+i]

    l1 = ["Less than a high school diploma, 2000",
          "High school diploma only, 2000",
          "Some college or associate's degree, 2000",
          "Bachelor's degree or higher, 2000",
          "Percent of adults with less than a high school diploma, 2000",
          "Percent of adults with a high school diploma only, 2000",
          "Percent of adults completing some college or associate's degree, 2000",
          "Percent of adults with a bachelor's degree or higher, 2000"]

    l2 = ["Less than a high school diploma, delta from 2017",
          "High school diploma only, delta from 2017",
          "Some college or associate's degree, delta from 2017",
          "Bachelor's degree or higher, delta from 2017",
          "Percent of adults with less than a high school diploma, delta from 2017",
          "Percent of adults with a high school diploma only, delta from 2017",
          "Percent of adults completing some college or associate's degree, delta from 2017",
          "Percent of adults with a bachelor's degree or higher, delta from 2017"]

    to_proccess = to_proccess.rename(dict(zip(l1, l2)), axis=1)
    to_proccess.to_csv(os.path.join(get_project_root(), './data/better_processed/education.csv') , index=False, sep=';')


def process_GDP():
    data_path = os.path.join(
        get_project_root(), './data/processed/GDP_data.csv')

    data = pd.read_csv(data_path, sep=';')

    new_data = pd.DataFrame(columns=['FIPS code', 'GeoName', 'State', 'Real GDP delta from 2021',
                            'Real GDP 2021', 'Chain GDP delta from 2021', 'Chain GDP 2021'])
    new_data['FIPS code'] = data['FIPS code']
    new_data['GeoName'] = data['GeoName']
    new_data['State'] = data['State']
    new_data['Real GDP delta from 2021'] = data['2021 Real GDP (thousands of chained 2012 dollars) '] - \
        data['2001 Real GDP (thousands of chained 2012 dollars) ']
    new_data['Chain GDP delta from 2021'] = data['2021 Chain-type quantity indexes for real GDP '] - \
        data['2001 Chain-type quantity indexes for real GDP ']
    new_data['Chain GDP 2021'] = data['2021 Chain-type quantity indexes for real GDP ']
    new_data['Real GDP 2021'] = data['2021 Real GDP (thousands of chained 2012 dollars) ']

    new_data.to_csv('../data/better_processed/GDP_data.csv',
                    index=False, sep=';')


def process_unemployment():
    data_path = os.path.join(
        get_project_root(), './data/processed/unemployment_data.csv')
    data = pd.read_csv(data_path, sep=';')
    to_proccess = data.iloc[:, [0, 1, 2, 6, 7, 8, 9, 90, 91, 92, 93]]
    for i in range(0, 4):
        to_proccess.iloc[:, 3+i] = to_proccess.iloc[:,
                                                    3+i+4] - to_proccess.iloc[:, 3+i]
        l1 = ['Civilian_labor_force_2000', 'Employed_2000',
              'Unemployed_2000', 'Unemployment_rate_2000']

    l2 = ['Civilian_labor_force_delta_from_2021', 'Employed_delta_from_2021',
          'Unemployed_delta_from_2021', 'Unemployment_rate_delta_from_2021']

    to_proccess = to_proccess.rename(dict(zip(l1, l2)), axis=1)

    to_proccess.to_csv(
        '../data//better_processed/unemplyment_data.csv', index=False, sep=';')


process_education()
