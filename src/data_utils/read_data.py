import pandas as pd
from src.utils.name_utils import US_STATES_DIR
from src.utils.projekt_utils import get_project_root
import os
from glob import glob


def process_migration_data():
    core_data = pd.read_csv(os.path.join(get_project_root(), 'data/processed/MigrationData.csv'), encoding='latin-1',
                            sep=';')
    return core_data


def process_unemployment_data():
    data = pd.read_excel(os.path.join(get_project_root(), './data/raw/Unemployment.xlsx'), skiprows=4)
    data['State'] = data['State'].map(US_STATES_DIR)
    data.dropna(subset=['State'], inplace=True)
    data = data[~data['Area_name'].isin(list(US_STATES_DIR.values()))]
    data['Area_name'] = data['Area_name'].str[:-4]
    data.rename({'FIPS_code': 'FIPS code'}, inplace=True, axis=1)
    return data


def process_education_data():
    data = pd.read_excel(os.path.join(get_project_root(), './data/raw/Education.xlsx'), skiprows=3)
    data['State'] = data['State'].map(US_STATES_DIR)
    data.dropna(subset=['State'], inplace=True)
    data = data[~data['Area name'].isin(list(US_STATES_DIR.values()))]
    data.rename({'Federal Information Processing Standard (FIPS) Code': 'FIPS code'}, inplace=True, axis=1)
    return data


def process_gdp_data():
    data = pd.read_csv(os.path.join(get_project_root(), './data/raw/CAGDP1__ALL_AREAS_2001_2021.csv'),
                       encoding='latin-1')
    data['State'] = data['GeoName'].apply(lambda x: str(x)[-2:] if ',' in str(x) else None)
    current_columns = list(data.columns)
    current_columns.insert(2, current_columns.pop())
    data = data[current_columns]
    data['State'] = data['State'].map(US_STATES_DIR)
    data.dropna(subset=['State'], inplace=True)
    data['GeoName'] = data['GeoName'].str[:-4]
    data['GeoName'] = data['GeoName'] + ' County'

    for col in [str(i) for i in range(2001, 2022)]:
        data[col] = pd.to_numeric(data[col], errors='coerce')
    data.drop(['TableName', 'Unit', 'IndustryClassification', 'Region'], inplace=True, axis=1)

    data1 = data[data['LineCode'] == 1.0]
    data2 = data[data['LineCode'] == 2.0]
    data3 = data[data['LineCode'] == 3.0]

    year_list = list(range(2001, 2022))
    for df in [data1, data2, data3]:
        name = df.iloc[0]['Description']

        rename_dict = dict(zip([str(x) for x in year_list], [str(i) + ' ' + name for i in year_list]))
        df.rename(columns=rename_dict, inplace=True)

    data1.drop(['LineCode', 'Description'], inplace=True, axis=1)

    data1.reset_index(drop=True, inplace=True)

    tmp2 = data2.iloc[:, 5:]
    tmp2.reset_index(drop=True, inplace=True)
    tmp3 = data2.iloc[:, 5:]
    tmp3.reset_index(drop=True, inplace=True)

    full_data = pd.concat([data1, tmp2, tmp3], axis=1, ignore_index=True)
    full_data = full_data.rename(
        dict(zip(range(0, len(full_data.columns)), list(data1.columns) + list(tmp2.columns) + list(tmp3.columns))),
        axis=1)

    full_data['GeoFIPS'] = full_data['GeoFIPS'].str.replace('"', '')
    full_data['GeoFIPS'] = full_data['GeoFIPS'].astype('int')
    full_data.rename({'GeoFIPS': 'FIPS code'}, inplace=True, axis=1)
    return full_data


def process_income_data():
    data = pd.read_csv(os.path.join(get_project_root(), './data/raw/CAINC1__ALL_AREAS_1969_2021.csv'),
                       encoding='latin-1')
    data['State'] = data['GeoName'].apply(lambda x: str(x)[-2:] if ',' in str(x) else None)
    current_columns = list(data.columns)
    current_columns.insert(2, current_columns.pop())
    data = data[current_columns]
    data['State'] = data['State'].map(US_STATES_DIR)
    data.dropna(subset=['State'], inplace=True)
    data['GeoName'] = data['GeoName'].str[:-4]
    data['GeoName'] = data['GeoName'] + ' County'

    for col in [str(i) for i in range(2001, 2022)]:
        data[col] = pd.to_numeric(data[col], errors='coerce')

    data = data.drop([str(i) for i in range(1969, 2001)], axis=1)
    data = data.drop(['TableName', 'IndustryClassification', 'Unit', 'Region'], axis=1)

    data1 = data[data['LineCode'] == 1.0]
    data2 = data[data['LineCode'] == 2.0]
    data3 = data[data['LineCode'] == 3.0]

    year_list = list(range(2001, 2022))
    for df in [data1, data2, data3]:
        name = df.iloc[0]['Description']

        rename_dict = dict(zip([str(x) for x in year_list], [str(i) + ' ' + name for i in year_list]))
        df.rename(columns=rename_dict, inplace=True)

    data1.drop(['LineCode', 'Description'], inplace=True, axis=1)

    data1.reset_index(drop=True, inplace=True)

    tmp2 = data2.iloc[:, 5:]
    tmp2.reset_index(drop=True, inplace=True)
    tmp3 = data2.iloc[:, 5:]
    tmp3.reset_index(drop=True, inplace=True)

    full_data = pd.concat([data1, tmp2, tmp3], axis=1, ignore_index=True)
    full_data = full_data.rename(
        dict(zip(range(0, len(full_data.columns)), list(data1.columns) + list(tmp2.columns) + list(tmp3.columns))),
        axis=1)
    full_data['GeoFIPS'] = full_data['GeoFIPS'].str.replace('"', '')
    full_data['GeoFIPS'] = full_data['GeoFIPS'].astype('int')
    full_data.rename({'GeoFIPS': 'FIPS code'}, inplace=True, axis=1)
    return full_data


def process_hpi_data():
    data = pd.read_excel(os.path.join(get_project_root(), './data/raw/HPI_AT_BDL_county.xlsx'), skiprows=6)
    data['State'] = data['State'].map(US_STATES_DIR)
    data.dropna(subset=['State'], inplace=True)
    data['County'] = data['County'] + ' County'
    new_data = data[data['Year'] >= 2001]
    new_data = new_data.drop(['HPI', 'HPI with 1990 base', 'HPI with 2000 base'], axis=1)
    new_data = new_data.rename({'Annual Change (%)': 'HPI change'}, axis=1)
    grouped = new_data.groupby(by=['FIPS code']).agg({'State': 'max',
                                                      'County': 'max',
                                                      'Year': 'count',
                                                      'HPI change': 'count'})
    base_columns = ['FIPS code', 'State', 'County']
    base_columns.extend([str(i) + ' HPI Change' for i in range(2001, 2023)])
    final_dataframe = pd.DataFrame(columns=base_columns)

    for idx, row in grouped.iterrows():
        if row['Year'] != 22:
            values = [idx, row['State'], row['County']]
            empty_dict = dict(zip(list(range(2001, 2023)),
                                  [None] * 22))
            tmp_df = new_data[new_data['FIPS code'] == idx]
            for i_idx, i_row in tmp_df.iterrows():
                if i_row['Year'] in empty_dict.keys():
                    empty_dict[i_row['Year']] = i_row['HPI change']
            values.extend(empty_dict.values())
        else:
            values = [idx, row['State'], row['County']]
            values.extend(list(new_data[new_data['FIPS code'] == idx]['HPI change']))
        row_dict = dict(zip(base_columns, values))
        new_df = pd.DataFrame(row_dict, index=[0])
        final_dataframe = pd.concat([final_dataframe, new_df], ignore_index=True)
    return final_dataframe


def process_health_data():
    df_list = []
    processed_df_list = []
    for file in glob(os.path.join(get_project_root(), "data/raw/analytic_data*.csv")):
        data = pd.read_csv(file)
        thresh = len(data) * 0.9
        cols_to_drop = [col for col in data.columns if 'CI' in col or 'numerator' in col or 'denominator' in col]
        cols_to_drop.append('Release Year')
        data = data.drop(cols_to_drop, axis=1)
        data = data.drop(0)
        data['State Abbreviation'] = data['State Abbreviation'].map(US_STATES_DIR)
        data.dropna(subset=['State Abbreviation'], inplace=True)
        data = data.dropna(thresh=thresh, axis=1)
        df_list.append(data)

    intersection = set(df_list[0]).intersection(set(df_list[1]), set(df_list[2]), set(df_list[3]), set(df_list[4]))

    first_cols = ['State FIPS Code', 'County FIPS Code', '5-digit FIPS Code',
                  'State Abbreviation', 'Name']

    for dataframe in df_list:
        dataframe = dataframe[first_cols + [col for col in list(intersection) if col not in first_cols]]
        processed_df_list.append(dataframe)

    for idx, dataframe in enumerate(processed_df_list):
        dataframe.rename(dict(zip([col for col in list(intersection) if col not in first_cols],
                                  [col + ' ' + str(2016 + idx) for col in list(intersection) if
                                   col not in first_cols])),
                         axis=1, inplace=True)

    for idx, dataframe in enumerate(df_list):
        if idx == 0:
            dataframe.reset_index(drop=True, inplace=True)
        else:
            dataframe = dataframe.iloc[:, 5:]
            dataframe.reset_index(drop=True, inplace=True)

    print([i.shape for i in processed_df_list])

    final_data = pd.concat(processed_df_list, axis=1, ignore_index=True)
    final_data = final_data.rename(
        dict(zip(range(0, len(final_data.columns)),
                 list(processed_df_list[0].columns) + list(processed_df_list[1].columns) + list(
                     processed_df_list[2].columns) + list(processed_df_list[3].columns) + list(
                     processed_df_list[4].columns))),
        axis=1)

    final_data.rename({'5-digit FIPS Code': 'FIPS code'}, inplace=True, axis=1)
    return final_data


def save_files_to_process_directory():
    gdp_data = process_gdp_data()
    gdp_data.to_csv(os.path.join(get_project_root(), 'data/processed/GDP_data.csv'), sep=';', index=False)
    print('DONE processing GDP data')

    unemployment_data = process_unemployment_data()
    unemployment_data.to_csv(os.path.join(get_project_root(), 'data/processed/unemployment_data.csv'), sep=';',
                             index=False)
    print('DONE processing unemployment data')

    education_data = process_education_data()
    education_data.to_csv(os.path.join(get_project_root(), 'data/processed/education_data.csv'), sep=';', index=False)
    print('DONE processing education data')

    hpi_data = process_hpi_data()
    hpi_data.to_csv(os.path.join(get_project_root(), 'data/processed/HPI_data.csv'), sep=';', index=False)
    print('DONE processing HPI data')

    income_data = process_income_data()
    income_data.to_csv(os.path.join(get_project_root(), 'data/processed/income_data.csv'), sep=';', index=False)
    print('DONE processing income data')

    health_data = process_health_data()
    health_data.to_csv(os.path.join(get_project_root(), 'data/processed/health_data.csv'), sep=';', index=False)
    print('DONE processing health data')


if __name__ == '__main__':
    save_files_to_process_directory()
