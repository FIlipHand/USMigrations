import pandas as pd
import numpy as np
import os
from src.utils.projekt_utils import get_project_root


def process_education():
    data_path = os.path.join(get_project_root(), './data/processed/education_data.csv')
    data = pd.read_csv(data_path, sep=';')

    to_proccess = data.iloc[:, [1,2, 31, 32, 33, 34, 35, 36, 37, 38, -8, -7, -6, -5, -4, -3, -2, -1]]
    for i in range(0, 8):
        to_proccess.iloc[:, 2+i] -= to_proccess.iloc[:, 2+i+8]

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
    to_proccess.to_csv('./data/better_processed/education.csv', index=False)