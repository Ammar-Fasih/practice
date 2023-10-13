import pandas as pd
import time
import os

t1 = time.time()

df_alacarte = pd.read_csv('input_files/mapping_alacarte.csv')
df_shippedLoose = pd.read_csv('input_files/mapping_shipped_loose.csv')
df_piip = pd.read_csv('input_files/piip_data_report.csv')
df_piip.set_index('varkey', inplace=True)

# pricing update

headers = ['c1_models', 'c2_models', 'c3_models', 'c4_models', 'c5_models', 'c6_models', 'models']
for header in headers:
    df_alacarte[header] = df_alacarte[header].str.cat(df_alacarte['option_code'], sep='.')

df_alacarte['C1'] = df_alacarte['c1_models'].map(df_piip['new_price'])
df_alacarte['C2'] = df_alacarte['c2_models'].map(df_piip['new_price'])
df_alacarte['C3'] = df_alacarte['c3_models'].map(df_piip['new_price'])
df_alacarte['C4'] = df_alacarte['c4_models'].map(df_piip['new_price'])
df_alacarte['C5'] = df_alacarte['c5_models'].map(df_piip['new_price'])
df_alacarte['C6'] = df_alacarte['c6_models'].map(df_piip['new_price'])
df_alacarte['Models Price'] = df_alacarte['models'].map(df_piip['new_price'])

table_names = df_alacarte['table'].unique().tolist()
table_col_mapping = {"05_6":['option_code_label','description','C1','C2','C3','notes'],"3_22":['option_code_label','description','C4','C5','C6','notes'],"12_50":['option_code_label','description','models_used_on','notes','Models Price'],"24_100":['option_code_label','description','models_used_on','notes','Models Price']}

os.makedirs('interProcess_files', exist_ok=True)


for table_name in table_names:
    df_table = df_alacarte[df_alacarte['table'] == table_name]
    option_types = df_table['option_type'].unique().tolist()
    for option_type in option_types:
        df_table_type_filter = df_table[df_table['option_type'] == option_type]
        df_table_type_filter = df_table_type_filter[table_col_mapping[table_name]]
        df_table_type_filter.to_csv(f'interProcess_files/{table_name}_alacarte_{option_type}.csv', index=False)


df_shippedLoose['list_price'] = df_shippedLoose['part_number_label'].map(df_piip['new_price'])
table_col_mapping = {"electrical_options":['part_number_label','description','list_price'], "ND":['part_number_label','description','list_price'], "CPR":['size','part_number_label','list_price']}
table_names = df_shippedLoose['table'].unique().tolist()

for table_name in table_names:
    df_table = df_shippedLoose[df_shippedLoose['table'] == table_name]
    option_types = df_table['option_type'].unique().tolist()
    # print(f'{len(df_table)} {option_types} {table_name}')
    for option_type in option_types:
        df_table_type_filter = df_table[df_table['option_type'] == option_type]
        df_table_type_filter = df_table_type_filter[table_col_mapping[option_type]]
        df_table_type_filter.to_csv(f'interProcess_files/{table_name}_shippedLoose_{option_type}.csv', index=False)


print(f'total time: {time.time() - t1}')