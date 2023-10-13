import pandas as pd
import numpy as np
import time
pd.options.mode.chained_assignment = None  # default='warn'
from os import path
import re

def etl_cu():
    """Generate PRO3 wholesaler sheet by transforming and joining piip data and 
    product data imported from lab-lennox project."""
    def format_numeric(value):
        """
        Format numeric values in price column"""
        try:
            numeric_value = float(value)
            formatted_value = f'${numeric_value:,.0f}'
            return formatted_value
        except ValueError:
            return value  

    # Apply the formatting function to the DataFrame column
    # Create Platform column.
    def platform_values(text):
        """Function to extract platform values"""
        if type(text) == str:
            match = re.search(r'[^-]+', text[::-1])
            if match:
                return match.group()[::-1].upper()
        return 'NA'

    #Names of individual files that are read or modified/created.
    piip_input_file, cu_output_file = 'input_files/piip_data_report.csv', 'interProcess_files/cu_wholesaler.csv'
    options_file, cu_non_pricing_data_file = 'input_files/cu_option_code_mapping.csv', 'input_files/cu_wholesaler_prod_data.csv'
    #Lists to store the final header names
    cu_final_headers = ["Product Category","Style","Cabinet","Platform","Voltage","Application","Compressor Technology",
    # "Compressor Manufacturer",
    "Operating Range", "New Model No", "Configurable Model (Add Options to Order)",
    "Option Code","Option Description","List Price ($US)"]
    #List to store names of relevant columns
    future_price = 'Future Price\n Motor + BO\n Adder(s) + BO\n Curr. Price'
    columns_to_read = ['ProdH1 (Item Class) Descrip.', 'ProdH2 (Category) Descrip.','VarKey',\
    'Material','Option (Variant)','Current Price', future_price]
    t1 = time.time()
    #Create dataframe containing all of the piip data. Select relevant columns only
    piip_raw_df = pd.read_csv(piip_input_file, usecols=columns_to_read, dtype=object, encoding='unicode_escape')
    #Filtered dataframe. Use condensing unit filters
    cu_pricing_df = piip_raw_df.loc[(piip_raw_df['ProdH1 (Item Class) Descrip.'].isin(['Compressorized','Custom Compressorize']))\
                            
    # & piip_raw_df['ProdH2 (Category) Descrip.'].isin()      filters?                         
                                
    #And select data for all the model(base + variants) associated with the required Materials.                         
    & (piip_raw_df['Option (Variant)'].str.contains('UNIT.A', case=False, regex=True))\
    #Filter for current Materials- have 11 characters in nomeclature.
    & (piip_raw_df['Material'].str.len() == 11),['Material' ,'Option (Variant)', future_price]]
    #Filter for required part codes and materials. Part code mapping dictionary used.

    #Rename columns
    cu_pricing_df.rename(columns={'Option (Variant)':'Option Code', future_price:"List Price ($US)"}, inplace=True)

    #Trim Option Code column and create Base Model column
    cu_pricing_df['Option Code'] = cu_pricing_df['Option Code'].apply(lambda x: x.split('.')[-1]) 
    cu_pricing_df['New Model No'] = cu_pricing_df['Material'] + cu_pricing_df['Option Code']

    #Read option code mapping
    op_desc_df = pd.read_csv(options_file, encoding='unicode_escape')
    op_desc_dict = dict(zip(op_desc_df['Option Code'], op_desc_df['Option Description']))
    #Add option description column
    cu_pricing_df['Option Description'] = cu_pricing_df['Option Code'].map(op_desc_dict)

    #Drop rows where option code is null
    cu_pricing_df.dropna(subset=['Option Description'], inplace=True)

    #Read non pricing data
    cu_prod_df = pd.read_csv(cu_non_pricing_data_file)
    #Join with pricing data to get wholesale CU dataset.
    wholesaler_cu_df = cu_prod_df.merge(cu_pricing_df, how='right', on='Material')

    #Adding and removing columns. 
    wholesaler_cu_df['Platform'] = wholesaler_cu_df['product_style'].apply(platform_values)
    wholesaler_cu_df['List Price ($US)'] = wholesaler_cu_df['List Price ($US)'].apply(format_numeric)
    #Replace values in product_style column
    style_dict = {'05-6-hp-hts':"1/2-6 Horizontal Air Discharge", "12-50-hp-vcu":"12 - 50 HP Vertical Air Discharge", \
    "24-100-hp-dvcu":"24 - 100 HP Dual Compressor", "3-22-hp-hcu":"3 - 22 HP Horizontal Air Discharge"}
    wholesaler_cu_df.replace({'product_style':style_dict, 'product_type':{'air-cooled':'Air-Cooled Condensing Unit'}}, inplace=True),  wholesaler_cu_df.fillna('NA',inplace=True)

    #Rename columns
    columns_dict = {'product_type':"Product Category", 'product_style':"Style", \
    'application':"Application", 'operating_range':"Operating Range", 'compressor_type':"Compressor Technology",\
    'voltage':"Voltage", 'cabinet':"Cabinet", 'Material':"Configurable Model (Add Options to Order)"}
    wholesaler_cu_df.rename(columns=columns_dict, inplace=True)
    #Select columns in proper sequence
    # wholesaler_cu_df = wholesaler_cu_df[["Product Category","Style", "Cabinet", "Platform", "Voltage", "Application", \
    # "Compressor Technology", "Operating Range", "New Model No", "Configurable Model (Add Options to Order)", "Option Code", \
    # "Option Description", "List Price ($US)"]]
    wholesaler_cu_df[cu_final_headers].to_csv(cu_output_file, index=False)
    
    print('='*100)
    print('CU Wholesale CSV')
    print(f'time consumed: {time.time() - t1}')
    print('='*100)

if __name__ == "__main__":
    etl_cu()