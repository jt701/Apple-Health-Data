import pandas as pd
import xml.etree.ElementTree as et
import datetime as dt

#To do/progess
""" 1. validate enough data points are present (remember 1 year time frame)
    2. exports metrics to CSV, fill with NaN if not valid
    3. deal with days being cutoff on backend
    4. case work, we need to drop first value because it is cut off during function, figure out best
    total inital restirction value to accomodate, month, year, week, etc. 
    
Current Algo
1. process data
2. chunk into time frame, reduce into time frame
""" 

#converts xml file to df using filepath
def xml_to_df(filepath):
    tree = et.parse(filepath) 
    root = tree.getroot()
    record_list = [x.attrib for x in root.iter('Record')]
    return pd.DataFrame(record_list)

#proccess df to make it cleaner (dates, NaN values, etc.)
def process_df(df):
    for col in ['startDate']:
       df[col] = pd.to_datetime(df[col])
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df.dropna(inplace= True)
    df['type'] = df['type'].str.replace('HKQuantityTypeIdentifier', '')
    df['type'] = df['type'].str.replace('HKCategoryTypeIdentifier', '')
    #df['startDate'] = df['startDate'].apply(lambda x: x.date())

#returns new df with only the given metric  
def get_metric_df(df, metric):
    return df[df["type"] == metric]


#takes in time period and reduces to only this time period in days, does not include the lower bound
#starts at max data point and goes backwards (not at start of day)
def reduce(df, time_period):
    #time_frame = df['startDate'].max().replace(hour=0, minute=0, second=0, microsecond=0) - dt.timedelta(days=time_period)
    #print(type(df['startDate'].max()))
    max_date = df['startDate'].max().replace(hour=0, minute=0, second=0, microsecond=0)
    time_frame = max_date - dt.timedelta(days=time_period)
    #max_date_only = max_date.date()
    #max_date_begin = dt.datetime.combine(max_date_only,dt.time.min)
    #max_date_begin = pd.Timestamp(max_date_begin)
    #print(type(max_date_begin))
    #time_frame = max_date_begin - pd.Timedelta(days=time_period)
    df = df[df['startDate'] < max_date]
    return df[df['startDate'] > time_frame]


#returns df in chunks of time_period (day, week, month)
#does so by resampling every x days (goes backwards from max date, not at start of day)
#aggregates by summing
def resample_sum(df, time_period):
    df.set_index('startDate', inplace=True)
    daily_counts = df['value'].resample('D').sum()
    
    if time_period == 'day':
        pass
    elif time_period == 'week':
        daily_counts = daily_counts.resample('7D').sum()
    elif time_period == 'month':
        daily_counts = daily_counts.resample('30D').sum()
    elif time_period == 'year':
        daily_counts = daily_counts.resample('Y').sum()
    return daily_counts.to_frame()

#takes in metric df, how long the sample period is in days,the chunk size
#returns array of arrays
#first array is last week statistics, 2nd is month, 3rd is year
#in each smaller area, mean, median, max, min
def daily_stats(df, sample_period):
    reduced_df = reduce(df, sample_period)
    chunked_df = resample_sum(reduced_df, 'day')
    print(chunked_df)
    adjusted_df = chunked_df
    #print(adjusted_df.index.max())
    #chunked_df.drop(0, inplace = True)
    mean = int(adjusted_df.mean())
    median = int(adjusted_df.median())
    max = int(adjusted_df.max())
    min = int(adjusted_df.min())
    return [mean, median, max, min]




