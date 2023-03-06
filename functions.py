import pandas as pd
import xml.etree.ElementTree as et
import datetime as dt

#converts xml file to df using filepath
def xml_to_df(filepath):
    tree = et.parse(filepath) 
    root = tree.getroot()
    record_list = [x.attrib for x in root.iter('Record')]
    return pd.DataFrame(record_list)

#proccess df to make it cleaner  
def process_df(df):
    for col in ['creationDate', 'startDate', 'endDate']:
       df[col] = pd.to_datetime(df[col])
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df.dropna(inplace= True)
    df['type'] = df['type'].str.replace('HKQuantityTypeIdentifier', '')
    df['type'] = df['type'].str.replace('HKCategoryTypeIdentifier', '')
    df['startDate'] = df['startDate'].apply(lambda x: x.date())

#returns new df with only the given metric  
def get_metric_df(df, metric):
    return
