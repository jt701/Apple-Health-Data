import pandas as pd
import xml.etree.ElementTree as et
import datetime as dt

#To do/progess
""" 1. validate enough data points are present (remember 1 year time frame)
    2. exports metrics to CSV, fill with NaN if not valid
    3. deal with days being cutoff on backend
        - solved by using an exact reduce function
    4. What to inform investigator
    - format of results, units as well
    - ios update needed, fixed vs regular export.xml
    5. figure out why standing time is dropped when using process_df
    6. look at colab for worko
    
    
Current Algo
1. process data
2. chunk into time frame, reduce into time frame
""" 

#converts xml file to df using filepath
#need filepath export_cda.xml, (if a "fixed" xml file is present, use that one)
#phone must be updated to latest IOS
def xml_to_df(filepath):
    tree = et.parse(filepath) 
    root = tree.getroot()
    record_list = [x.attrib for x in root.iter('Record')]
    return pd.DataFrame(record_list)

#proccess df to make it cleaner (dates, NaN values, etc.), mutates df
def process_df(df):
    for col in ['startDate']:
       df[col] = pd.to_datetime(df[col])
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df.dropna(subset=['value'], inplace= True)
    df['type'] = df['type'].str.replace('HKQuantityTypeIdentifier', '')
    df['type'] = df['type'].str.replace('HKCategoryTypeIdentifier', '')

#returns new df with only the given metric  
def get_metric_df(df, metric):
    return df[df["type"] == metric]


#takes in time period and reduces to only this time period in days, does not include the lower bound
#starts at max data point and goes backwards (not at start of day)
def reduce(df, time_period):
    max_date = df['startDate'].max().replace(hour=0, minute=0, second=0, microsecond=0)
    time_frame = max_date - dt.timedelta(days=time_period)
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
        daily_counts = daily_counts.resample('365D').sum()
    return daily_counts.to_frame()

def resample_sum_avg(df, time_period):
    df.set_index('startDate', inplace=True)
    daily_counts = df['value'].resample('D').mean()
    
    if time_period == 'day':
        pass
    elif time_period == 'week':
        daily_counts = daily_counts.resample('7D').sum()
    elif time_period == 'month':
        daily_counts = daily_counts.resample('30D').sum()
    elif time_period == 'year':
        daily_counts = daily_counts.resample('365D').sum()
    return daily_counts.to_frame()

#takes in metric df, how long the sample period is in days,the chunk size
#returns array of arrays
#first array is last week statistics, 2nd is month, 3rd is year
#in each smaller area, mean, median, max, min
def daily_stats(df, sample_period):
    reduced_df = reduce(df, sample_period)
    chunked_df = resample_sum(reduced_df, 'day')
    mean = round(float(chunked_df.mean()), 2)
    median = round(float(chunked_df.median()), 2)
    max = round(float(chunked_df.max()), 2)
    min = round(float(chunked_df.min()), 2)
    return [mean, median, max, min]

def daily_stats_avg(df, sample_period):
    reduced_df = reduce(df, sample_period)
    chunked_df = resample_sum_avg(reduced_df, 'day')
    mean = round(float(chunked_df.mean()), 2)
    median = round(float(chunked_df.median()), 2)
    max = round(float(chunked_df.max()), 2)
    min = round(float(chunked_df.min()), 2)
    return [mean, median, max, min]

#return array of arrays reflecting daily data
#minimum one year data needed
def combined_daily_stats(df, metric):
    metric_df = get_metric_df(df, metric)
    #if len(metric_df) == 0:
        #return "NA"
    results = ["daily" + metric]
    results.extend(["week", daily_stats(metric_df, 7) ])
    results.extend(["month", daily_stats(metric_df, 30) ])
    results.extend(["year", daily_stats(metric_df, 365) ])
    results.extend(["all time", daily_stats(metric_df, 10000) ])
    return results

def combined_daily_stats_avg(df, metric):
    metric_df = get_metric_df(df, metric)
    #if len(metric_df) == 0:
        #return "NA"
    results = ["daily" + metric]
    results.extend(["week", daily_stats_avg(metric_df, 7) ])
    results.extend(["month", daily_stats_avg(metric_df, 30) ])
    results.extend(["year", daily_stats_avg(metric_df, 365) ])
    results.extend(["all time", daily_stats_avg(metric_df, 10000) ])
    return results

#defined as 7 days, chunks and provides stats based on week
def weekly_stats(df, sample_period):
    reduced_df = reduce(df, sample_period)
    chunked_df = resample_sum(reduced_df, 'week')
    mean = round(float(chunked_df.mean()), 2)
    median = round(float(chunked_df.median()), 2)
    max = round(float(chunked_df.max()), 2)
    min = round(float(chunked_df.min()), 2)
    return [mean, median, max, min]

def weekly_stats_avg(df, sample_period):
    reduced_df = reduce(df, sample_period)
    chunked_df = resample_sum_avg(reduced_df, 'week')
    mean = round(float(chunked_df.mean()), 2)
    median = round(float(chunked_df.median()), 2)
    max = round(float(chunked_df.max()), 2)
    min = round(float(chunked_df.min()), 2)
    return [mean, median, max, min]

#defined as 30 days, chunks and provides stats based on month
def monthly_stats(df, sample_period):
    reduced_df = reduce(df, sample_period)
    chunked_df = resample_sum(reduced_df, 'month')
    mean = round(float(chunked_df.mean()), 2)
    median = round(float(chunked_df.median()), 2)
    max = round(float(chunked_df.max()), 2)
    min = round(float(chunked_df.min()), 2)
    return [mean, median, max, min]

def monthly_stats_avg(df, sample_period):
    reduced_df = reduce(df, sample_period)
    chunked_df = resample_sum_avg(reduced_df, 'month')
    mean = round(float(chunked_df.mean()), 2)
    median = round(float(chunked_df.median()), 2)
    max = round(float(chunked_df.max()), 2)
    min = round(float(chunked_df.min()), 2)
    return [mean, median, max, min]

#defined as 365 days
def yearly_stats(df, sample_period):
    reduced_df = reduce(df, sample_period)
    chunked_df = resample_sum(reduced_df, 'year')
    mean = round(float(chunked_df.mean()), 2)
    median = round(float(chunked_df.median()), 2)
    max = round(float(chunked_df.max()), 2)
    min = round(float(chunked_df.min()), 2)
    return [mean, median, max, min]

def yearly_stats_avg(df, sample_period):
    reduced_df = reduce(df, sample_period)
    chunked_df = resample_sum(reduced_df, 'year')
    mean = round(float(chunked_df.mean()), 2)
    median = round(float(chunked_df.median()), 2)
    max = round(float(chunked_df.max()), 2)
    min = round(float(chunked_df.min()), 2)
    return [mean, median, max, min]


#monthly and weekly stats combined, over 52 weeks and 12 30 day periods
def combined_longer_stats(df, metric):
    metric_df = get_metric_df(df, metric)
    results = ["daily" + metric]
    results.extend(["cumulative week", weekly_stats(metric_df, 364) ])
    results.extend(["cumulative month", monthly_stats(metric_df, 360) ])
    numYears = (metric_df['startDate'].max() -  metric_df['startDate'].min()) / dt.timedelta(days=1)  // 365
    print(numYears)
    results.extend(["cumulative year", yearly_stats(metric_df, numYears * 365)])
    return results

def combined_longer_stats_avg(df, metric):
    metric_df = get_metric_df(df, metric)
    results = ["daily" + metric]
    results.extend(["cumulative week", weekly_stats_avg(metric_df, 364) ])
    results.extend(["cumulative month", monthly_stats_avg(metric_df, 360) ])
    numYears = (metric_df['startDate'].max() -  metric_df['startDate'].min()) / dt.timedelta(days=1)  // 365
    print(numYears)
    results.extend(["cumulative year", yearly_stats_avg(metric_df, numYears * 365)])
    return results
    
    
    
    
    
    

    



